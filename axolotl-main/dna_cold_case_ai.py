#!/usr/bin/env python3
"""
DNA Cold Case AI - Main Application
Integrated system for forensic genetic genealogy investigations
"""

import sys
from pathlib import Path
from typing import List, Optional
import logging
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from core.dna_matcher import DNAMatcher, DNAProfile, DNAMatch
from core.case_manager import CaseManager, ColdCase
from analysis.probability_simulator import ProbabilitySimulator
from models.ml_prioritizer import MLMatchPrioritizer, MatchFeatures

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DNAColdCaseAI:
    """
    Main application class for DNA Cold Case AI system

    Integrates all components:
    - DNA matching and kinship analysis
    - Case management
    - Probability simulations
    - ML-based match prioritization
    - Reporting and visualization
    """

    def __init__(self, data_dir: Optional[str] = None):
        """
        Initialize DNA Cold Case AI system

        Args:
            data_dir: Base data directory
        """
        self.dna_matcher = DNAMatcher()
        self.case_manager = CaseManager(data_dir)
        self.simulator = ProbabilitySimulator(random_seed=42)
        self.ml_prioritizer = MLMatchPrioritizer()

        # Train ML model on startup
        logger.info("Training ML prioritization model...")
        self.ml_prioritizer.train()

        logger.info("DNA Cold Case AI initialized successfully")

    def analyze_cold_case(
        self,
        case_id: str,
        evidence_dna_profile_path: str,
        database_profiles: Optional[List[DNAProfile]] = None,
        min_cm: float = 20.0,
        confidence_threshold: float = 0.70
    ) -> dict:
        """
        Complete analysis of a cold case

        Args:
            case_id: Case identifier
            evidence_dna_profile_path: Path to crime scene DNA profile
            database_profiles: List of database profiles (or None for demo)
            min_cm: Minimum shared cM threshold
            confidence_threshold: Minimum confidence score

        Returns:
            Analysis results dictionary
        """
        logger.info(f"Analyzing cold case: {case_id}")
        logger.info("=" * 60)

        # Load case
        try:
            case = self.case_manager.load_case(case_id)
            logger.info(f"Loaded case: {case.case_number}")
        except FileNotFoundError:
            logger.error(f"Case {case_id} not found")
            return {'error': f'Case {case_id} not found'}

        # Load DNA profile
        logger.info(f"Loading DNA profile: {evidence_dna_profile_path}")
        crime_profile = self.dna_matcher.load_profile(evidence_dna_profile_path)

        # Find DNA matches
        logger.info(f"Searching for DNA matches (min_cm={min_cm})...")
        matches = self.dna_matcher.find_matches(
            crime_profile,
            database_profiles=database_profiles,
            min_cm=min_cm,
            confidence_threshold=confidence_threshold
        )

        logger.info(f"Found {len(matches)} potential matches")

        # Run probability simulations for top matches
        logger.info("Running probability simulations...")
        simulation_results = []

        for match in matches[:10]:  # Top 10
            sim_result = self.simulator.simulate_likelihood_ratio(
                observed_cm=match.shared_cm,
                hypothesized_relationship=match.predicted_relationship,
                num_simulations=1000
            )
            simulation_results.append(sim_result)

        # ML prioritization
        logger.info("Applying ML prioritization...")
        prioritized_matches = self._prioritize_matches(matches)

        # Add top suspects to case
        logger.info("Adding suspects to case...")
        for i, (match_idx, priority_score) in enumerate(prioritized_matches[:5]):
            match = matches[match_idx]

            suspect_id = f"SUSP-{case_id}-{i+1:03d}"

            try:
                self.case_manager.add_suspect_to_case(
                    case_id=case_id,
                    suspect_id=suspect_id,
                    dna_match_id=match.match_id,
                    relationship_to_match=match.predicted_relationship,
                    likelihood_ratio=match.likelihood_ratio,
                    confidence=match.confidence,
                    investigator="AI_SYSTEM"
                )
                logger.info(f"Added suspect: {suspect_id} (ML Score: {priority_score:.3f})")
            except Exception as e:
                logger.error(f"Error adding suspect: {e}")

        # Update case status
        case.update_status('leads_identified', 'AI_SYSTEM',
                          f"AI analysis identified {len(prioritized_matches)} potential leads")

        # Prepare results
        results = {
            'case_id': case_id,
            'analysis_date': datetime.now().isoformat(),
            'total_matches': len(matches),
            'top_matches': [
                {
                    'rank': i+1,
                    'match_id': matches[idx].match_id,
                    'profile_id': matches[idx].profile_id,
                    'shared_cm': matches[idx].shared_cm,
                    'relationship': matches[idx].predicted_relationship,
                    'likelihood_ratio': matches[idx].likelihood_ratio,
                    'confidence': matches[idx].confidence,
                    'ml_priority_score': score
                }
                for i, (idx, score) in enumerate(prioritized_matches[:10])
            ],
            'simulation_results': simulation_results[:5],
            'case_summary': case.get_summary()
        }

        logger.info("Analysis complete")
        return results

    def _prioritize_matches(self, matches: List[DNAMatch]) -> List[tuple]:
        """
        Prioritize matches using ML model

        Args:
            matches: List of DNA matches

        Returns:
            List of (match_index, priority_score) tuples
        """
        features_list = []

        for match in matches:
            features = MatchFeatures(
                shared_cm=match.shared_cm,
                longest_segment_cm=match.longest_segment_cm,
                num_segments=match.num_segments,
                kinship_coefficient=match.kinship_coefficient,
                likelihood_ratio=match.likelihood_ratio,
                confidence=match.confidence,
                database_size_log=6.0,  # Assume 1M database
                population_frequency=0.5,  # Average
                geographic_distance_km=100.0,  # Placeholder
                age_match=True,
                prior_criminal_record=False
            )
            features_list.append(features)

        return self.ml_prioritizer.rank_matches(features_list)

    def generate_investigative_report(self, case_id: str, output_path: Optional[str] = None) -> str:
        """
        Generate comprehensive investigative report

        Args:
            case_id: Case identifier
            output_path: Output file path

        Returns:
            Report text
        """
        report = self.case_manager.generate_report(case_id, output_path)
        return report

    def simulate_match_probability(
        self,
        observed_cm: float,
        hypothesized_relationship: str
    ) -> dict:
        """
        Run probability simulation for a DNA match

        Args:
            observed_cm: Observed shared centiMorgans
            hypothesized_relationship: Proposed relationship

        Returns:
            Simulation results
        """
        return self.simulator.simulate_likelihood_ratio(
            observed_cm=observed_cm,
            hypothesized_relationship=hypothesized_relationship,
            num_simulations=10000
        )


def main():
    """Main entry point"""
    print("=" * 80)
    print(" " * 20 + "DNA COLD CASE AI SYSTEM")
    print(" " * 15 + "Forensic Genetic Genealogy Platform")
    print("=" * 80)
    print()

    # Initialize system
    print("Initializing AI system...")
    ai_system = DNAColdCaseAI()
    print("✓ System initialized\n")

    # Create demo case
    print("Creating demonstration case...")
    case = ai_system.case_manager.create_case(
        case_id="CC-DEMO-001",
        case_number="DEMO-2024-001",
        jurisdiction="Metro Police Department",
        crime_type="homicide",
        incident_date="2000-03-15",
        location="Downtown District",
        description="Cold case homicide. Degraded DNA sample recovered from crime scene.",
        victim_name="Demo Victim",
        priority=1
    )
    print(f"✓ Created case: {case.case_id}\n")

    # Add evidence
    print("Adding DNA evidence...")
    evidence = ai_system.case_manager.add_evidence_to_case(
        case_id=case.case_id,
        evidence_id="EV-DEMO-001",
        evidence_type="blood",
        collection_date="2000-03-16",
        location="Crime scene - living room",
        description="Blood sample from perpetrator",
        handler="Det. Smith",
        dna_profile_path="data/evidence/demo_sample.vcf"
    )
    print(f"✓ Added evidence: {evidence.evidence_id}\n")

    # Run analysis
    print("=" * 80)
    print("RUNNING DNA ANALYSIS")
    print("=" * 80)
    print()

    results = ai_system.analyze_cold_case(
        case_id=case.case_id,
        evidence_dna_profile_path="data/evidence/demo_sample.vcf",
        min_cm=20.0,
        confidence_threshold=0.70
    )

    # Display results
    print("\n" + "=" * 80)
    print("ANALYSIS RESULTS")
    print("=" * 80)
    print(f"\nCase: {results['case_id']}")
    print(f"Total Matches Found: {results['total_matches']}")
    print(f"\nTop {len(results['top_matches'])} Prioritized Matches:")
    print("-" * 80)

    for match in results['top_matches'][:5]:
        print(f"\n{match['rank']}. Match ID: {match['match_id']}")
        print(f"   Profile: {match['profile_id']}")
        print(f"   Shared DNA: {match['shared_cm']:.1f} cM")
        print(f"   Relationship: {match['relationship']}")
        print(f"   Likelihood Ratio: {match['likelihood_ratio']:.2e}")
        print(f"   Confidence: {match['confidence']*100:.1f}%")
        print(f"   ML Priority Score: {match['ml_priority_score']:.3f}")

    # Probability simulation example
    print("\n" + "=" * 80)
    print("PROBABILITY SIMULATION")
    print("=" * 80)

    sim_result = ai_system.simulate_match_probability(
        observed_cm=75.0,
        hypothesized_relationship='3rd_cousin'
    )

    print(f"\nObserved: {sim_result['observed_cm']} cM")
    print(f"Hypothesis: {sim_result['hypothesis_h1']}")
    print(f"Likelihood Ratio: {sim_result['likelihood_ratio']:.2e}")
    print(f"Log10(LR): {sim_result['log_lr']:.2f}")
    print(f"Posterior Probability: {sim_result['posterior_probability']:.4f}")
    print(f"Interpretation: {sim_result['interpretation']}")

    # Generate report
    print("\n" + "=" * 80)
    print("GENERATING INVESTIGATIVE REPORT")
    print("=" * 80)
    print()

    report_path = f"reports/case_{case.case_id}_report.txt"
    report = ai_system.generate_investigative_report(case.case_id, report_path)

    print(report[:1000] + "\n... (truncated)\n")
    print(f"✓ Full report saved to: {report_path}")

    print("\n" + "=" * 80)
    print("ANALYSIS COMPLETE")
    print("=" * 80)
    print("\nNext Steps:")
    print("  1. Review prioritized suspect list")
    print("  2. Conduct genealogical research on top matches")
    print("  3. Investigate suspects based on ML priority scores")
    print("  4. Document all findings in case file")
    print()


if __name__ == "__main__":
    main()
