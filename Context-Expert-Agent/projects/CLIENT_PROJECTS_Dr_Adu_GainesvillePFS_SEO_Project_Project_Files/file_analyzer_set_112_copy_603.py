#!/usr/bin/env python3
"""
Dr. Adu SEO Project File Analyzer and Organizer
Deep reads all files in the project directory and creates a comprehensive analysis
"""

import os
import re
import json
from datetime import datetime
from pathlib import Path
import markdown
from bs4 import BeautifulSoup

class DrAduProjectAnalyzer:
    def __init__(self, project_dir):
        self.project_dir = Path(project_dir)
        self.analysis_results = {
            'project_info': {},
            'files_analyzed': [],
            'content_summary': {},
            'recommendations': [],
            'organization_plan': {}
        }
        
    def analyze_file(self, file_path):
        """Analyze a single file and extract key information"""
        file_info = {
            'filename': file_path.name,
            'file_type': file_path.suffix,
            'size_bytes': file_path.stat().st_size,
            'word_count': 0,
            'line_count': 0,
            'content_preview': '',
            'key_topics': [],
            'seo_elements': {},
            'technical_details': {}
        }
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            file_info['word_count'] = len(content.split())
            file_info['line_count'] = len(content.splitlines())
            file_info['content_preview'] = content[:500] + "..." if len(content) > 500 else content
            
            # Extract key topics and SEO elements
            file_info['key_topics'] = self.extract_topics(content)
            file_info['seo_elements'] = self.extract_seo_elements(content)
            file_info['technical_details'] = self.extract_technical_details(content, file_path.suffix)
            
        except Exception as e:
            file_info['error'] = str(e)
            
        return file_info
    
    def extract_topics(self, content):
        """Extract key topics from content"""
        topics = []
        
        # Common SEO and medical topics
        topic_patterns = {
            'seo': r'\b(?:SEO|search engine optimization|meta tags|keywords|ranking)\b',
            'psychiatry': r'\b(?:psychiatry|psychiatrist|mental health|TMS therapy|forensic psychiatry)\b',
            'gainesville': r'\b(?:Gainesville|Florida|FL|local|location)\b',
            'technical': r'\b(?:HTML|CSS|JavaScript|structured data|schema|JSON-LD)\b',
            'business': r'\b(?:business|practice|clinic|services|patients|insurance)\b',
            'optimization': r'\b(?:optimization|improvement|enhancement|performance)\b'
        }
        
        for topic, pattern in topic_patterns.items():
            if re.search(pattern, content, re.IGNORECASE):
                topics.append(topic)
                
        return topics
    
    def extract_seo_elements(self, content):
        """Extract SEO-specific elements from content"""
        seo_elements = {
            'title_tags': [],
            'meta_descriptions': [],
            'h1_tags': [],
            'keywords': [],
            'structured_data': False,
            'contact_info': []
        }
        
        # Extract title tags
        title_matches = re.findall(r'<title[^>]*>(.*?)</title>', content, re.IGNORECASE | re.DOTALL)
        seo_elements['title_tags'] = [t.strip() for t in title_matches]
        
        # Extract meta descriptions
        meta_desc_matches = re.findall(r'<meta[^>]*name=["\']description["\'][^>]*content=["\']([^"\']*)["\']', content, re.IGNORECASE)
        seo_elements['meta_descriptions'] = meta_desc_matches
        
        # Extract H1 tags
        h1_matches = re.findall(r'<h1[^>]*>(.*?)</h1>', content, re.IGNORECASE | re.DOTALL)
        seo_elements['h1_tags'] = [h.strip() for h in h1_matches]
        
        # Check for structured data
        if 'application/ld+json' in content or 'schema.org' in content:
            seo_elements['structured_data'] = True
            
        # Extract contact information
        phone_matches = re.findall(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', content)
        email_matches = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', content)
        seo_elements['contact_info'] = {
            'phones': phone_matches,
            'emails': email_matches
        }
        
        return seo_elements
    
    def extract_technical_details(self, content, file_type):
        """Extract technical details based on file type"""
        details = {}
        
        if file_type == '.html':
            details['html_elements'] = self.analyze_html_structure(content)
        elif file_type == '.md':
            details['markdown_structure'] = self.analyze_markdown_structure(content)
            
        return details
    
    def analyze_html_structure(self, content):
        """Analyze HTML structure and elements"""
        try:
            soup = BeautifulSoup(content, 'html.parser')
            return {
                'head_elements': len(soup.find_all('head')),
                'body_elements': len(soup.find_all('body')),
                'div_count': len(soup.find_all('div')),
                'link_count': len(soup.find_all('a')),
                'image_count': len(soup.find_all('img')),
                'script_count': len(soup.find_all('script')),
                'style_count': len(soup.find_all('style'))
            }
        except:
            return {}
    
    def analyze_markdown_structure(self, content):
        """Analyze Markdown structure"""
        lines = content.split('\n')
        return {
            'headers': len([line for line in lines if line.startswith('#')]),
            'code_blocks': len([line for line in lines if line.startswith('```')]),
            'lists': len([line for line in lines if line.startswith('-') or line.startswith('*')]),
            'tables': len([line for line in lines if '|' in line])
        }
    
    def analyze_all_files(self):
        """Analyze all files in the project directory"""
        print("🔍 Analyzing Dr. Adu SEO Project Files...")
        
        for file_path in self.project_dir.iterdir():
            if file_path.is_file() and file_path.suffix in ['.md', '.html', '.txt', '.json']:
                print(f"   📄 Analyzing: {file_path.name}")
                file_analysis = self.analyze_file(file_path)
                self.analysis_results['files_analyzed'].append(file_analysis)
        
        self.generate_summary()
        self.generate_recommendations()
        self.create_organization_plan()
        
    def generate_summary(self):
        """Generate project summary"""
        files = self.analysis_results['files_analyzed']
        
        self.analysis_results['project_info'] = {
            'total_files': len(files),
            'total_word_count': sum(f.get('word_count', 0) for f in files),
            'total_size_bytes': sum(f.get('size_bytes', 0) for f in files),
            'file_types': list(set(f.get('file_type', '') for f in files)),
            'analysis_date': datetime.now().isoformat()
        }
        
        # Content summary
        all_topics = []
        for file_info in files:
            all_topics.extend(file_info.get('key_topics', []))
        
        topic_counts = {}
        for topic in all_topics:
            topic_counts[topic] = topic_counts.get(topic, 0) + 1
            
        self.analysis_results['content_summary'] = {
            'most_common_topics': sorted(topic_counts.items(), key=lambda x: x[1], reverse=True),
            'seo_files': len([f for f in files if 'seo' in f.get('key_topics', [])]),
            'technical_files': len([f for f in files if 'technical' in f.get('key_topics', [])]),
            'business_files': len([f for f in files if 'business' in f.get('key_topics', [])])
        }
    
    def generate_recommendations(self):
        """Generate recommendations based on analysis"""
        recommendations = []
        
        files = self.analysis_results['files_analyzed']
        
        # Check for missing elements
        has_invoice = any('invoice' in f['filename'].lower() for f in files)
        has_technical_report = any('technical' in f['filename'].lower() or 'improvements' in f['filename'].lower() for f in files)
        has_client_report = any('client' in f['filename'].lower() for f in files)
        has_visual_comparison = any('comparison' in f['filename'].lower() for f in files)
        
        if not has_invoice:
            recommendations.append("Create a detailed invoice document")
        if not has_technical_report:
            recommendations.append("Add technical implementation report")
        if not has_client_report:
            recommendations.append("Include client-friendly summary report")
        if not has_visual_comparison:
            recommendations.append("Add visual comparison documents")
            
        # Check for SEO completeness
        seo_files = [f for f in files if 'seo' in f.get('key_topics', [])]
        if len(seo_files) < 3:
            recommendations.append("Expand SEO documentation with more detailed reports")
            
        self.analysis_results['recommendations'] = recommendations
    
    def create_organization_plan(self):
        """Create a plan for better file organization"""
        files = self.analysis_results['files_analyzed']
        
        organization = {
            'reports': [],
            'technical': [],
            'client_facing': [],
            'visual': [],
            'invoices': []
        }
        
        for file_info in files:
            filename = file_info['filename'].lower()
            
            if 'invoice' in filename or 'pricing' in filename:
                organization['invoices'].append(file_info['filename'])
            elif 'technical' in filename or 'improvements' in filename or 'audit' in filename:
                organization['technical'].append(file_info['filename'])
            elif 'client' in filename or 'non_technical' in filename:
                organization['client_facing'].append(file_info['filename'])
            elif 'comparison' in filename or 'visual' in filename or 'live' in filename:
                organization['visual'].append(file_info['filename'])
            else:
                organization['reports'].append(file_info['filename'])
        
        self.analysis_results['organization_plan'] = organization
    
    def generate_report(self):
        """Generate comprehensive analysis report"""
        report = f"""
# Dr. Adu SEO Project - Comprehensive Analysis Report
**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Project Overview
- **Total Files Analyzed:** {self.analysis_results['project_info']['total_files']}
- **Total Word Count:** {self.analysis_results['project_info']['total_word_count']:,}
- **Total Size:** {self.analysis_results['project_info']['total_size_bytes']:,} bytes
- **File Types:** {', '.join(self.analysis_results['project_info']['file_types'])}

## Content Analysis
### Most Common Topics
"""
        
        for topic, count in self.analysis_results['content_summary']['most_common_topics'][:10]:
            report += f"- **{topic.title()}:** {count} mentions\n"
        
        report += f"""
### File Distribution
- **SEO Files:** {self.analysis_results['content_summary']['seo_files']}
- **Technical Files:** {self.analysis_results['content_summary']['technical_files']}
- **Business Files:** {self.analysis_results['content_summary']['business_files']}

## Detailed File Analysis
"""
        
        for file_info in self.analysis_results['files_analyzed']:
            report += f"""
### {file_info['filename']}
- **Type:** {file_info['file_type']}
- **Size:** {file_info['size_bytes']:,} bytes
- **Words:** {file_info['word_count']:,}
- **Lines:** {file_info['line_count']:,}
- **Topics:** {', '.join(file_info['key_topics'])}
- **SEO Elements:** {len(file_info['seo_elements']['title_tags'])} title tags, {len(file_info['seo_elements']['meta_descriptions'])} meta descriptions
"""
        
        report += f"""
## Recommendations
"""
        for rec in self.analysis_results['recommendations']:
            report += f"- {rec}\n"
        
        report += f"""
## Suggested Organization Structure
```
Dr_Adu_GainesvillePFS_SEO_Project/
├── 01_Invoices/
│   └── {', '.join(self.analysis_results['organization_plan']['invoices'])}
├── 02_Technical_Reports/
│   └── {', '.join(self.analysis_results['organization_plan']['technical'])}
├── 03_Client_Facing/
│   └── {', '.join(self.analysis_results['organization_plan']['client_facing'])}
├── 04_Visual_Comparisons/
│   └── {', '.join(self.analysis_results['organization_plan']['visual'])}
└── 05_General_Reports/
    └── {', '.join(self.analysis_results['organization_plan']['reports'])}
```

## Next Steps
1. Reorganize files according to the suggested structure
2. Create additional documentation based on recommendations
3. Generate a master index file for easy navigation
4. Create a project summary document
"""
        
        return report
    
    def save_analysis(self):
        """Save analysis results to files"""
        # Save JSON analysis
        with open(self.project_dir / 'project_analysis.json', 'w') as f:
            json.dump(self.analysis_results, f, indent=2)
        
        # Save markdown report
        report = self.generate_report()
        with open(self.project_dir / 'PROJECT_ANALYSIS_REPORT.md', 'w') as f:
            f.write(report)
        
        print(f"✅ Analysis saved to {self.project_dir}")
        print(f"   📊 JSON data: project_analysis.json")
        print(f"   📋 Report: PROJECT_ANALYSIS_REPORT.md")

def main():
    """Main execution function"""
    project_dir = Path(__file__).parent
    analyzer = DrAduProjectAnalyzer(project_dir)
    
    print("🚀 Starting Dr. Adu SEO Project Analysis...")
    analyzer.analyze_all_files()
    analyzer.save_analysis()
    
    print("\n📈 Analysis Complete!")
    print("Check the generated files for detailed insights and organization recommendations.")

if __name__ == "__main__":
    main()