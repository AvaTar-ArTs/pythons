#!/usr/bin/env python3
"""
Setup Periodic Quality Monitoring
=================================

Sets up and configures the periodic quality monitoring system.

Author: Enhanced by Claude
Version: 1.0
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime

def setup_monitoring():
    """Set up periodic quality monitoring."""
    print("🔧 Setting up Periodic Quality Monitoring...")
    
    # Check if required tools exist
    base_path = Path(__file__).parent.parent
    analyzer_path = base_path / "06_development_tools" / "content_aware_analyzer.py"
    improver_path = base_path / "06_development_tools" / "content_aware_improver.py"
    focused_analyzer_path = base_path / "06_development_tools" / "focused_quality_analyzer.py"
    
    if not analyzer_path.exists():
        print("❌ Content-aware analyzer not found!")
        return False
    
    if not improver_path.exists():
        print("❌ Content-aware improver not found!")
        return False
    
    if not focused_analyzer_path.exists():
        print("❌ Focused analyzer not found!")
        return False
    
    print("✅ All required tools found")
    
    # Create configuration
    config = {
        "analysis_schedule": "daily",
        "analysis_time": "02:00",
        "quality_thresholds": {
            "min_quality_score": 50.0,
            "min_docstring_coverage": 20.0,
            "min_type_hint_coverage": 15.0,
            "min_error_handling_coverage": 30.0,
            "min_logging_coverage": 25.0,
            "max_anti_patterns": 10
        },
        "alert_settings": {
            "enabled": True,
            "email_notifications": False,
            "email_recipients": [],
            "smtp_server": "",
            "smtp_port": 587,
            "smtp_username": "",
            "smtp_password": ""
        },
        "reporting": {
            "generate_reports": True,
            "report_directory": "quality_reports",
            "keep_reports_days": 30
        },
        "auto_improvements": {
            "enabled": True,
            "max_improvements_per_run": 10,
            "improvement_types": ["logging", "type_hints", "docstrings", "error_handling"]
        }
    }
    
    config_file = base_path / "quality_monitor_config.json"
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"✅ Configuration created: {config_file}")
    
    # Create quality reports directory
    reports_dir = base_path / "quality_reports"
    reports_dir.mkdir(exist_ok=True)
    print(f"✅ Reports directory created: {reports_dir}")
    
    # Run initial analysis
    print("🔍 Running initial quality analysis...")
    try:
        result = subprocess.run([
            sys.executable, str(analyzer_path),
            str(base_path),
            "--output", str(base_path / "initial_analysis.json")
        ], capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print("✅ Initial analysis completed successfully")
        else:
            print(f"⚠️ Initial analysis had issues: {result.stderr}")
    except subprocess.TimeoutExpired:
        print("⚠️ Initial analysis timed out")
    except Exception as e:
        print(f"⚠️ Error running initial analysis: {e}")
    
    # Create monitoring scripts
    create_monitoring_scripts(base_path)
    
    print("\n🎉 Periodic Quality Monitoring Setup Complete!")
    print("\n📋 Next Steps:")
    print("1. Review the configuration in quality_monitor_config.json")
    print("2. Run 'python start_monitoring.py' to begin monitoring")
    print("3. Check quality_reports/ for generated reports")
    print("4. Use 'python check_quality.py' to view current status")
    
    return True

def create_monitoring_scripts(base_path: Path):
    """Create convenient monitoring scripts."""
    
    # Start monitoring script
    start_script = base_path / "start_monitoring.py"
    with open(start_script, 'w') as f:
        f.write('''#!/usr/bin/env python3
"""
Start Periodic Quality Monitoring
=================================

Starts the periodic quality monitoring system.
"""

import sys
import os
from pathlib import Path

# Add the development tools to the path
sys.path.insert(0, str(Path(__file__).parent / "06_development_tools"))

from periodic_quality_monitor import PeriodicQualityMonitor

if __name__ == "__main__":
    base_path = Path(__file__).parent
    monitor = PeriodicQualityMonitor(str(base_path))
    
    print("🚀 Starting Periodic Quality Monitoring...")
    print("Press Ctrl+C to stop")
    
    try:
        monitor.start_monitoring()
    except KeyboardInterrupt:
        print("\\n⏹️ Monitoring stopped by user")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
''')
    
    # Check quality script
    check_script = base_path / "check_quality.py"
    with open(check_script, 'w') as f:
        f.write('''#!/usr/bin/env python3
"""
Check Current Quality Status
============================

Shows the current quality status and dashboard.
"""

import sys
import json
from pathlib import Path

# Add the development tools to the path
sys.path.insert(0, str(Path(__file__).parent / "06_development_tools"))

from periodic_quality_monitor import PeriodicQualityMonitor

if __name__ == "__main__":
    base_path = Path(__file__).parent
    monitor = PeriodicQualityMonitor(str(base_path))
    
    print("📊 Current Quality Status")
    print("=" * 50)
    
    # Run analysis once
    metrics = monitor.run_analysis()
    
    # Show dashboard
    dashboard = monitor.get_quality_dashboard()
    
    if "error" in dashboard:
        print(f"❌ {dashboard['error']}")
    else:
        current = dashboard["current_metrics"]
        print(f"📁 Total Files: {current['total_files']:,}")
        print(f"📝 Total Lines: {current['total_lines']:,}")
        print(f"🔧 Functions: {current['total_functions']:,}")
        print(f"🏗️ Classes: {current['total_classes']:,}")
        print(f"⭐ Quality Score: {current['average_quality_score']:.1f}/100")
        print(f"🧠 Semantic Score: {current['semantic_score']:.1f}/100")
        print(f"🔧 Maintainability: {current['maintainability_score']:.1f}/100")
        print(f"⚡ Performance Potential: {current['performance_potential']:.1f}/100")
        
        # Coverage metrics
        total_files = current['total_files']
        if total_files > 0:
            docstring_coverage = (current['files_with_docstrings'] / total_files) * 100
            type_hint_coverage = (current['files_with_type_hints'] / total_files) * 100
            error_handling_coverage = (current['files_with_error_handling'] / total_files) * 100
            logging_coverage = (current['files_with_logging'] / total_files) * 100
            
            print(f"\\n📊 Coverage Metrics:")
            print(f"📖 Docstrings: {docstring_coverage:.1f}%")
            print(f"🏷️ Type Hints: {type_hint_coverage:.1f}%")
            print(f"⚠️ Error Handling: {error_handling_coverage:.1f}%")
            print(f"📝 Logging: {logging_coverage:.1f}%")
        
        # Trends
        if dashboard["trends"]:
            print(f"\\n📈 Trends:")
            for trend in dashboard["trends"]:
                direction = "📈" if trend["trend_direction"] == "improving" else "📉" if trend["trend_direction"] == "declining" else "➡️"
                print(f"{direction} {trend['metric_name']}: {trend['change_percentage']:+.1f}%")
        
        # Recent alerts
        if dashboard["recent_alerts"]:
            print(f"\\n🚨 Recent Alerts ({len(dashboard['recent_alerts'])}):")
            for alert in dashboard["recent_alerts"][:5]:  # Show last 5
                severity_icon = "🔴" if alert["severity"] == "high" else "🟡" if alert["severity"] == "medium" else "🟢"
                print(f"{severity_icon} {alert['message']}")
        
        print(f"\\n📅 Last Analysis: {dashboard['last_analysis']}")
        print(f"📊 History Length: {dashboard['history_length']} records")
''')
    
    # Make scripts executable
    start_script.chmod(0o755)
    check_script.chmod(0o755)
    
    print(f"✅ Created start_monitoring.py")
    print(f"✅ Created check_quality.py")

if __name__ == "__main__":
    setup_monitoring()