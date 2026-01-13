#!/usr/bin/env python3
"""
Case Management System
Track cold cases, evidence, suspects, and investigation progress
"""

import json
import hashlib
from datetime import datetime
from typing import List, Dict, Optional
from dataclasses import dataclass, field, asdict
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class Evidence:
    """DNA Evidence item"""
    evidence_id: str
    case_id: str
    type: str  # 'blood', 'hair', 'saliva', 'touch_dna', etc.
    collection_date: str
    location: str
    description: str
    chain_of_custody: List[Dict] = field(default_factory=list)
    dna_profile_path: Optional[str] = None
    quality_score: float = 0.0  # 0-1 scale
    metadata: Dict = field(default_factory=dict)

    def add_custody_entry(self, handler: str, action: str, notes: str = ""):
        """Add chain of custody entry"""
        entry = {
            'timestamp': datetime.now().isoformat(),
            'handler': handler,
            'action': action,
            'notes': notes,
            'hash': self._generate_hash()
        }
        self.chain_of_custody.append(entry)

    def _generate_hash(self) -> str:
        """Generate cryptographic hash for integrity verification"""
        data = f"{self.evidence_id}{self.case_id}{len(self.chain_of_custody)}"
        return hashlib.sha256(data.encode()).hexdigest()[:16]


@dataclass
class Suspect:
    """Potential suspect identified through DNA matching"""
    suspect_id: str
    case_id: str
    name: Optional[str]
    dna_match_id: str
    relationship_to_match: str
    likelihood_ratio: float
    confidence: float
    investigative_priority: int  # 1=highest
    status: str  # 'identified', 'investigating', 'cleared', 'charged'
    notes: List[Dict] = field(default_factory=list)
    alibi_info: Optional[str] = None
    created_date: str = field(default_factory=lambda: datetime.now().isoformat())

    def add_note(self, investigator: str, content: str):
        """Add investigative note"""
        note = {
            'timestamp': datetime.now().isoformat(),
            'investigator': investigator,
            'content': content
        }
        self.notes.append(note)


@dataclass
class ColdCase:
    """Cold case investigation"""
    case_id: str
    case_number: str  # Official case number
    jurisdiction: str
    crime_type: str  # 'homicide', 'sexual_assault', 'unidentified_remains'
    incident_date: str
    location: str
    victim_name: Optional[str]
    description: str
    status: str  # 'open', 'leads_identified', 'suspect_identified', 'closed'
    priority: int  # 1-5, 1=highest
    evidence_items: List[Evidence] = field(default_factory=list)
    suspects: List[Suspect] = field(default_factory=list)
    investigators: List[str] = field(default_factory=list)
    timeline: List[Dict] = field(default_factory=list)
    created_date: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_date: str = field(default_factory=lambda: datetime.now().isoformat())
    metadata: Dict = field(default_factory=dict)

    def add_evidence(self, evidence: Evidence):
        """Add evidence to case"""
        self.evidence_items.append(evidence)
        self.add_timeline_event('evidence_added', f"Evidence {evidence.evidence_id} added")
        self.updated_date = datetime.now().isoformat()

    def add_suspect(self, suspect: Suspect):
        """Add suspect to case"""
        self.suspects.append(suspect)
        self.add_timeline_event('suspect_identified', f"Suspect {suspect.suspect_id} identified")
        self.updated_date = datetime.now().isoformat()

    def add_timeline_event(self, event_type: str, description: str, investigator: str = "SYSTEM"):
        """Add event to case timeline"""
        event = {
            'timestamp': datetime.now().isoformat(),
            'type': event_type,
            'description': description,
            'investigator': investigator
        }
        self.timeline.append(event)

    def update_status(self, new_status: str, investigator: str, notes: str = ""):
        """Update case status"""
        old_status = self.status
        self.status = new_status
        self.add_timeline_event(
            'status_change',
            f"Status changed from {old_status} to {new_status}. {notes}",
            investigator
        )
        self.updated_date = datetime.now().isoformat()

    def get_summary(self) -> Dict:
        """Get case summary"""
        return {
            'case_id': self.case_id,
            'case_number': self.case_number,
            'crime_type': self.crime_type,
            'incident_date': self.incident_date,
            'status': self.status,
            'priority': self.priority,
            'num_evidence': len(self.evidence_items),
            'num_suspects': len(self.suspects),
            'num_investigators': len(self.investigators),
            'days_open': (datetime.now() - datetime.fromisoformat(self.created_date)).days
        }


class CaseManager:
    """
    Manage cold case investigations

    Features:
    - Case creation and tracking
    - Evidence management with chain of custody
    - Suspect tracking and prioritization
    - Audit trail and reporting
    - JSON-based persistence
    """

    def __init__(self, data_dir: str = None):
        """
        Initialize Case Manager

        Args:
            data_dir: Directory for case data storage
        """
        if data_dir is None:
            data_dir = Path.home() / "AVATARARTS" / "DNA_COLD_CASE_AI" / "data" / "cases"

        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)

        logger.info(f"CaseManager initialized: {self.data_dir}")

    def create_case(
        self,
        case_id: str,
        case_number: str,
        jurisdiction: str,
        crime_type: str,
        incident_date: str,
        location: str,
        description: str,
        victim_name: Optional[str] = None,
        priority: int = 3
    ) -> ColdCase:
        """
        Create new cold case

        Args:
            case_id: Unique case identifier
            case_number: Official case number
            jurisdiction: Law enforcement jurisdiction
            crime_type: Type of crime
            incident_date: Date of incident (YYYY-MM-DD)
            location: Crime location
            description: Case description
            victim_name: Victim name (if applicable)
            priority: Priority level (1-5)

        Returns:
            ColdCase object
        """
        case = ColdCase(
            case_id=case_id,
            case_number=case_number,
            jurisdiction=jurisdiction,
            crime_type=crime_type,
            incident_date=incident_date,
            location=location,
            victim_name=victim_name,
            description=description,
            status='open',
            priority=priority
        )

        case.add_timeline_event('case_created', f"Case {case_id} created")

        # Save to disk
        self.save_case(case)

        logger.info(f"Created case: {case_id} ({case_number})")

        return case

    def save_case(self, case: ColdCase):
        """Save case to disk"""
        case_file = self.data_dir / f"{case.case_id}.json"

        # Convert to dict
        case_dict = asdict(case)

        # Save with pretty formatting
        with open(case_file, 'w') as f:
            json.dump(case_dict, f, indent=2)

        logger.debug(f"Saved case to {case_file}")

    def load_case(self, case_id: str) -> ColdCase:
        """Load case from disk"""
        case_file = self.data_dir / f"{case_id}.json"

        if not case_file.exists():
            raise FileNotFoundError(f"Case not found: {case_id}")

        with open(case_file, 'r') as f:
            case_dict = json.load(f)

        # Reconstruct objects
        case = ColdCase(**case_dict)

        logger.debug(f"Loaded case: {case_id}")

        return case

    def list_cases(self, status: Optional[str] = None) -> List[Dict]:
        """
        List all cases

        Args:
            status: Filter by status (optional)

        Returns:
            List of case summaries
        """
        cases = []

        for case_file in self.data_dir.glob("*.json"):
            try:
                case = self.load_case(case_file.stem)

                if status is None or case.status == status:
                    cases.append(case.get_summary())
            except Exception as e:
                logger.error(f"Error loading {case_file}: {e}")

        # Sort by priority then date
        cases.sort(key=lambda x: (x['priority'], x['case_id']))

        return cases

    def add_evidence_to_case(
        self,
        case_id: str,
        evidence_id: str,
        evidence_type: str,
        collection_date: str,
        location: str,
        description: str,
        handler: str,
        dna_profile_path: Optional[str] = None
    ) -> Evidence:
        """Add evidence to case"""
        case = self.load_case(case_id)

        evidence = Evidence(
            evidence_id=evidence_id,
            case_id=case_id,
            type=evidence_type,
            collection_date=collection_date,
            location=location,
            description=description,
            dna_profile_path=dna_profile_path
        )

        evidence.add_custody_entry(handler, "collected", "Initial collection")

        case.add_evidence(evidence)
        self.save_case(case)

        logger.info(f"Added evidence {evidence_id} to case {case_id}")

        return evidence

    def add_suspect_to_case(
        self,
        case_id: str,
        suspect_id: str,
        dna_match_id: str,
        relationship_to_match: str,
        likelihood_ratio: float,
        confidence: float,
        investigator: str,
        name: Optional[str] = None
    ) -> Suspect:
        """Add suspect to case"""
        case = self.load_case(case_id)

        # Calculate priority based on LR and confidence
        priority = self._calculate_suspect_priority(likelihood_ratio, confidence)

        suspect = Suspect(
            suspect_id=suspect_id,
            case_id=case_id,
            name=name,
            dna_match_id=dna_match_id,
            relationship_to_match=relationship_to_match,
            likelihood_ratio=likelihood_ratio,
            confidence=confidence,
            investigative_priority=priority,
            status='identified'
        )

        suspect.add_note(investigator, f"Suspect identified via DNA match {dna_match_id}")

        case.add_suspect(suspect)
        self.save_case(case)

        logger.info(f"Added suspect {suspect_id} to case {case_id} (Priority: {priority})")

        return suspect

    def _calculate_suspect_priority(self, likelihood_ratio: float, confidence: float) -> int:
        """
        Calculate suspect investigative priority

        Returns:
            1-5 (1=highest priority)
        """
        # Combine LR and confidence
        score = (np.log10(likelihood_ratio) if likelihood_ratio > 0 else 0) * confidence

        if score >= 6.0:
            return 1  # Extremely strong
        elif score >= 4.0:
            return 2  # Very strong
        elif score >= 2.0:
            return 3  # Strong
        elif score >= 1.0:
            return 4  # Moderate
        else:
            return 5  # Weak

    def generate_report(self, case_id: str, output_path: Optional[str] = None) -> str:
        """Generate case report"""
        case = self.load_case(case_id)

        report = []
        report.append("=" * 80)
        report.append(f"COLD CASE INVESTIGATION REPORT")
        report.append("=" * 80)
        report.append(f"\nCase ID: {case.case_id}")
        report.append(f"Case Number: {case.case_number}")
        report.append(f"Jurisdiction: {case.jurisdiction}")
        report.append(f"Crime Type: {case.crime_type}")
        report.append(f"Incident Date: {case.incident_date}")
        report.append(f"Location: {case.location}")
        report.append(f"Status: {case.status}")
        report.append(f"Priority: {case.priority}")

        if case.victim_name:
            report.append(f"Victim: {case.victim_name}")

        report.append(f"\nDescription:")
        report.append(f"{case.description}")

        # Evidence
        report.append(f"\n\nEVIDENCE ({len(case.evidence_items)} items)")
        report.append("-" * 80)
        for i, ev in enumerate(case.evidence_items, 1):
            report.append(f"\n{i}. {ev.evidence_id}")
            report.append(f"   Type: {ev.type}")
            report.append(f"   Collected: {ev.collection_date} at {ev.location}")
            report.append(f"   Chain of Custody: {len(ev.chain_of_custody)} entries")

        # Suspects
        report.append(f"\n\nSUSPECTS ({len(case.suspects)} identified)")
        report.append("-" * 80)

        # Sort by priority
        sorted_suspects = sorted(case.suspects, key=lambda x: x.investigative_priority)

        for i, suspect in enumerate(sorted_suspects, 1):
            report.append(f"\n{i}. {suspect.suspect_id} (Priority {suspect.investigative_priority})")
            if suspect.name:
                report.append(f"   Name: {suspect.name}")
            report.append(f"   DNA Match: {suspect.dna_match_id}")
            report.append(f"   Relationship: {suspect.relationship_to_match}")
            report.append(f"   Likelihood Ratio: {suspect.likelihood_ratio:.2e}")
            report.append(f"   Confidence: {suspect.confidence*100:.1f}%")
            report.append(f"   Status: {suspect.status}")

        # Timeline
        report.append(f"\n\nTIMELINE ({len(case.timeline)} events)")
        report.append("-" * 80)
        for event in case.timeline[-10:]:  # Last 10 events
            report.append(f"\n{event['timestamp']}")
            report.append(f"  [{event['type']}] {event['description']}")
            report.append(f"  By: {event['investigator']}")

        report.append("\n" + "=" * 80)
        report.append(f"Report generated: {datetime.now().isoformat()}")
        report.append("=" * 80)

        report_text = "\n".join(report)

        # Save if path provided
        if output_path:
            with open(output_path, 'w') as f:
                f.write(report_text)
            logger.info(f"Report saved to {output_path}")

        return report_text


# For numpy import
import numpy as np


if __name__ == "__main__":
    print("Case Manager - Cold Case Investigation System")
    print("=" * 60)

    # Initialize
    manager = CaseManager()

    # Create case
    case = manager.create_case(
        case_id="CC-1998-0042",
        case_number="98-HOMI-042",
        jurisdiction="Metro PD",
        crime_type="homicide",
        incident_date="1998-07-15",
        location="123 Main St, Downtown",
        description="Unsolved homicide. Victim found in apartment. DNA recovered from crime scene.",
        victim_name="Jane Doe",
        priority=1
    )

    print(f"\nCreated case: {case.case_id}")

    # Add evidence
    evidence = manager.add_evidence_to_case(
        case_id=case.case_id,
        evidence_id="EV-1998-042-001",
        evidence_type="blood",
        collection_date="1998-07-16",
        location="Crime scene - living room",
        description="Blood sample from suspect DNA",
        handler="Det. Smith",
        dna_profile_path="data/evidence/sample_042_001.vcf"
    )

    print(f"Added evidence: {evidence.evidence_id}")

    # Add suspect
    suspect = manager.add_suspect_to_case(
        case_id=case.case_id,
        suspect_id="SUSP-042-001",
        dna_match_id="M-042-DB12345",
        relationship_to_match="3rd_cousin",
        likelihood_ratio=2.3e4,
        confidence=0.87,
        investigator="Det. Johnson",
        name="John Smith"
    )

    print(f"Added suspect: {suspect.suspect_id} (Priority: {suspect.investigative_priority})")

    # Generate report
    print("\n" + "=" * 60)
    print("CASE REPORT")
    print("=" * 60)

    report = manager.generate_report(case.case_id)
    print(report)

    # List all cases
    print("\n\nALL CASES:")
    for case_summary in manager.list_cases():
        print(f"  {case_summary['case_id']}: {case_summary['crime_type']} - {case_summary['status']}")
