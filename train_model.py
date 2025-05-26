import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
import pickle

# Load datasets
fake_data = pd.read_csv("C:/Users/bhuva/fake-news-detector/Fake.csv")
true_data = pd.read_csv("C:/Users/bhuva/fake-news-detector/True.csv")

# Label datasets
fake_data['label'] = 0  # 0 for fake news
true_data['label'] = 1  # 1 for authentic news

# Combine datasets
data = pd.concat([fake_data, true_data])
data = data.sample(frac=1).reset_index(drop=True)  # Shuffle data

# Split data
X_train, X_test, y_train, y_test = train_test_split(data['text'], data['label'], test_size=0.2, random_state=42)

# TF-IDF Vectorization
tfidf_vectorizer = TfidfVectorizer(max_features=5000)
X_train_tfidf = tfidf_vectorizer.fit_transform(X_train)
X_test_tfidf = tfidf_vectorizer.transform(X_test)

# Model Training
model = LogisticRegression()
model.fit(X_train_tfidf, y_train)

# Evaluate Model
y_pred = model.predict(X_test_tfidf)
print("Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))

# Save model and vectorizer
with open("model.pkl", "wb") as model_file:
    pickle.dump(model, model_file)
with open("vectorizer.pkl", "wb") as vectorizer_file:
    pickle.dump(tfidf_vectorizer, vectorizer_file)
