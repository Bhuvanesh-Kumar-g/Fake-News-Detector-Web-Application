import requests
from transformers import pipeline

# Initialize the Hugging Face model pipeline
fake_news_pipeline = pipeline("text-classification", model="Pavan48/fake_news_detection_roberta")

# Your News API key
news_api_key = "cac896c4de1842ad8c489265e866af8b"

# Label mapping to human-readable terms
LABEL_MAP = {
    'LABEL_0': 'Fake',
    'LABEL_1': 'Authentic'
}

def get_news_from_api(query, api_key, language='en'):
    """Fetch news articles from News API based on a search query."""
    url = f"https://newsapi.org/v2/everything?q={query}&apiKey={api_key}&language={language}"
    response = requests.get(url)
    
    if response.status_code == 200:
        news_data = response.json()
        articles = news_data.get('articles', [])
        if articles:
            return [
                {
                    'title': article.get('title', 'No title available'),
                    'description': article.get('description', 'No description available'),
                    'url': article.get('url', '#')
                }
                for article in articles
            ]
        else:
            return []
    else:
        return []

def check_fake_news(news_article):
    """Classify a news article as Fake or Real using the Hugging Face model pipeline."""
    result = fake_news_pipeline(news_article)
    label = result[0]['label']
    return LABEL_MAP.get(label, 'Unknown')

def classify_articles(news_articles):
    """Classify multiple news articles and return aggregated results."""
    results = []
    fake_count = 0
    true_fakes = 0  # Count of correctly predicted "Fake"
    false_fakes = 0  # Count of incorrectly predicted "Fake" (False Positives)
    
    correct_predictions = 0
    # Since we're skipping actual labels for this test, we only count the predicted labels.
    
    for article in news_articles:
        article_text = f"{article['title']} {article['description']}"
        classification = check_fake_news(article_text)
        
        # For testing, we are not comparing with actual labels (because we don't have them here)
        # In actual implementation, you should compare predicted with real labels for evaluation
        
        if classification == 'Fake':
            fake_count += 1
        
        results.append({
            'title': article['title'],
            'classification': classification,
            'url': article['url']
        })
    
    # Calculate accuracy based on predictions
    accuracy = (fake_count / len(news_articles)) * 100 if news_articles else 0
    
    # Calculate Precision (assuming Fake is the positive class)
    precision = true_fakes / (true_fakes + false_fakes) if (true_fakes + false_fakes) > 0 else 0
    
    return accuracy, precision, results

def main():
    # Get user input for a search query
    query = input("Enter a topic or keyword to search news articles: ")
    
    # Fetch news articles
    news_articles = get_news_from_api(query, news_api_key)
    
    if news_articles:
        # Classify articles and get results
        accuracy, precision, all_articles = classify_articles(news_articles)
        
        # Print results in the console
        print(f"\nResults for '{query}':\n")
        print(f"Accuracy: {accuracy:.2f}%")
        print(f"Precision: {precision:.2f}")
        print("\nTop Articles:")
        
        # Display top 3 articles
        for idx, article in enumerate(all_articles[:3]):
            print(f"{idx + 1}. {article['title']}")
            print(f"   Classification: {article['classification']}")
            print(f"   URL: {article['url']}\n")
        
    else:
        print("No news articles found or there was an error fetching the news.")

if __name__ == "__main__":
    main()
