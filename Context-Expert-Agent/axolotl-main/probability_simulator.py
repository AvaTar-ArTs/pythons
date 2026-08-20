#!/usr/bin/env python3
"""
Probability Simulation Framework
Monte Carlo simulations for relationship probability estimation
"""

import numpy as np
from scipy.stats import gamma, expon, norm
from typing import Dict, List, Tuple
from dataclasses import dataclass
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class SimulationResult:
    """Results from Monte Carlo simulation"""
    relationship: str
    mean_shared_cm: float
    median_shared_cm: float
    std_shared_cm: float
    confidence_intervals: Dict[float, Tuple[float, float]]  # {95: (low, high)}
    samples: np.ndarray

    def __repr__(self):
        ci_95 = self.confidence_intervals.get(95, (0, 0))
        return (f"SimulationResult({self.relationship}: "
                f"mean={self.mean_shared_cm:.1f}cM, "
                f"95%CI=[{ci_95[0]:.1f}, {ci_95[1]:.1f}])")


class ProbabilitySimulator:
    """
    Monte Carlo simulator for forensic DNA probability estimation

    Simulates:
    - DNA sharing distributions for various relationships
    - Likelihood ratios with uncertainty quantification
    - False positive/negative rates
    - Database size effects
    """

    # Relationship parameters (mean cM, std cM)
    RELATIONSHIP_PARAMS = {
        'parent_child': (3400, 200),
        'full_sibling': (2550, 450),
        'half_sibling': (1700, 400),
        'grandparent_grandchild': (1700, 400),
        'aunt_uncle_niece_nephew': (1700, 400),
        '1st_cousin': (850, 250),
        '1st_cousin_once_removed': (425, 150),
        '2nd_cousin': (212, 107),
        '2nd_cousin_once_removed': (106, 60),
        '3rd_cousin': (75, 50),
        '3rd_cousin_once_removed': (37, 30),
        '4th_cousin': (30, 25),
        '4th_cousin_once_removed': (15, 15),
        '5th_cousin': (15, 15),
        '6th_cousin': (7, 7),
        'unrelated': (5, 5)
    }

    def __init__(self, random_seed: int = None):
        """
        Initialize simulator

        Args:
            random_seed: Random seed for reproducibility
        """
        if random_seed is not None:
            np.random.seed(random_seed)
            logger.info(f"Random seed set to {random_seed}")

    def simulate_relationship(
        self,
        relationship: str,
        num_simulations: int = 10000
    ) -> SimulationResult:
        """
        Simulate DNA sharing for a relationship

        Args:
            relationship: Relationship type
            num_simulations: Number of Monte Carlo samples

        Returns:
            SimulationResult object
        """
        if relationship not in self.RELATIONSHIP_PARAMS:
            raise ValueError(f"Unknown relationship: {relationship}")

        mean_cm, std_cm = self.RELATIONSHIP_PARAMS[relationship]

        # Use gamma distribution (non-negative, right-skewed)
        shape = (mean_cm ** 2) / (std_cm ** 2)
        scale = (std_cm ** 2) / mean_cm

        # Generate samples
        samples = gamma.rvs(shape, scale=scale, size=num_simulations)

        # Calculate statistics
        mean_val = np.mean(samples)
        median_val = np.median(samples)
        std_val = np.std(samples)

        # Confidence intervals
        confidence_intervals = {
            68: (np.percentile(samples, 16), np.percentile(samples, 84)),  # 1-sigma
            95: (np.percentile(samples, 2.5), np.percentile(samples, 97.5)),  # 2-sigma
            99: (np.percentile(samples, 0.5), np.percentile(samples, 99.5))  # 3-sigma
        }

        result = SimulationResult(
            relationship=relationship,
            mean_shared_cm=mean_val,
            median_shared_cm=median_val,
            std_shared_cm=std_val,
            confidence_intervals=confidence_intervals,
            samples=samples
        )

        logger.info(f"Simulated {num_simulations:,} samples for {relationship}")

        return result

    def simulate_likelihood_ratio(
        self,
        observed_cm: float,
        hypothesized_relationship: str,
        null_relationship: str = 'unrelated',
        num_simulations: int = 10000
    ) -> Dict:
        """
        Simulate likelihood ratio distribution

        LR = P(observed_cm | H1) / P(observed_cm | H0)

        Args:
            observed_cm: Observed shared centiMorgans
            hypothesized_relationship: Proposed relationship (H1)
            null_relationship: Null hypothesis (H0)
            num_simulations: Number of simulations

        Returns:
            Dictionary with LR statistics
        """
        # Simulate under H1
        h1_result = self.simulate_relationship(hypothesized_relationship, num_simulations)

        # Simulate under H0
        h0_result = self.simulate_relationship(null_relationship, num_simulations)

        # Get parameters for probability calculations
        mean_h1, std_h1 = self.RELATIONSHIP_PARAMS[hypothesized_relationship]
        mean_h0, std_h0 = self.RELATIONSHIP_PARAMS[null_relationship]

        # Calculate likelihoods using gamma distributions
        shape_h1 = (mean_h1 ** 2) / (std_h1 ** 2)
        scale_h1 = (std_h1 ** 2) / mean_h1
        L1 = gamma.pdf(observed_cm, shape_h1, scale=scale_h1)

        # For unrelated, use exponential
        if null_relationship == 'unrelated':
            L0 = expon.pdf(observed_cm, scale=5.0)
        else:
            shape_h0 = (mean_h0 ** 2) / (std_h0 ** 2)
            scale_h0 = (std_h0 ** 2) / mean_h0
            L0 = gamma.pdf(observed_cm, shape_h0, scale=scale_h0)

        # Likelihood ratio
        lr = L1 / max(L0, 1e-20)

        # Calculate percentile of observed value in each distribution
        percentile_h1 = np.sum(h1_result.samples <= observed_cm) / num_simulations * 100
        percentile_h0 = np.sum(h0_result.samples <= observed_cm) / num_simulations * 100

        # Bayesian interpretation with prior
        prior_odds = 0.001  # Prior: 1 in 1000 chance of relationship
        posterior_odds = prior_odds * lr
        posterior_probability = posterior_odds / (1 + posterior_odds)

        result = {
            'observed_cm': observed_cm,
            'hypothesis_h1': hypothesized_relationship,
            'hypothesis_h0': null_relationship,
            'likelihood_ratio': lr,
            'log_lr': np.log10(lr) if lr > 0 else -np.inf,
            'posterior_probability': posterior_probability,
            'percentile_in_h1': percentile_h1,
            'percentile_in_h0': percentile_h0,
            'h1_mean': mean_h1,
            'h0_mean': mean_h0,
            'interpretation': self._interpret_lr(lr)
        }

        return result

    def _interpret_lr(self, lr: float) -> str:
        """Interpret likelihood ratio using standard scale"""
        if lr >= 1e6:
            return "Extremely strong support for H1"
        elif lr >= 1e4:
            return "Very strong support for H1"
        elif lr >= 1e3:
            return "Strong support for H1"
        elif lr >= 100:
            return "Moderate support for H1"
        elif lr >= 10:
            return "Weak support for H1"
        elif lr >= 1:
            return "Minimal support for H1"
        else:
            return "Supports H0 over H1"

    def simulate_database_search(
        self,
        query_relationship: str,
        database_size: int = 1000000,
        false_match_rate: float = 0.001,
        num_simulations: int = 1000
    ) -> Dict:
        """
        Simulate database search with false positive analysis

        Args:
            query_relationship: True relationship to query
            database_size: Number of profiles in database
            false_match_rate: Rate of false matches
            num_simulations: Number of search simulations

        Returns:
            Statistics on true positives, false positives
        """
        true_positives = 0
        false_positives_list = []

        for _ in range(num_simulations):
            # Simulate true match
            true_match_result = self.simulate_relationship(query_relationship, 1)
            true_match_cm = true_match_result.samples[0]

            # Simulate false matches from database
            false_matches = np.random.binomial(database_size, false_match_rate)
            false_match_cms = expon.rvs(scale=5.0, size=false_matches)

            # Count matches above threshold (e.g., 20 cM)
            threshold_cm = 20.0

            if true_match_cm >= threshold_cm:
                true_positives += 1

            false_positives = np.sum(false_match_cms >= threshold_cm)
            false_positives_list.append(false_positives)

        result = {
            'database_size': database_size,
            'query_relationship': query_relationship,
            'num_simulations': num_simulations,
            'true_positive_rate': true_positives / num_simulations,
            'mean_false_positives': np.mean(false_positives_list),
            'median_false_positives': np.median(false_positives_list),
            'max_false_positives': np.max(false_positives_list),
            'false_positive_list': false_positives_list
        }

        logger.info(f"Database search simulation: TPR={result['true_positive_rate']:.2%}, "
                   f"Mean FP={result['mean_false_positives']:.1f}")

        return result

    def calculate_confidence_interval(
        self,
        observed_cm: float,
        relationship: str,
        confidence_level: float = 0.95
    ) -> Tuple[float, float]:
        """
        Calculate confidence interval for relationship probability

        Args:
            observed_cm: Observed shared cM
            relationship: Hypothesized relationship
            confidence_level: Confidence level (default 95%)

        Returns:
            (lower_bound, upper_bound)
        """
        mean_cm, std_cm = self.RELATIONSHIP_PARAMS[relationship]

        # Using normal approximation for large samples
        z_score = norm.ppf((1 + confidence_level) / 2)
        margin = z_score * std_cm

        lower = max(0, mean_cm - margin)
        upper = mean_cm + margin

        return (lower, upper)

    def monte_carlo_pedigree_simulation(
        self,
        generations: int = 5,
        num_simulations: int = 1000
    ) -> Dict:
        """
        Simulate DNA transmission through pedigrees

        Models meiotic recombination and chromosome segregation
        to estimate DNA sharing in complex relationships

        Args:
            generations: Number of generations to simulate
            num_simulations: Number of pedigree simulations

        Returns:
            Sharing statistics by generation
        """
        results_by_generation = {}

        for gen in range(1, generations + 1):
            # Simplified: each generation halves expected sharing
            # Real implementation would simulate crossovers
            base_sharing = 3400  # Parent-child baseline
            expected_sharing = base_sharing / (2 ** gen)

            # Add variance (increases with generations)
            std_sharing = expected_sharing * 0.3 * gen

            # Simulate
            samples = gamma.rvs(
                a=(expected_sharing ** 2) / (std_sharing ** 2),
                scale=(std_sharing ** 2) / expected_sharing,
                size=num_simulations
            )

            results_by_generation[gen] = {
                'generation': gen,
                'mean_cm': np.mean(samples),
                'std_cm': np.std(samples),
                'median_cm': np.median(samples),
                'ci_95': (np.percentile(samples, 2.5), np.percentile(samples, 97.5))
            }

        return results_by_generation


if __name__ == "__main__":
    print("Probability Simulator - Monte Carlo Analysis")
    print("=" * 60)

    simulator = ProbabilitySimulator(random_seed=42)

    # Simulation 1: Relationship distributions
    print("\n1. SIMULATING RELATIONSHIP DISTRIBUTIONS")
    print("-" * 60)
    relationships = ['3rd_cousin', '2nd_cousin', '1st_cousin']

    for rel in relationships:
        result = simulator.simulate_relationship(rel, num_simulations=10000)
        print(f"\n{rel}:")
        print(f"  Mean: {result.mean_shared_cm:.1f} cM")
        print(f"  95% CI: [{result.confidence_intervals[95][0]:.1f}, {result.confidence_intervals[95][1]:.1f}]")

    # Simulation 2: Likelihood ratio calculation
    print("\n\n2. LIKELIHOOD RATIO ANALYSIS")
    print("-" * 60)

    observed = 75.0  # Observed shared cM
    lr_result = simulator.simulate_likelihood_ratio(
        observed_cm=observed,
        hypothesized_relationship='3rd_cousin',
        num_simulations=10000
    )

    print(f"\nObserved: {lr_result['observed_cm']} cM")
    print(f"H1: {lr_result['hypothesis_h1']}")
    print(f"H0: {lr_result['hypothesis_h0']}")
    print(f"Likelihood Ratio: {lr_result['likelihood_ratio']:.2e}")
    print(f"Log10(LR): {lr_result['log_lr']:.2f}")
    print(f"Posterior Probability: {lr_result['posterior_probability']:.4f}")
    print(f"Interpretation: {lr_result['interpretation']}")

    # Simulation 3: Database search
    print("\n\n3. DATABASE SEARCH SIMULATION")
    print("-" * 60)

    db_result = simulator.simulate_database_search(
        query_relationship='3rd_cousin',
        database_size=1000000,
        num_simulations=1000
    )

    print(f"\nDatabase Size: {db_result['database_size']:,}")
    print(f"True Positive Rate: {db_result['true_positive_rate']:.2%}")
    print(f"Mean False Positives: {db_result['mean_false_positives']:.1f}")
    print(f"Max False Positives: {db_result['max_false_positives']}")

    print("\n" + "=" * 60)
