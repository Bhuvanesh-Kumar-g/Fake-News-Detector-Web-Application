# Fake News Detector Web Application

This project is a web application designed to help users identify potentially fake news articles. It takes a news headline or topic as input, fetches related articles using the News API, classifies them using a pre-trained Hugging Face model, and presents an overall assessment.

*(Optional: Add a screenshot of your web app here. Name it `Screenshot 2025-05-26 121759.png` and place it in the root directory.)*
<!-- ![Screenshot of the Fake News Detector](./app_screenshot.png) -->

## Features

*   **News Input:** Users can enter a news headline or topic.
*   **News Aggregation:** Fetches relevant articles from the News API.
*   **AI-Powered Classification:** Uses a Hugging Face `roberta-base` model fine-tuned for fake news detection (`Pavan48/fake_news_detection_roberta`) to classify articles.
*   **Aggregated Results:** Provides an overall "Fake" or "Authentic" assessment based on the fetched articles.
*   **Accuracy Score:** Displays a (currently boosted for demonstration) accuracy percentage.
*   **Article Listing:** Shows top related articles and allows users to view all fetched articles with their classifications and links to the original source.
*   **Web Interface:** A Flask-based web application with a user-friendly interface.


**Note on Model Usage:** The primary classification in `fake_news_app.py` is done via a Hugging Face model (`Pavan48/fake_news_detection_roberta`). The `.pkl` files and `train_model.py` seem to relate to an alternative, locally trained model approach which is not currently integrated into the main web application's classification logic.

## Prerequisites

*   Python 3.7+
*   `pip` (Python package installer)
*   Git (for cloning from GitHub)
*   A News API Key (from [newsapi.org](https://newsapi.org/)) - Instructions to get one are below.

---

## How to Run This Application

Follow these steps carefully to set up and run the project:

### Step 1: Get a News API Key

This application requires an API key from [NewsAPI.org](https://newsapi.org/) to fetch news articles.
1.  Go to [https://newsapi.org/](https://newsapi.org/).
2.  Click on **"Get API Key"** or "Register".
3.  Follow the registration process. They offer a free plan suitable for development and personal projects.
4.  Once registered, you will find your API key in your account dashboard. **Copy this key and keep it safe.** You will need it in Step 4.

### Step 2: Clone the Repository (If you haven't already)

1.  Open your terminal or command prompt.
2.  Clone the repository (replace `YOUR_USERNAME/YOUR_REPOSITORY_NAME` with the actual GitHub path):
    ```bash
    git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY_NAME.git
    ```
3.  Navigate into the cloned project directory:
    ```bash
    cd YOUR_REPOSITORY_NAME
    ```

### Step 3: Set Up a Python Virtual Environment (Recommended)

This isolates project dependencies.
1.  **Create the virtual environment:**
    *   Windows: `python -m venv venv`
    *   macOS/Linux: `python3 -m venv venv`
2.  **Activate the virtual environment:**
    *   Windows: `.\venv\Scripts\activate`
    *   macOS/Linux: `source venv/bin/activate`
    You should see `(venv)` or similar at the beginning of your terminal prompt.

### Step 4: Configure the News API Key in the Application

You have two options:

**Option A: Using Environment Variables (Recommended for Security)**

1.  Set an environment variable named `NEWS_API_KEY` to the value of the API key you obtained in Step 1.
    *   **Windows (Command Prompt for current session):**
        ```bash
        set NEWS_API_KEY=YOUR_ACTUAL_NEWS_API_KEY
        ```
    *   **Windows (PowerShell for current session):**
        ```powershell
        $env:NEWS_API_KEY="YOUR_ACTUAL_NEWS_API_KEY"
        ```
    *   **macOS/Linux (for current session):**
        ```bash
        export NEWS_API_KEY=YOUR_ACTUAL_NEWS_API_KEY
        ```
    To make it permanent, add this export line to your shell's configuration file (e.g., `.bashrc`, `.zshrc`).
2.  Modify `fake_news_app.py` to use this environment variable. Ensure the top of your `fake_news_app.py` has:
    ```python
    import os
    # ...
    news_api_key = os.environ.get("NEWS_API_KEY")
    if not news_api_key:
        raise ValueError("NEWS_API_KEY environment variable not set. Please set it before running the app.")
    # ...
    ```
    (Your current `fake_news_app.py` might already have a placeholder for this logic, or you'll need to add it as shown above, removing the hardcoded key.)

**Option B: Hardcoding (Less Secure, for quick local testing only)**
   *BEWARE: Do not commit this version to a public repository.*
1.  Open the `fake_news_app.py` file in a text editor.
2.  Find the line: `news_api_key = "cac896c4de1842ad8c489265e866af8b"` (or similar).
3.  Replace `"cac896c4de1842ad8c489265e866af8b"` with **your actual News API key** obtained in Step 1.
    Example: `news_api_key = "YOUR_ACTUAL_NEWS_API_KEY"`

### Step 5: Install Python Dependencies

1.  Ensure your virtual environment is activated.
2.  Create a `requirements.txt` file in the project's root directory with the following content (or generate it using `pip freeze > requirements.txt` if you've already installed packages):
    ```txt
    Flask
    requests
    transformers
    torch 
    # or tensorflow (depending on what transformers defaults to or your preference)
    # Add other libraries if used by train_model.py, test.py etc. e.g., scikit-learn, pandas
    ```
3.  Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```
    This might take a few minutes, especially for `torch` and `transformers`.

### Step 6: Run the Flask Application

1.  Make sure you are in the project's root directory in your terminal and your virtual environment is activated.
2.  If you used **Option A** for the API key, ensure the environment variable is set in your current terminal session.
3.  Execute the main application file:
    ```bash
    python fake_news_app.py
    ```
4.  You should see output similar to this, indicating the server is running:
    ```
    * Serving Flask app 'fake_news_app' (lazy loading)
    * Environment: production
      WARNING: This is a development server. Do not use it in a production deployment.
      Use a production WSGI server instead.
    * Debug mode: on
    * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
    ...
    ```
    (Note: Your app runs in `debug=True` mode as per your `if __name__ == "__main__": app.run(debug=True)`.)

### Step 7: Access the Application in Your Browser

1.  Open your web browser (e.g., Chrome, Firefox, Edge).
2.  Navigate to the following address: `http://127.0.0.1:5000/`
3.  You should see the landing page of the Fake News Detector.

---

## Usage Guide

1.  The application opens to a landing page (`index.html`).
2.  Click "Get Started" or "Check News" to navigate to the news checking page (`check_new.html`).
3.  Enter a news headline, topic, or keywords into the text area.
4.  Click the "Check if it's Fake" button.
5.  The application will fetch related news articles, classify them, and display:
    *   An overall classification ("Fake" or "Authentic").
    *   An "accuracy" score.
    *   A list of the top 3 articles with their individual classifications and links.
    *   A button to "Show All Articles" fetched and their classifications.

## Technical Details

*   **Backend:** Flask (Python)
*   **Frontend:** HTML, CSS, JavaScript
*   **News Source:** [News API](https://newsapi.org/)
*   **Fake News Classification Model:** Hugging Face Transformers pipeline using the `Pavan48/fake_news_detection_roberta` model (a RoBERTa-base model fine-tuned for fake news detection).
*   **Local Model Training (Experimental/Alternative):** `train_model.py` likely uses traditional ML techniques (e.g., TF-IDF + Logistic Regression/SVM) with `scikit-learn`, using `Fake.csv` and `True.csv` datasets.

## Important Security Notes

*   **`client_secret_....json`:** This file should **NEVER** be public. If it's for Google services, ensure it's handled securely, typically loaded from a secure location or environment variable, and add the filename to your `.gitignore` file.
*   **API Keys:** Never hardcode API keys directly into source code that will be made public. Use environment variables (as described in Step 4, Option A) or other secure configuration methods.

## Troubleshooting

*   **`ValueError: NEWS_API_KEY environment variable not set`:** You chose Option A for API key setup but didn't set the environment variable correctly in your current terminal session. Re-run the `export` or `set` command.
*   **API Key Errors / No Articles Found:**
    *   Ensure your News API key is correct and active. Double-check for typos.
    *   Check your News API plan for request limits (free plans have daily limits).
    *   The query might not return any articles; try broader search terms.
*   **Model Loading Issues (Hugging Face):**
    *   Ensure you have a stable internet connection for the first run, as the Hugging Face model (`Pavan48/fake_news_detection_roberta`) will be downloaded.
    *   Make sure `transformers` and `torch` (or `tensorflow`) are installed correctly in your virtual environment.
*   **Missing `requirements.txt` or Dependencies:** If `pip install -r requirements.txt` fails or you get "ModuleNotFoundError", ensure `requirements.txt` exists and is correct, and your virtual environment is active. You might need to manually install packages: `pip install Flask requests transformers torch`.
