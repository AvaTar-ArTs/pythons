#!/usr/bin/env python3
"""
🎮 Gamification Engine - User Engagement System
Comprehensive gamification system for user retention
"""

import os
import json
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
import logging
import random

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class Achievement:
    """Achievement data structure"""
    id: str
    name: str
    description: str
    category: str
    points: int
    requirements: Dict
    icon: str
    rarity: str  # common, rare, epic, legendary

@dataclass
class Challenge:
    """Challenge data structure"""
    id: str
    title: str
    description: str
    challenge_type: str
    difficulty: str
    points_reward: int
    requirements: Dict
    duration_hours: int
    is_active: bool

@dataclass
class UserProgress:
    """User progress tracking"""
    user_id: str
    total_points: int
    level: int
    current_xp: int
    next_level_xp: int
    achievements: List[str]
    challenges_completed: List[str]
    streak_days: int
    last_activity: datetime

class GamificationEngine:
    """Main gamification engine"""
    
    def __init__(self, db_path: str = None):
        self.db_path = db_path or "/Users/steven/ai-sites/retention-products-suite/engagement-tools/gamification.db"
        self.setup_database()
        self.achievements = self._initialize_achievements()
        self.challenges = self._initialize_challenges()
        
    def setup_database(self):
        """Set up gamification database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                username TEXT,
                email TEXT,
                total_points INTEGER DEFAULT 0,
                level INTEGER DEFAULT 1,
                current_xp INTEGER DEFAULT 0,
                streak_days INTEGER DEFAULT 0,
                last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Achievements table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS achievements (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT,
                category TEXT,
                points INTEGER DEFAULT 0,
                requirements TEXT,
                icon TEXT,
                rarity TEXT DEFAULT 'common'
            )
        """)
        
        # User achievements
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_achievements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                achievement_id TEXT,
                unlocked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id),
                FOREIGN KEY (achievement_id) REFERENCES achievements (id)
            )
        """)
        
        # Challenges table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS challenges (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                description TEXT,
                challenge_type TEXT,
                difficulty TEXT DEFAULT 'easy',
                points_reward INTEGER DEFAULT 10,
                requirements TEXT,
                duration_hours INTEGER DEFAULT 24,
                is_active BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # User challenges
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_challenges (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                challenge_id TEXT,
                status TEXT DEFAULT 'active',
                started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                completed_at TIMESTAMP,
                progress INTEGER DEFAULT 0,
                FOREIGN KEY (user_id) REFERENCES users (id),
                FOREIGN KEY (challenge_id) REFERENCES challenges (id)
            )
        """)
        
        # User actions (for tracking)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_actions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                action_type TEXT NOT NULL,
                action_value INTEGER DEFAULT 1,
                points_earned INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        """)
        
        # Leaderboards
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS leaderboards (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                leaderboard_type TEXT NOT NULL,
                user_id TEXT,
                score INTEGER DEFAULT 0,
                rank INTEGER,
                period TEXT DEFAULT 'all_time',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        """)
        
        conn.commit()
        conn.close()
        
    def _initialize_achievements(self) -> List[Achievement]:
        """Initialize predefined achievements"""
        return [
            # Content Creation Achievements
            Achievement(
                id="first_content",
                name="First Steps",
                description="Create your first piece of content",
                category="content_creation",
                points=10,
                requirements={"content_created": 1},
                icon="🎨",
                rarity="common"
            ),
            Achievement(
                id="content_master",
                name="Content Master",
                description="Create 100 pieces of content",
                category="content_creation",
                points=500,
                requirements={"content_created": 100},
                icon="👑",
                rarity="legendary"
            ),
            Achievement(
                id="daily_creator",
                name="Daily Creator",
                description="Create content for 7 consecutive days",
                category="content_creation",
                points=100,
                requirements={"daily_streak": 7},
                icon="🔥",
                rarity="rare"
            ),
            
            # Social Achievements
            Achievement(
                id="social_butterfly",
                name="Social Butterfly",
                description="Share 50 pieces of content",
                category="social",
                points=200,
                requirements={"content_shared": 50},
                icon="🦋",
                rarity="epic"
            ),
            Achievement(
                id="community_hero",
                name="Community Hero",
                description="Help 25 other users",
                category="social",
                points=300,
                requirements={"users_helped": 25},
                icon="🦸",
                rarity="epic"
            ),
            
            # Learning Achievements
            Achievement(
                id="knowledge_seeker",
                name="Knowledge Seeker",
                category="learning",
                description="Complete 10 courses",
                points=150,
                requirements={"courses_completed": 10},
                icon="📚",
                rarity="rare"
            ),
            Achievement(
                id="skill_master",
                name="Skill Master",
                description="Master 5 different skills",
                category="learning",
                points=400,
                requirements={"skills_mastered": 5},
                icon="🎯",
                rarity="legendary"
            ),
            
            # Engagement Achievements
            Achievement(
                id="early_bird",
                name="Early Bird",
                description="Login for 30 consecutive days",
                category="engagement",
                points=250,
                requirements={"login_streak": 30},
                icon="🐦",
                rarity="epic"
            ),
            Achievement(
                id="night_owl",
                name="Night Owl",
                description="Be active during late hours for 7 days",
                category="engagement",
                points=100,
                requirements={"late_night_sessions": 7},
                icon="🦉",
                rarity="rare"
            )
        ]
    
    def _initialize_challenges(self) -> List[Challenge]:
        """Initialize predefined challenges"""
        return [
            # Daily Challenges
            Challenge(
                id="daily_content",
                title="Daily Content Creator",
                description="Create at least one piece of content today",
                challenge_type="daily",
                difficulty="easy",
                points_reward=20,
                requirements={"content_created": 1},
                duration_hours=24,
                is_active=True
            ),
            Challenge(
                id="daily_share",
                title="Social Sharer",
                description="Share your content on social media",
                challenge_type="daily",
                difficulty="easy",
                points_reward=15,
                requirements={"content_shared": 1},
                duration_hours=24,
                is_active=True
            ),
            
            # Weekly Challenges
            Challenge(
                id="weekly_creator",
                title="Weekly Creator",
                description="Create 10 pieces of content this week",
                challenge_type="weekly",
                difficulty="medium",
                points_reward=100,
                requirements={"content_created": 10},
                duration_hours=168,
                is_active=True
            ),
            Challenge(
                id="weekly_learner",
                title="Weekly Learner",
                description="Complete 3 courses this week",
                challenge_type="weekly",
                difficulty="medium",
                points_reward=150,
                requirements={"courses_completed": 3},
                duration_hours=168,
                is_active=True
            ),
            
            # Monthly Challenges
            Challenge(
                id="monthly_master",
                title="Monthly Master",
                description="Create 50 pieces of content this month",
                challenge_type="monthly",
                difficulty="hard",
                points_reward=500,
                requirements={"content_created": 50},
                duration_hours=720,
                is_active=True
            ),
            Challenge(
                id="monthly_mentor",
                title="Monthly Mentor",
                description="Help 10 other users this month",
                challenge_type="monthly",
                difficulty="hard",
                points_reward=400,
                requirements={"users_helped": 10},
                duration_hours=720,
                is_active=True
            )
        ]
    
    def register_user(self, user_id: str, username: str = None, email: str = None) -> bool:
        """Register a new user in the gamification system"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT OR IGNORE INTO users (id, username, email)
                VALUES (?, ?, ?)
            """, (user_id, username, email))
            
            conn.commit()
            return True
        except Exception as e:
            logger.error(f"Error registering user {user_id}: {e}")
            return False
        finally:
            conn.close()
    
    def track_action(self, user_id: str, action_type: str, action_value: int = 1) -> Dict:
        """Track user action and award points"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Calculate points for action
        points_earned = self._calculate_points(action_type, action_value)
        
        # Record action
        cursor.execute("""
            INSERT INTO user_actions (user_id, action_type, action_value, points_earned)
            VALUES (?, ?, ?, ?)
        """, (user_id, action_type, action_value, points_earned))
        
        # Update user points and level
        cursor.execute("""
            UPDATE users 
            SET total_points = total_points + ?, 
                current_xp = current_xp + ?,
                last_activity = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (points_earned, points_earned, user_id))
        
        # Check for level up
        level_up = self._check_level_up(user_id)
        
        # Check for new achievements
        new_achievements = self._check_achievements(user_id)
        
        # Update streak
        self._update_streak(user_id)
        
        conn.commit()
        conn.close()
        
        return {
            'points_earned': points_earned,
            'level_up': level_up,
            'new_achievements': new_achievements
        }
    
    def _calculate_points(self, action_type: str, action_value: int) -> int:
        """Calculate points for different actions"""
        point_values = {
            'content_created': 10,
            'content_shared': 5,
            'course_completed': 25,
            'user_helped': 15,
            'login': 1,
            'challenge_completed': 50,
            'social_interaction': 3,
            'feedback_given': 5
        }
        
        base_points = point_values.get(action_type, 1)
        return base_points * action_value
    
    def _check_level_up(self, user_id: str) -> bool:
        """Check if user should level up"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT level, current_xp FROM users WHERE id = ?", (user_id,))
        user = cursor.fetchone()
        
        if not user:
            conn.close()
            return False
        
        current_level, current_xp = user
        next_level_xp = self._calculate_level_xp(current_level + 1)
        
        if current_xp >= next_level_xp:
            # Level up!
            cursor.execute("""
                UPDATE users 
                SET level = level + 1, current_xp = current_xp - ?
                WHERE id = ?
            """, (next_level_xp, user_id))
            
            conn.commit()
            conn.close()
            return True
        
        conn.close()
        return False
    
    def _calculate_level_xp(self, level: int) -> int:
        """Calculate XP required for a level"""
        return level * 100 + (level - 1) * 50
    
    def _check_achievements(self, user_id: str) -> List[str]:
        """Check for new achievements"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        new_achievements = []
        
        for achievement in self.achievements:
            # Check if user already has this achievement
            cursor.execute("""
                SELECT id FROM user_achievements 
                WHERE user_id = ? AND achievement_id = ?
            """, (user_id, achievement.id))
            
            if cursor.fetchone():
                continue
            
            # Check if requirements are met
            if self._check_achievement_requirements(user_id, achievement.requirements):
                # Award achievement
                cursor.execute("""
                    INSERT INTO user_achievements (user_id, achievement_id)
                    VALUES (?, ?)
                """, (user_id, achievement.id))
                
                # Add points
                cursor.execute("""
                    UPDATE users 
                    SET total_points = total_points + ?
                    WHERE id = ?
                """, (achievement.points, user_id))
                
                new_achievements.append(achievement.name)
        
        conn.commit()
        conn.close()
        
        return new_achievements
    
    def _check_achievement_requirements(self, user_id: str, requirements: Dict) -> bool:
        """Check if achievement requirements are met"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for requirement, target_value in requirements.items():
            if requirement == "content_created":
                cursor.execute("""
                    SELECT COUNT(*) FROM user_actions 
                    WHERE user_id = ? AND action_type = 'content_created'
                """, (user_id,))
                count = cursor.fetchone()[0]
                if count < target_value:
                    conn.close()
                    return False
            
            elif requirement == "daily_streak":
                cursor.execute("""
                    SELECT streak_days FROM users WHERE id = ?
                """, (user_id,))
                streak = cursor.fetchone()[0]
                if streak < target_value:
                    conn.close()
                    return False
            
            # Add more requirement checks as needed
        
        conn.close()
        return True
    
    def _update_streak(self, user_id: str):
        """Update user streak"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT last_activity FROM users WHERE id = ?
        """, (user_id,))
        
        last_activity = cursor.fetchone()[0]
        if last_activity:
            last_activity = datetime.fromisoformat(last_activity)
            today = datetime.now().date()
            last_activity_date = last_activity.date()
            
            if last_activity_date == today:
                # Already updated today
                conn.close()
                return
            elif last_activity_date == today - timedelta(days=1):
                # Consecutive day
                cursor.execute("""
                    UPDATE users SET streak_days = streak_days + 1
                    WHERE id = ?
                """, (user_id,))
            else:
                # Streak broken
                cursor.execute("""
                    UPDATE users SET streak_days = 1
                    WHERE id = ?
                """, (user_id,))
        
        conn.commit()
        conn.close()
    
    def get_user_progress(self, user_id: str) -> UserProgress:
        """Get user progress information"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT total_points, level, current_xp, streak_days, last_activity
            FROM users WHERE id = ?
        """, (user_id,))
        
        user = cursor.fetchone()
        if not user:
            conn.close()
            return None
        
        total_points, level, current_xp, streak_days, last_activity = user
        next_level_xp = self._calculate_level_xp(level + 1)
        
        # Get achievements
        cursor.execute("""
            SELECT a.name FROM user_achievements ua
            JOIN achievements a ON ua.achievement_id = a.id
            WHERE ua.user_id = ?
        """, (user_id,))
        achievements = [row[0] for row in cursor.fetchall()]
        
        # Get completed challenges
        cursor.execute("""
            SELECT c.title FROM user_challenges uc
            JOIN challenges c ON uc.challenge_id = c.id
            WHERE uc.user_id = ? AND uc.status = 'completed'
        """, (user_id,))
        challenges_completed = [row[0] for row in cursor.fetchall()]
        
        conn.close()
        
        return UserProgress(
            user_id=user_id,
            total_points=total_points,
            level=level,
            current_xp=current_xp,
            next_level_xp=next_level_xp,
            achievements=achievements,
            challenges_completed=challenges_completed,
            streak_days=streak_days,
            last_activity=datetime.fromisoformat(last_activity) if last_activity else datetime.now()
        )
    
    def get_leaderboard(self, leaderboard_type: str = "points", limit: int = 50) -> List[Dict]:
        """Get leaderboard"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if leaderboard_type == "points":
            cursor.execute("""
                SELECT username, total_points, level, streak_days
                FROM users
                ORDER BY total_points DESC
                LIMIT ?
            """, (limit,))
        elif leaderboard_type == "streak":
            cursor.execute("""
                SELECT username, streak_days, total_points, level
                FROM users
                ORDER BY streak_days DESC
                LIMIT ?
            """, (limit,))
        
        leaderboard = cursor.fetchall()
        conn.close()
        
        return [{
            'username': user[0] or f"User {user[0][:8]}",
            'points': user[1],
            'level': user[2],
            'streak': user[3]
        } for user in leaderboard]
    
    def get_available_challenges(self, user_id: str) -> List[Challenge]:
        """Get available challenges for user"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get challenges user hasn't completed
        cursor.execute("""
            SELECT c.* FROM challenges c
            LEFT JOIN user_challenges uc ON c.id = uc.challenge_id AND uc.user_id = ?
            WHERE c.is_active = 1 AND (uc.id IS NULL OR uc.status != 'completed')
            ORDER BY c.difficulty, c.points_reward DESC
        """, (user_id,))
        
        challenges = cursor.fetchall()
        conn.close()
        
        return [Challenge(
            id=challenge[0],
            title=challenge[1],
            description=challenge[2],
            challenge_type=challenge[3],
            difficulty=challenge[4],
            points_reward=challenge[5],
            requirements=json.loads(challenge[6]) if challenge[6] else {},
            duration_hours=challenge[7],
            is_active=bool(challenge[8])
        ) for challenge in challenges]
    
    def start_challenge(self, user_id: str, challenge_id: str) -> bool:
        """Start a challenge for user"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO user_challenges (user_id, challenge_id, status)
                VALUES (?, ?, 'active')
            """, (user_id, challenge_id))
            
            conn.commit()
            return True
        except Exception as e:
            logger.error(f"Error starting challenge {challenge_id} for user {user_id}: {e}")
            return False
        finally:
            conn.close()
    
    def complete_challenge(self, user_id: str, challenge_id: str) -> bool:
        """Complete a challenge for user"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Get challenge points
            cursor.execute("""
                SELECT points_reward FROM challenges WHERE id = ?
            """, (challenge_id,))
            challenge = cursor.fetchone()
            
            if not challenge:
                return False
            
            points_reward = challenge[0]
            
            # Update challenge status
            cursor.execute("""
                UPDATE user_challenges 
                SET status = 'completed', completed_at = CURRENT_TIMESTAMP
                WHERE user_id = ? AND challenge_id = ?
            """, (user_id, challenge_id))
            
            # Award points
            cursor.execute("""
                UPDATE users 
                SET total_points = total_points + ?
                WHERE id = ?
            """, (points_reward, user_id))
            
            conn.commit()
            return True
        except Exception as e:
            logger.error(f"Error completing challenge {challenge_id} for user {user_id}: {e}")
            return False
        finally:
            conn.close()

def main():
    """Main function to test gamification engine"""
    engine = GamificationEngine()
    
    print("🎮 Gamification Engine - User Engagement System")
    print("=" * 50)
    
    # Test user registration
    test_user = "test_user_123"
    engine.register_user(test_user, "TestUser", "test@example.com")
    print(f"✅ User {test_user} registered")
    
    # Test action tracking
    result = engine.track_action(test_user, "content_created", 1)
    print(f"✅ Action tracked: {result['points_earned']} points earned")
    
    # Test progress
    progress = engine.get_user_progress(test_user)
    print(f"✅ User progress: Level {progress.level}, {progress.total_points} points")
    
    # Test leaderboard
    leaderboard = engine.get_leaderboard()
    print(f"✅ Leaderboard generated with {len(leaderboard)} users")
    
    print("\n🎉 Gamification engine is ready!")

if __name__ == "__main__":
    main()