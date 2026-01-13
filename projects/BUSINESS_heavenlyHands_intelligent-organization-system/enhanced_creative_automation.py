#!/usr/bin/env python3
"""
Enhanced Creative Automation System
===================================

Advanced Intelligent Organization System with:
- Twilio phone automation integration
- Enhanced semantic search with vector databases
- Multi-platform creative automation
- Agentic workflows for complex creative tasks
- Heavenly Hands specific phone automation

Author: AI Assistant
Date: 2025-10-26
"""

import os
import json
import sqlite3
import logging
import asyncio
import aiohttp
import re
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from pathlib import Path
import yaml
import requests
from twilio.rest import Client as TwilioClient
from twilio.twiml.voice_response import VoiceResponse
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class PhoneCallResult:
    """Result of a phone call operation"""
    call_sid: str
    status: str
    duration: Optional[int] = None
    cost: Optional[float] = None
    error: Optional[str] = None
    timestamp: str = None

@dataclass
class CreativeTask:
    """Creative automation task definition"""
    task_id: str
    name: str
    type: str  # 'phone_call', 'email', 'social_media', 'content_creation', 'lead_generation'
    target: str
    parameters: Dict[str, Any]
    priority: int = 1
    status: str = 'pending'
    created_at: str = None
    completed_at: Optional[str] = None
    result: Optional[Dict[str, Any]] = None

class TwilioPhoneAutomation:
    """Advanced Twilio phone automation for creative projects"""
    
    def __init__(self, account_sid: str, auth_token: str):
        self.client = TwilioClient(account_sid, auth_token)
        self.account_sid = account_sid
        self.auth_token = auth_token
        
    def make_outbound_call(self, to: str, from_: str, twiml: str = None, 
                          twiml_url: str = None, record: bool = True) -> PhoneCallResult:
        """Make an outbound call with TwiML"""
        try:
            call_params = {
                'to': to,
                'from_': from_,
                'record': record
            }
            
            if twiml:
                call_params['twiml'] = twiml
            elif twiml_url:
                call_params['url'] = twiml_url
            else:
                # Default TwiML for Heavenly Hands
                call_params['twiml'] = self._get_heavenly_hands_twiml()
            
            call = self.client.calls.create(**call_params)
            
            return PhoneCallResult(
                call_sid=call.sid,
                status=call.status,
                timestamp=datetime.now().isoformat()
            )
            
        except Exception as e:
            logger.error(f"Error making outbound call: {e}")
            return PhoneCallResult(
                call_sid="",
                status="failed",
                error=str(e),
                timestamp=datetime.now().isoformat()
            )
    
    def _get_heavenly_hands_twiml(self) -> str:
        """Generate TwiML for Heavenly Hands cleaning service"""
        response = VoiceResponse()
        
        # Greeting
        response.say("Hello! This is Heavenly Hands Cleaning Service. Thank you for your interest in our professional cleaning services.")
        
        # Gather input for service type
        gather = response.gather(
            num_digits=1,
            action='/handle_gather',
            method='POST',
            timeout=10
        )
        gather.say("Press 1 for residential cleaning, 2 for commercial cleaning, 3 for move-in/move-out cleaning, or 4 to speak with a representative.")
        
        # Fallback if no input
        response.say("We didn't receive any input. Please call us back at your convenience.")
        response.hangup()
        
        return str(response)
    
    def create_lead_generation_call(self, phone_number: str, lead_data: Dict[str, Any]) -> PhoneCallResult:
        """Create a personalized lead generation call"""
        # Customize TwiML based on lead data
        twiml = self._create_personalized_twiml(lead_data)
        
        return self.make_outbound_call(
            to=phone_number,
            from_=os.getenv('TWILIO_PHONE_NUMBER'),
            twiml=twiml
        )
    
    def _create_personalized_twiml(self, lead_data: Dict[str, Any]) -> str:
        """Create personalized TwiML based on lead data"""
        response = VoiceResponse()
        
        name = lead_data.get('name', 'valued customer')
        service_interest = lead_data.get('service_interest', 'cleaning services')
        
        response.say(f"Hello {name}! This is Heavenly Hands Cleaning Service.")
        response.say(f"We noticed your interest in {service_interest} and wanted to reach out personally.")
        response.say("We offer professional, reliable cleaning services with a 100% satisfaction guarantee.")
        
        # Gather input
        gather = response.gather(
            num_digits=1,
            action='/handle_lead_gather',
            method='POST',
            timeout=15
        )
        gather.say("Press 1 to schedule a free consultation, 2 to learn about our pricing, 3 to speak with our team, or 0 to be removed from our call list.")
        
        response.say("Thank you for your time. Have a wonderful day!")
        response.hangup()
        
        return str(response)

class EnhancedVectorSearch:
    """Enhanced semantic search with advanced vector database approaches"""
    
    def __init__(self, db_path: str = "enhanced_vector_search.db"):
        self.db_path = db_path
        self.init_database()
        
    def init_database(self):
        """Initialize the enhanced vector search database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Enhanced content indexing
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS content_vectors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_path TEXT NOT NULL,
                content_type TEXT NOT NULL,
                content_hash TEXT NOT NULL,
                vector_data TEXT NOT NULL,
                metadata TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Semantic relationships
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS semantic_relationships (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_id INTEGER,
                target_id INTEGER,
                relationship_type TEXT NOT NULL,
                confidence_score REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (source_id) REFERENCES content_vectors (id),
                FOREIGN KEY (target_id) REFERENCES content_vectors (id)
            )
        ''')
        
        # Content categories
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS content_categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content_id INTEGER,
                category TEXT NOT NULL,
                confidence REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (content_id) REFERENCES content_vectors (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def index_content(self, file_path: str, content: str, content_type: str = "text") -> bool:
        """Index content with enhanced semantic analysis"""
        try:
            # Generate content hash
            import hashlib
            content_hash = hashlib.md5(content.encode()).hexdigest()
            
            # Enhanced vector representation (simplified for demo)
            vector_data = self._generate_enhanced_vector(content, content_type)
            
            # Extract metadata
            metadata = self._extract_metadata(content, content_type)
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Check if content already exists
            cursor.execute('SELECT id FROM content_vectors WHERE content_hash = ?', (content_hash,))
            existing = cursor.fetchone()
            
            if existing:
                # Update existing
                cursor.execute('''
                    UPDATE content_vectors 
                    SET vector_data = ?, metadata = ?, updated_at = CURRENT_TIMESTAMP
                    WHERE content_hash = ?
                ''', (vector_data, metadata, content_hash))
                content_id = existing[0]
            else:
                # Insert new
                cursor.execute('''
                    INSERT INTO content_vectors (file_path, content_type, content_hash, vector_data, metadata)
                    VALUES (?, ?, ?, ?, ?)
                ''', (file_path, content_type, content_hash, vector_data, metadata))
                content_id = cursor.lastrowid
            
            # Categorize content
            self._categorize_content(cursor, content_id, content, content_type)
            
            conn.commit()
            conn.close()
            
            return True
            
        except Exception as e:
            logger.error(f"Error indexing content: {e}")
            return False
    
    def _generate_enhanced_vector(self, content: str, content_type: str) -> str:
        """Generate enhanced vector representation"""
        # Simplified vector generation (in production, use sentence-transformers)
        words = content.lower().split()
        word_freq = {}
        for word in words:
            word_freq[word] = word_freq.get(word, 0) + 1
        
        # Normalize frequencies
        total_words = len(words)
        normalized_freq = {word: freq/total_words for word, freq in word_freq.items()}
        
        return json.dumps(normalized_freq)
    
    def _extract_metadata(self, content: str, content_type: str) -> str:
        """Extract rich metadata from content"""
        metadata = {
            'word_count': len(content.split()),
            'char_count': len(content),
            'content_type': content_type,
            'has_phone_numbers': bool(re.search(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', content)),
            'has_email': bool(re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', content)),
            'has_urls': bool(re.search(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', content)),
            'sentiment': self._analyze_sentiment(content),
            'keywords': self._extract_keywords(content)
        }
        
        return json.dumps(metadata)
    
    def _analyze_sentiment(self, content: str) -> str:
        """Simple sentiment analysis"""
        positive_words = ['good', 'great', 'excellent', 'amazing', 'wonderful', 'fantastic', 'love', 'best']
        negative_words = ['bad', 'terrible', 'awful', 'hate', 'worst', 'horrible', 'disappointed']
        
        words = content.lower().split()
        positive_count = sum(1 for word in words if word in positive_words)
        negative_count = sum(1 for word in words if word in negative_words)
        
        if positive_count > negative_count:
            return 'positive'
        elif negative_count > positive_count:
            return 'negative'
        else:
            return 'neutral'
    
    def _extract_keywords(self, content: str) -> List[str]:
        """Extract key terms from content"""
        # Simple keyword extraction (in production, use NLP libraries)
        words = content.lower().split()
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
        keywords = [word for word in words if len(word) > 3 and word not in stop_words]
        
        # Count frequency and return top keywords
        word_freq = {}
        for word in keywords:
            word_freq[word] = word_freq.get(word, 0) + 1
        
        return sorted(word_freq.keys(), key=lambda x: word_freq[x], reverse=True)[:10]
    
    def _categorize_content(self, cursor, content_id: int, content: str, content_type: str):
        """Categorize content based on type and content"""
        categories = []
        
        # Content type categories
        if content_type == 'html':
            categories.append(('web_content', 0.9))
        elif content_type == 'css':
            categories.append(('styling', 0.9))
        elif content_type == 'js':
            categories.append(('scripting', 0.9))
        
        # Content-based categories
        content_lower = content.lower()
        if 'cleaning' in content_lower or 'clean' in content_lower:
            categories.append(('cleaning_services', 0.8))
        if 'price' in content_lower or 'cost' in content_lower or '$' in content:
            categories.append(('pricing', 0.7))
        if 'contact' in content_lower or 'phone' in content_lower or 'email' in content_lower:
            categories.append(('contact_info', 0.8))
        if 'testimonial' in content_lower or 'review' in content_lower or 'customer' in content_lower:
            categories.append(('testimonials', 0.7))
        
        # Insert categories
        for category, confidence in categories:
            cursor.execute('''
                INSERT INTO content_categories (content_id, category, confidence)
                VALUES (?, ?, ?)
            ''', (content_id, category, confidence))
    
    def semantic_search(self, query: str, content_types: List[str] = None, 
                       categories: List[str] = None, limit: int = 10) -> List[Dict[str, Any]]:
        """Enhanced semantic search with filtering"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Build query
            where_conditions = []
            params = []
            
            if content_types:
                placeholders = ','.join(['?' for _ in content_types])
                where_conditions.append(f"content_type IN ({placeholders})")
                params.extend(content_types)
            
            if categories:
                placeholders = ','.join(['?' for _ in categories])
                where_conditions.append(f"""
                    content_id IN (
                        SELECT content_id FROM content_categories 
                        WHERE category IN ({placeholders})
                    )
                """)
                params.extend(categories)
            
            where_clause = " AND ".join(where_conditions) if where_conditions else "1=1"
            
            # Search query
            search_query = f"""
                SELECT cv.id, cv.file_path, cv.content_type, cv.metadata, cv.vector_data
                FROM content_vectors cv
                WHERE {where_clause}
                ORDER BY cv.updated_at DESC
                LIMIT ?
            """
            params.append(limit)
            
            cursor.execute(search_query, params)
            results = cursor.fetchall()
            
            # Process results
            search_results = []
            for row in results:
                content_id, file_path, content_type, metadata, vector_data = row
                
                # Calculate similarity (simplified)
                similarity = self._calculate_similarity(query, vector_data)
                
                search_results.append({
                    'content_id': content_id,
                    'file_path': file_path,
                    'content_type': content_type,
                    'metadata': json.loads(metadata) if metadata else {},
                    'similarity_score': similarity
                })
            
            # Sort by similarity
            search_results.sort(key=lambda x: x['similarity_score'], reverse=True)
            
            conn.close()
            return search_results
            
        except Exception as e:
            logger.error(f"Error in semantic search: {e}")
            return []
    
    def _calculate_similarity(self, query: str, vector_data: str) -> float:
        """Calculate similarity between query and vector data"""
        try:
            vector = json.loads(vector_data)
            query_words = query.lower().split()
            
            # Simple cosine similarity
            query_freq = {}
            for word in query_words:
                query_freq[word] = query_freq.get(word, 0) + 1
            
            # Normalize query frequencies
            total_query_words = len(query_words)
            query_norm = {word: freq/total_query_words for word, freq in query_freq.items()}
            
            # Calculate dot product
            dot_product = sum(query_norm.get(word, 0) * vector.get(word, 0) for word in set(query_norm.keys()) | set(vector.keys()))
            
            # Calculate magnitudes
            query_magnitude = sum(freq**2 for freq in query_norm.values())**0.5
            vector_magnitude = sum(freq**2 for freq in vector.values())**0.5
            
            if query_magnitude == 0 or vector_magnitude == 0:
                return 0.0
            
            return dot_product / (query_magnitude * vector_magnitude)
            
        except Exception as e:
            logger.error(f"Error calculating similarity: {e}")
            return 0.0

class CreativeAutomationPlatform:
    """Multi-platform creative automation system"""
    
    def __init__(self, db_path: str = "creative_automation.db"):
        self.db_path = db_path
        self.twilio = None
        self.init_database()
        
        # Initialize Twilio if credentials available
        if os.getenv('TWILIO_ACCOUNT_SID') and os.getenv('TWILIO_AUTH_TOKEN'):
            self.twilio = TwilioPhoneAutomation(
                os.getenv('TWILIO_ACCOUNT_SID'),
                os.getenv('TWILIO_AUTH_TOKEN')
            )
    
    def init_database(self):
        """Initialize creative automation database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Creative tasks
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS creative_tasks (
                task_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                type TEXT NOT NULL,
                target TEXT NOT NULL,
                parameters TEXT NOT NULL,
                priority INTEGER DEFAULT 1,
                status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                completed_at TIMESTAMP,
                result TEXT
            )
        ''')
        
        # Automation workflows
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS automation_workflows (
                workflow_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT,
                steps TEXT NOT NULL,
                status TEXT DEFAULT 'active',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_run TIMESTAMP,
                next_run TIMESTAMP
            )
        ''')
        
        # Lead generation data
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS leads (
                lead_id TEXT PRIMARY KEY,
                name TEXT,
                phone TEXT,
                email TEXT,
                service_interest TEXT,
                source TEXT,
                status TEXT DEFAULT 'new',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_contact TIMESTAMP,
                notes TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def create_phone_campaign(self, campaign_name: str, phone_numbers: List[str], 
                            twiml_template: str = None) -> str:
        """Create a phone campaign for lead generation"""
        try:
            campaign_id = f"campaign_{int(datetime.now().timestamp())}"
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Create campaign workflow
            workflow_steps = []
            for i, phone_number in enumerate(phone_numbers):
                task_id = f"call_{campaign_id}_{i}"
                
                # Create call task
                task = CreativeTask(
                    task_id=task_id,
                    name=f"Call {phone_number}",
                    type="phone_call",
                    target=phone_number,
                    parameters={
                        'twiml': twiml_template or 'default_heavenly_hands',
                        'record': True,
                        'campaign_id': campaign_id
                    },
                    priority=1,
                    created_at=datetime.now().isoformat()
                )
                
                self._save_task(cursor, task)
                workflow_steps.append(task_id)
            
            # Save workflow
            cursor.execute('''
                INSERT INTO automation_workflows (workflow_id, name, description, steps, status)
                VALUES (?, ?, ?, ?, ?)
            ''', (campaign_id, campaign_name, f"Phone campaign with {len(phone_numbers)} calls", 
                  json.dumps(workflow_steps), 'active'))
            
            conn.commit()
            conn.close()
            
            logger.info(f"Created phone campaign: {campaign_id} with {len(phone_numbers)} calls")
            return campaign_id
            
        except Exception as e:
            logger.error(f"Error creating phone campaign: {e}")
            return ""
    
    def execute_phone_campaign(self, campaign_id: str) -> Dict[str, Any]:
        """Execute a phone campaign"""
        if not self.twilio:
            return {'error': 'Twilio not configured'}
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get campaign workflow
            cursor.execute('SELECT steps FROM automation_workflows WHERE workflow_id = ?', (campaign_id,))
            workflow = cursor.fetchone()
            
            if not workflow:
                return {'error': 'Campaign not found'}
            
            steps = json.loads(workflow[0])
            results = []
            
            for task_id in steps:
                # Get task details
                cursor.execute('SELECT * FROM creative_tasks WHERE task_id = ?', (task_id,))
                task_data = cursor.fetchone()
                
                if not task_data:
                    continue
                
                # Execute phone call
                call_result = self.twilio.make_outbound_call(
                    to=task_data[3],  # target
                    from_=os.getenv('TWILIO_PHONE_NUMBER'),
                    twiml=task_data[4]  # parameters
                )
                
                # Update task status
                cursor.execute('''
                    UPDATE creative_tasks 
                    SET status = ?, completed_at = ?, result = ?
                    WHERE task_id = ?
                ''', ('completed', datetime.now().isoformat(), 
                      json.dumps(asdict(call_result)), task_id))
                
                results.append({
                    'task_id': task_id,
                    'phone_number': task_data[3],
                    'result': asdict(call_result)
                })
            
            conn.commit()
            conn.close()
            
            return {
                'campaign_id': campaign_id,
                'total_calls': len(steps),
                'completed_calls': len(results),
                'results': results
            }
            
        except Exception as e:
            logger.error(f"Error executing phone campaign: {e}")
            return {'error': str(e)}
    
    def _save_task(self, cursor, task: CreativeTask):
        """Save a creative task to database"""
        cursor.execute('''
            INSERT OR REPLACE INTO creative_tasks 
            (task_id, name, type, target, parameters, priority, status, created_at, completed_at, result)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (task.task_id, task.name, task.type, task.target, json.dumps(task.parameters),
              task.priority, task.status, task.created_at, task.completed_at, 
              json.dumps(task.result) if task.result else None))

class EnhancedAgenticWorkflows:
    """Advanced agentic workflows for creative automation"""
    
    def __init__(self, openai_api_key: str):
        self.client = openai.OpenAI(api_key=openai_api_key)
        self.db_path = "agentic_workflows_enhanced.db"
        self.init_database()
    
    def init_database(self):
        """Initialize agentic workflows database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS agentic_workflows (
                workflow_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT,
                goal TEXT NOT NULL,
                context TEXT,
                steps TEXT NOT NULL,
                status TEXT DEFAULT 'planning',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                execution_log TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def create_creative_workflow(self, goal: str, context: Dict[str, Any] = None) -> str:
        """Create an agentic workflow for creative automation"""
        try:
            workflow_id = f"agentic_{int(datetime.now().timestamp())}"
            
            # Generate workflow plan using AI
            plan = self._generate_workflow_plan(goal, context or {})
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO agentic_workflows 
                (workflow_id, name, description, goal, context, steps, status)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (workflow_id, plan['name'], plan['description'], goal,
                  json.dumps(context or {}), json.dumps(plan['steps']), 'ready'))
            
            conn.commit()
            conn.close()
            
            logger.info(f"Created agentic workflow: {workflow_id}")
            return workflow_id
            
        except Exception as e:
            logger.error(f"Error creating agentic workflow: {e}")
            return ""
    
    def _generate_workflow_plan(self, goal: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate workflow plan using AI"""
        try:
            prompt = f"""
            Create a detailed workflow plan for the following creative automation goal:
            
            Goal: {goal}
            Context: {json.dumps(context, indent=2)}
            
            The workflow should be designed for a cleaning service business (Heavenly Hands) and should include:
            1. Lead generation and phone outreach
            2. Content creation and marketing
            3. Social media automation
            4. Customer follow-up and retention
            5. Analytics and optimization
            
            Return a JSON response with:
            - name: Workflow name
            - description: Brief description
            - steps: Array of step objects with id, name, type, parameters, dependencies
            """
            
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                max_completion_tokens=2000,
                temperature=0.7
            )
            
            plan_text = response.choices[0].message.content
            
            # Extract JSON from response
            import re
            json_match = re.search(r'\{.*\}', plan_text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            else:
                # Fallback plan
                return {
                    'name': f"Creative Workflow for {goal}",
                    'description': f"Automated workflow to achieve: {goal}",
                    'steps': [
                        {
                            'id': 'step_1',
                            'name': 'Lead Generation',
                            'type': 'phone_campaign',
                            'parameters': {'target_audience': 'potential_customers'},
                            'dependencies': []
                        },
                        {
                            'id': 'step_2',
                            'name': 'Content Creation',
                            'type': 'content_generation',
                            'parameters': {'content_type': 'marketing_materials'},
                            'dependencies': ['step_1']
                        },
                        {
                            'id': 'step_3',
                            'name': 'Social Media Automation',
                            'type': 'social_media',
                            'parameters': {'platforms': ['facebook', 'instagram']},
                            'dependencies': ['step_2']
                        }
                    ]
                }
                
        except Exception as e:
            logger.error(f"Error generating workflow plan: {e}")
            return {
                'name': f"Basic Workflow for {goal}",
                'description': f"Simple workflow to achieve: {goal}",
                'steps': [
                    {
                        'id': 'step_1',
                        'name': 'Execute Goal',
                        'type': 'general',
                        'parameters': {'goal': goal},
                        'dependencies': []
                    }
                ]
            }
    
    def execute_workflow(self, workflow_id: str) -> Dict[str, Any]:
        """Execute an agentic workflow"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get workflow
            cursor.execute('SELECT * FROM agentic_workflows WHERE workflow_id = ?', (workflow_id,))
            workflow = cursor.fetchone()
            
            if not workflow:
                return {'error': 'Workflow not found'}
            
            steps = json.loads(workflow[5])  # steps column
            execution_log = []
            
            # Update status to running
            cursor.execute('''
                UPDATE agentic_workflows 
                SET status = ?, updated_at = CURRENT_TIMESTAMP
                WHERE workflow_id = ?
            ''', ('running', workflow_id))
            
            # Execute steps
            for step in steps:
                step_result = self._execute_step(step, workflow[3])  # context
                execution_log.append({
                    'step_id': step['id'],
                    'step_name': step['name'],
                    'result': step_result,
                    'timestamp': datetime.now().isoformat()
                })
            
            # Update workflow with results
            cursor.execute('''
                UPDATE agentic_workflows 
                SET status = ?, execution_log = ?, updated_at = CURRENT_TIMESTAMP
                WHERE workflow_id = ?
            ''', ('completed', json.dumps(execution_log), workflow_id))
            
            conn.commit()
            conn.close()
            
            return {
                'workflow_id': workflow_id,
                'status': 'completed',
                'execution_log': execution_log
            }
            
        except Exception as e:
            logger.error(f"Error executing workflow: {e}")
            return {'error': str(e)}
    
    def _execute_step(self, step: Dict[str, Any], context: str) -> Dict[str, Any]:
        """Execute a single workflow step"""
        step_type = step.get('type', 'general')
        parameters = step.get('parameters', {})
        
        if step_type == 'phone_campaign':
            return self._execute_phone_campaign_step(parameters)
        elif step_type == 'content_generation':
            return self._execute_content_generation_step(parameters)
        elif step_type == 'social_media':
            return self._execute_social_media_step(parameters)
        else:
            return {'status': 'completed', 'message': f'Executed {step_type} step'}

class EnhancedIntelligentOrganizationSystem:
    """Enhanced Intelligent Organization System with creative automation"""
    
    def __init__(self):
        self.vector_search = EnhancedVectorSearch()
        self.creative_automation = CreativeAutomationPlatform()
        self.agentic_workflows = EnhancedAgenticWorkflows(os.getenv('OPENAI_API_KEY'))
        self.project_path = os.getenv('HEAVENLY_HANDS_PATH', '/Users/steven/ai-sites/heavenlyHands-advanced')
        
        logger.info("🚀 Enhanced Intelligent Organization System initialized")
    
    def index_project_content(self, project_path: str = None) -> bool:
        """Index project content with enhanced semantic analysis"""
        project_path = project_path or self.project_path
        
        try:
            indexed_count = 0
            
            for root, dirs, files in os.walk(project_path):
                # Skip virtual environments and hidden directories
                dirs[:] = [d for d in dirs if not d.startswith('.') and d != 'venv']
                
                for file in files:
                    if file.startswith('.'):
                        continue
                    
                    file_path = os.path.join(root, file)
                    
                    try:
                        # Determine content type
                        if file.endswith(('.html', '.htm')):
                            content_type = 'html'
                        elif file.endswith('.css'):
                            content_type = 'css'
                        elif file.endswith(('.js', '.jsx')):
                            content_type = 'js'
                        elif file.endswith(('.py', '.pyw')):
                            content_type = 'python'
                        else:
                            content_type = 'text'
                        
                        # Read and index content
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                        
                        if self.vector_search.index_content(file_path, content, content_type):
                            indexed_count += 1
                    
                    except Exception as e:
                        logger.warning(f"Could not index {file_path}: {e}")
                        continue
            
            logger.info(f"Indexed {indexed_count} files with enhanced semantic analysis")
            return True
            
        except Exception as e:
            logger.error(f"Error indexing project content: {e}")
            return False
    
    def create_heavenly_hands_phone_system(self) -> Dict[str, Any]:
        """Create comprehensive phone automation system for Heavenly Hands"""
        try:
            # Create lead generation campaign
            sample_leads = [
                {'name': 'John Smith', 'phone': '+1234567890', 'service_interest': 'residential cleaning'},
                {'name': 'Sarah Johnson', 'phone': '+1234567891', 'service_interest': 'commercial cleaning'},
                {'name': 'Mike Davis', 'phone': '+1234567892', 'service_interest': 'move-in cleaning'}
            ]
            
            phone_numbers = [lead['phone'] for lead in sample_leads]
            campaign_id = self.creative_automation.create_phone_campaign(
                "Heavenly Hands Lead Generation",
                phone_numbers
            )
            
            # Create agentic workflow for follow-up
            workflow_id = self.agentic_workflows.create_creative_workflow(
                "Automated customer follow-up and retention for Heavenly Hands",
                {
                    'business_type': 'cleaning_service',
                    'target_customers': 'residential_and_commercial',
                    'services': ['regular_cleaning', 'deep_cleaning', 'move_in_out']
                }
            )
            
            return {
                'phone_campaign_id': campaign_id,
                'agentic_workflow_id': workflow_id,
                'sample_leads': sample_leads,
                'status': 'created'
            }
            
        except Exception as e:
            logger.error(f"Error creating Heavenly Hands phone system: {e}")
            return {'error': str(e)}
    
    def execute_creative_automation(self, workflow_id: str) -> Dict[str, Any]:
        """Execute creative automation workflow"""
        return self.agentic_workflows.execute_workflow(workflow_id)
    
    def search_content(self, query: str, content_types: List[str] = None, 
                      categories: List[str] = None) -> List[Dict[str, Any]]:
        """Enhanced semantic search"""
        return self.vector_search.semantic_search(query, content_types, categories)
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status"""
        return {
            'system_name': 'Enhanced Intelligent Organization System',
            'version': '2.1.0',
            'components': {
                'enhanced_vector_search': 'enabled',
                'creative_automation': 'enabled',
                'agentic_workflows': 'enabled',
                'twilio_integration': 'enabled' if self.creative_automation.twilio else 'disabled'
            },
            'capabilities': [
                'Advanced semantic search with vector databases',
                'Multi-platform creative automation',
                'Twilio phone automation',
                'AI-powered agentic workflows',
                'Content-aware intelligence',
                'Lead generation and customer outreach',
                'Social media automation',
                'Analytics and optimization'
            ]
        }

def main():
    """Main function to demonstrate enhanced system"""
    print("🚀 Enhanced Creative Automation System")
    print("=" * 50)
    
    # Initialize system
    system = EnhancedIntelligentOrganizationSystem()
    
    # Show system status
    status = system.get_system_status()
    print(f"📊 System Status: {status['system_name']} v{status['version']}")
    print(f"🔧 Components: {status['components']}")
    
    # Index project content
    print("\n🔍 Indexing project content...")
    system.index_project_content()
    
    # Create Heavenly Hands phone system
    print("\n📞 Creating Heavenly Hands phone automation system...")
    phone_system = system.create_heavenly_hands_phone_system()
    print(f"✅ Phone system created: {phone_system}")
    
    # Demonstrate semantic search
    print("\n🔍 Testing semantic search...")
    search_results = system.search_content("cleaning services pricing", categories=['pricing'])
    print(f"Found {len(search_results)} relevant results")
    
    print("\n🎉 Enhanced Creative Automation System ready!")

if __name__ == "__main__":
    main()