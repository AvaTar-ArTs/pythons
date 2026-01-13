#!/usr/bin/env python3
"""
DNA Cold Case AI - Comprehensive Demo
Demonstrates all major features of the system
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from core.dna_matcher import DNAMatcher, DNAMatch
from core.case_manager import CaseManager
from analysis.probability_simulator import ProbabilitySimulator
from models.ml_prioritizer import MLMatchPrioritizer, MatchFeatures


def print_header(title):
    """Print formatted header"""
    print("\n" + "=" * 80)
    print(f" {title}")
    print("=" * 80 + "\n")


def demo_dna_matching():
    """Demonstrate DNA matching capabilities"""
    print_header("DEMO 1: DNA MATCHING & KINSHIP ANALYSIS")

    matcher = DNAMatcher(min_segment_cm=7.0, min_total_cm=15.0)

    # Load crime scene profile
    print("Loading crime scene DNA profile...")
    crime_profile = matcher.load_profile("evidence/crime_scene_001.vcf")
    print(f"✓ Loaded profile: {crime_profile.sample_id}")
    print(f"  Markers: {crime_profile.num_markers:,}")

    # Find matches
    print("\nSearching database for matches...")
    matches = matcher.find_matches(
        crime_profile,
        min_cm=20.0,
        confidence_threshold=0.70
    )

    print(f"✓ Found {len(matches)} potential matches\n")

    # Display top matches
    print("TOP 5 MATCHES:")
    print("-" * 80)

    for i, match in enumerate(matches[:5], 1):
        print(f"\n{i}. Match ID: {match.match_id}")
        print(f"   Profile: {match.profile_id}")
        print(f"   Shared DNA: {match.shared_cm:.1f} cM ({match.num_segments} segments)")
        print(f"   Longest Segment: {match.longest_segment_cm:.1f} cM")
        print(f"   Kinship Coefficient: {match.kinship_coefficient:.6f}")
        print(f"   Predicted Relationship: {match.predicted_relationship}")
        print(f"   Confidence: {match.confidence*100:.1f}%")
        print(f"   Likelihood Ratio: {match.likelihood_ratio:.2e}")

    return matches


def demo_probability_simulation():
    """Demonstrate probability simulations"""
    print_header("DEMO 2: PROBABILITY SIMULATIONS")

    simulator = ProbabilitySimulator(random_seed=42)

    # Simulate relationship distributions
    print("RELATIONSHIP DISTRIBUTIONS:")
    print("-" * 80)

    relationships = ['3rd_cousin', '2nd_cousin', '1st_cousin']

    for rel in relationships:
        result = simulator.simulate_relationship(rel, num_simulations=10000)
        ci_95 = result.confidence_intervals[95]

        print(f"\n{rel.replace('_', ' ').title()}:")
        print(f"  Mean: {result.mean_shared_cm:.1f} cM")
        print(f"  Median: {result.median_shared_cm:.1f} cM")
        print(f"  Std Dev: {result.std_shared_cm:.1f} cM")
        print(f"  95% CI: [{ci_95[0]:.1f}, {ci_95[1]:.1f}] cM")

    # Likelihood ratio calculation
    print("\n\nLIKELIHOOD RATIO ANALYSIS:")
    print("-" * 80)

    observed_cm = 75.0
    print(f"\nObserved shared DNA: {observed_cm} cM")

    lr_result = simulator.simulate_likelihood_ratio(
        observed_cm=observed_cm,
        hypothesized_relationship='3rd_cousin',
        num_simulations=10000
    )

    print(f"\nHypothesis H1: {lr_result['hypothesis_h1']}")
    print(f"Hypothesis H0: {lr_result['hypothesis_h0']}")
    print(f"\nLikelihood Ratio: {lr_result['likelihood_ratio']:.2e}")
    print(f"Log10(LR): {lr_result['log_lr']:.2f}")
    print(f"Posterior Probability: {lr_result['posterior_probability']:.6f}")
    print(f"\nInterpretation: {lr_result['interpretation']}")

    # Database search simulation
    print("\n\nDATABASE SEARCH SIMULATION:")
    print("-" * 80)

    db_result = simulator.simulate_database_search(
        query_relationship='3rd_cousin',
        database_size=1000000,
        num_simulations=500
    )

    print(f"\nDatabase Size: {db_result['database_size']:,}")
    print(f"Query Relationship: {db_result['query_relationship']}")
    print(f"Simulations: {db_result['num_simulations']}")
    print(f"\nTrue Positive Rate: {db_result['true_positive_rate']*100:.1f}%")
    print(f"Mean False Positives: {db_result['mean_false_positives']:.1f}")
    print(f"Median False Positives: {db_result['median_false_positives']:.0f}")
    print(f"Max False Positives: {db_result['max_false_positives']}")


def demo_ml_prioritization():
    """Demonstrate ML match prioritization"""
    print_header("DEMO 3: MACHINE LEARNING PRIORITIZATION")

    prioritizer = MLMatchPrioritizer()

    print("Training ML models...")
    prioritizer.train()
    print("✓ Training complete\n")

    # Create test matches
    test_matches = [
        # Strong match
        MatchFeatures(
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
        ),
        # Moderate match
        MatchFeatures(
            shared_cm=55.0,
            longest_segment_cm=28.0,
            num_segments=8,
            kinship_coefficient=0.0028,
            likelihood_ratio=1.2e3,
            confidence=0.75,
            database_size_log=6.0,
            population_frequency=0.4,
            geographic_distance_km=75.0,
            age_match=True,
            prior_criminal_record=False
        ),
        # Weak match
        MatchFeatures(
            shared_cm=22.0,
            longest_segment_cm=15.0,
            num_segments=4,
            kinship_coefficient=0.0011,
            likelihood_ratio=85,
            confidence=0.52,
            database_size_log=6.0,
            population_frequency=0.3,
            geographic_distance_km=200.0,
            age_match=False,
            prior_criminal_record=False
        )
    ]

    # Rank matches
    ranked = prioritizer.rank_matches(test_matches)

    print("PRIORITIZED MATCHES:")
    print("-" * 80)

    for rank, (idx, score) in enumerate(ranked, 1):
        match = test_matches[idx]

        print(f"\n{rank}. Match Index: {idx}")
        print(f"   ML Priority Score: {score:.3f}")

        explanation = prioritizer.explain_prediction(match)

        print(f"   Interpretation: {explanation['interpretation']}")
        print(f"   Model Confidence: {explanation['model_confidence']:.3f}")
        print(f"\n   Match Details:")
        print(f"     Shared cM: {match.shared_cm}")
        print(f"     LR: {match.likelihood_ratio:.2e}")
        print(f"     Confidence: {match.confidence*100:.0f}%")

        print(f"\n   Top Contributing Features:")
        for feat in explanation['top_contributing_features'][:3]:
            print(f"     - {feat['feature']}: {feat['value']:.2f} "
                  f"(importance: {feat['importance']:.3f})")

    # Feature importance
    print("\n\nFEATURE IMPORTANCE:")
    print("-" * 80)

    importance_df = prioritizer.get_feature_importance()

    print("\nTop 5 Most Important Features:")
    for _, row in importance_df.head(5).iterrows():
        print(f"  {row['feature']:<25} {row['avg_importance']:.4f}")


def demo_case_management():
    """Demonstrate case management system"""
    print_header("DEMO 4: CASE MANAGEMENT SYSTEM")

    manager = CaseManager()

    # Create case
    print("Creating cold case...")
    case = manager.create_case(
        case_id="CC-DEMO-2026",
        case_number="26-HOMI-042",
        jurisdiction="Metro Police Department",
        crime_type="homicide",
        incident_date="2000-07-15",
        location="Downtown District - 456 Oak Street",
        description="Unsolved homicide. Victim found in apartment. DNA evidence recovered from scene.",
        victim_name="Jane Smith",
        priority=1
    )

    print(f"✓ Created case: {case.case_id}\n")

    # Add evidence
    print("Adding DNA evidence...")
    evidence = manager.add_evidence_to_case(
        case_id=case.case_id,
        evidence_id="EV-2026-042-001",
        evidence_type="blood",
        collection_date="2000-07-16",
        location="Crime scene - living room floor",
        description="Blood sample from perpetrator (non-victim DNA)",
        handler="Det. Johnson",
        dna_profile_path="data/evidence/case_042_sample.vcf"
    )

    print(f"✓ Added evidence: {evidence.evidence_id}\n")

    # Add chain of custody entries
    evidence.add_custody_entry("Det. Johnson", "collected", "Initial collection at scene")
    evidence.add_custody_entry("Lab Tech Martinez", "received", "Delivered to crime lab")
    evidence.add_custody_entry("Lab Tech Martinez", "processed", "DNA extraction completed")
    evidence.add_custody_entry("Det. Johnson", "received", "Results obtained from lab")

    # Add suspects
    print("Adding suspects from DNA analysis...")

    suspects_data = [
        ("SUSP-042-001", "M-042-DB12345", "3rd_cousin", 2.3e4, 0.87, "Robert Jones"),
        ("SUSP-042-002", "M-042-DB67890", "4th_cousin", 450, 0.72, "Michael Davis"),
        ("SUSP-042-003", "M-042-DB11111", "4th_cousin", 180, 0.65, None)
    ]

    for susp_id, match_id, rel, lr, conf, name in suspects_data:
        manager.add_suspect_to_case(
            case_id=case.case_id,
            suspect_id=susp_id,
            dna_match_id=match_id,
            relationship_to_match=rel,
            likelihood_ratio=lr,
            confidence=conf,
            investigator="Det. Johnson",
            name=name
        )

    print(f"✓ Added {len(suspects_data)} suspects\n")

    # Generate report
    print("Generating investigative report...")
    report = manager.generate_report(case.case_id)

    print("\n" + report)

    # List all cases
    print("\n\nALL CASES IN SYSTEM:")
    print("-" * 80)

    for case_summary in manager.list_cases():
        print(f"\n{case_summary['case_id']}:")
        print(f"  Status: {case_summary['status']}")
        print(f"  Priority: {case_summary['priority']}")
        print(f"  Evidence: {case_summary['num_evidence']} items")
        print(f"  Suspects: {case_summary['num_suspects']} identified")
        print(f"  Days Open: {case_summary['days_open']}")


def main():
    """Run all demos"""
    print("\n" + "=" * 80)
    print(" " * 20 + "DNA COLD CASE AI SYSTEM")
    print(" " * 15 + "Comprehensive Feature Demonstration")
    print("=" * 80)

    try:
        # Run demos
        matches = demo_dna_matching()
        demo_probability_simulation()
        demo_ml_prioritization()
        demo_case_management()

        # Summary
        print_header("DEMO COMPLETE")

        print("✓ All modules tested successfully")
        print("\nKey Capabilities Demonstrated:")
        print("  1. DNA matching and kinship analysis")
        print("  2. Probability simulations (Monte Carlo)")
        print("  3. Machine learning match prioritization")
        print("  4. Case management and evidence tracking")
        print("\nSystem Status: OPERATIONAL")

        print("\n" + "=" * 80)
        print("Next Steps:")
        print("  - Review USAGE_GUIDE.md for detailed instructions")
        print("  - Load your own DNA profiles")
        print("  - Create real cases")
        print("  - Integrate with existing databases")
        print("=" * 80 + "\n")

    except Exception as e:
        print(f"\n❌ Error during demo: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
