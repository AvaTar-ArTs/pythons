#!/usr/bin/env python3
"""
DNA Matcher Module - Core kinship and IBD analysis
Implements forensic genetic genealogy matching algorithms
"""

import numpy as np
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from scipy.stats import gamma, expon
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class DNAProfile:
    """Represents a DNA profile with SNP markers"""
    sample_id: str
    snps: Dict[str, Tuple[str, str]]  # {rsid: (allele1, allele2)}
    metadata: Dict = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}

    @property
    def num_markers(self) -> int:
        return len(self.snps)


@dataclass
class DNAMatch:
    """Represents a DNA match with kinship statistics"""
    match_id: str
    profile_id: str
    shared_cm: float
    longest_segment_cm: float
    num_segments: int
    kinship_coefficient: float
    predicted_relationship: str
    confidence: float
    likelihood_ratio: float = 0.0

    def __repr__(self):
        return (f"DNAMatch(id={self.match_id}, shared_cm={self.shared_cm:.1f}, "
                f"relationship={self.predicted_relationship}, LR={self.likelihood_ratio:.2e})")


class DNAMatcher:
    """
    Core DNA matching engine for forensic genetic genealogy

    Implements:
    - Kinship coefficient calculation (Wright's coefficient)
    - IBD (Identity-by-Descent) segment detection
    - Likelihood ratio calculations
    - Relationship prediction
    """

    # Relationship thresholds (kinship coefficient θ)
    RELATIONSHIP_THRESHOLDS = {
        'identical_twins': (0.5, float('inf')),
        'parent_child': (0.25, 0.5),
        'full_sibling': (0.125, 0.25),
        '1st_cousin': (0.0625, 0.125),
        '2nd_cousin': (0.0156, 0.0625),
        '3rd_cousin': (0.0039, 0.0156),
        '4th_cousin': (0.00098, 0.0039),
        '5th_cousin': (0.00024, 0.00098),
        'unrelated': (0.0, 0.00024)
    }

    # Expected shared cM by relationship (mean, std)
    EXPECTED_SHARED_CM = {
        'parent_child': (3400, 200),
        'full_sibling': (2550, 450),
        '1st_cousin': (850, 250),
        '2nd_cousin': (212, 107),
        '3rd_cousin': (75, 50),
        '4th_cousin': (30, 25),
        '5th_cousin': (15, 15),
        'unrelated': (5, 5)
    }

    def __init__(self, min_segment_cm: float = 7.0, min_total_cm: float = 15.0):
        """
        Initialize DNA Matcher

        Args:
            min_segment_cm: Minimum segment length in cM (default 7.0)
            min_total_cm: Minimum total shared cM (default 15.0)
        """
        self.min_segment_cm = min_segment_cm
        self.min_total_cm = min_total_cm
        logger.info(f"DNAMatcher initialized: min_segment={min_segment_cm}cM, min_total={min_total_cm}cM")

    def load_profile(self, file_path: str) -> DNAProfile:
        """
        Load DNA profile from VCF or CSV file

        Args:
            file_path: Path to DNA profile file

        Returns:
            DNAProfile object
        """
        # Placeholder implementation - you'll implement VCF parsing
        logger.info(f"Loading DNA profile from {file_path}")

        # For demonstration, create synthetic profile
        sample_id = file_path.split('/')[-1].split('.')[0]
        snps = self._generate_synthetic_snps(500000)  # 500K SNPs

        return DNAProfile(sample_id=sample_id, snps=snps)

    def _generate_synthetic_snps(self, num_snps: int) -> Dict[str, Tuple[str, str]]:
        """Generate synthetic SNP data for testing"""
        snps = {}
        alleles = ['A', 'T', 'G', 'C']

        for i in range(num_snps):
            rsid = f"rs{i}"
            allele1 = np.random.choice(alleles)
            allele2 = np.random.choice(alleles)
            snps[rsid] = (allele1, allele2)

        return snps

    def calculate_kinship_coefficient(
        self,
        profile1: DNAProfile,
        profile2: DNAProfile
    ) -> float:
        """
        Calculate kinship coefficient (θ) using Wright's formula

        θ = (k₁/2) + k₂
        where k₁, k₂ = probabilities of sharing 1 or 2 alleles IBD

        Args:
            profile1: First DNA profile
            profile2: Second DNA profile

        Returns:
            Kinship coefficient θ
        """
        shared_rsids = set(profile1.snps.keys()) & set(profile2.snps.keys())

        if not shared_rsids:
            logger.warning("No shared SNPs between profiles")
            return 0.0

        ibs0 = 0  # No alleles shared
        ibs1 = 0  # One allele shared
        ibs2 = 0  # Two alleles shared

        for rsid in shared_rsids:
            alleles1 = set(profile1.snps[rsid])
            alleles2 = set(profile2.snps[rsid])
            shared = len(alleles1 & alleles2)

            if shared == 0:
                ibs0 += 1
            elif shared == 1:
                ibs1 += 1
            else:
                ibs2 += 1

        total = ibs0 + ibs1 + ibs2

        # Estimate IBD from IBS
        # This is a simplified model; real implementation uses KING or PLINK algorithms
        k1_estimate = ibs1 / total
        k2_estimate = ibs2 / total

        theta = (k1_estimate / 2.0) + k2_estimate

        logger.debug(f"Kinship: θ={theta:.6f} (IBS0={ibs0}, IBS1={ibs1}, IBS2={ibs2})")

        return theta

    def detect_ibd_segments(
        self,
        profile1: DNAProfile,
        profile2: DNAProfile
    ) -> List[Tuple[int, int, float]]:
        """
        Detect IBD (Identity-by-Descent) segments

        Returns list of segments: (start_pos, end_pos, length_cM)

        This is a simplified implementation. Production systems use:
        - GERMLINE (hash-based matching)
        - RaPID (positional Burrows-Wheeler transform)
        - IBIS (sparse representation)
        """
        # Simplified: simulate IBD detection
        # In real implementation, this would analyze chromosome positions

        segments = []
        num_segments = np.random.randint(1, 20)

        for i in range(num_segments):
            # Simulate segment properties
            length_cm = np.random.exponential(15)  # Exponential distribution

            if length_cm >= self.min_segment_cm:
                start = np.random.randint(1, 100000000)
                end = start + int(length_cm * 1000000)  # Rough conversion
                segments.append((start, end, length_cm))

        return sorted(segments, key=lambda x: x[2], reverse=True)

    def predict_relationship(self, theta: float, shared_cm: float) -> Tuple[str, float]:
        """
        Predict relationship from kinship coefficient and shared cM

        Args:
            theta: Kinship coefficient
            shared_cm: Total shared centiMorgans

        Returns:
            (relationship_name, confidence_score)
        """
        # Find relationship based on theta
        relationship = 'unrelated'
        confidence = 0.0

        for rel_name, (min_theta, max_theta) in self.RELATIONSHIP_THRESHOLDS.items():
            if min_theta <= theta < max_theta:
                relationship = rel_name

                # Calculate confidence based on how well shared_cm matches expected
                if rel_name in self.EXPECTED_SHARED_CM:
                    expected_cm, std_cm = self.EXPECTED_SHARED_CM[rel_name]
                    z_score = abs(shared_cm - expected_cm) / std_cm
                    confidence = max(0.0, 1.0 - (z_score / 3.0))  # 3-sigma rule
                else:
                    confidence = 0.5

                break

        return relationship, min(1.0, confidence)

    def calculate_likelihood_ratio(
        self,
        match: DNAMatch,
        population: str = 'EUR'
    ) -> float:
        """
        Calculate Likelihood Ratio (LR) for match

        LR = P(Data | Related) / P(Data | Unrelated)

        Args:
            match: DNA match object
            population: Population code (EUR, AFR, ASN, etc.)

        Returns:
            Likelihood ratio
        """
        shared_cm = match.shared_cm
        relationship = match.predicted_relationship

        # H1: Related (using expected distribution for relationship)
        if relationship in self.EXPECTED_SHARED_CM:
            mean_h1, std_h1 = self.EXPECTED_SHARED_CM[relationship]
            # Use gamma distribution for related
            shape_h1 = (mean_h1 ** 2) / (std_h1 ** 2)
            scale_h1 = (std_h1 ** 2) / mean_h1
            L1 = gamma.pdf(shared_cm, shape_h1, scale=scale_h1)
        else:
            L1 = 1e-10

        # H0: Unrelated (exponential distribution with mean 5 cM)
        L0 = expon.pdf(shared_cm, scale=5.0)

        # Likelihood ratio
        lr = L1 / max(L0, 1e-20)  # Avoid division by zero

        return lr

    def find_matches(
        self,
        query_profile: DNAProfile,
        database_profiles: List[DNAProfile] = None,
        min_cm: float = None,
        confidence_threshold: float = 0.0
    ) -> List[DNAMatch]:
        """
        Find DNA matches in database

        Args:
            query_profile: DNA profile to match
            database_profiles: List of profiles to search (or None for synthetic demo)
            min_cm: Minimum shared cM threshold
            confidence_threshold: Minimum confidence score

        Returns:
            List of DNAMatch objects
        """
        min_cm = min_cm or self.min_total_cm
        matches = []

        # If no database provided, generate synthetic matches for demo
        if database_profiles is None:
            logger.info("No database provided - generating synthetic matches for demonstration")
            database_profiles = [self._generate_synthetic_profile(f"DB_{i}") for i in range(50)]

        logger.info(f"Searching {len(database_profiles)} profiles...")

        for db_profile in database_profiles:
            # Calculate kinship
            theta = self.calculate_kinship_coefficient(query_profile, db_profile)

            # Detect IBD segments
            segments = self.detect_ibd_segments(query_profile, db_profile)

            if not segments:
                continue

            total_cm = sum(seg[2] for seg in segments)
            longest_cm = max(seg[2] for seg in segments) if segments else 0.0

            # Filter by minimum cM
            if total_cm < min_cm:
                continue

            # Predict relationship
            relationship, confidence = self.predict_relationship(theta, total_cm)

            # Filter by confidence
            if confidence < confidence_threshold:
                continue

            # Create match object
            match = DNAMatch(
                match_id=f"M-{query_profile.sample_id}-{db_profile.sample_id}",
                profile_id=db_profile.sample_id,
                shared_cm=total_cm,
                longest_segment_cm=longest_cm,
                num_segments=len(segments),
                kinship_coefficient=theta,
                predicted_relationship=relationship,
                confidence=confidence
            )

            # Calculate likelihood ratio
            match.likelihood_ratio = self.calculate_likelihood_ratio(match)

            matches.append(match)

        # Sort by likelihood ratio (descending)
        matches.sort(key=lambda x: x.likelihood_ratio, reverse=True)

        logger.info(f"Found {len(matches)} matches above thresholds")

        return matches

    def _generate_synthetic_profile(self, sample_id: str) -> DNAProfile:
        """Generate synthetic profile for testing"""
        snps = self._generate_synthetic_snps(500000)
        return DNAProfile(sample_id=sample_id, snps=snps)


if __name__ == "__main__":
    # Demo usage
    print("DNA Matcher - Forensic Genetic Genealogy Engine")
    print("=" * 60)

    # Initialize matcher
    matcher = DNAMatcher(min_segment_cm=7.0, min_total_cm=15.0)

    # Load crime scene profile
    crime_profile = matcher.load_profile("crime_scene_001.vcf")
    print(f"\nLoaded crime scene profile: {crime_profile.sample_id}")
    print(f"Markers: {crime_profile.num_markers:,}")

    # Find matches
    print("\nSearching database...")
    matches = matcher.find_matches(
        crime_profile,
        min_cm=20.0,
        confidence_threshold=0.70
    )

    # Display results
    print(f"\n{'='*60}")
    print(f"MATCHES FOUND: {len(matches)}")
    print(f"{'='*60}\n")

    for i, match in enumerate(matches[:10], 1):  # Top 10
        print(f"{i}. {match}")
        print(f"   Shared: {match.shared_cm:.1f} cM ({match.num_segments} segments)")
        print(f"   Longest: {match.longest_segment_cm:.1f} cM")
        print(f"   Confidence: {match.confidence*100:.1f}%")
        print()
