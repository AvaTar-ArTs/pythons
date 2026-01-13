#!/usr/bin/env python3
"""
Machine Learning Match Prioritization
Ensemble models for ranking DNA matches and investigative leads
"""

import numpy as np
import pandas as pd
from typing import List, Dict, Tuple
from dataclasses import dataclass
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import cross_val_score
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class MatchFeatures:
    """Features for ML model"""
    shared_cm: float
    longest_segment_cm: float
    num_segments: int
    kinship_coefficient: float
    likelihood_ratio: float
    confidence: float
    database_size_log: float  # log10 of database size
    population_frequency: float  # allele frequency in population
    geographic_distance_km: float = 0.0  # Distance between crime and match location
    age_match: bool = True  # Does age match crime timeline
    prior_criminal_record: bool = False

    def to_array(self) -> np.ndarray:
        """Convert to numpy array for ML model"""
        return np.array([
            self.shared_cm,
            self.longest_segment_cm,
            self.num_segments,
            self.kinship_coefficient,
            np.log10(self.likelihood_ratio) if self.likelihood_ratio > 0 else 0,
            self.confidence,
            self.database_size_log,
            self.population_frequency,
            self.geographic_distance_km,
            1.0 if self.age_match else 0.0,
            1.0 if self.prior_criminal_record else 0.0
        ])

    @staticmethod
    def feature_names() -> List[str]:
        """Get feature names"""
        return [
            'shared_cm',
            'longest_segment_cm',
            'num_segments',
            'kinship_coefficient',
            'log_likelihood_ratio',
            'confidence',
            'database_size_log',
            'population_frequency',
            'geographic_distance_km',
            'age_match',
            'prior_criminal_record'
        ]


class MLMatchPrioritizer:
    """
    Machine Learning model for prioritizing DNA matches

    Uses ensemble learning to combine:
    - DNA match strength
    - Statistical confidence
    - Contextual evidence
    - Geographic/temporal factors

    Models:
    - Random Forest: Captures non-linear relationships
    - Gradient Boosting: Optimizes ranking
    - Ensemble: Combines predictions
    """

    def __init__(self):
        """Initialize ML models"""
        self.rf_model = RandomForestClassifier(
            n_estimators=200,
            max_depth=10,
            min_samples_split=5,
            random_state=42
        )

        self.gb_model = GradientBoostingClassifier(
            n_estimators=200,
            learning_rate=0.1,
            max_depth=5,
            random_state=42
        )

        self.scaler = StandardScaler()
        self.is_trained = False

        logger.info("MLMatchPrioritizer initialized")

    def generate_training_data(self, num_samples: int = 1000) -> Tuple[np.ndarray, np.ndarray]:
        """
        Generate synthetic training data

        In production, this would use historical case data
        where matches were confirmed as true/false positives

        Args:
            num_samples: Number of training examples

        Returns:
            (X, y) training data
        """
        X = []
        y = []

        for _ in range(num_samples):
            # Simulate true positive (70% of data)
            if np.random.random() < 0.7:
                # Strong match characteristics
                shared_cm = np.random.gamma(8, 10)  # Mean ~80 cM
                longest_segment = shared_cm * np.random.uniform(0.3, 0.7)
                num_segments = int(np.random.gamma(5, 2))
                kinship = shared_cm / 10000  # Rough approximation
                lr = 10 ** np.random.uniform(2, 6)  # LR 100-1M
                confidence = np.random.beta(8, 2)  # High confidence
                pop_freq = np.random.uniform(0.3, 0.7)
                geo_distance = np.random.exponential(50)  # Nearby
                age_match = np.random.random() > 0.2  # Usually matches
                criminal_record = np.random.random() > 0.8  # Sometimes

                label = 1  # True positive
            else:
                # False positive characteristics
                shared_cm = np.random.gamma(3, 5)  # Mean ~15 cM
                longest_segment = shared_cm * np.random.uniform(0.5, 1.0)
                num_segments = int(np.random.gamma(2, 1))
                kinship = shared_cm / 20000
                lr = 10 ** np.random.uniform(0, 2)  # LR 1-100
                confidence = np.random.beta(2, 5)  # Low confidence
                pop_freq = np.random.uniform(0.1, 0.5)
                geo_distance = np.random.exponential(200)  # Farther
                age_match = np.random.random() > 0.6  # Often doesn't match
                criminal_record = np.random.random() > 0.95  # Rarely

                label = 0  # False positive

            features = MatchFeatures(
                shared_cm=shared_cm,
                longest_segment_cm=longest_segment,
                num_segments=num_segments,
                kinship_coefficient=kinship,
                likelihood_ratio=lr,
                confidence=confidence,
                database_size_log=np.log10(1e6),  # 1M database
                population_frequency=pop_freq,
                geographic_distance_km=geo_distance,
                age_match=age_match,
                prior_criminal_record=criminal_record
            )

            X.append(features.to_array())
            y.append(label)

        return np.array(X), np.array(y)

    def train(self, X: np.ndarray = None, y: np.ndarray = None):
        """
        Train the ML models

        Args:
            X: Feature matrix (if None, generates synthetic data)
            y: Labels
        """
        if X is None or y is None:
            logger.info("Generating synthetic training data...")
            X, y = self.generate_training_data(num_samples=2000)

        logger.info(f"Training on {len(X)} samples...")

        # Scale features
        X_scaled = self.scaler.fit_transform(X)

        # Train Random Forest
        logger.info("Training Random Forest...")
        self.rf_model.fit(X_scaled, y)
        rf_score = cross_val_score(self.rf_model, X_scaled, y, cv=5).mean()
        logger.info(f"Random Forest CV Score: {rf_score:.3f}")

        # Train Gradient Boosting
        logger.info("Training Gradient Boosting...")
        self.gb_model.fit(X_scaled, y)
        gb_score = cross_val_score(self.gb_model, X_scaled, y, cv=5).mean()
        logger.info(f"Gradient Boosting CV Score: {gb_score:.3f}")

        self.is_trained = True
        logger.info("Training complete")

    def predict_priority_score(self, features: MatchFeatures) -> float:
        """
        Predict priority score for a match

        Args:
            features: Match features

        Returns:
            Priority score (0-1, higher = more important)
        """
        if not self.is_trained:
            logger.warning("Model not trained - training on synthetic data...")
            self.train()

        X = features.to_array().reshape(1, -1)
        X_scaled = self.scaler.transform(X)

        # Get probabilities from both models
        rf_prob = self.rf_model.predict_proba(X_scaled)[0, 1]
        gb_prob = self.gb_model.predict_proba(X_scaled)[0, 1]

        # Ensemble: weighted average
        ensemble_score = 0.5 * rf_prob + 0.5 * gb_prob

        return ensemble_score

    def rank_matches(self, matches_features: List[MatchFeatures]) -> List[Tuple[int, float]]:
        """
        Rank matches by priority

        Args:
            matches_features: List of match features

        Returns:
            List of (match_index, priority_score) sorted by priority
        """
        scores = []

        for i, features in enumerate(matches_features):
            score = self.predict_priority_score(features)
            scores.append((i, score))

        # Sort by score descending
        scores.sort(key=lambda x: x[1], reverse=True)

        return scores

    def get_feature_importance(self) -> pd.DataFrame:
        """
        Get feature importance from models

        Returns:
            DataFrame with feature importances
        """
        if not self.is_trained:
            raise ValueError("Model must be trained first")

        feature_names = MatchFeatures.feature_names()

        importance_df = pd.DataFrame({
            'feature': feature_names,
            'rf_importance': self.rf_model.feature_importances_,
            'gb_importance': self.gb_model.feature_importances_
        })

        importance_df['avg_importance'] = (
            importance_df['rf_importance'] + importance_df['gb_importance']
        ) / 2

        importance_df = importance_df.sort_values('avg_importance', ascending=False)

        return importance_df

    def explain_prediction(self, features: MatchFeatures) -> Dict:
        """
        Explain why a match received its priority score

        Args:
            features: Match features

        Returns:
            Dictionary with explanation
        """
        score = self.predict_priority_score(features)

        # Get feature values
        feature_values = features.to_array()
        feature_names = MatchFeatures.feature_names()

        # Get feature importance
        importance_df = self.get_feature_importance()

        # Identify top contributing features
        top_features = []
        for i, name in enumerate(feature_names):
            importance = importance_df[importance_df['feature'] == name]['avg_importance'].values[0]
            value = feature_values[i]

            contribution = importance * abs(value)
            top_features.append({
                'feature': name,
                'value': value,
                'importance': importance,
                'contribution': contribution
            })

        top_features.sort(key=lambda x: x['contribution'], reverse=True)

        explanation = {
            'priority_score': score,
            'interpretation': self._interpret_score(score),
            'top_contributing_features': top_features[:5],
            'model_confidence': max(score, 1 - score)  # Distance from 0.5
        }

        return explanation

    def _interpret_score(self, score: float) -> str:
        """Interpret priority score"""
        if score >= 0.9:
            return "CRITICAL - Immediate investigation required"
        elif score >= 0.75:
            return "HIGH - Priority investigation"
        elif score >= 0.5:
            return "MODERATE - Standard follow-up"
        elif score >= 0.3:
            return "LOW - Additional validation needed"
        else:
            return "MINIMAL - Likely false positive"


if __name__ == "__main__":
    print("ML Match Prioritizer - Ensemble Learning System")
    print("=" * 60)

    # Initialize
    prioritizer = MLMatchPrioritizer()

    # Train model
    print("\nTraining models...")
    prioritizer.train()

    # Test with example matches
    print("\n" + "=" * 60)
    print("TESTING ON SAMPLE MATCHES")
    print("=" * 60)

    # Strong match
    strong_match = MatchFeatures(
        shared_cm=85.0,
        longest_segment_cm=45.0,
        num_segments=12,
        kinship_coefficient=0.0042,
        likelihood_ratio=2.3e4,
        confidence=0.87,
        database_size_log=6.0,
        population_frequency=0.5,
        geographic_distance_km=25.0,
        age_match=True,
        prior_criminal_record=False
    )

    # Weak match
    weak_match = MatchFeatures(
        shared_cm=18.0,
        longest_segment_cm=12.0,
        num_segments=3,
        kinship_coefficient=0.0009,
        likelihood_ratio=120,
        confidence=0.42,
        database_size_log=6.0,
        population_frequency=0.3,
        geographic_distance_km=300.0,
        age_match=False,
        prior_criminal_record=False
    )

    # Evaluate matches
    for i, match in enumerate([strong_match, weak_match], 1):
        print(f"\nMatch {i}:")
        print(f"  Shared cM: {match.shared_cm}")
        print(f"  LR: {match.likelihood_ratio:.2e}")

        explanation = prioritizer.explain_prediction(match)

        print(f"\n  Priority Score: {explanation['priority_score']:.3f}")
        print(f"  Interpretation: {explanation['interpretation']}")
        print(f"  Model Confidence: {explanation['model_confidence']:.3f}")

        print("\n  Top Contributing Features:")
        for feat in explanation['top_contributing_features'][:3]:
            print(f"    - {feat['feature']}: {feat['value']:.2f} (importance: {feat['importance']:.3f})")

    # Feature importance
    print("\n" + "=" * 60)
    print("FEATURE IMPORTANCE")
    print("=" * 60)
    print(prioritizer.get_feature_importance().to_string(index=False))
