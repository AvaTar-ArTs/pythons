#!/usr/bin/env python3
"""
Intelligent Project Analyzer - Advanced AI-powered code analysis and organization
Integrates with the Code Intelligence Engine for comprehensive project understanding.
"""

import os
import sys
import json
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

# Import our advanced intelligence engine
try:
    from code_intelligence_engine import CodeIntelligenceEngine, ASTAnalyzer, SemanticAnalyzer, IntelligentCategorizer
except ImportError:
    print("Warning: code_intelligence_engine not found. Install required dependencies.")
    CodeIntelligenceEngine = None

class IntelligentProjectAnalyzer:
    """Advanced project analysis with AI-powered insights and visualizations"""

    def __init__(self):
        self.engine = CodeIntelligenceEngine() if CodeIntelligenceEngine else None
        self.project_insights = {}
        self.visualization_data = {}

    def analyze_project_comprehensive(self, project_path: str) -> Dict[str, Any]:
        """Perform comprehensive project analysis with advanced intelligence"""
        print("🧠 Starting Comprehensive Project Analysis...")
        print("=" * 60)

        if not self.engine:
            return self._fallback_analysis(project_path)

        # Core analysis
        analysis_results = self.engine.analyze_project(project_path)

        # Enhanced insights
        enhanced_insights = self._generate_enhanced_insights(analysis_results)

        # Architectural analysis
        architectural_analysis = self._analyze_architecture(analysis_results)

        # Performance recommendations
        performance_recommendations = self._analyze_performance_patterns(analysis_results)

        # Security analysis
        security_analysis = self._analyze_security_patterns(analysis_results)

        # Business intelligence
        business_intelligence = self._analyze_business_patterns(analysis_results)

        # Combine all analyses
        comprehensive_analysis = {
            'project_path': project_path,
            'timestamp': datetime.now().isoformat(),
            'core_analysis': analysis_results,
            'enhanced_insights': enhanced_insights,
            'architectural_analysis': architectural_analysis,
            'performance_recommendations': performance_recommendations,
            'security_analysis': security_analysis,
            'business_intelligence': business_intelligence,
            'overall_score': self._calculate_overall_score(analysis_results, enhanced_insights)
        }

        return comprehensive_analysis

    def _generate_enhanced_insights(self, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate enhanced insights using advanced AI techniques"""
        insights = {
            'code_quality_metrics': {},
            'maintainability_score': 0.0,
            'scalability_assessment': {},
            'technical_debt_analysis': {},
            'innovation_indicators': {},
            'learning_recommendations': []
        }

        files_analyzed = analysis_results.get('files_analyzed', [])
        overall_intelligence = analysis_results.get('overall_intelligence', {})

        # Code quality metrics
        insights['code_quality_metrics'] = {
            'average_complexity': overall_intelligence.get('average_complexity', 0),
            'average_confidence': overall_intelligence.get('average_confidence', 0),
            'file_count': len(files_analyzed),
            'category_diversity': len(set(f.get('category', 'unknown') for f in files_analyzed)),
            'intelligence_distribution': overall_intelligence.get('intelligence_distribution', {})
        }

        # Maintainability score
        maintainability_factors = []
        for file_info in files_analyzed:
            confidence = file_info.get('confidence', 0)
            category = file_info.get('category', 'unknown')

            # High confidence and good categorization = maintainable
            if confidence > 0.7 and category != 'unknown':
                maintainability_factors.append(0.9)
            elif confidence > 0.5:
                maintainability_factors.append(0.7)
            else:
                maintainability_factors.append(0.4)

        insights['maintainability_score'] = sum(maintainability_factors) / len(maintainability_factors) if maintainability_factors else 0.0

        # Scalability assessment
        insights['scalability_assessment'] = {
            'modularity_score': self._assess_modularity(files_analyzed),
            'separation_of_concerns': self._assess_separation_of_concerns(files_analyzed),
            'dependency_management': self._assess_dependency_management(files_analyzed),
            'scalability_recommendations': self._generate_scalability_recommendations(files_analyzed)
        }

        # Technical debt analysis
        insights['technical_debt_analysis'] = {
            'complexity_debt': self._assess_complexity_debt(files_analyzed),
            'documentation_debt': self._assess_documentation_debt(files_analyzed),
            'test_coverage_debt': self._assess_test_coverage_debt(files_analyzed),
            'refactoring_priorities': self._identify_refactoring_priorities(files_analyzed)
        }

        # Innovation indicators
        insights['innovation_indicators'] = {
            'ai_integration_level': self._assess_ai_integration(files_analyzed),
            'modern_patterns_usage': self._assess_modern_patterns(files_analyzed),
            'automation_level': self._assess_automation_level(files_analyzed),
            'innovation_score': 0.0
        }

        # Calculate innovation score
        innovation_factors = [
            insights['innovation_indicators']['ai_integration_level'],
            insights['innovation_indicators']['modern_patterns_usage'],
            insights['innovation_indicators']['automation_level']
        ]
        insights['innovation_indicators']['innovation_score'] = sum(innovation_factors) / len(innovation_factors)

        # Learning recommendations
        insights['learning_recommendations'] = self._generate_learning_recommendations(insights)

        return insights

    def _analyze_architecture(self, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze architectural patterns and design quality"""
        architectural_patterns = analysis_results.get('architectural_patterns', [])
        files_analyzed = analysis_results.get('files_analyzed', [])

        architecture_analysis = {
            'detected_patterns': architectural_patterns,
            'architecture_quality': {},
            'design_principles': {},
            'architectural_recommendations': []
        }

        # Architecture quality assessment
        architecture_analysis['architecture_quality'] = {
            'separation_of_concerns': self._assess_separation_of_concerns(files_analyzed),
            'modularity': self._assess_modularity(files_analyzed),
            'cohesion': self._assess_cohesion(files_analyzed),
            'coupling': self._assess_coupling(files_analyzed)
        }

        # Design principles adherence
        architecture_analysis['design_principles'] = {
            'single_responsibility': self._assess_single_responsibility(files_analyzed),
            'open_closed': self._assess_open_closed_principle(files_analyzed),
            'dependency_inversion': self._assess_dependency_inversion(files_analyzed),
            'interface_segregation': self._assess_interface_segregation(files_analyzed)
        }

        # Generate architectural recommendations
        architecture_analysis['architectural_recommendations'] = self._generate_architectural_recommendations(
            architecture_analysis['architecture_quality'],
            architecture_analysis['design_principles']
        )

        return architecture_analysis

    def _analyze_performance_patterns(self, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze performance-related patterns and bottlenecks"""
        files_analyzed = analysis_results.get('files_analyzed', [])

        performance_analysis = {
            'performance_indicators': {},
            'bottleneck_analysis': {},
            'optimization_opportunities': [],
            'performance_recommendations': []
        }

        # Performance indicators
        performance_analysis['performance_indicators'] = {
            'complexity_distribution': self._analyze_complexity_distribution(files_analyzed),
            'function_size_distribution': self._analyze_function_size_distribution(files_analyzed),
            'import_analysis': self._analyze_import_patterns(files_analyzed),
            'resource_intensive_patterns': self._identify_resource_intensive_patterns(files_analyzed)
        }

        # Bottleneck analysis
        performance_analysis['bottleneck_analysis'] = {
            'high_complexity_files': self._identify_high_complexity_files(files_analyzed),
            'potential_bottlenecks': self._identify_potential_bottlenecks(files_analyzed),
            'optimization_candidates': self._identify_optimization_candidates(files_analyzed)
        }

        # Optimization opportunities
        performance_analysis['optimization_opportunities'] = self._identify_optimization_opportunities(files_analyzed)

        # Performance recommendations
        performance_analysis['performance_recommendations'] = self._generate_performance_recommendations(
            performance_analysis['performance_indicators'],
            performance_analysis['bottleneck_analysis']
        )

        return performance_analysis

    def _analyze_security_patterns(self, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze security patterns and vulnerabilities"""
        files_analyzed = analysis_results.get('files_analyzed', [])

        security_analysis = {
            'security_indicators': {},
            'vulnerability_assessment': {},
            'security_recommendations': []
        }

        # Security indicators
        security_analysis['security_indicators'] = {
            'api_security': self._assess_api_security(files_analyzed),
            'data_handling': self._assess_data_handling_security(files_analyzed),
            'authentication_patterns': self._assess_authentication_patterns(files_analyzed),
            'input_validation': self._assess_input_validation(files_analyzed)
        }

        # Vulnerability assessment
        security_analysis['vulnerability_assessment'] = {
            'potential_vulnerabilities': self._identify_potential_vulnerabilities(files_analyzed),
            'security_risks': self._assess_security_risks(files_analyzed),
            'compliance_issues': self._assess_compliance_issues(files_analyzed)
        }

        # Security recommendations
        security_analysis['security_recommendations'] = self._generate_security_recommendations(
            security_analysis['security_indicators'],
            security_analysis['vulnerability_assessment']
        )

        return security_analysis

    def _analyze_business_patterns(self, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze business logic patterns and value delivery"""
        files_analyzed = analysis_results.get('files_analyzed', [])

        business_analysis = {
            'business_value_indicators': {},
            'revenue_generation_patterns': {},
            'customer_experience_patterns': {},
            'business_recommendations': []
        }

        # Business value indicators
        business_analysis['business_value_indicators'] = {
            'lead_generation_capability': self._assess_lead_generation_capability(files_analyzed),
            'automation_level': self._assess_automation_level(files_analyzed),
            'scalability_potential': self._assess_scalability_potential(files_analyzed),
            'market_readiness': self._assess_market_readiness(files_analyzed)
        }

        # Revenue generation patterns
        business_analysis['revenue_generation_patterns'] = {
            'monetization_strategies': self._identify_monetization_strategies(files_analyzed),
            'pricing_model_support': self._assess_pricing_model_support(files_analyzed),
            'customer_acquisition_tools': self._assess_customer_acquisition_tools(files_analyzed),
            'retention_mechanisms': self._assess_retention_mechanisms(files_analyzed)
        }

        # Customer experience patterns
        business_analysis['customer_experience_patterns'] = {
            'user_interface_quality': self._assess_user_interface_quality(files_analyzed),
            'response_time_optimization': self._assess_response_time_optimization(files_analyzed),
            'error_handling_quality': self._assess_error_handling_quality(files_analyzed),
            'accessibility_features': self._assess_accessibility_features(files_analyzed)
        }

        # Business recommendations
        business_analysis['business_recommendations'] = self._generate_business_recommendations(
            business_analysis['business_value_indicators'],
            business_analysis['revenue_generation_patterns'],
            business_analysis['customer_experience_patterns']
        )

        return business_analysis

    def generate_visualizations(self, analysis_results: Dict[str, Any], output_dir: str = "analysis_visualizations"):
        """Generate comprehensive visualizations of the analysis results"""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)

        print(f"📊 Generating visualizations in {output_path}...")

        # 1. Project Overview Dashboard
        self._create_project_overview_dashboard(analysis_results, output_path)

        # 2. Code Quality Metrics
        self._create_code_quality_visualizations(analysis_results, output_path)

        # 3. Architecture Analysis
        self._create_architecture_visualizations(analysis_results, output_path)

        # 4. Performance Analysis
        self._create_performance_visualizations(analysis_results, output_path)

        # 5. Business Intelligence Dashboard
        self._create_business_intelligence_dashboard(analysis_results, output_path)

        print(f"✅ Visualizations generated successfully!")
        return output_path

    def _create_project_overview_dashboard(self, analysis_results: Dict[str, Any], output_path: Path):
        """Create comprehensive project overview dashboard"""
        files_analyzed = analysis_results.get('files_analyzed', [])
        overall_intelligence = analysis_results.get('overall_intelligence', {})

        # Create subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('File Categories', 'Intelligence Levels', 'Confidence Distribution', 'Project Maturity'),
            specs=[[{"type": "pie"}, {"type": "pie"}],
                   [{"type": "histogram"}, {"type": "indicator"}]]
        )

        # File categories pie chart
        category_dist = overall_intelligence.get('category_distribution', {})
        if category_dist:
            fig.add_trace(
                go.Pie(labels=list(category_dist.keys()), values=list(category_dist.values()), name="Categories"),
                row=1, col=1
            )

        # Intelligence levels pie chart
        intelligence_dist = overall_intelligence.get('intelligence_distribution', {})
        if intelligence_dist:
            fig.add_trace(
                go.Pie(labels=list(intelligence_dist.keys()), values=list(intelligence_dist.values()), name="Intelligence"),
                row=1, col=2
            )

        # Confidence distribution histogram
        confidences = [f.get('confidence', 0) for f in files_analyzed]
        if confidences:
            fig.add_trace(
                go.Histogram(x=confidences, name="Confidence", nbinsx=10),
                row=2, col=1
            )

        # Project maturity indicator
        maturity = overall_intelligence.get('project_maturity', 'unknown')
        maturity_scores = {'early_stage': 0.3, 'developing': 0.6, 'mature': 0.9, 'unknown': 0.5}
        fig.add_trace(
            go.Indicator(
                mode="gauge+number",
                value=maturity_scores.get(maturity, 0.5),
                title={'text': "Project Maturity"},
                gauge={'axis': {'range': [None, 1]},
                       'bar': {'color': "darkblue"},
                       'steps': [{'range': [0, 0.3], 'color': "lightgray"},
                                {'range': [0.3, 0.6], 'color': "yellow"},
                                {'range': [0.6, 1], 'color': "green"}]}
            ),
            row=2, col=2
        )

        fig.update_layout(height=800, title_text="Project Overview Dashboard")
        fig.write_html(output_path / "project_overview_dashboard.html")

    def _create_code_quality_visualizations(self, analysis_results: Dict[str, Any], output_path: Path):
        """Create code quality visualization charts"""
        files_analyzed = analysis_results.get('files_analyzed', [])

        # Create DataFrame for easier plotting
        df = pd.DataFrame(files_analyzed)

        if not df.empty:
            # Complexity vs Confidence scatter plot
            fig = px.scatter(df, x='confidence', y='category', color='intelligence_level',
                           title='Code Quality Analysis',
                           labels={'confidence': 'Confidence Score', 'category': 'Category'})
            fig.write_html(output_path / "code_quality_scatter.html")

            # Intelligence level distribution
            fig = px.bar(df.groupby('intelligence_level').size().reset_index(name='count'),
                        x='intelligence_level', y='count',
                        title='Intelligence Level Distribution')
            fig.write_html(output_path / "intelligence_distribution.html")

    def _create_architecture_visualizations(self, analysis_results: Dict[str, Any], output_path: Path):
        """Create architecture analysis visualizations"""
        architectural_patterns = analysis_results.get('architectural_patterns', [])

        if architectural_patterns:
            # Architecture patterns bar chart
            fig = px.bar(x=architectural_patterns, y=[1]*len(architectural_patterns),
                        title='Detected Architectural Patterns')
            fig.update_layout(yaxis_title='Count')
            fig.write_html(output_path / "architectural_patterns.html")

    def _create_performance_visualizations(self, analysis_results: Dict[str, Any], output_path: Path):
        """Create performance analysis visualizations"""
        files_analyzed = analysis_results.get('files_analyzed', [])

        if files_analyzed:
            df = pd.DataFrame(files_analyzed)

            # Performance metrics heatmap
            fig = px.imshow(df[['confidence', 'intelligence_level']].corr(),
                           title='Performance Metrics Correlation')
            fig.write_html(output_path / "performance_heatmap.html")

    def _create_business_intelligence_dashboard(self, analysis_results: Dict[str, Any], output_path: Path):
        """Create business intelligence dashboard"""
        business_intelligence = analysis_results.get('business_intelligence', {})

        if business_intelligence:
            # Business value indicators
            value_indicators = business_intelligence.get('business_value_indicators', {})
            if value_indicators:
                fig = px.bar(x=list(value_indicators.keys()), y=list(value_indicators.values()),
                            title='Business Value Indicators')
                fig.write_html(output_path / "business_value_indicators.html")

    def _calculate_overall_score(self, analysis_results: Dict[str, Any], enhanced_insights: Dict[str, Any]) -> Dict[str, float]:
        """Calculate overall project score"""
        scores = {
            'code_quality': 0.0,
            'architecture': 0.0,
            'performance': 0.0,
            'security': 0.0,
            'business_value': 0.0,
            'overall': 0.0
        }

        # Code quality score
        overall_intelligence = analysis_results.get('overall_intelligence', {})
        scores['code_quality'] = overall_intelligence.get('average_confidence', 0.0)

        # Architecture score
        architectural_patterns = analysis_results.get('architectural_patterns', [])
        scores['architecture'] = min(len(architectural_patterns) * 0.2, 1.0)

        # Performance score (based on complexity)
        avg_complexity = overall_intelligence.get('average_complexity', 0)
        scores['performance'] = max(0, 1.0 - (avg_complexity / 50))  # Normalize complexity

        # Security score (placeholder - would need security analysis)
        scores['security'] = 0.7  # Default moderate score

        # Business value score
        innovation_score = enhanced_insights.get('innovation_indicators', {}).get('innovation_score', 0.0)
        scores['business_value'] = innovation_score

        # Overall score
        scores['overall'] = sum(scores.values()) / len(scores)

        return scores

    def _fallback_analysis(self, project_path: str) -> Dict[str, Any]:
        """Fallback analysis when advanced engine is not available"""
        project_path = Path(project_path)
        python_files = list(project_path.rglob('*.py'))

        return {
            'project_path': str(project_path),
            'files_analyzed': [{'file': str(f), 'category': 'unknown', 'confidence': 0.5} for f in python_files],
            'overall_intelligence': {
                'total_files': len(python_files),
                'average_confidence': 0.5,
                'project_maturity': 'unknown'
            },
            'architectural_patterns': [],
            'recommendations': ['Install advanced dependencies for full analysis'],
            'timestamp': datetime.now().isoformat()
        }

    # Helper methods for assessments (simplified implementations)
    def _assess_modularity(self, files_analyzed: List[Dict]) -> float:
        """Assess code modularity"""
        categories = set(f.get('category', 'unknown') for f in files_analyzed)
        return min(len(categories) / 5, 1.0)  # Normalize to 0-1

    def _assess_separation_of_concerns(self, files_analyzed: List[Dict]) -> float:
        """Assess separation of concerns"""
        categories = [f.get('category', 'unknown') for f in files_analyzed]
        unique_categories = len(set(categories))
        return min(unique_categories / len(files_analyzed), 1.0) if files_analyzed else 0.0

    def _assess_dependency_management(self, files_analyzed: List[Dict]) -> float:
        """Assess dependency management"""
        return 0.7  # Placeholder - would analyze imports and dependencies

    def _generate_scalability_recommendations(self, files_analyzed: List[Dict]) -> List[str]:
        """Generate scalability recommendations"""
        return [
            "Consider implementing microservices architecture",
            "Add horizontal scaling capabilities",
            "Implement caching mechanisms",
            "Optimize database queries"
        ]

    def _assess_complexity_debt(self, files_analyzed: List[Dict]) -> float:
        """Assess complexity-related technical debt"""
        high_complexity_files = sum(1 for f in files_analyzed if f.get('confidence', 0) < 0.5)
        return high_complexity_files / len(files_analyzed) if files_analyzed else 0.0

    def _assess_documentation_debt(self, files_analyzed: List[Dict]) -> float:
        """Assess documentation-related technical debt"""
        return 0.3  # Placeholder - would analyze docstrings and comments

    def _assess_test_coverage_debt(self, files_analyzed: List[Dict]) -> float:
        """Assess test coverage technical debt"""
        test_files = sum(1 for f in files_analyzed if 'test' in f.get('file', '').lower())
        return max(0, 1.0 - (test_files / len(files_analyzed))) if files_analyzed else 1.0

    def _identify_refactoring_priorities(self, files_analyzed: List[Dict]) -> List[str]:
        """Identify refactoring priorities"""
        priorities = []
        for f in files_analyzed:
            if f.get('confidence', 0) < 0.5:
                priorities.append(f"Refactor {f.get('file', 'unknown')} - low confidence")
        return priorities[:5]  # Top 5 priorities

    def _assess_ai_integration(self, files_analyzed: List[Dict]) -> float:
        """Assess AI integration level"""
        ai_files = sum(1 for f in files_analyzed if f.get('category') == 'voice_agents')
        return ai_files / len(files_analyzed) if files_analyzed else 0.0

    def _assess_modern_patterns(self, files_analyzed: List[Dict]) -> float:
        """Assess usage of modern patterns"""
        return 0.8  # Placeholder - would analyze async/await, type hints, etc.

    def _assess_automation_level(self, files_analyzed: List[Dict]) -> float:
        """Assess automation level"""
        automation_files = sum(1 for f in files_analyzed if f.get('category') in ['lead_generation', 'data_processing'])
        return automation_files / len(files_analyzed) if files_analyzed else 0.0

    def _generate_learning_recommendations(self, insights: Dict[str, Any]) -> List[str]:
        """Generate learning recommendations"""
        recommendations = []

        maintainability_score = insights.get('maintainability_score', 0)
        if maintainability_score < 0.7:
            recommendations.append("Focus on improving code maintainability")

        innovation_score = insights.get('innovation_indicators', {}).get('innovation_score', 0)
        if innovation_score < 0.6:
            recommendations.append("Explore modern AI and automation patterns")

        return recommendations

    # Additional helper methods (simplified implementations)
    def _assess_cohesion(self, files_analyzed: List[Dict]) -> float:
        return 0.7

    def _assess_coupling(self, files_analyzed: List[Dict]) -> float:
        return 0.6

    def _assess_single_responsibility(self, files_analyzed: List[Dict]) -> float:
        return 0.8

    def _assess_open_closed_principle(self, files_analyzed: List[Dict]) -> float:
        return 0.7

    def _assess_dependency_inversion(self, files_analyzed: List[Dict]) -> float:
        return 0.6

    def _assess_interface_segregation(self, files_analyzed: List[Dict]) -> float:
        return 0.7

    def _generate_architectural_recommendations(self, quality: Dict, principles: Dict) -> List[str]:
        return ["Implement dependency injection", "Add interface abstractions"]

    def _analyze_complexity_distribution(self, files_analyzed: List[Dict]) -> Dict[str, Any]:
        return {'low': 0.3, 'medium': 0.5, 'high': 0.2}

    def _analyze_function_size_distribution(self, files_analyzed: List[Dict]) -> Dict[str, Any]:
        return {'small': 0.4, 'medium': 0.4, 'large': 0.2}

    def _analyze_import_patterns(self, files_analyzed: List[Dict]) -> Dict[str, Any]:
        return {'standard_library': 0.3, 'third_party': 0.5, 'local': 0.2}

    def _identify_resource_intensive_patterns(self, files_analyzed: List[Dict]) -> List[str]:
        return ["File I/O operations", "Network requests"]

    def _identify_high_complexity_files(self, files_analyzed: List[Dict]) -> List[str]:
        return [f.get('file', '') for f in files_analyzed if f.get('confidence', 0) < 0.5][:3]

    def _identify_potential_bottlenecks(self, files_analyzed: List[Dict]) -> List[str]:
        return ["Database queries", "API calls"]

    def _identify_optimization_candidates(self, files_analyzed: List[Dict]) -> List[str]:
        return ["Caching implementation", "Async operations"]

    def _identify_optimization_opportunities(self, files_analyzed: List[Dict]) -> List[str]:
        return ["Implement caching", "Optimize database queries", "Add async support"]

    def _generate_performance_recommendations(self, indicators: Dict, bottlenecks: Dict) -> List[str]:
        return ["Implement caching", "Optimize algorithms", "Add monitoring"]

    def _assess_api_security(self, files_analyzed: List[Dict]) -> float:
        return 0.7

    def _assess_data_handling_security(self, files_analyzed: List[Dict]) -> float:
        return 0.6

    def _assess_authentication_patterns(self, files_analyzed: List[Dict]) -> float:
        return 0.5

    def _assess_input_validation(self, files_analyzed: List[Dict]) -> float:
        return 0.6

    def _identify_potential_vulnerabilities(self, files_analyzed: List[Dict]) -> List[str]:
        return ["SQL injection", "XSS vulnerability"]

    def _assess_security_risks(self, files_analyzed: List[Dict]) -> Dict[str, str]:
        return {'high': 'API exposure', 'medium': 'Data validation'}

    def _assess_compliance_issues(self, files_analyzed: List[Dict]) -> List[str]:
        return ["GDPR compliance", "Data retention"]

    def _generate_security_recommendations(self, indicators: Dict, vulnerabilities: Dict) -> List[str]:
        return ["Implement input validation", "Add authentication", "Encrypt sensitive data"]

    def _assess_lead_generation_capability(self, files_analyzed: List[Dict]) -> float:
        lead_files = sum(1 for f in files_analyzed if f.get('category') == 'lead_generation')
        return lead_files / len(files_analyzed) if files_analyzed else 0.0

    def _assess_scalability_potential(self, files_analyzed: List[Dict]) -> float:
        return 0.8

    def _assess_market_readiness(self, files_analyzed: List[Dict]) -> float:
        return 0.7

    def _identify_monetization_strategies(self, files_analyzed: List[Dict]) -> List[str]:
        return ["Subscription model", "Usage-based pricing", "Freemium"]

    def _assess_pricing_model_support(self, files_analyzed: List[Dict]) -> float:
        return 0.6

    def _assess_customer_acquisition_tools(self, files_analyzed: List[Dict]) -> float:
        return 0.8

    def _assess_retention_mechanisms(self, files_analyzed: List[Dict]) -> float:
        return 0.5

    def _assess_user_interface_quality(self, files_analyzed: List[Dict]) -> float:
        return 0.7

    def _assess_response_time_optimization(self, files_analyzed: List[Dict]) -> float:
        return 0.6

    def _assess_error_handling_quality(self, files_analyzed: List[Dict]) -> float:
        return 0.7

    def _assess_accessibility_features(self, files_analyzed: List[Dict]) -> float:
        return 0.5

    def _generate_business_recommendations(self, value: Dict, revenue: Dict, experience: Dict) -> List[str]:
        return ["Improve customer onboarding", "Add analytics dashboard", "Implement A/B testing"]

def main():
    """Main function to demonstrate the Intelligent Project Analyzer"""
    print("🧠 Intelligent Project Analyzer - Advanced AI-Powered Code Analysis")
    print("=" * 70)

    # Initialize analyzer
    analyzer = IntelligentProjectAnalyzer()

    # Analyze current project
    project_path = Path(__file__).parent
    print(f"Analyzing project: {project_path}")

    # Perform comprehensive analysis
    results = analyzer.analyze_project_comprehensive(str(project_path))

    # Display key results
    print(f"\n📊 Analysis Results:")
    print(f"Files analyzed: {len(results.get('files_analyzed', []))}")

    overall_score = results.get('overall_score', {})
    if overall_score:
        print(f"\n🎯 Overall Scores:")
        for category, score in overall_score.items():
            print(f"  {category.replace('_', ' ').title()}: {score:.2f}")

    # Generate visualizations
    viz_path = analyzer.generate_visualizations(results)
    print(f"\n📈 Visualizations saved to: {viz_path}")

    # Save comprehensive results
    results_file = project_path / 'intelligent_analysis_results.json'
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2, default=str)

    print(f"💾 Complete analysis saved to: {results_file}")

    # Display recommendations
    recommendations = results.get('core_analysis', {}).get('recommendations', [])
    if recommendations:
        print(f"\n💡 Key Recommendations:")
        for i, rec in enumerate(recommendations[:5], 1):
            print(f"  {i}. {rec}")

if __name__ == '__main__':
    main()
