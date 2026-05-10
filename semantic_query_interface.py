import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
"""
Semantic Query Interface for AVATARARTS Ecosystem
Provides advanced search capabilities leveraging the database and AutoTag system
"""

import sqlite3
import json
from avatararts_db_schema import connect_to_avatararts_db


class SemanticQueryInterface:
    def __init__(self, db_path="avatararts.db"):
        self.db_path = db_path
        self.conn = connect_to_avatararts_db(db_path)
    
    def search_by_keywords(self, keywords, limit=10):
        """
        Search for files using keywords across multiple fields
        """
        cursor = self.conn.cursor()
        
        # Use FTS for full-text search
        fts_query = " OR ".join([f'"{kw}"*' for kw in keywords.split()])
        
        cursor.execute(f'''
            SELECT f.*, aa.business_value_score, aa.content_summary, aa.semantic_tags
            FROM files f
            JOIN autotag_analysis aa ON f.id = aa.file_id
            JOIN file_content_fts fts ON aa.id = fts.rowid
            WHERE fts MATCH ?
            ORDER BY aa.business_value_score DESC, f.modified_at DESC
            LIMIT ?
        ''', (fts_query, limit))
        
        return cursor.fetchall()
    
    def search_by_semantic_tags(self, tags, limit=10):
        """
        Search for files by semantic tags (using JSON operations)
        """
        cursor = self.conn.cursor()
        
        # Create a query that looks for files with specific tags in the semantic_tags JSON
        tag_conditions = " OR ".join([
            f"json_extract(semantic_tags, '$') LIKE '%{tag}%'"
            for tag in tags.split()
        ])
        
        cursor.execute(f'''
            SELECT f.*, aa.business_value_score, aa.content_summary, aa.semantic_tags
            FROM files f
            JOIN autotag_analysis aa ON f.id = aa.file_id
            WHERE ({tag_conditions})
            ORDER BY aa.business_value_score DESC, f.modified_at DESC
            LIMIT ?
        ''', (limit,))
        
        return cursor.fetchall()
    
    def search_by_business_vertical(self, vertical, min_business_value=0, limit=10):
        """
        Search for files within a specific business vertical
        """
        cursor = self.conn.cursor()
        
        cursor.execute('''
            SELECT f.*, aa.business_value_score, aa.content_summary, aa.semantic_tags
            FROM files f
            JOIN autotag_analysis aa ON f.id = aa.file_id
            WHERE f.business_vertical = ? AND aa.business_value_score >= ?
            ORDER BY aa.business_value_score DESC, f.modified_at DESC
            LIMIT ?
        ''', (vertical, min_business_value, limit))
        
        return cursor.fetchall()
    
    def search_by_file_type(self, extensions, limit=10):
        """
        Search for files by extension/type
        """
        cursor = self.conn.cursor()
        
        # Handle multiple extensions
        if isinstance(extensions, str):
            extensions = [extensions]
        
        placeholders = ','.join(['?' for _ in extensions])
        cursor.execute(f'''
            SELECT f.*, aa.business_value_score, aa.content_summary, aa.semantic_tags
            FROM files f
            JOIN autotag_analysis aa ON f.id = aa.file_id
            WHERE f.extension IN ({placeholders})
            ORDER BY aa.business_value_score DESC, f.modified_at DESC
            LIMIT ?
        ''', (*extensions, limit))
        
        return cursor.fetchall()
    
    def search_by_business_value_range(self, min_value, max_value, limit=10):
        """
        Search for files within a business value range
        """
        cursor = self.conn.cursor()
        
        cursor.execute('''
            SELECT f.*, aa.business_value_score, aa.content_summary, aa.semantic_tags
            FROM files f
            JOIN autotag_analysis aa ON f.id = aa.file_id
            WHERE aa.business_value_score BETWEEN ? AND ?
            ORDER BY aa.business_value_score DESC, f.modified_at DESC
            LIMIT ?
        ''', (min_value, max_value, limit))
        
        return cursor.fetchall()
    
    def semantic_similarity_search(self, reference_file_id, limit=10):
        """
        Find files that are semantically similar to a reference file
        """
        cursor = self.conn.cursor()
        
        # Get the semantic tags of the reference file
        cursor.execute('''
            SELECT semantic_tags
            FROM autotag_analysis
            WHERE file_id = ?
        ''', (reference_file_id,))
        
        result = cursor.fetchone()
        if not result:
            return []
        
        ref_tags = json.loads(result[0]) if result[0] else []
        if not ref_tags:
            return []
        
        # Build a query to find files with overlapping tags
        tag_placeholders = ','.join(['?' for _ in ref_tags])
        cursor.execute(f'''
            SELECT f.*, aa.business_value_score, aa.content_summary, aa.semantic_tags,
                   (SELECT COUNT(*) FROM json_each(?) 
                    WHERE json_extract(value, '$') IN ({tag_placeholders})) AS tag_overlap
            FROM files f
            JOIN autotag_analysis aa ON f.id = aa.file_id
            WHERE tag_overlap > 0
            ORDER BY tag_overlap DESC, aa.business_value_score DESC
            LIMIT ?
        ''', (json.dumps(ref_tags), *ref_tags, limit))
        
        return cursor.fetchall()
    
    def advanced_search(self, filters=None, sort_by='business_value', sort_order='DESC', limit=10):
        """
        Advanced search with multiple filters
        """
        cursor = self.conn.cursor()
        
        # Build dynamic query based on filters
        where_clauses = []
        params = []
        
        if filters:
            if 'keywords' in filters:
                # This would require FTS integration
                where_clauses.append("(f.filename LIKE ? OR aa.content_summary LIKE ?)")
                keyword_param = f"%{filters['keywords']}%"
                params.extend([keyword_param, keyword_param])
            
            if 'extensions' in filters:
                ext_list = filters['extensions'] if isinstance(ext_list, list) else [ext_list]
                placeholders = ','.join(['?' for _ in ext_list])
                where_clauses.append(f"f.extension IN ({placeholders})")
                params.extend(ext_list)
            
            if 'business_vertical' in filters:
                where_clauses.append("f.business_vertical = ?")
                params.append(filters['business_vertical'])
            
            if 'min_business_value' in filters:
                where_clauses.append("aa.business_value_score >= ?")
                params.append(filters['min_business_value'])
            
            if 'max_business_value' in filters:
                where_clauses.append("aa.business_value_score <= ?")
                params.append(filters['max_business_value'])
            
            if 'min_size' in filters:
                where_clauses.append("f.size_bytes >= ?")
                params.append(filters['min_size'])
            
            if 'max_size' in filters:
                where_clauses.append("f.size_bytes <= ?")
                params.append(filters['max_size'])
        
        # Construct the query
        query = '''
            SELECT f.*, aa.business_value_score, aa.content_summary, aa.semantic_tags
            FROM files f
            JOIN autotag_analysis aa ON f.id = aa.file_id
        '''
        
        if where_clauses:
            query += " WHERE " + " AND ".join(where_clauses)
        
        # Add sorting
        valid_sort_fields = ['business_value', 'modified_at', 'size_bytes', 'filename']
        sort_field_map = {
            'business_value': 'aa.business_value_score',
            'modified_at': 'f.modified_at',
            'size_bytes': 'f.size_bytes',
            'filename': 'f.filename'
        }
        
        if sort_by in valid_sort_fields:
            query += f" ORDER BY {sort_field_map[sort_by]} {sort_order}"
        else:
            query += " ORDER BY aa.business_value_score DESC"
        
        query += f" LIMIT ?"
        params.append(limit)
        
        cursor.execute(query, params)
        return cursor.fetchall()
    
    def get_business_insights(self):
        """
        Get insights about business value distribution across verticals
        """
        cursor = self.conn.cursor()
        
        cursor.execute('''
            SELECT 
                f.business_vertical,
                COUNT(*) as file_count,
                AVG(aa.business_value_score) as avg_business_value,
                SUM(ac.revenue_potential) as potential_revenue
            FROM files f
            JOIN autotag_analysis aa ON f.id = aa.file_id
            LEFT JOIN asset_categories ac ON f.business_vertical = ac.category_name
            GROUP BY f.business_vertical
            ORDER BY avg_business_value DESC
        ''')
        
        return cursor.fetchall()
    
    def get_top_valued_assets(self, limit=20):
        """
        Get the top valued assets across the entire system
        """
        cursor = self.conn.cursor()
        
        cursor.execute('''
            SELECT f.*, aa.business_value_score, aa.content_summary, aa.semantic_tags
            FROM files f
            JOIN autotag_analysis aa ON f.id = aa.file_id
            ORDER BY aa.business_value_score DESC, f.size_bytes DESC
            LIMIT ?
        ''', (limit,))
        
        return cursor.fetchall()
    
    def format_results(self, results):
        """
        Format query results for display
        """
        formatted = []
        for row in results:
            formatted_row = {
                'id': row['id'],
                'path': row['path'],
                'filename': row['filename'],
                'extension': row['extension'],
                'size_bytes': row['size_bytes'],
                'business_vertical': row['business_vertical'],
                'business_value_score': row['business_value_score'],
                'content_summary': row['content_summary'],
                'semantic_tags': json.loads(row['semantic_tags']) if row['semantic_tags'] else [],
                'modified_at': row['modified_at']
            }
            formatted.append(formatted_row)
        return formatted
    
    def close(self):
        """Close the database connection"""
        self.conn.close()


def demo_queries():
    """Demonstrate the query capabilities"""
    print("Initializing Semantic Query Interface...")
    sqi = SemanticQueryInterface()
    
    print("\n1. Top 5 highest business value assets:")
    top_assets = sqi.get_top_valued_assets(5)
    for asset in sqi.format_results(top_assets):
        print(f"  - {asset['filename']} (Value: {asset['business_value_score']:.2f})")
    
    print("\n2. Business insights by vertical:")
    insights = sqi.get_business_insights()
    for insight in insights:
        print(f"  - {insight['business_vertical']}: {insight['file_count']} files, "
              f"Avg Value: {insight['avg_business_value']:.2f}")
    
    print("\n3. Sample search by business vertical (AI Automation Tools):")
    ai_auto_files = sqi.search_by_business_vertical("AI Automation Tools", min_business_value=5.0, limit=3)
    for f in sqi.format_results(ai_auto_files):
        print(f"  - {f['filename']}: {f['business_value_score']:.2f} value")
    
    # Close the interface
    sqi.close()
    print("\nQuery demonstration completed!")


try:
        demo_queries()
except KeyboardInterrupt:
    logger.info("Execution interrupted by user")
    sys.exit(1)
except Exception as e:
    logger.error(f"An error occurred: {e}", exc_info=True)
    sys.exit(1)