#!/usr/bin/env python3
"""
AI Course Creator - Automated course generation using AI
Creates comprehensive courses with content, assessments, and certificates
"""

import os
import json
import sqlite3
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from datetime import datetime
import logging
import openai

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class CourseModule:
    """Course module structure"""
    id: str
    title: str
    description: str
    content: str
    duration: int  # minutes
    difficulty: str
    learning_objectives: List[str]
    resources: List[str]
    assessments: List[str]

@dataclass
class Course:
    """Course structure"""
    id: str
    title: str
    description: str
    instructor: str
    level: str
    duration: int  # total hours
    modules: List[CourseModule]
    prerequisites: List[str]
    learning_outcomes: List[str]
    certification: bool
    price: float
    created_at: str
    updated_at: str

class AICourseCreator:
    """AI-powered course creation system"""
    
    def __init__(self, db_path: str = "databases/courses.db"):
        self.db_path = db_path
        self.openai_client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self._init_database()
        
    def _init_database(self):
        """Initialize course database"""
        try:
            os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Courses table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS courses (
                    id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    description TEXT,
                    instructor TEXT,
                    level TEXT,
                    duration INTEGER,
                    modules TEXT,
                    prerequisites TEXT,
                    learning_outcomes TEXT,
                    certification BOOLEAN,
                    price REAL,
                    created_at TEXT,
                    updated_at TEXT
                )
            ''')
            
            # Course modules table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS course_modules (
                    id TEXT PRIMARY KEY,
                    course_id TEXT,
                    title TEXT,
                    description TEXT,
                    content TEXT,
                    duration INTEGER,
                    difficulty TEXT,
                    learning_objectives TEXT,
                    resources TEXT,
                    assessments TEXT,
                    created_at TEXT
                )
            ''')
            
            conn.commit()
            conn.close()
            logger.info("Course database initialized")
            
        except Exception as e:
            logger.error(f"Database initialization failed: {e}")
            raise
    
    def generate_course(self, 
                       topic: str, 
                       level: str = "beginner",
                       duration_hours: int = 10,
                       instructor: str = "AI Instructor") -> Course:
        """Generate a complete course using AI"""
        try:
            # Generate course outline
            course_outline = self._generate_course_outline(topic, level, duration_hours)
            
            # Create course ID
            course_id = f"course_{topic.lower().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # Generate modules
            modules = []
            for i, module_outline in enumerate(course_outline["modules"]):
                module = self._generate_course_module(
                    course_id=course_id,
                    module_index=i + 1,
                    module_outline=module_outline,
                    level=level
                )
                modules.append(module)
            
            # Create course
            course = Course(
                id=course_id,
                title=course_outline["title"],
                description=course_outline["description"],
                instructor=instructor,
                level=level,
                duration=duration_hours,
                modules=modules,
                prerequisites=course_outline["prerequisites"],
                learning_outcomes=course_outline["learning_outcomes"],
                certification=True,
                price=self._calculate_course_price(level, duration_hours),
                created_at=datetime.now().isoformat(),
                updated_at=datetime.now().isoformat()
            )
            
            # Save course to database
            self._save_course(course)
            
            return course
            
        except Exception as e:
            logger.error(f"Course generation failed: {e}")
            return None
    
    def _generate_course_outline(self, topic: str, level: str, duration_hours: int) -> Dict[str, Any]:
        """Generate course outline using AI"""
        try:
            prompt = f"""
            Create a comprehensive course outline for a {level} level course on "{topic}".
            The course should be {duration_hours} hours long.
            
            Please provide:
            1. Course title
            2. Course description (2-3 paragraphs)
            3. Prerequisites (list of required knowledge/skills)
            4. Learning outcomes (what students will learn)
            5. Module breakdown (5-10 modules with titles and brief descriptions)
            
            Format as JSON with the following structure:
            {{
                "title": "Course Title",
                "description": "Course description...",
                "prerequisites": ["prerequisite1", "prerequisite2"],
                "learning_outcomes": ["outcome1", "outcome2"],
                "modules": [
                    {{
                        "title": "Module Title",
                        "description": "Module description",
                        "duration": 60,
                        "topics": ["topic1", "topic2"]
                    }}
                ]
            }}
            """
            
            response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert course designer and educator."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )
            
            content = response.choices[0].message.content
            return json.loads(content)
            
        except Exception as e:
            logger.error(f"Course outline generation failed: {e}")
            return self._create_default_outline(topic, level, duration_hours)
    
    def _generate_course_module(self, 
                               course_id: str, 
                               module_index: int, 
                               module_outline: Dict[str, Any],
                               level: str) -> CourseModule:
        """Generate detailed course module content"""
        try:
            prompt = f"""
            Create detailed content for a course module titled "{module_outline['title']}".
            Level: {level}
            Duration: {module_outline['duration']} minutes
            Topics: {', '.join(module_outline['topics'])}
            
            Please provide:
            1. Detailed module description
            2. Comprehensive content (2000+ words)
            3. Learning objectives (3-5 objectives)
            4. Required resources (books, articles, tools)
            5. Assessment questions (5-10 questions)
            
            Format as JSON:
            {{
                "description": "Module description...",
                "content": "Detailed content...",
                "learning_objectives": ["objective1", "objective2"],
                "resources": ["resource1", "resource2"],
                "assessments": ["question1", "question2"]
            }}
            """
            
            response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert educator creating detailed course content."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )
            
            content = response.choices[0].message.content
            module_data = json.loads(content)
            
            return CourseModule(
                id=f"{course_id}_module_{module_index}",
                title=module_outline["title"],
                description=module_data["description"],
                content=module_data["content"],
                duration=module_outline["duration"],
                difficulty=level,
                learning_objectives=module_data["learning_objectives"],
                resources=module_data["resources"],
                assessments=module_data["assessments"]
            )
            
        except Exception as e:
            logger.error(f"Module generation failed: {e}")
            return self._create_default_module(course_id, module_index, module_outline, level)
    
    def _calculate_course_price(self, level: str, duration_hours: int) -> float:
        """Calculate course price based on level and duration"""
        base_prices = {
            "beginner": 50.0,
            "intermediate": 75.0,
            "advanced": 100.0,
            "expert": 150.0
        }
        
        base_price = base_prices.get(level, 75.0)
        duration_multiplier = duration_hours / 10.0  # 10 hours as baseline
        
        return base_price * duration_multiplier
    
    def _save_course(self, course: Course):
        """Save course to database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Save course
            cursor.execute('''
                INSERT OR REPLACE INTO courses 
                (id, title, description, instructor, level, duration, modules, 
                 prerequisites, learning_outcomes, certification, price, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                course.id,
                course.title,
                course.description,
                course.instructor,
                course.level,
                course.duration,
                json.dumps([module.__dict__ for module in course.modules]),
                json.dumps(course.prerequisites),
                json.dumps(course.learning_outcomes),
                course.certification,
                course.price,
                course.created_at,
                course.updated_at
            ))
            
            # Save modules
            for module in course.modules:
                cursor.execute('''
                    INSERT OR REPLACE INTO course_modules 
                    (id, course_id, title, description, content, duration, difficulty, 
                     learning_objectives, resources, assessments, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    module.id,
                    course.id,
                    module.title,
                    module.description,
                    module.content,
                    module.duration,
                    module.difficulty,
                    json.dumps(module.learning_objectives),
                    json.dumps(module.resources),
                    json.dumps(module.assessments),
                    datetime.now().isoformat()
                ))
            
            conn.commit()
            conn.close()
            logger.info(f"Course {course.id} saved to database")
            
        except Exception as e:
            logger.error(f"Failed to save course: {e}")
    
    def _create_default_outline(self, topic: str, level: str, duration_hours: int) -> Dict[str, Any]:
        """Create default course outline if AI generation fails"""
        return {
            "title": f"Introduction to {topic}",
            "description": f"A comprehensive {level} level course covering the fundamentals of {topic}.",
            "prerequisites": ["Basic computer skills", "Internet access"],
            "learning_outcomes": [
                f"Understand the basics of {topic}",
                f"Apply {topic} concepts in practical scenarios",
                f"Develop skills in {topic} implementation"
            ],
            "modules": [
                {
                    "title": f"Introduction to {topic}",
                    "description": f"Overview of {topic} concepts",
                    "duration": 60,
                    "topics": ["basics", "fundamentals"]
                }
            ]
        }
    
    def _create_default_module(self, course_id: str, module_index: int, 
                              module_outline: Dict[str, Any], level: str) -> CourseModule:
        """Create default module if AI generation fails"""
        return CourseModule(
            id=f"{course_id}_module_{module_index}",
            title=module_outline["title"],
            description=module_outline["description"],
            content="Module content will be generated...",
            duration=module_outline["duration"],
            difficulty=level,
            learning_objectives=["Learn the fundamentals"],
            resources=["Course materials"],
            assessments=["Module quiz"]
        )
    
    def get_course(self, course_id: str) -> Optional[Course]:
        """Get course by ID"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM courses WHERE id = ?', (course_id,))
            row = cursor.fetchone()
            
            if row:
                # Reconstruct course object
                course = Course(
                    id=row[0],
                    title=row[1],
                    description=row[2],
                    instructor=row[3],
                    level=row[4],
                    duration=row[5],
                    modules=[],  # Would load from modules table
                    prerequisites=json.loads(row[7]),
                    learning_outcomes=json.loads(row[8]),
                    certification=bool(row[9]),
                    price=row[10],
                    created_at=row[11],
                    updated_at=row[12]
                )
                return course
            
            conn.close()
            return None
            
        except Exception as e:
            logger.error(f"Failed to get course: {e}")
            return None
    
    def list_courses(self) -> List[Dict[str, Any]]:
        """List all courses"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id, title, description, instructor, level, duration, 
                       certification, price, created_at
                FROM courses
                ORDER BY created_at DESC
            ''')
            
            courses = []
            for row in cursor.fetchall():
                courses.append({
                    "id": row[0],
                    "title": row[1],
                    "description": row[2],
                    "instructor": row[3],
                    "level": row[4],
                    "duration": row[5],
                    "certification": row[6],
                    "price": row[7],
                    "created_at": row[8]
                })
            
            conn.close()
            return courses
            
        except Exception as e:
            logger.error(f"Failed to list courses: {e}")
            return []

# Example usage
def main():
    """Example usage of AI Course Creator"""
    creator = AICourseCreator()
    
    # Generate a course
    course = creator.generate_course(
        topic="AI Content Creation",
        level="intermediate",
        duration_hours=15,
        instructor="AI Education System"
    )
    
    if course:
        print(f"Generated course: {course.title}")
        print(f"Duration: {course.duration} hours")
        print(f"Modules: {len(course.modules)}")
        print(f"Price: ${course.price}")
        
        # List all courses
        courses = creator.list_courses()
        print(f"\nTotal courses: {len(courses)}")

if __name__ == "__main__":
    main()