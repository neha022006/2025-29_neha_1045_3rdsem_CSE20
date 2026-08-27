import pandas as pd
import re

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import FeatureUnion
from sklearn.preprocessing import FunctionTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

# Sample dataset
data = {
    "email": [
        "Congratulations! You have won a free iPhone. Click here http://fake-prize.com",
        "Your bank account has been suspended. Verify your account immediately.",
        "Urgent! Click this link to claim your reward http://scam-link.com",
        "You won a lottery! Send your bank details now.",
        "Update your password immediately using this link http://secure-login.xyz",
        "Meeting scheduled for tomorrow at 10 AM.",
        "Please find the project report attached.",
        "Thank you for your purchase. Your order has been confirmed.",
        "Don't forget about our team meeting this afternoon.",
        "Your monthly salary has been credited to your account.",
        "Can we discuss the assignment tomorrow?",
        "Here are the notes from today's cybersecurity lecture."
    ],
    "label": [
        "Phishing", "Phishing", "Phishing", "Phishing",
        "Phishing", "Safe", "Safe", "Safe",
        "Safe", "Safe", "Safe", "Safe"
    ]
}

df = pd.DataFrame(data)

# Convert labels into numbers
df["label"] = df["label"].map({
    "Safe": 0,
    "Phishing": 1
})

X = df["email"]
y = df["label"]

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.25,
    random_state=42,
    stratify=y
)

# Extract text features
vectorizer = TfidfVectorizer(
    stop_words="english",
    ngram_range=(1, 2)
)

# Train model
model = Pipeline([
    ("vectorizer", vectorizer),
    ("classifier", MultinomialNB())
])

model.fit(X_train, y_train)

# Predictions
predictions = model.predict(X_test)

# Accuracy
accuracy = accuracy_score(y_test, predictions)

print("\n--- Phishing Email Detection Results ---")
print(f"Accuracy: {accuracy * 100:.2f}%")

print("\nClassification Report:")
print(classification_report(
    y_test,
    predictions,
    target_names=["Safe", "Phishing"]
))

# Confusion Matrix
cm = confusion_matrix(y_test, predictions)

print("Confusion Matrix:")
print(cm)

# Test custom emails
print("\n--- Test Email Classification ---")

test_emails = [
    "Congratulations! Click here immediately to claim your free reward.",
    "Hi team, the meeting is scheduled for Monday at 11 AM."
]

results = model.predict(test_emails)

for email, result in zip(test_emails, results):
    label = "Phishing" if result == 1 else "Safe"
    print(f"\nEmail: {email}")
    print(f"Prediction: {label}")