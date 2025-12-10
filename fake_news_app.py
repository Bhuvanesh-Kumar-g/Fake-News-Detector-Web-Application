import os
import pickle
import requests
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import google.generativeai as genai
from google.api_core import exceptions

load_dotenv()

# --- 1. SETUP & MODEL LOADING ---
try:
    with open("model.pkl", "rb") as model_file:
        model = pickle.load(model_file)
    with open("vectorizer.pkl", "rb") as vectorizer_file:
        tfidf_vectorizer = pickle.load(vectorizer_file)
except FileNotFoundError:
    model = None
    tfidf_vectorizer = None
    print("Warning: model.pkl or vectorizer.pkl not found.")

# --- 2. INTELLIGENT AI CONFIGURATION ---
gemini_api_key = os.getenv("GEMINI_API_KEY")
ACTIVE_MODEL_NAME = "gemini-pro" # Default fallback

if gemini_api_key:
    genai.configure(api_key=gemini_api_key)
    try:
        print("Checking available AI models...")
        available_models = []
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                available_models.append(m.name)
        
        # Priority Logic: Try to find Flash (fastest), then Pro, then 1.0
        # The API returns names like 'models/gemini-1.5-flash'
        found = False
        for name in available_models:
            if 'flash' in name and '1.5' in name:
                ACTIVE_MODEL_NAME = name
                found = True
                break
        
        if not found:
            for name in available_models:
                if 'pro' in name and '1.5' in name:
                    ACTIVE_MODEL_NAME = name
                    found = True
                    break

        # Fallback to whatever is available if specific ones aren't found
        if not found and available_models:
             ACTIVE_MODEL_NAME = available_models[0]

        print(f"--> Using AI Model: {ACTIVE_MODEL_NAME}")
        
    except Exception as e:
        print(f"--> Warning: Could not list models ({e}). Defaulting to {ACTIVE_MODEL_NAME}")

news_api_key = os.getenv("NEWS_API_KEY")

LABEL_MAP = {0: 'Fake', 1: 'Authentic'}

# --- 3. HELPER FUNCTIONS ---

def get_news_from_api(query, api_key):
    if not api_key: return []
    url = f"https://newsapi.org/v2/everything?q={query}&apiKey={api_key}&language=en&sortBy=relevancy&pageSize=5"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            articles = response.json().get('articles', [])
            return [{'title': a['title'], 'url': a['url'], 'description': a['description']} for a in articles]
        return []
    except:
        return []

def check_fake_news(news_article):
    if not model or not tfidf_vectorizer: return "Unknown"
    try:
        tfidf_article = tfidf_vectorizer.transform([news_article])
        prediction = model.predict(tfidf_article)
        return LABEL_MAP.get(prediction[0], 'Unknown')
    except:
        return "Error"

def get_gemini_explanation(user_input):
    if not gemini_api_key: return "API Key missing."
    
    try:
        # Use the auto-detected model name
        model_ai = genai.GenerativeModel(ACTIVE_MODEL_NAME)
        
        prompt = f"""Act as a fact-checker. Analyze: '{user_input}'.
        
        1. Determine if it is Authentic, Fake, or Satire.
        2. Provide a 3-point explanation.
        
        Format output exactly like this:
        Status: [Authentic/Fake]
        * Point 1
        * Point 2
        * Point 3
        """
        
        response = model_ai.generate_content(prompt)
        return response.text
        
    except Exception as e:
        error_str = str(e)
        if "429" in error_str:
            return "Status: Error\n* Daily Quota Exceeded."
        elif "404" in error_str:
            return f"Status: Error\n* Model '{ACTIVE_MODEL_NAME}' not found. Check API key permissions."
        else:
            return f"Status: Error\n* System Error: {error_str}"

def classify_articles(news_articles):
    results = []
    fake_count = 0
    for article in news_articles:
        text = f"{article['title']} {str(article['description'])}"
        classification = check_fake_news(text)
        results.append({'title': article['title'], 'classification': classification, 'url': article['url']})
        if classification == 'Fake': fake_count += 1
        
    accuracy = 0
    if news_articles:
        accuracy = (fake_count / len(news_articles)) * 100 if fake_count > len(news_articles)/2 else ((len(news_articles)-fake_count)/len(news_articles))*100

    majority_vote = 'Fake' if fake_count > len(news_articles) / 2 else 'Authentic'
    return majority_vote, accuracy, results

# --- 4. FLASK ROUTES ---

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    # Attempt to load index.html, fallback to check_new.html if missing
    return render_template('check_new.html')

@app.route('/check_news', methods=['GET', 'POST'])
def check_news():
    if request.method == 'GET':
        return render_template('index.html')

    data = request.get_json()
    news_input = data.get('news_input', '').strip()
    
    if not news_input:
        return jsonify({'error': 'Please enter a headline.'})
    
    # 1. Get AI Explanation
    explanation_text = get_gemini_explanation(news_input)
    
    # Extract AI Verdict
    ai_status = "Unknown"
    if "Status: Authentic" in explanation_text: ai_status = "Authentic"
    elif "Status: Fake" in explanation_text: ai_status = "Fake"

    # 2. Get Articles
    news_articles = get_news_from_api(news_input, news_api_key)
    
    # 3. Determine Final Verdict
    majority_vote = "Unknown"
    accuracy = 0
    all_articles = []

    if news_articles:
        majority_vote, accuracy, all_articles = classify_articles(news_articles)
    else:
        # If no articles, rely purely on AI
        majority_vote = ai_status if ai_status != "Unknown" else "Unverified"
        accuracy = 0

    final_verdict = majority_vote
    
    # LOGIC: AI overrides local model if AI is confident
    if ai_status == "Authentic":
        final_verdict = "Authentic"
        accuracy = 95.0
    elif ai_status == "Fake":
        final_verdict = "Fake"
        accuracy = 95.0
    
    # If both failed to find info
    if final_verdict == "Unknown":
        final_verdict = "Unverified"

    return jsonify({
        'majority_vote': final_verdict,
        'accuracy': round(accuracy, 2),
        'top_articles': all_articles[:3],
        'all_articles': all_articles,
        'explanation': explanation_text
    })

if __name__ == "__main__":
    app.run(debug=True)
