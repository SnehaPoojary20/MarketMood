import pandas as pd
import os
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

# Get the current script directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Define the correct data path
DATA_PATH = os.path.join(BASE_DIR, "..", "data", "data.csv")

# ✅ Ensure the data file exists before loading
if not os.path.exists(DATA_PATH):
    raise FileNotFoundError(f"❌ Data file not found: {DATA_PATH}")

# Load dataset
df = pd.read_csv(DATA_PATH)

# ✅ Print column names for debugging
print("Dataset Columns:", df.columns)

# ✅ Ensure the correct column names are used
if 'full_text' not in df.columns or 'label' not in df.columns:
    raise KeyError("❌ Required columns 'full_text' or 'label' not found in the dataset!")

X = df['full_text']
y = df['label']

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create a pipeline (TF-IDF + Naive Bayes)
model = Pipeline([
    ('tfidf', TfidfVectorizer(max_features=5000)),
    ('nb', MultinomialNB())
])

# Train the model
model.fit(X_train, y_train)

# ✅ Ensure 'data' directory exists before saving the model
MODEL_PATH = os.path.join(BASE_DIR, "..", "data", "fake_news_model.pkl")
os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)

# Save the trained model
joblib.dump(model, MODEL_PATH)

print(f"✅ Model trained and saved successfully at: {MODEL_PATH}")



