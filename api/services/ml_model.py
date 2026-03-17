"""
ML Model service - Phase 3

Loads the trained TF-IDF + Logistic Regression model and provides
content credibility predictions.
"""

import os
import re
import joblib
from typing import Dict

# Path to saved model (relative to api/ directory)
MODEL_PATH = os.path.join(os.path.dirname(__file__), '../../model/models/credibility_model.pkl')
METADATA_PATH = os.path.join(os.path.dirname(__file__), '../../model/models/model_metadata.pkl')

# Cache loaded model in memory
_model = None
_metadata = None


def _load_model():
    global _model, _metadata
    if _model is None:
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(f"Model not found at {MODEL_PATH}. Run model/train.py first.")
        _model = joblib.load(MODEL_PATH)
        _metadata = joblib.load(METADATA_PATH)
        print(f"  [ML] Model loaded (accuracy: {_metadata['accuracy']:.1%})")
    return _model, _metadata


def preprocess_text(text: str) -> str:
    """Same preprocessing as used during training."""
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r'http\S+|www\S+', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def predict_credibility(title: str, text_content: str) -> Dict:
    """
    Predict content credibility using ML model.

    Returns:
        {
            'score': int (0-100),
            'label': str ('Likely Unreliable' | 'Mixed' | 'Likely Reliable'),
            'confidence': float (0-1)
        }
    """
    try:
        model, metadata = _load_model()

        # Use title + first 500 chars of content for prediction
        combined = title + " " + text_content[:500]
        cleaned = preprocess_text(combined)

        if not cleaned:
            return {'score': 50, 'label': 'Mixed', 'confidence': 0.0}

        label_id = model.predict([cleaned])[0]
        probabilities = model.predict_proba([cleaned])[0]
        confidence = float(probabilities[label_id])

        label_names = metadata['label_names']
        label = label_names[label_id]

        # Map label to 0-100 score
        score_map = {
            0: 30,  # Likely Unreliable
            1: 55,  # Mixed
            2: 80,  # Likely Reliable
        }
        base_score = score_map[label_id]

        # Nudge score based on confidence (higher confidence = more extreme score)
        confidence_boost = int((confidence - 0.5) * 20)
        score = max(10, min(95, base_score + confidence_boost))

        return {'score': score, 'label': label, 'confidence': confidence}

    except Exception as e:
        print(f"  [ML] Prediction failed: {e}, falling back to neutral score")
        return {'score': 50, 'label': 'Mixed', 'confidence': 0.0}
