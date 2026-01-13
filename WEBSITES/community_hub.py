#!/usr/bin/env python3
"""
👥 Community Hub - User Engagement Platform
Comprehensive community platform for user retention
"""

import os
import json
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
import logging
import hashlib
import uuid

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class User:
    """User data structure"""
    id: str
    username: str
    email: str
    display_name: str
    bio: str
    avatar_url: str
    join_date: str
    last_active: str
    reputation: int
    level: int
    badges: List[str]
    following: List[str]
    followers: List[str]

@dataclass
class Post:
    """Post data structure"""
    id: str
    user_id: str
    title: str
    content: str
    post_type: str  # discussion, question, showcase, tutorial
    category: str
    tags: List[str]
    likes: int
    comments: int
    views: int
    created_at: str
    updated_at: str
    is_pinned: bool
    is_featured: bool

@dataclass
class Comment:
    """Comment data structure"""
    id: str
    post_id: str
    user_id: str
    content: str
    likes: int
    created_at: str
    parent_id: Optional[str]  # For replies

class CommunityHub:
    """Main community hub system"""
    
    def __init__(self, db_path: str = None):
        self.db_path = db_path or "/Users/steven/ai-sites/retention-products-suite/community-platforms/community_hub.db"
        self.setup_database()
        
    def setup_database(self):
        """Set up community database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                display_name TEXT NOT NULL,
                bio TEXT,
                avatar_url TEXT,
                join_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                reputation INTEGER DEFAULT 0,
                level INTEGER DEFAULT 1,
                password_hash TEXT NOT NULL
            )
        """)
        
        # User badges
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_badges (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                badge_name TEXT NOT NULL,
                earned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        """)
        
        # User follows
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_follows (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                follower_id TEXT,
                following_id TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (follower_id) REFERENCES users (id),
                FOREIGN KEY (following_id) REFERENCES users (id),
                UNIQUE(follower_id, following_id)
            )
        """)
        
        # Posts table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS posts (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                post_type TEXT DEFAULT 'discussion',
                category TEXT NOT NULL,
                tags TEXT,  -- JSON array
                likes INTEGER DEFAULT 0,
                comments INTEGER DEFAULT 0,
                views INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_pinned BOOLEAN DEFAULT 0,
                is_featured BOOLEAN DEFAULT 0,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        """)
        
        # Comments table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS comments (
                id TEXT PRIMARY KEY,
                post_id TEXT NOT NULL,
                user_id TEXT NOT NULL,
                content TEXT NOT NULL,
                likes INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                parent_id TEXT,
                FOREIGN KEY (post_id) REFERENCES posts (id),
                FOREIGN KEY (user_id) REFERENCES users (id),
                FOREIGN KEY (parent_id) REFERENCES comments (id)
            )
        """)
        
        # Post likes
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS post_likes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                post_id TEXT,
                user_id TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (post_id) REFERENCES posts (id),
                FOREIGN KEY (user_id) REFERENCES users (id),
                UNIQUE(post_id, user_id)
            )
        """)
        
        # Comment likes
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS comment_likes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                comment_id TEXT,
                user_id TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (comment_id) REFERENCES comments (id),
                FOREIGN KEY (user_id) REFERENCES users (id),
                UNIQUE(comment_id, user_id)
            )
        """)
        
        # Categories
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                description TEXT,
                color TEXT DEFAULT '#007bff',
                icon TEXT DEFAULT '📁',
                post_count INTEGER DEFAULT 0
            )
        """)
        
        # Initialize default categories
        default_categories = [
            ("General Discussion", "General community discussions", "#007bff", "💬"),
            ("Questions & Help", "Ask questions and get help", "#28a745", "❓"),
            ("Showcase", "Show off your work and projects", "#ffc107", "🎨"),
            ("Tutorials", "Share tutorials and guides", "#17a2b8", "📚"),
            ("Announcements", "Community announcements", "#dc3545", "📢"),
            ("Feedback", "Share feedback and suggestions", "#6f42c1", "💡")
        ]
        
        for name, desc, color, icon in default_categories:
            cursor.execute("""
                INSERT OR IGNORE INTO categories (name, description, color, icon)
                VALUES (?, ?, ?, ?)
            """, (name, desc, color, icon))
        
        conn.commit()
        conn.close()
    
    def register_user(self, username: str, email: str, display_name: str, password: str, bio: str = "") -> str:
        """Register a new user"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Check if username or email already exists
        cursor.execute("SELECT id FROM users WHERE username = ? OR email = ?", (username, email))
        if cursor.fetchone():
            conn.close()
            raise ValueError("Username or email already exists")
        
        # Create user
        user_id = str(uuid.uuid4())
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        cursor.execute("""
            INSERT INTO users (id, username, email, display_name, bio, password_hash)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (user_id, username, email, display_name, bio, password_hash))
        
        conn.commit()
        conn.close()
        
        logger.info(f"User {username} registered with ID {user_id}")
        return user_id
    
    def authenticate_user(self, username: str, password: str) -> Optional[str]:
        """Authenticate user and return user ID"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        cursor.execute("""
            SELECT id FROM users 
            WHERE username = ? AND password_hash = ?
        """, (username, password_hash))
        
        result = cursor.fetchone()
        if result:
            user_id = result[0]
            # Update last active
            cursor.execute("""
                UPDATE users SET last_active = CURRENT_TIMESTAMP 
                WHERE id = ?
            """, (user_id,))
            conn.commit()
        
        conn.close()
        return result[0] if result else None
    
    def get_user(self, user_id: str) -> Optional[User]:
        """Get user information"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        user_data = cursor.fetchone()
        
        if not user_data:
            conn.close()
            return None
        
        # Get badges
        cursor.execute("SELECT badge_name FROM user_badges WHERE user_id = ?", (user_id,))
        badges = [row[0] for row in cursor.fetchall()]
        
        # Get following
        cursor.execute("SELECT following_id FROM user_follows WHERE follower_id = ?", (user_id,))
        following = [row[0] for row in cursor.fetchall()]
        
        # Get followers
        cursor.execute("SELECT follower_id FROM user_follows WHERE following_id = ?", (user_id,))
        followers = [row[0] for row in cursor.fetchall()]
        
        conn.close()
        
        return User(
            id=user_data[0],
            username=user_data[1],
            email=user_data[2],
            display_name=user_data[3],
            bio=user_data[4] or "",
            avatar_url=user_data[5] or "",
            join_date=user_data[6],
            last_active=user_data[7],
            reputation=user_data[8],
            level=user_data[9],
            badges=badges,
            following=following,
            followers=followers
        )
    
    def create_post(self, user_id: str, title: str, content: str, post_type: str, category: str, tags: List[str] = None) -> str:
        """Create a new post"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        post_id = str(uuid.uuid4())
        tags_json = json.dumps(tags or [])
        
        cursor.execute("""
            INSERT INTO posts (id, user_id, title, content, post_type, category, tags)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (post_id, user_id, title, content, post_type, category, tags_json))
        
        # Update category post count
        cursor.execute("""
            UPDATE categories SET post_count = post_count + 1 
            WHERE name = ?
        """, (category,))
        
        conn.commit()
        conn.close()
        
        logger.info(f"Post '{title}' created by user {user_id}")
        return post_id
    
    def get_posts(self, category: str = None, post_type: str = None, limit: int = 20, offset: int = 0) -> List[Post]:
        """Get posts with optional filtering"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        query = """
            SELECT p.*, u.display_name, u.username
            FROM posts p
            JOIN users u ON p.user_id = u.id
            WHERE 1=1
        """
        params = []
        
        if category:
            query += " AND p.category = ?"
            params.append(category)
        
        if post_type:
            query += " AND p.post_type = ?"
            params.append(post_type)
        
        query += " ORDER BY p.is_pinned DESC, p.created_at DESC LIMIT ? OFFSET ?"
        params.extend([limit, offset])
        
        cursor.execute(query, params)
        posts_data = cursor.fetchall()
        
        posts = []
        for post_data in posts_data:
            tags = json.loads(post_data[6]) if post_data[6] else []
            
            posts.append(Post(
                id=post_data[0],
                user_id=post_data[1],
                title=post_data[2],
                content=post_data[3],
                post_type=post_data[4],
                category=post_data[5],
                tags=tags,
                likes=post_data[7],
                comments=post_data[8],
                views=post_data[9],
                created_at=post_data[10],
                updated_at=post_data[11],
                is_pinned=bool(post_data[12]),
                is_featured=bool(post_data[13])
            ))
        
        conn.close()
        return posts
    
    def get_post(self, post_id: str) -> Optional[Post]:
        """Get a specific post"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM posts WHERE id = ?", (post_id,))
        post_data = cursor.fetchone()
        
        if not post_data:
            conn.close()
            return None
        
        # Increment view count
        cursor.execute("""
            UPDATE posts SET views = views + 1 
            WHERE id = ?
        """, (post_id,))
        
        conn.commit()
        conn.close()
        
        tags = json.loads(post_data[6]) if post_data[6] else []
        
        return Post(
            id=post_data[0],
            user_id=post_data[1],
            title=post_data[2],
            content=post_data[3],
            post_type=post_data[4],
            category=post_data[5],
            tags=tags,
            likes=post_data[7],
            comments=post_data[8],
            views=post_data[9],
            created_at=post_data[10],
            updated_at=post_data[11],
            is_pinned=bool(post_data[12]),
            is_featured=bool(post_data[13])
        )
    
    def add_comment(self, post_id: str, user_id: str, content: str, parent_id: str = None) -> str:
        """Add a comment to a post"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        comment_id = str(uuid.uuid4())
        
        cursor.execute("""
            INSERT INTO comments (id, post_id, user_id, content, parent_id)
            VALUES (?, ?, ?, ?, ?)
        """, (comment_id, post_id, user_id, content, parent_id))
        
        # Update post comment count
        cursor.execute("""
            UPDATE posts SET comments = comments + 1 
            WHERE id = ?
        """, (post_id,))
        
        conn.commit()
        conn.close()
        
        logger.info(f"Comment added to post {post_id} by user {user_id}")
        return comment_id
    
    def get_comments(self, post_id: str) -> List[Comment]:
        """Get comments for a post"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT c.*, u.display_name, u.username
            FROM comments c
            JOIN users u ON c.user_id = u.id
            WHERE c.post_id = ?
            ORDER BY c.created_at ASC
        """, (post_id,))
        
        comments_data = cursor.fetchall()
        conn.close()
        
        comments = []
        for comment_data in comments_data:
            comments.append(Comment(
                id=comment_data[0],
                post_id=comment_data[1],
                user_id=comment_data[2],
                content=comment_data[3],
                likes=comment_data[4],
                created_at=comment_data[5],
                parent_id=comment_data[6]
            ))
        
        return comments
    
    def like_post(self, post_id: str, user_id: str) -> bool:
        """Like a post"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Check if already liked
            cursor.execute("""
                SELECT id FROM post_likes 
                WHERE post_id = ? AND user_id = ?
            """, (post_id, user_id))
            
            if cursor.fetchone():
                conn.close()
                return False  # Already liked
            
            # Add like
            cursor.execute("""
                INSERT INTO post_likes (post_id, user_id)
                VALUES (?, ?)
            """, (post_id, user_id))
            
            # Update post like count
            cursor.execute("""
                UPDATE posts SET likes = likes + 1 
                WHERE id = ?
            """, (post_id,))
            
            conn.commit()
            return True
            
        except Exception as e:
            logger.error(f"Error liking post {post_id}: {e}")
            return False
        finally:
            conn.close()
    
    def follow_user(self, follower_id: str, following_id: str) -> bool:
        """Follow a user"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT OR IGNORE INTO user_follows (follower_id, following_id)
                VALUES (?, ?)
            """, (follower_id, following_id))
            
            conn.commit()
            return True
            
        except Exception as e:
            logger.error(f"Error following user {following_id}: {e}")
            return False
        finally:
            conn.close()
    
    def get_categories(self) -> List[Dict]:
        """Get all categories"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT name, description, color, icon, post_count
            FROM categories
            ORDER BY post_count DESC
        """)
        
        categories = cursor.fetchall()
        conn.close()
        
        return [{
            'name': cat[0],
            'description': cat[1],
            'color': cat[2],
            'icon': cat[3],
            'post_count': cat[4]
        } for cat in categories]
    
    def get_leaderboard(self, limit: int = 10) -> List[Dict]:
        """Get user leaderboard"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT u.display_name, u.username, u.reputation, u.level,
                   COUNT(p.id) as post_count,
                   COUNT(f.follower_id) as follower_count
            FROM users u
            LEFT JOIN posts p ON u.id = p.user_id
            LEFT JOIN user_follows f ON u.id = f.following_id
            GROUP BY u.id
            ORDER BY u.reputation DESC, post_count DESC
            LIMIT ?
        """, (limit,))
        
        leaderboard = cursor.fetchall()
        conn.close()
        
        return [{
            'display_name': user[0],
            'username': user[1],
            'reputation': user[2],
            'level': user[3],
            'post_count': user[4],
            'follower_count': user[5]
        } for user in leaderboard]
    
    def search_posts(self, query: str, limit: int = 20) -> List[Post]:
        """Search posts by title and content"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        search_query = f"%{query}%"
        cursor.execute("""
            SELECT * FROM posts 
            WHERE title LIKE ? OR content LIKE ?
            ORDER BY created_at DESC
            LIMIT ?
        """, (search_query, search_query, limit))
        
        posts_data = cursor.fetchall()
        conn.close()
        
        posts = []
        for post_data in posts_data:
            tags = json.loads(post_data[6]) if post_data[6] else []
            
            posts.append(Post(
                id=post_data[0],
                user_id=post_data[1],
                title=post_data[2],
                content=post_data[3],
                post_type=post_data[4],
                category=post_data[5],
                tags=tags,
                likes=post_data[7],
                comments=post_data[8],
                views=post_data[9],
                created_at=post_data[10],
                updated_at=post_data[11],
                is_pinned=bool(post_data[12]),
                is_featured=bool(post_data[13])
            ))
        
        return posts

def main():
    """Main function to test community hub"""
    hub = CommunityHub()
    
    print("👥 Community Hub - User Engagement Platform")
    print("=" * 50)
    
    # Test user registration
    try:
        user_id = hub.register_user("testuser", "test@example.com", "Test User", "password123", "Test bio")
        print(f"✅ User registered with ID: {user_id}")
        
        # Test post creation
        post_id = hub.create_post(
            user_id, 
            "Welcome to the Community!", 
            "This is our first community post. Welcome everyone!",
            "discussion",
            "General Discussion",
            ["welcome", "community", "introduction"]
        )
        print(f"✅ Post created with ID: {post_id}")
        
        # Test getting posts
        posts = hub.get_posts(limit=5)
        print(f"✅ Retrieved {len(posts)} posts")
        
        # Test categories
        categories = hub.get_categories()
        print(f"✅ Found {len(categories)} categories")
        
        print("\n🎉 Community hub is ready!")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()