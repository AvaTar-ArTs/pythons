"""
Integration Module for AVATARARTS Ecosystem
Connects the existing AutoTag analysis engine with the new database system
"""

import json
import os
import sqlite3
from datetime import datetime
from avatararts_db_schema import connect_to_avatararts_db, update_autotag_analysis
from incremental_indexer import IncrementalIndexer


class AutoTagDatabaseIntegrator:
    def __init__(self, db_path="avatararts.db", autotag_output_dir="/Users/steven/AutoTag/output"):
        self.db_path = db_path
        self.autotag_output_dir = autotag_output_dir
        self.conn = connect_to_avatararts_db(db_path)
    
    def get_file_id_by_path(self, file_path):
        """Get the database file ID for a given file path"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT id FROM files WHERE path = ?", (file_path,))
        result = cursor.fetchone()
        return result[0] if result else None
    
    def import_autotag_results(self, run_name):
        """
        Import results from an AutoTag run into the database
        """
        run_output_dir = os.path.join(self.autotag_output_dir, run_name)
        
        if not os.path.exists(run_output_dir):
            raise ValueError(f"AutoTag run directory does not exist: {run_output_dir}")
        
        # Look for the results CSV file
        csv_file = os.path.join(run_output_dir, f"{run_name}_results.csv")
        
        if os.path.exists(csv_file):
            print(f"Importing AutoTag results from CSV: {csv_file}")
            return self._import_from_csv(csv_file)
        else:
            # Look for the Phase 3 JSON file
            json_file = os.path.join(run_output_dir, f"{run_name}_phase3.json")
            
            if os.path.exists(json_file):
                print(f"Importing AutoTag results from JSON: {json_file}")
                return self._import_from_json(json_file)
            else:
                raise ValueError(f"No results file found in {run_output_dir} (expected {run_name}_results.csv or {run_name}_phase3.json)")
    
    def _import_from_csv(self, csv_file_path):
        """Import AutoTag results from CSV file"""
        import csv
        
        with open(csv_file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            imported_count = 0
            
            for row in reader:
                file_path = row['path']
                
                # Get the file ID from the database
                file_id = self.get_file_id_by_path(file_path)
                
                if not file_id:
                    print(f"Warning: File not found in database: {file_path}")
                    continue
                
                # Prepare analysis data from CSV row
                analysis_data = {
                    'rapid_scan_result': {
                        'file_type': row.get('primary_type', ''),
                        'size_category': self._categorize_size(float(row.get('size_mb', 0)) * 1024 * 1024)  # Convert MB to bytes
                    },
                    'intelligent_org_result': {
                        'category': row.get('intelligent_category', ''),
                        'confidence_score': float(row.get('confidence_score', 0))
                    },
                    'advanced_intel_result': {
                        'integration_potential': row.get('integration_potential_has_potential', False)
                    },
                    'business_value_score': float(row.get('predicted_business_value', 0)),
                    'business_value_reason': 'AutoTag analysis',
                    'semantic_tags': [row.get('intelligent_category', ''), row.get('primary_type', '')],
                    'content_summary': row.get('description', '')[:200]  # Limit description length
                }
                
                # Update the database with AutoTag analysis
                update_autotag_analysis(self.conn, file_id, analysis_data)
                imported_count += 1
        
        print(f"Imported {imported_count} records from CSV: {csv_file_path}")
        return imported_count
    
    def _import_from_json(self, json_file_path):
        """Import AutoTag results from JSON file"""
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        imported_count = 0
        
        if 'automation_tools' in data:
            for tool in data['automation_tools']:
                file_path = tool['path']
                
                # Get the file ID from the database
                file_id = self.get_file_id_by_path(file_path)
                
                if not file_id:
                    print(f"Warning: File not found in database: {file_path}")
                    continue
                
                # Prepare analysis data from JSON
                analysis_data = {
                    'rapid_scan_result': {
                        'file_type': tool.get('primary_type', ''),
                        'size_category': self._categorize_size(tool.get('size_mb', 0) * 1024 * 1024)  # Convert MB to bytes
                    },
                    'intelligent_org_result': {
                        'category': tool.get('intelligent_category', ''),
                        'confidence_score': tool.get('confidence_score', 0)
                    },
                    'advanced_intel_result': {
                        'integration_potential': tool.get('integration_potential', {}).get('has_potential', False),
                        'entities': tool.get('advanced_entities', {}),
                        'insights': tool.get('extracted_insights', [])
                    },
                    'business_value_score': tool.get('predicted_business_value', 0),
                    'business_value_reason': 'AutoTag advanced intelligence analysis',
                    'semantic_tags': self._extract_tags_from_tool(tool),
                    'content_summary': tool.get('description', '')[:200]  # Limit description length
                }
                
                # Update the database with AutoTag analysis
                update_autotag_analysis(self.conn, file_id, analysis_data)
                imported_count += 1
        
        print(f"Imported {imported_count} records from JSON: {json_file_path}")
        return imported_count
    
    def _categorize_size(self, size_bytes):
        """Categorize file size for rapid scanning"""
        if size_bytes < 1024:  # < 1KB
            return 'tiny'
        elif size_bytes < 1024 * 100:  # < 100KB
            return 'small'
        elif size_bytes < 1024 * 1024:  # < 1MB
            return 'medium'
        elif size_bytes < 1024 * 1024 * 10:  # < 10MB
            return 'large'
        else:
            return 'huge'
    
    def _extract_tags_from_tool(self, tool):
        """Extract semantic tags from a tool object"""
        tags = []
        
        # Add intelligent category
        if tool.get('intelligent_category'):
            tags.append(tool['intelligent_category'])
        
        # Add primary type
        if tool.get('primary_type'):
            tags.append(tool['primary_type'])
        
        # Add entities
        entities = tool.get('advanced_entities', {})
        for entity_type, entity_values in entities.items():
            if isinstance(entity_values, list):
                tags.extend(entity_values)
            elif isinstance(entity_values, str):
                tags.append(entity_values)
        
        # Add description keywords
        description = tool.get('description', '')
        if description:
            # Extract simple keywords from description
            desc_words = description.lower().replace(',', ' ').replace('.', ' ').split()
            # Add significant words (longer than 3 chars)
            for word in desc_words:
                if len(word) > 3 and word not in ['with', 'the', 'and', 'for', 'are', 'but', 'not', 'can', 'will']:
                    tags.append(word)
        
        # Remove duplicates and return
        return list(set(tags))
    
    def run_autotag_on_directory(self, directory_path, run_name=None):
        """
        Run AutoTag on a directory and import results into the database
        """
        if run_name is None:
            run_name = f"db_integration_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        print(f"Running AutoTag on directory: {directory_path}")
        print(f"Run name: {run_name}")
        
        # First, ensure the directory is indexed in the database
        indexer = IncrementalIndexer(db_path=self.db_path)
        indexer.scan_directory_incrementally(directory_path, max_files=None)
        indexer.close()
        
        # Run AutoTag on the directory
        import subprocess
        import sys
        
        autotag_script = "/Users/steven/AutoTag/autotag.sh"
        
        cmd = ["/bin/bash", autotag_script, directory_path, run_name, "--no-open"]
        
        print(f"Executing: {' '.join(cmd)}")
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            print("AutoTag execution completed successfully")
            print(f"Output: {result.stdout}")
            
            if result.stderr:
                print(f"Errors/Warnings: {result.stderr}")
        except subprocess.CalledProcessError as e:
            print(f"Error running AutoTag: {e}")
            print(f"Error output: {e.stderr}")
            return False
        
        # Import the results into the database
        try:
            imported_count = self.import_autotag_results(run_name)
            print(f"Successfully imported {imported_count} results into the database")
            return True
        except Exception as e:
            print(f"Error importing AutoTag results: {e}")
            return False
    
    def update_business_values_from_autotag(self):
        """
        Update business value scores in asset categories based on AutoTag analysis
        """
        cursor = self.conn.cursor()
        
        # Get average business value by business vertical
        cursor.execute('''
            SELECT 
                f.business_vertical,
                AVG(aa.business_value_score) as avg_business_value,
                COUNT(*) as file_count
            FROM files f
            JOIN autotag_analysis aa ON f.id = aa.file_id
            WHERE f.business_vertical IS NOT NULL
            GROUP BY f.business_vertical
        ''')
        
        results = cursor.fetchall()
        
        # Update asset categories with new average values
        for row in results:
            business_vertical = row['business_vertical']
            avg_business_value = row['avg_business_value']
            file_count = row['file_count']
            
            # Update the category with new computed values
            cursor.execute('''
                UPDATE asset_categories 
                SET 
                    revenue_potential = revenue_potential * (1 + (? / 10.0)),
                    activation_status = CASE 
                        WHEN ? > 7 THEN 'active'
                        WHEN ? > 4 THEN 'partial'
                        ELSE 'inactive'
                    END
                WHERE category_name = ?
            ''', (avg_business_value, avg_business_value, avg_business_value, business_vertical))
        
        self.conn.commit()
        print(f"Updated business values for {len(results)} business verticals")
    
    def get_latest_autotag_runs(self):
        """
        Get a list of available AutoTag runs from the output directory
        """
        if not os.path.exists(self.autotag_output_dir):
            return []
        
        runs = []
        for item in os.listdir(self.autotag_output_dir):
            item_path = os.path.join(self.autotag_output_dir, item)
            if os.path.isdir(item_path):
                # Check if it contains AutoTag results
                csv_file = os.path.join(item_path, f"{item}_results.csv")
                json_file = os.path.join(item_path, f"{item}_phase3.json")
                
                if os.path.exists(csv_file) or os.path.exists(json_file):
                    # Get modification time for sorting
                    mod_time = os.path.getmtime(item_path)
                    runs.append({
                        'name': item,
                        'path': item_path,
                        'modified': datetime.fromtimestamp(mod_time),
                        'has_csv': os.path.exists(csv_file),
                        'has_json': os.path.exists(json_file)
                    })
        
        # Sort by modification time (newest first)
        runs.sort(key=lambda x: x['modified'], reverse=True)
        return runs
    
    def close(self):
        """Close the database connection"""
        self.conn.close()


def demo_integration():
    """Demonstrate the AutoTag database integration"""
    print("Initializing AutoTag Database Integration...")
    
    integrator = AutoTagDatabaseIntegrator()
    
    # Show available AutoTag runs
    print("\nAvailable AutoTag runs:")
    runs = integrator.get_latest_autotag_runs()
    
    if runs:
        for i, run in enumerate(runs[:5]):  # Show first 5 runs
            print(f"  {i+1}. {run['name']} (Modified: {run['modified']})")
            print(f"     CSV: {'✓' if run['has_csv'] else '✗'}, JSON: {'✓' if run['has_json'] else '✗'}")
    else:
        print("  No AutoTag runs found")
    
    # Example: Run AutoTag on a small directory for demonstration
    # Note: This would typically be run on a specific directory of interest
    print("\nIntegration module initialized successfully!")
    print("To run AutoTag on a directory and import results:")
    print("  integrator.run_autotag_on_directory('/path/to/directory', 'run_name')")
    print("\nTo import existing AutoTag results:")
    print("  integrator.import_autotag_results('existing_run_name')")
    
    integrator.close()
    print("\nDemo completed!")


if __name__ == "__main__":
    demo_integration()