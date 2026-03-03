"""
Train credibility classification model on LIAR dataset

Phase 3: TF-IDF + Logistic Regression baseline
Target: 70%+ accuracy on test set
"""

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
import joblib
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')


# Label mapping: LIAR's 6 classes -> Our 4 classes
LABEL_MAPPING = {
    'pants-fire': 0,  # Likely Unreliable
    'false': 0,       # Likely Unreliable
    'barely-true': 1, # Mixed
    'half-true': 1,   # Mixed
    'mostly-true': 2, # Likely Reliable
    'true': 2         # Likely Reliable
}

LABEL_NAMES = {
    0: 'Likely Unreliable',
    1: 'Mixed',
    2: 'Likely Reliable'
}


def load_liar_dataset(filepath):
    """
    Load LIAR dataset from TSV file.

    Columns:
    0: ID, 1: label, 2: statement, 3: subject, 4-7: speaker info,
    8-12: credit history, 13: context

    We only need columns 1 (label) and 2 (statement)
    """
    print(f"Loading {filepath}...")

    df = pd.read_csv(
        filepath,
        sep='\t',
        header=None,
        usecols=[1, 2],  # label and statement only
        names=['label', 'statement']
    )

    print(f"  Loaded {len(df)} statements")
    return df


def preprocess_text(text):
    """
    Clean and preprocess text:
    - Lowercase
    - Basic cleaning
    - KEEP stopwords (they matter for credibility: "never", "always", etc.)
    """
    if not isinstance(text, str):
        return ""

    # Lowercase
    text = text.lower()

    # Remove URLs
    text = re.sub(r'http\S+|www\S+', '', text)

    # Keep most punctuation for now (! and ? can signal bias)
    # Just clean up extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()

    return text


def map_labels(df):
    """Map 6-class labels to 3-class labels"""
    df['label_mapped'] = df['label'].map(LABEL_MAPPING)

    # Drop any rows with unmapped labels
    df = df.dropna(subset=['label_mapped'])
    df['label_mapped'] = df['label_mapped'].astype(int)

    print(f"\nLabel distribution:")
    for label_id, count in df['label_mapped'].value_counts().sort_index().items():
        print(f"  {LABEL_NAMES[label_id]}: {count} ({count/len(df)*100:.1f}%)")

    return df


def main():
    print("=" * 60)
    print("VERITAS AI - Phase 3: Train Credibility Model")
    print("=" * 60)

    # 1. Load datasets
    print("\n[1/6] Loading LIAR dataset...")
    train_df = load_liar_dataset('data/train.tsv')
    test_df = load_liar_dataset('data/test.tsv')
    valid_df = load_liar_dataset('data/valid.tsv')

    # 2. Map labels
    print("\n[2/6] Mapping labels (6-class -> 3-class)...")
    train_df = map_labels(train_df)
    test_df = map_labels(test_df)
    valid_df = map_labels(valid_df)

    # 3. Preprocess text
    print("\n[3/6] Preprocessing text...")
    print("  (lowercase, remove stopwords, clean punctuation)")

    train_df['statement_clean'] = train_df['statement'].apply(preprocess_text)
    test_df['statement_clean'] = test_df['statement'].apply(preprocess_text)
    valid_df['statement_clean'] = valid_df['statement'].apply(preprocess_text)

    # Remove empty statements
    train_df = train_df[train_df['statement_clean'].str.len() > 0]
    test_df = test_df[test_df['statement_clean'].str.len() > 0]

    print(f"  Training samples: {len(train_df)}")
    print(f"  Test samples: {len(test_df)}")
    print(f"  Validation samples: {len(valid_df)}")

    # 4. Build pipeline: TF-IDF + Logistic Regression
    print("\n[4/6] Building ML pipeline...")
    print("  TF-IDF Vectorizer -> Logistic Regression")

    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(
            max_features=10000,     # Increased from 5000
            ngram_range=(1, 3),     # Unigrams, bigrams, trigrams
            min_df=2,               # Ignore very rare words
            max_df=0.7,             # Ignore very common words (more aggressive)
            sublinear_tf=True       # Use log scaling for term frequency
        )),
        ('classifier', LogisticRegression(
            max_iter=2000,          # More iterations
            C=1.5,                  # Regularization strength
            class_weight='balanced',  # Handle class imbalance
            solver='saga',          # Better for large datasets
            random_state=42
        ))
    ])

    # 5. Train model
    print("\n[5/6] Training model...")
    X_train = train_df['statement_clean']
    y_train = train_df['label_mapped']

    pipeline.fit(X_train, y_train)
    print("  ✓ Training complete!")

    # 6. Evaluate on test set
    print("\n[6/6] Evaluating on test set...")
    X_test = test_df['statement_clean']
    y_test = test_df['label_mapped']

    y_pred = pipeline.predict(X_test)
    y_proba = pipeline.predict_proba(X_test)

    accuracy = accuracy_score(y_test, y_pred)
    print(f"\n{'='*60}")
    print(f"TEST SET ACCURACY: {accuracy:.1%}")
    print(f"{'='*60}")

    if accuracy >= 0.70:
        print("✓ SUCCESS: Exceeded 70% target!")
    else:
        print("⚠ WARNING: Below 70% target")

    print("\nDetailed Classification Report:")
    print(classification_report(
        y_test,
        y_pred,
        target_names=[LABEL_NAMES[i] for i in sorted(LABEL_NAMES.keys())]
    ))

    print("\nConfusion Matrix:")
    cm = confusion_matrix(y_test, y_pred)
    print("              Predicted")
    print("                 0    1    2")
    for i, row in enumerate(cm):
        if i == 0:
            print(f"Actual   {i}   {row[0]:4} {row[1]:4} {row[2]:4}")
        else:
            print(f"         {i}   {row[0]:4} {row[1]:4} {row[2]:4}")

    # 7. Save model
    print("\n[7/7] Saving model...")
    model_path = 'models/credibility_model.pkl'

    import os
    os.makedirs('models', exist_ok=True)

    joblib.dump(pipeline, model_path)
    print(f"  ✓ Model saved to: {model_path}")

    # Save label mapping
    metadata = {
        'label_names': LABEL_NAMES,
        'accuracy': accuracy,
        'num_features': 5000,
        'model_type': 'TF-IDF + Logistic Regression'
    }
    joblib.dump(metadata, 'models/model_metadata.pkl')
    print(f"  ✓ Metadata saved to: models/model_metadata.pkl")

    print("\n" + "=" * 60)
    print("TRAINING COMPLETE!")
    print("=" * 60)
    print("\nNext steps:")
    print("  1. Integrate model into API (api/services/ml_model.py)")
    print("  2. Update analyzer.py to use real model predictions")
    print("  3. Test end-to-end with extension")


if __name__ == '__main__':
    main()
