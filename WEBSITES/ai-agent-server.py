#!/usr/bin/env python3
"""
AI Agent Server - Enhanced with ~/.env.d Integration
===================================================
Intelligent AI orchestration server with modular environment loading
"""

import os
import json
import logging
import time
import threading
import requests
from datetime import datetime
from flask import Flask, request, jsonify
from pathlib import Path
import subprocess
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
import hashlib
import re
from collections import Counter

# Load environment from ~/.env.d
def load_env_d():
    """Load environment variables from ~/.env.d"""
    try:
        # Use the environment loader
        from env_loader import AIAgentEnvLoader
        loader = AIAgentEnvLoader()
        result = loader.load_all_categories()
        
        # Set environment variables
        for key, value in result['loaded_vars'].items():
            os.environ[key] = value
        
        logging.info(f"✅ Loaded {result['total_vars']} variables from {len(result['loaded_categories'])} categories")
        return True
    except Exception as e:
        logging.warning(f"⚠️  Failed to load from ~/.env.d: {e}")
        return False

# Try to load from ~/.env.d first
if not load_env_d():
    # Fallback to env_d_loader
    try:
        from env_d_loader import load_dotenv
        load_dotenv()
        logging.info("✅ Loaded environment using env_d_loader")
    except ImportError:
        logging.warning("⚠️  No environment loader available")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Flask app
app = Flask(__name__)

@dataclass
class WorkflowStep:
    """Represents a single step in a workflow"""
    step_id: str
    step_type: str
    parameters: Dict[str, Any]
    dependencies: List[str] = field(default_factory=list)
    status: str = "pending"
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    execution_time: float = 0.0

@dataclass
class WorkflowExecution:
    """Represents a complete workflow execution"""
    workflow_id: str
    request_data: Dict[str, Any]
    steps: List[WorkflowStep]
    status: str = "pending"
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    total_execution_time: float = 0.0
    quality_score: float = 0.0
    cost: float = 0.0

class AIAgent:
    """Enhanced AI Agent with ~/.env.d integration"""
    
    def __init__(self):
        self.active_workflows = {}
        self.workflow_history = []
        self.knowledge_base = self._load_knowledge_base()
        self.api_services = self._initialize_api_services()
        
    def _load_knowledge_base(self) -> Dict[str, Any]:
        """Load the agent's knowledge base"""
        kb_file = Path("/app/data/knowledge_base.json")
        if kb_file.exists():
            with open(kb_file, 'r') as f:
                return json.load(f)
        return {
            "content_patterns": {},
            "workflow_templates": {},
            "quality_metrics": {},
            "cost_tracking": {},
            "last_updated": None
        }
    
    def _save_knowledge_base(self):
        """Save the agent's knowledge base"""
        kb_file = Path("/app/data/knowledge_base.json")
        kb_file.parent.mkdir(parents=True, exist_ok=True)
        
        self.knowledge_base["last_updated"] = datetime.now().isoformat()
        with open(kb_file, 'w') as f:
            json.dump(self.knowledge_base, f, indent=2)
    
    def _initialize_api_services(self) -> Dict[str, bool]:
        """Check which API services are available"""
        services = {}
        
        # Core LLM APIs
        services['openai'] = bool(os.getenv('OPENAI_API_KEY'))
        services['anthropic'] = bool(os.getenv('ANTHROPIC_API_KEY'))
        services['groq'] = bool(os.getenv('GROQ_API_KEY'))
        services['xai'] = bool(os.getenv('XAI_API_KEY'))
        services['deepseek'] = bool(os.getenv('DEEPSEEK_API_KEY'))
        
        # Audio & Music APIs
        services['elevenlabs'] = bool(os.getenv('ELEVENLABS_API_KEY'))
        services['suno'] = bool(os.getenv('SUNO_COOKIE'))
        services['assemblyai'] = bool(os.getenv('ASSEMBLYAI_API_KEY'))
        services['deepgram'] = bool(os.getenv('DEEPGRAM_API_KEY'))
        
        # Art & Vision APIs
        services['stability'] = bool(os.getenv('STABILITY_API_KEY'))
        services['replicate'] = bool(os.getenv('REPLICATE_API_TOKEN'))
        services['runway'] = bool(os.getenv('RUNWAY_API_KEY'))
        services['leonardo'] = bool(os.getenv('LEONARDO_API_KEY'))
        
        # Automation & Agents APIs
        services['pinecone'] = bool(os.getenv('PINECONE_API_KEY'))
        services['openrouter'] = bool(os.getenv('OPENROUTER_API_KEY'))
        services['cohere'] = bool(os.getenv('COHERE_API_KEY'))
        services['fireworks'] = bool(os.getenv('FIREWORKS_API_KEY'))
        services['langsmith'] = bool(os.getenv('LANGSMITH_API_KEY'))
        
        # Documents & Knowledge APIs
        services['notion'] = bool(os.getenv('NOTION_TOKEN'))
        
        # SEO & Analytics APIs
        services['serpapi'] = bool(os.getenv('SERPAPI_KEY'))
        services['newsapi'] = bool(os.getenv('NEWSAPI_KEY'))
        
        return services
    
    def analyze_request(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze incoming request and determine requirements"""
        logger.info("🔍 Analyzing request...")
        
        # Extract key information
        content_type = request_data.get('content_type', 'text')
        requirements = request_data.get('requirements', {})
        target_audience = request_data.get('target_audience', 'general')
        tone = request_data.get('tone', 'professional')
        length = request_data.get('length', 'medium')
        
        # Determine complexity
        complexity = self._assess_complexity(request_data)
        
        # Check available services
        available_services = [k for k, v in self.api_services.items() if v]
        
        analysis = {
            "content_type": content_type,
            "complexity": complexity,
            "estimated_steps": self._estimate_steps(content_type, complexity),
            "required_services": self._get_required_services(content_type),
            "available_services": available_services,
            "can_fulfill": self._can_fulfill_request(content_type, available_services),
            "estimated_cost": self._estimate_cost(content_type, complexity),
            "estimated_time": self._estimate_time(content_type, complexity),
            "quality_expectations": self._get_quality_expectations(content_type, complexity)
        }
        
        logger.info(f"✅ Request analyzed: {analysis['content_type']} ({analysis['complexity']} complexity)")
        return analysis
    
    def plan_workflow(self, analysis: Dict[str, Any]) -> List[WorkflowStep]:
        """Plan the workflow steps based on analysis"""
        logger.info("📋 Planning workflow...")
        
        steps = []
        step_id = 1
        
        # Research phase
        if analysis['content_type'] in ['blog_post', 'article', 'research']:
            steps.append(WorkflowStep(
                step_id=f"step_{step_id}",
                step_type="research",
                parameters={
                    "query": analysis.get('topic', ''),
                    "sources": ["serpapi", "newsapi"],
                    "depth": "comprehensive"
                }
            ))
            step_id += 1
        
        # Content generation phase
        steps.append(WorkflowStep(
            step_id=f"step_{step_id}",
            step_type="content_generation",
            parameters={
                "content_type": analysis['content_type'],
                "tone": analysis.get('tone', 'professional'),
                "length": analysis.get('length', 'medium'),
                "target_audience": analysis.get('target_audience', 'general'),
                "model": self._select_best_model(analysis['content_type'])
            }
        ))
        step_id += 1
        
        # Quality control phase
        steps.append(WorkflowStep(
            step_id=f"step_{step_id}",
            step_type="quality_control",
            parameters={
                "quality_threshold": 0.8,
                "check_grammar": True,
                "check_tone": True,
                "check_facts": True
            }
        ))
        step_id += 1
        
        # Enhancement phase (if needed)
        if analysis['complexity'] == 'high':
            steps.append(WorkflowStep(
                step_id=f"step_{step_id}",
                step_type="enhancement",
                parameters={
                    "enhancement_type": "comprehensive",
                    "add_examples": True,
                    "improve_structure": True,
                    "add_visual_elements": True
                }
            ))
            step_id += 1
        
        # Finalization phase
        steps.append(WorkflowStep(
            step_id=f"step_{step_id}",
            step_type="finalization",
            parameters={
                "format": "final",
                "optimize": True,
                "add_metadata": True
            }
        ))
        
        logger.info(f"✅ Workflow planned: {len(steps)} steps")
        return steps
    
    def execute_workflow(self, workflow_id: str, steps: List[WorkflowStep]) -> WorkflowExecution:
        """Execute the planned workflow"""
        logger.info(f"🚀 Executing workflow {workflow_id}...")
        
        execution = WorkflowExecution(
            workflow_id=workflow_id,
            request_data={},
            steps=steps
        )
        
        self.active_workflows[workflow_id] = execution
        
        try:
            for step in steps:
                step.status = "running"
                start_time = time.time()
                
                try:
                    result = self._execute_step(step)
                    step.result = result
                    step.status = "completed"
                    step.execution_time = time.time() - start_time
                    
                    logger.info(f"✅ Step {step.step_id} completed in {step.execution_time:.2f}s")
                    
                except Exception as e:
                    step.error = str(e)
                    step.status = "failed"
                    step.execution_time = time.time() - start_time
                    
                    logger.error(f"❌ Step {step.step_id} failed: {e}")
                    
                    # Try fallback if available
                    if self._has_fallback(step):
                        logger.info(f"🔄 Trying fallback for step {step.step_id}")
                        try:
                            result = self._execute_fallback(step)
                            step.result = result
                            step.status = "completed"
                            step.error = None
                        except Exception as fallback_error:
                            logger.error(f"❌ Fallback also failed: {fallback_error}")
            
            # Calculate final metrics
            execution.status = "completed"
            execution.completed_at = datetime.now()
            execution.total_execution_time = sum(step.execution_time for step in steps)
            execution.quality_score = self._calculate_quality_score(execution)
            execution.cost = self._calculate_cost(execution)
            
            # Update knowledge base
            self._update_knowledge_base(execution)
            
            logger.info(f"🎉 Workflow {workflow_id} completed successfully!")
            
        except Exception as e:
            execution.status = "failed"
            execution.completed_at = datetime.now()
            logger.error(f"❌ Workflow {workflow_id} failed: {e}")
        
        finally:
            # Move to history
            self.workflow_history.append(execution)
            if workflow_id in self.active_workflows:
                del self.active_workflows[workflow_id]
        
        return execution
    
    def _execute_step(self, step: WorkflowStep) -> Dict[str, Any]:
        """Execute a single workflow step"""
        if step.step_type == "research":
            return self._execute_research(step)
        elif step.step_type == "content_generation":
            return self._execute_content_generation(step)
        elif step.step_type == "quality_control":
            return self._execute_quality_control(step)
        elif step.step_type == "enhancement":
            return self._execute_enhancement(step)
        elif step.step_type == "finalization":
            return self._execute_finalization(step)
        else:
            raise ValueError(f"Unknown step type: {step.step_type}")
    
    def _execute_research(self, step: WorkflowStep) -> Dict[str, Any]:
        """Execute research step"""
        query = step.parameters.get('query', '')
        sources = step.parameters.get('sources', [])
        
        research_results = {
            "query": query,
            "sources_used": [],
            "findings": [],
            "credibility_score": 0.0
        }
        
        # Use SERP API if available
        if 'serpapi' in sources and self.api_services.get('serpapi'):
            try:
                serp_results = self._call_serp_api(query)
                research_results["sources_used"].append("serpapi")
                research_results["findings"].extend(serp_results.get('organic_results', []))
            except Exception as e:
                logger.warning(f"SERP API failed: {e}")
        
        # Use News API if available
        if 'newsapi' in sources and self.api_services.get('newsapi'):
            try:
                news_results = self._call_news_api(query)
                research_results["sources_used"].append("newsapi")
                research_results["findings"].extend(news_results.get('articles', []))
            except Exception as e:
                logger.warning(f"News API failed: {e}")
        
        # Calculate credibility score
        research_results["credibility_score"] = self._calculate_credibility_score(research_results["findings"])
        
        return research_results
    
    def _execute_content_generation(self, step: WorkflowStep) -> Dict[str, Any]:
        """Execute content generation step"""
        content_type = step.parameters.get('content_type', 'text')
        model = step.parameters.get('model', 'gpt-4')
        
        # Generate content using the best available model
        if self.api_services.get('openai'):
            return self._call_openai(model, step.parameters)
        elif self.api_services.get('anthropic'):
            return self._call_anthropic(step.parameters)
        elif self.api_services.get('groq'):
            return self._call_groq(step.parameters)
        else:
            raise Exception("No LLM service available")
    
    def _execute_quality_control(self, step: WorkflowStep) -> Dict[str, Any]:
        """Execute quality control step"""
        # This would implement quality checking logic
        return {
            "quality_score": 0.85,
            "issues_found": [],
            "recommendations": [],
            "passed": True
        }
    
    def _execute_enhancement(self, step: WorkflowStep) -> Dict[str, Any]:
        """Execute enhancement step"""
        # This would implement content enhancement logic
        return {
            "enhancements_applied": [],
            "improvement_score": 0.15,
            "enhanced_content": ""
        }
    
    def _execute_finalization(self, step: WorkflowStep) -> Dict[str, Any]:
        """Execute finalization step"""
        # This would implement final formatting and optimization
        return {
            "final_content": "",
            "metadata": {},
            "optimization_applied": True,
            "ready_for_delivery": True
        }
    
    def _call_openai(self, model: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Call OpenAI API"""
        # Implementation would go here
        return {"content": "Generated content", "model": model}
    
    def _call_anthropic(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Call Anthropic API"""
        # Implementation would go here
        return {"content": "Generated content", "model": "claude"}
    
    def _call_groq(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Call Groq API"""
        # Implementation would go here
        return {"content": "Generated content", "model": "groq"}
    
    def _call_serp_api(self, query: str) -> Dict[str, Any]:
        """Call SERP API"""
        # Implementation would go here
        return {"organic_results": []}
    
    def _call_news_api(self, query: str) -> Dict[str, Any]:
        """Call News API"""
        # Implementation would go here
        return {"articles": []}
    
    def _assess_complexity(self, request_data: Dict[str, Any]) -> str:
        """Assess request complexity"""
        # Simple complexity assessment
        if request_data.get('length') == 'long' or request_data.get('requirements', {}).get('research_required'):
            return 'high'
        elif request_data.get('length') == 'medium':
            return 'medium'
        else:
            return 'low'
    
    def _estimate_steps(self, content_type: str, complexity: str) -> int:
        """Estimate number of workflow steps"""
        base_steps = 3  # research, generation, quality control
        if complexity == 'high':
            base_steps += 2  # enhancement, finalization
        return base_steps
    
    def _get_required_services(self, content_type: str) -> List[str]:
        """Get required services for content type"""
        services = ['llm']
        if content_type in ['blog_post', 'article']:
            services.extend(['research', 'quality_control'])
        elif content_type in ['image', 'art']:
            services.extend(['image_generation'])
        elif content_type in ['audio', 'voice']:
            services.extend(['audio_generation'])
        return services
    
    def _can_fulfill_request(self, content_type: str, available_services: List[str]) -> bool:
        """Check if request can be fulfilled with available services"""
        required_services = self._get_required_services(content_type)
        return all(service in available_services for service in required_services)
    
    def _estimate_cost(self, content_type: str, complexity: str) -> float:
        """Estimate cost for request"""
        base_cost = 0.01
        if complexity == 'high':
            base_cost *= 3
        elif complexity == 'medium':
            base_cost *= 2
        return base_cost
    
    def _estimate_time(self, content_type: str, complexity: str) -> int:
        """Estimate time in seconds"""
        base_time = 30
        if complexity == 'high':
            base_time *= 3
        elif complexity == 'medium':
            base_time *= 2
        return base_time
    
    def _get_quality_expectations(self, content_type: str, complexity: str) -> Dict[str, Any]:
        """Get quality expectations"""
        return {
            "min_score": 0.8,
            "check_grammar": True,
            "check_facts": complexity == 'high',
            "check_tone": True
        }
    
    def _select_best_model(self, content_type: str) -> str:
        """Select best model for content type"""
        if self.api_services.get('openai'):
            return 'gpt-4'
        elif self.api_services.get('anthropic'):
            return 'claude-3-sonnet'
        elif self.api_services.get('groq'):
            return 'llama-3-8b'
        else:
            return 'gpt-3.5-turbo'
    
    def _has_fallback(self, step: WorkflowStep) -> bool:
        """Check if step has fallback option"""
        return step.step_type in ['content_generation', 'research']
    
    def _execute_fallback(self, step: WorkflowStep) -> Dict[str, Any]:
        """Execute fallback for step"""
        if step.step_type == 'content_generation':
            # Try different model
            return self._call_openai('gpt-3.5-turbo', step.parameters)
        else:
            raise Exception("No fallback available")
    
    def _calculate_quality_score(self, execution: WorkflowExecution) -> float:
        """Calculate overall quality score"""
        # Simple quality calculation
        return 0.85
    
    def _calculate_cost(self, execution: WorkflowExecution) -> float:
        """Calculate total cost"""
        # Simple cost calculation
        return 0.05
    
    def _calculate_credibility_score(self, findings: List[Dict[str, Any]]) -> float:
        """Calculate credibility score for research findings"""
        if not findings:
            return 0.0
        
        # Simple credibility calculation
        return 0.8
    
    def _update_knowledge_base(self, execution: WorkflowExecution):
        """Update knowledge base with execution results"""
        # Update patterns, costs, quality metrics
        self._save_knowledge_base()

# Initialize AI Agent
ai_agent = AIAgent()

# Flask Routes
@app.route('/ai-agent/analyze', methods=['POST'])
def analyze_request():
    """Analyze incoming request"""
    try:
        request_data = request.get_json()
        analysis = ai_agent.analyze_request(request_data)
        return jsonify({
            "status": "success",
            "analysis": analysis
        })
    except Exception as e:
        logger.error(f"Analysis failed: {e}")
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500

@app.route('/ai-agent/execute', methods=['POST'])
def execute_workflow():
    """Execute AI workflow"""
    try:
        request_data = request.get_json()
        
        # Analyze request
        analysis = ai_agent.analyze_request(request_data)
        
        # Plan workflow
        steps = ai_agent.plan_workflow(analysis)
        
        # Generate workflow ID
        workflow_id = hashlib.md5(f"{request_data}_{datetime.now()}".encode()).hexdigest()[:12]
        
        # Execute workflow
        execution = ai_agent.execute_workflow(workflow_id, steps)
        
        return jsonify({
            "status": "success",
            "workflow_id": workflow_id,
            "execution": {
                "status": execution.status,
                "total_time": execution.total_execution_time,
                "quality_score": execution.quality_score,
                "cost": execution.cost
            }
        })
    except Exception as e:
        logger.error(f"Execution failed: {e}")
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500

@app.route('/ai-agent/status/<workflow_id>', methods=['GET'])
def get_workflow_status(workflow_id):
    """Get workflow status"""
    if workflow_id in ai_agent.active_workflows:
        execution = ai_agent.active_workflows[workflow_id]
        return jsonify({
            "status": "success",
            "workflow_id": workflow_id,
            "execution": {
                "status": execution.status,
                "steps": [
                    {
                        "step_id": step.step_id,
                        "status": step.status,
                        "execution_time": step.execution_time
                    }
                    for step in execution.steps
                ]
            }
        })
    else:
        return jsonify({
            "status": "error",
            "error": "Workflow not found"
        }), 404

@app.route('/ai-agent/services', methods=['GET'])
def get_services():
    """Get available services"""
    return jsonify({
        "status": "success",
        "services": ai_agent.api_services,
        "available_count": sum(ai_agent.api_services.values())
    })

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "services": ai_agent.api_services,
        "active_workflows": len(ai_agent.active_workflows)
    })

if __name__ == '__main__':
    print("🤖 Starting AI Agent Server...")
    print("=" * 40)
    print(f"📊 Available services: {sum(ai_agent.api_services.values())}/{len(ai_agent.api_services)}")
    print(f"🔧 Environment loaded from: ~/.env.d")
    print(f"🌐 Server starting on: http://0.0.0.0:5000")
    print("=" * 40)
    
    app.run(host='0.0.0.0', port=5000, debug=False)