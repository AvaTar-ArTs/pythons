"""
Devops

This module provides functionality for devops.

Author: Auto-generated
Date: 2025-11-01
"""

import logging

logger = logging.getLogger(__name__)

#!/usr/bin/env python3
"""
Context-Efficient DevOps Engineer Agent
Specialized expert for deployment, CI/CD, and infrastructure analysis.
"""

import sys
from pathlib import Path
from typing import Dict, List
import re
import yaml
import json


class DevOpsEngineerAgent:
    """
    Lightweight agent specialized in DevOps and infrastructure.
    Focuses on: CI/CD, containers, deployment, monitoring, security.
    """

    def __init__(self):
        """__init__ function."""

        self.config_patterns = {
            "docker": [".dockerfile", "dockerfile", "docker-compose"],
            "kubernetes": ["deployment.yaml", "service.yaml", "k8s", "kube"],
            "ci_cd": [".github/workflows", ".gitlab-ci", "jenkinsfile", ".travis"],
            "terraform": [".tf", "terraform"],
            "ansible": ["playbook", "ansible"],
        }

    def analyze_project(self, project_path: Path) -> Dict:
        """Analyze project for DevOps best practices."""
        if not project_path.is_dir():
            project_path = project_path.parent

        analysis = {
            "infrastructure": self._detect_infrastructure(project_path),
            "ci_cd": self._analyze_ci_cd(project_path),
            "containerization": self._analyze_containers(project_path),
            "configuration": self._analyze_configuration(project_path),
            "security": self._check_security(project_path),
            "recommendations": [],
        }

        analysis["recommendations"] = self._generate_recommendations(analysis)

        return analysis

    def _detect_infrastructure(self, project_path: Path) -> Dict:
        """Detect infrastructure-as-code files."""
        infra = {
            "docker": [],
            "kubernetes": [],
            "terraform": [],
            "ansible": [],
            "other": [],
        }

        for pattern_type, patterns in self.config_patterns.items():
            for file_path in project_path.rglob("*"):
                if file_path.is_file():
                    filename = file_path.name.lower()
                    if any(p in filename for p in patterns):
                        if pattern_type in infra:
                            infra[pattern_type].append(
                                str(file_path.relative_to(project_path))
                            )

        return infra

    def _analyze_ci_cd(self, project_path: Path) -> Dict:
        """Analyze CI/CD configuration."""
        ci_cd = {"present": False, "platform": None, "workflows": [], "checks": []}

        # GitHub Actions
        github_workflows = project_path / ".github" / "workflows"
        if github_workflows.exists():
            ci_cd["present"] = True
            ci_cd["platform"] = "GitHub Actions"
            ci_cd["workflows"] = [
                f.name for f in github_workflows.glob("*.yml") if f.is_file()
            ]

            # Analyze workflow content
            for workflow_file in github_workflows.glob("*.yml"):
                try:
                    content = workflow_file.read_text()
                    if "test" in content.lower():
                        ci_cd["checks"].append("testing")
                    if "lint" in content.lower():
                        ci_cd["checks"].append("linting")
                    if "security" in content.lower() or "bandit" in content.lower():
                        ci_cd["checks"].append("security")
                    if "deploy" in content.lower():
                        ci_cd["checks"].append("deployment")
                except (IndexError, KeyError):
                    pass

        # GitLab CI
        gitlab_ci = project_path / ".gitlab-ci.yml"
        if gitlab_ci.exists():
            ci_cd["present"] = True
            ci_cd["platform"] = "GitLab CI"

        # Travis CI
        travis_ci = project_path / ".travis.yml"
        if travis_ci.exists():
            ci_cd["present"] = True
            ci_cd["platform"] = "Travis CI"

        ci_cd["checks"] = list(set(ci_cd["checks"]))
        return ci_cd

    def _analyze_containers(self, project_path: Path) -> Dict:
        """Analyze containerization setup."""
        containers = {
            "dockerfile_present": False,
            "docker_compose_present": False,
            "issues": [],
            "best_practices": [],
        }

        # Check for Dockerfile
        dockerfiles = list(project_path.glob("**/Dockerfile*"))
        if dockerfiles:
            containers["dockerfile_present"] = True

            for dockerfile in dockerfiles[:5]:  # Analyze first 5
                try:
                    content = dockerfile.read_text()
                    issues, practices = self._analyze_dockerfile(content)
                    containers["issues"].extend(issues)
                    containers["best_practices"].extend(practices)
                except (OSError, IOError, FileNotFoundError):
                    pass

        # Check for docker-compose
        compose_files = list(project_path.glob("**/docker-compose*.yml"))
        if compose_files:
            containers["docker_compose_present"] = True

        return containers

    def _analyze_dockerfile(self, content: str) -> tuple:
        """Analyze Dockerfile for best practices."""
        issues = []
        practices = []

        lines = content.split("\n")

        # Check for base image
        if not any(line.strip().startswith("FROM") for line in lines):
            issues.append(
                {"severity": "critical", "message": "No FROM instruction found"}
            )

        # Check for latest tag
        if "FROM" in content and ":latest" in content:
            issues.append(
                {
                    "severity": "warning",
                    "message": "Using :latest tag - pin to specific versions",
                }
            )

        # Check for COPY instead of ADD
        if "ADD " in content and "http" not in content.lower():
            issues.append(
                {
                    "severity": "suggestion",
                    "message": "Prefer COPY over ADD for local files",
                }
            )

        # Check for multi-stage builds
        if content.count("FROM") > 1:
            practices.append("Using multi-stage builds ✅")

        # Check for non-root user
        if "USER" in content and "USER root" not in content:
            practices.append("Running as non-root user ✅")
        else:
            issues.append(
                {
                    "severity": "warning",
                    "message": "No USER instruction - container runs as root",
                }
            )

        # Check for HEALTHCHECK
        if "HEALTHCHECK" in content:
            practices.append("Health checks configured ✅")
        else:
            issues.append({"severity": "info", "message": "No HEALTHCHECK instruction"})

        # Check for .dockerignore
        if ".dockerignore" in content or True:  # We can't check this from content alone
            practices.append("Consider using .dockerignore file")

        return issues, practices

    def _analyze_configuration(self, project_path: Path) -> Dict:
        """Analyze configuration management."""
        config = {"env_files": [], "config_files": [], "secrets_management": False}

        # Check for .env files (should be gitignored)
        env_files = list(project_path.glob("**/.env*"))
        config["env_files"] = [
            str(f.relative_to(project_path)) for f in env_files if f.is_file()
        ]

        # Check for config files
        config_patterns = [
            "config.yaml",
            "config.json",
            "settings.yaml",
            "settings.json",
        ]
        for pattern in config_patterns:
            files = list(project_path.glob(f"**/{pattern}"))
            config["config_files"].extend(
                [str(f.relative_to(project_path)) for f in files if f.is_file()]
            )

        # Check for secrets management
        if any(
            p.name in ["vault", "secrets", ".secrets"] for p in project_path.rglob("*")
        ):
            config["secrets_management"] = True

        return config

    def _check_security(self, project_path: Path) -> Dict:
        """Check security configurations."""
        security = {
            "gitignore_present": False,
            "secrets_exposed": [],
            "dependency_security": False,
            "issues": [],
        }

        # Check .gitignore
        gitignore = project_path / ".gitignore"
        if gitignore.exists():
            security["gitignore_present"] = True

            try:
                content = gitignore.read_text()
                required_patterns = [".env", "secret", "credential", "token", "*.key"]

                missing = [p for p in required_patterns if p not in content.lower()]
                if missing:
                    security["issues"].append(
                        {
                            "severity": "warning",
                            "message": f'Gitignore missing patterns: {", ".join(missing)}',
                        }
                    )
            except (IndexError, KeyError):
                pass
        else:
            security["issues"].append(
                {"severity": "critical", "message": "No .gitignore file found"}
            )

        # Check for dependency security tools
        if (project_path / "Pipfile").exists() or (
            project_path / "requirements.txt"
        ).exists():
            # Check for safety, bandit, etc.
            for file in [".github/workflows/*.yml", ".gitlab-ci.yml"]:
                workflow_files = list(project_path.glob(file))
                for wf in workflow_files:
                    try:
                        content = wf.read_text()
                        if any(
                            tool in content for tool in ["safety", "bandit", "snyk"]
                        ):
                            security["dependency_security"] = True
                            break
                    except (OSError, IOError, FileNotFoundError):
                        pass

        return security

    def _generate_recommendations(self, analysis: Dict) -> List[Dict]:
        """Generate DevOps recommendations."""
        recommendations = []

        # CI/CD recommendations
        if not analysis["ci_cd"]["present"]:
            recommendations.append(
                {
                    "priority": "high",
                    "category": "ci_cd",
                    "title": "Set Up CI/CD Pipeline",
                    "description": "No CI/CD configuration found",
                    "suggestion": "Add GitHub Actions, GitLab CI, or Travis CI for automated testing and deployment",
                }
            )
        else:
            checks = analysis["ci_cd"]["checks"]
            if "testing" not in checks:
                recommendations.append(
                    {
                        "priority": "high",
                        "category": "ci_cd",
                        "title": "Add Automated Testing",
                        "description": "CI/CD present but no automated tests",
                        "suggestion": "Add test automation to your CI/CD pipeline",
                    }
                )

        # Container recommendations
        containers = analysis["containerization"]
        if not containers["dockerfile_present"]:
            recommendations.append(
                {
                    "priority": "medium",
                    "category": "containerization",
                    "title": "Containerize Application",
                    "description": "No Dockerfile found",
                    "suggestion": "Add Dockerfile for consistent deployment environments",
                }
            )

        if containers["issues"]:
            for issue in containers["issues"][:3]:  # Top 3 issues
                recommendations.append(
                    {
                        "priority": issue["severity"],
                        "category": "docker",
                        "title": "Docker Best Practice",
                        "description": issue["message"],
                        "suggestion": "Review Docker best practices documentation",
                    }
                )

        # Security recommendations
        security = analysis["security"]
        for issue in security["issues"]:
            recommendations.append(
                {
                    "priority": issue["severity"],
                    "category": "security",
                    "title": "Security Issue",
                    "description": issue["message"],
                    "suggestion": "Address security configuration gaps",
                }
            )

        if not security["dependency_security"]:
            recommendations.append(
                {
                    "priority": "medium",
                    "category": "security",
                    "title": "Add Dependency Security Scanning",
                    "description": "No security scanning for dependencies detected",
                    "suggestion": "Add tools like Safety, Bandit, or Snyk to your CI/CD",
                }
            )

        return recommendations

    def format_analysis(self, analysis: Dict) -> str:
        """Format analysis as readable report."""
        output = []

        output.append(Path("\n") + "=" * 80)
        output.append("⚙️  DEVOPS ANALYSIS")
        output.append("=" * 80 + Path("\n"))

        # Infrastructure
        infra = analysis["infrastructure"]
        output.append("🏗️  INFRASTRUCTURE")
        has_infra = False
        for infra_type, files in infra.items():
            if files:
                has_infra = True
                output.append(f"  • {infra_type.title()}: {len(files)} file(s)")
        if not has_infra:
            output.append("  ⚠️  No infrastructure-as-code detected")
        output.append("")

        # CI/CD
        ci_cd = analysis["ci_cd"]
        output.append("🔄 CI/CD")
        if ci_cd["present"]:
            output.append(f"  • Platform: {ci_cd['platform']} ✅")
            if ci_cd["workflows"]:
                output.append(f"  • Workflows: {', '.join(ci_cd['workflows'])}")
            if ci_cd["checks"]:
                output.append(f"  • Automated Checks: {', '.join(ci_cd['checks'])}")
        else:
            output.append("  ❌ No CI/CD configuration found")
        output.append("")

        # Containerization
        containers = analysis["containerization"]
        output.append("🐳 CONTAINERIZATION")
        if containers["dockerfile_present"]:
            output.append("  • Dockerfile: Present ✅")
        else:
            output.append("  • Dockerfile: Not found ❌")

        if containers["docker_compose_present"]:
            output.append("  • Docker Compose: Present ✅")

        if containers["best_practices"]:
            output.append("  Best Practices:")
            for practice in containers["best_practices"][:5]:
                output.append(f"    - {practice}")
        output.append("")

        # Security
        security = analysis["security"]
        output.append("🔒 SECURITY")
        output.append(
            f"  • .gitignore: {'Present ✅' if security['gitignore_present'] else 'Missing ❌'}"
        )
        output.append(
            f"  • Dependency Security: {'Configured ✅' if security['dependency_security'] else 'Not configured ⚠️'}"
        )
        output.append("")

        # Recommendations
        recommendations = analysis["recommendations"]
        if recommendations:
            output.append("💡 RECOMMENDATIONS\n")
            priority_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
            sorted_recs = sorted(
                recommendations, key=lambda x: priority_order.get(x["priority"], 4)
            )

            for i, rec in enumerate(sorted_recs, 1):
                emoji = {
                    "critical": "🔴",
                    "high": "🔴",
                    "medium": "🟡",
                    "low": "🔵",
                }.get(rec["priority"], "⚪")
                output.append(
                    f"{i}. {emoji} {rec['title']} [{rec['priority'].upper()}]"
                )
                output.append(f"   Category: {rec['category']}")
                output.append(f"   {rec['description']}")
                output.append(f"   → {rec['suggestion']}")
                output.append("")

        return "\n".join(output)


def main():
    """Main entry point for DevOps engineer agent."""
    if len(sys.argv) < 2:
        logger.info("Usage: python devops_engineer.py <project_directory>")
        logger.info("\nContext-Efficient DevOps Engineer Agent")
        logger.info("Analyzes DevOps setup for:")
        logger.info("  • CI/CD configuration")
        logger.info("  • Containerization")
        logger.info("  • Infrastructure-as-code")
        logger.info("  • Security best practices")
        sys.exit(1)

    project_path = Path(sys.argv[1])
    if not project_path.exists():
        logger.info(f"❌ Path not found: {project_path}")
        sys.exit(1)

    agent = DevOpsEngineerAgent()
    analysis = agent.analyze_project(project_path)

    logger.info(agent.format_analysis(analysis))


if __name__ == "__main__":
    main()
