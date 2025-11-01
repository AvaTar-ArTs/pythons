"""
Setup 12

This module provides functionality for setup 12.

Author: Auto-generated
Date: 2025-11-01
"""

# Constants
CONSTANT_100 = 100
CONSTANT_255 = 255
CONSTANT_587 = 587
CONSTANT_1000 = 1000
CONSTANT_5000 = 5000
CONSTANT_5432 = 5432
CONSTANT_5678 = 5678

#!/usr/bin/env python3
"""
Social Media Automation Setup Script
Sets up n8n workflows, backend services, and database for social media automation
"""

import os
import json
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Any
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class SocialMediaAutomationSetup:
    """Setup script for social media automation system."""

    def __init__(self, base_dir: str = Path("/Users/steven")):
        """__init__ function."""

        self.base_dir = Path(base_dir)
        self.n8n_dir = self.base_dir / "n8n_workflows"
        self.backend_dir = self.base_dir / "social_media_backend"
        self.config_dir = self.base_dir / "social_media_config"

    def setup_directories(self):
        """Create necessary directories."""
        logger.info("Creating directories...")

        directories = [
            self.n8n_dir,
            self.backend_dir,
            self.config_dir,
            self.config_dir / "credentials",
            self.config_dir / "templates",
            self.config_dir / "logs",
        ]

        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            logger.info(f"Created directory: {directory}")

    def create_environment_file(self):
        """Create .env file with required environment variables."""
        logger.info("Creating environment file...")

        env_content = """# Social Media Automation Environment Variables

# Database Configuration
DATABASE_URL=sqlite:///social_media_automation.db
POSTGRES_HOST=localhost
POSTGRES_PORT=CONSTANT_5432
POSTGRES_DB=social_media_automation
POSTGRES_USER=n8n_user
POSTGRES_PASSWORD=secure_password

# API Credentials
BEHANCE_API_KEY=your_behance_api_key
BEHANCE_CLIENT_ID=your_behance_client_id
BEHANCE_CLIENT_SECRET=your_behance_client_secret

LINKEDIN_CLIENT_ID=your_linkedin_client_id
LINKEDIN_CLIENT_SECRET=your_linkedin_client_secret
LINKEDIN_ACCESS_TOKEN=your_linkedin_access_token
LINKEDIN_PERSON_ID=your_linkedin_person_id

TWITTER_API_KEY=your_twitter_api_key
TWITTER_API_SECRET=your_twitter_api_secret
TWITTER_ACCESS_TOKEN=your_twitter_access_token
TWITTER_ACCESS_TOKEN_SECRET=your_twitter_access_token_secret

INSTAGRAM_ACCESS_TOKEN=your_instagram_access_token
INSTAGRAM_BUSINESS_ACCOUNT_ID=your_instagram_business_account_id

FACEBOOK_ACCESS_TOKEN=your_facebook_access_token
FACEBOOK_PAGE_ID=your_facebook_page_id

# Email Configuration
SMTP_HOST=smtp.gmail.com
SMTP_PORT=CONSTANT_587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_password

# n8n Configuration
N8N_HOST=localhost
N8N_PORT=CONSTANT_5678
N8N_PROTOCOL=http

# Backend Configuration
BACKEND_HOST=localhost
BACKEND_PORT=CONSTANT_5000
BACKEND_DEBUG=true

# Logging Configuration
LOG_LEVEL=INFO
LOG_FILE=social_media_automation.log
"""

        env_file = self.config_dir / ".env"
        with open(env_file, "w") as f:
            f.write(env_content)

        logger.info(f"Created environment file: {env_file}")

    def create_docker_compose(self):
        """Create Docker Compose file for the entire stack."""
        logger.info("Creating Docker Compose file...")

        docker_compose = {
            "version": "3.8",
            "services": {
                "n8n": {
                    "image": "n8nio/n8n:latest",
                    "ports": ["CONSTANT_5678:5678"],
                    "environment": [
                        "N8N_BASIC_AUTH_ACTIVE=true",
                        "N8N_BASIC_AUTH_USER=admin",
                        "N8N_BASIC_AUTH_PASSWORD=admin123",
                        "N8N_HOST=localhost",
                        "N8N_PORT=5678",
                        "N8N_PROTOCOL=http",
                        "WEBHOOK_URL=http://localhost:CONSTANT_5678/",
                        "GENERIC_TIMEZONE=UTC",
                    ],
                    "volumes": [
                        "./n8n_data:/home/node/.n8n",
                        "./n8n_workflows:/workflows",
                    ],
                    "depends_on": ["postgres"],
                },
                "postgres": {
                    "image": "postgres:13",
                    "environment": [
                        "POSTGRES_DB=social_media_automation",
                        "POSTGRES_USER=n8n_user",
                        "POSTGRES_PASSWORD=secure_password",
                    ],
                    "volumes": ["postgres_data:/var/lib/postgresql/data"],
                    "ports": ["CONSTANT_5432:5432"],
                },
                "backend": {
                    "build": "./social_media_backend",
                    "ports": ["CONSTANT_5000:5000"],
                    "environment": [
                        "FLASK_ENV=production",
                        "DATABASE_URL=postgresql://n8n_user:secure_password@postgres:CONSTANT_5432/social_media_automation",
                    ],
                    "depends_on": ["postgres"],
                    "volumes": ["./social_media_backend:/app"],
                },
                "redis": {
                    "image": "redis:6-alpine",
                    "ports": ["6379:6379"],
                    "volumes": ["redis_data:/data"],
                },
            },
            "volumes": {"postgres_data": {}, "redis_data": {}},
        }

        docker_compose_file = self.base_dir / "docker-compose.yml"
        with open(docker_compose_file, "w") as f:
            json.dump(docker_compose, f, indent=2)

        logger.info(f"Created Docker Compose file: {docker_compose_file}")

    def create_backend_dockerfile(self):
        """Create Dockerfile for the backend service."""
        logger.info("Creating backend Dockerfile...")

        dockerfile_content = """FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    gcc \\
    g++ \\
    libpq-dev \\
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd -m -u CONSTANT_1000 n8n && chown -R n8n:n8n /app
USER n8n

# Expose port
EXPOSE CONSTANT_5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \\
    CMD curl -f http://localhost:CONSTANT_5000/health || exit 1

# Start application
CMD ["python", "social_media_automation_backend.py"]
"""

        dockerfile_path = self.backend_dir / "Dockerfile"
        with open(dockerfile_path, "w") as f:
            f.write(dockerfile_content)

        logger.info(f"Created Dockerfile: {dockerfile_path}")

    def create_requirements_file(self):
        """Create requirements.txt for the backend service."""
        logger.info("Creating requirements file...")

        requirements = """Flask==2.3.3
Flask-CORS==4.0.0
requests==2.31.0
Pillow==10.0.1
python-dotenv==1.0.0
psycopg2-binary==2.9.7
sqlite3
hashlib
datetime
pathlib
logging
typing
dataclasses
"""

        requirements_file = self.backend_dir / "requirements.txt"
        with open(requirements_file, "w") as f:
            f.write(requirements)

        logger.info(f"Created requirements file: {requirements_file}")

    def create_n8n_workflow_files(self):
        """Create individual n8n workflow files."""
        logger.info("Creating n8n workflow files...")

        # Load the main workflow JSON
        with open(self.base_dir / "n8n_social_media_automation.json", "r") as f:
            workflows_data = json.load(f)

        # Create individual workflow files
        for workflow_name, workflow_data in workflows_data["n8n_workflows"].items():
            workflow_file = self.n8n_dir / f"{workflow_name}.json"
            with open(workflow_file, "w") as f:
                json.dump(workflow_data, f, indent=2)
            logger.info(f"Created workflow file: {workflow_file}")

    def create_database_schema(self):
        """Create database schema SQL file."""
        logger.info("Creating database schema...")

        schema_sql = """-- Social Media Automation Database Schema

-- Posts table
CREATE TABLE IF NOT EXISTS posts (
    id SERIAL PRIMARY KEY,
    platform VARCHAR(50) NOT NULL,
    content TEXT NOT NULL,
    hashtags TEXT[],
    mentions TEXT[],
    media_urls TEXT[],
    scheduled_time TIMESTAMP,
    published_time TIMESTAMP,
    status VARCHAR(20) DEFAULT 'draft',
    post_id VARCHAR(CONSTANT_100),
    engagement_metrics JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Analytics table
CREATE TABLE IF NOT EXISTS analytics (
    id SERIAL PRIMARY KEY,
    platform VARCHAR(50) NOT NULL,
    post_id VARCHAR(CONSTANT_100),
    followers_count INTEGER,
    engagement_rate FLOAT,
    reach INTEGER,
    impressions INTEGER,
    likes INTEGER,
    comments INTEGER,
    shares INTEGER,
    clicks INTEGER,
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Content templates table
CREATE TABLE IF NOT EXISTS content_templates (
    id SERIAL PRIMARY KEY,
    name VARCHAR(CONSTANT_100) NOT NULL,
    platform VARCHAR(50) NOT NULL,
    template TEXT NOT NULL,
    variables JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Portfolio analytics table
CREATE TABLE IF NOT EXISTS portfolio_analytics (
    id SERIAL PRIMARY KEY,
    project_id VARCHAR(50),
    title VARCHAR(CONSTANT_255),
    platforms JSONB,
    metrics JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- LinkedIn analytics table
CREATE TABLE IF NOT EXISTS linkedin_analytics (
    id SERIAL PRIMARY KEY,
    post_id VARCHAR(50),
    content TEXT,
    hashtags TEXT[],
    mentions TEXT[],
    engagement_score FLOAT,
    published_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Content distribution table
CREATE TABLE IF NOT EXISTS content_distribution (
    id SERIAL PRIMARY KEY,
    distribution_id VARCHAR(50),
    original_content JSONB,
    platforms JSONB,
    success_count INTEGER,
    failure_count INTEGER,
    success_rate FLOAT,
    distributed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Social media analytics table
CREATE TABLE IF NOT EXISTS social_media_analytics (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP,
    total_platforms INTEGER,
    successful_platforms INTEGER,
    total_followers BIGINT,
    average_engagement_rate FLOAT,
    platform_performance JSONB,
    insights TEXT[],
    recommendations TEXT[]
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_posts_platform ON posts(platform);
CREATE INDEX IF NOT EXISTS idx_posts_status ON posts(status);
CREATE INDEX IF NOT EXISTS idx_posts_published_time ON posts(published_time);
CREATE INDEX IF NOT EXISTS idx_analytics_platform ON analytics(platform);
CREATE INDEX IF NOT EXISTS idx_analytics_recorded_at ON analytics(recorded_at);
CREATE INDEX IF NOT EXISTS idx_templates_platform ON content_templates(platform);
"""

        schema_file = self.config_dir / "database_schema.sql"
        with open(schema_file, "w") as f:
            f.write(schema_sql)

        logger.info(f"Created database schema: {schema_file}")

    def create_setup_script(self):
        """Create setup script for easy deployment."""
        logger.info("Creating setup script...")

        setup_script = """#!/bin/bash
# Social Media Automation Setup Script

set -e

echo "🚀 Setting up Social Media Automation System..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p n8n_data
mkdir -p postgres_data
mkdir -p redis_data
mkdir -p logs

# Copy environment file
echo "⚙️ Setting up environment..."
if [ ! -f .env ]; then
    cp social_media_config/.env .env
    echo "📝 Please edit .env file with your API credentials"
fi

# Build and start services
echo "🐳 Building and starting services..."
docker-compose up -d --build

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 30

# Check if services are running
echo "🔍 Checking service status..."
docker-compose ps

# Run database migrations
echo "🗄️ Setting up database..."
docker-compose exec postgres psql -U n8n_user -d social_media_automation -f /docker-entrypoint-initdb.d/schema.sql

echo "✅ Setup complete!"
echo ""
echo "🌐 Access URLs:"
echo "  - n8n: http://localhost:5678"
echo "  - Backend API: http://localhost:5000"
echo "  - Health Check: http://localhost:CONSTANT_5000/health"
echo ""
echo "🔑 Default n8n credentials:"
echo "  - Username: admin"
echo "  - Password: admin123"
echo ""
echo "📚 Next steps:"
echo "  1. Edit .env file with your API credentials"
echo "  2. Import workflow files into n8n"
echo "  3. Configure OAuth2 credentials in n8n"
echo "  4. Test the workflows"
echo ""
echo "🛑 To stop services: docker-compose down"
echo "🔄 To restart services: docker-compose restart"
"""

        setup_file = self.base_dir / "setup.sh"
        with open(setup_file, "w") as f:
            f.write(setup_script)

        # Make script executable
        os.chmod(setup_file, 0o755)

        logger.info(f"Created setup script: {setup_file}")

    def create_readme(self):
        """Create comprehensive README file."""
        logger.info("Creating README file...")

        readme_content = """# Social Media Automation System

A comprehensive automation system for managing social media presence across multiple platforms including Behance, LinkedIn, Twitter, Instagram, and Facebook.

## 🚀 Features

### Platform Support
- **Behance**: Portfolio project uploads and management
- **LinkedIn**: Professional content publishing and analytics
- **Twitter**: Tweet scheduling and engagement tracking
- **Instagram**: Post publishing and story management
- **Facebook**: Page post automation and insights

### Automation Workflows
- **Portfolio Automation**: Automated Behance portfolio management
- **Content Distribution**: Multi-platform content publishing
- **Analytics Collection**: Automated metrics gathering
- **Engagement Tracking**: Performance monitoring across platforms
- **Content Optimization**: AI-powered content enhancement

### n8n Workflows
- **Behance Portfolio Automation**: Complete portfolio management workflow
- **LinkedIn Content Automation**: Professional content publishing
- **Multi-Platform Distribution**: Cross-platform content sharing
- **Social Media Analytics**: Comprehensive metrics collection
- **System Monitoring**: Health checks and alerting

## 🛠️ Installation

### Prerequisites
- Docker and Docker Compose
- API credentials for each platform
- SMTP server for notifications

### Quick Start
```bash
# Clone the repository
git clone <repository-url>
cd social-media-automation

# Run setup script
./setup.sh

# Edit environment variables
nano .env

# Start services
docker-compose up -d
```

### Manual Setup
```bash
# Create directories
mkdir -p n8n_data postgres_data redis_data logs

# Copy environment file
cp social_media_config/.env .env

# Edit .env with your credentials
nano .env

# Start services
docker-compose up -d --build

# Import workflows into n8n
# Access n8n at http://localhost:CONSTANT_5678
```

## ⚙️ Configuration

### Environment Variables
```bash
# Database
DATABASE_URL=postgresql://n8n_user:secure_password@postgres:CONSTANT_5432/social_media_automation

# API Credentials
BEHANCE_API_KEY=your_behance_api_key
LINKEDIN_CLIENT_ID=your_linkedin_client_id
TWITTER_API_KEY=your_twitter_api_key
INSTAGRAM_ACCESS_TOKEN=your_instagram_access_token
FACEBOOK_ACCESS_TOKEN=your_facebook_access_token

# Email
SMTP_HOST=smtp.gmail.com
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_password
```

### n8n Configuration
1. Access n8n at http://localhost:CONSTANT_5678
2. Login with admin/admin123
3. Import workflow files from n8n_workflows/
4. Configure OAuth2 credentials for each platform
5. Test workflows with sample data

## 📊 API Endpoints

### Backend API (Port CONSTANT_5000)
- `GET /health` - Health check
- `POST /behance/upload-project` - Upload project to Behance
- `POST /linkedin/publish-post` - Publish LinkedIn post
- `POST /twitter/publish-tweet` - Publish Twitter tweet
- `POST /instagram/publish-post` - Publish Instagram post
- `POST /facebook/publish-post` - Publish Facebook post
- `POST /content/generate` - Generate content
- `POST /content/optimize` - Optimize content
- `POST /analytics/collect` - Collect analytics
- `GET /posts/analytics` - Get post analytics

### n8n Webhooks
- `POST /webhook/behance-portfolio` - Behance portfolio trigger
- `POST /webhook/distribute-content` - Content distribution trigger
- `POST /webhook/linkedin-content` - LinkedIn content trigger

## 🔧 Usage

### 1. Portfolio Automation
```bash
# Trigger Behance portfolio upload
curl -X POST http://localhost:CONSTANT_5000/behance/upload-project \\
  -H "Content-Type: application/json" \\
  -d '{
    "title": "My AI Art Project",
    "description": "A collection of AI-generated artwork",
    "images": ["image1.jpg", "image2.jpg"],
    "tags": ["AI", "Art", "Digital"],
    "category": "Digital Art"
  }'
```

### 2. Content Distribution
```bash
# Distribute content across platforms
curl -X POST http://localhost:CONSTANT_5000/webhook/distribute-content \\
  -H "Content-Type: application/json" \\
  -d '{
    "content": {
      "text": "Check out my latest project!",
      "image_url": "https://example.com/image.jpg"
    },
    "platforms": ["linkedin", "twitter", "instagram"]
  }'
```

### 3. Analytics Collection
```bash
# Collect analytics from all platforms
curl -X POST http://localhost:CONSTANT_5000/analytics/collect \\
  -H "Content-Type: application/json" \\
  -d '{
    "platforms": ["linkedin", "twitter", "instagram", "facebook"]
  }'
```

## 📈 Monitoring

### Health Checks
- Backend: http://localhost:CONSTANT_5000/health
- n8n: http://localhost:CONSTANT_5678
- Database: Check Docker logs

### Logs
```bash
# View all logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f backend
docker-compose logs -f n8n
```

### Database
```bash
# Connect to database
docker-compose exec postgres psql -U n8n_user -d social_media_automation

# View tables
\\dt

# Query analytics
SELECT platform, AVG(engagement_rate) FROM analytics GROUP BY platform;
```

## 🔒 Security

### API Credentials
- Store all API credentials in .env file
- Never commit credentials to version control
- Use environment-specific credential files
- Rotate credentials regularly

### Database Security
- Use strong passwords
- Enable SSL connections
- Regular backups
- Access control

### Network Security
- Use HTTPS in production
- Firewall configuration
- VPN access for remote management

## 🚀 Deployment

### Production Deployment
1. Set up production database
2. Configure reverse proxy (nginx)
3. Set up SSL certificates
4. Configure monitoring and alerting
5. Set up automated backups

### Scaling
- Use multiple n8n instances
- Load balance backend services
- Scale database with read replicas
- Implement caching layer

## 📚 Documentation

### Workflow Documentation
- Each workflow includes detailed documentation
- API endpoints are documented with examples
- Database schema is fully documented

### Troubleshooting
- Check logs for error messages
- Verify API credentials
- Test individual components
- Monitor resource usage

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Make changes
4. Add tests
5. Submit pull request

## 📄 License

MIT License - see LICENSE file for details

## 🆘 Support

- GitHub Issues: Report bugs and feature requests
- Documentation: Check README and code comments
- Community: Join our Discord server

## 🔄 Updates

### Version 1.0.0
- Initial release
- Basic automation workflows
- Multi-platform support
- Analytics collection

### Roadmap
- Advanced AI content generation
- Video content automation
- Advanced analytics dashboard
- Mobile app integration
"""

        readme_file = self.base_dir / "README.md"
        with open(readme_file, "w") as f:
            f.write(readme_content)

        logger.info(f"Created README file: {readme_file}")

    def run_setup(self):
        """Run the complete setup process."""
        logger.info("Starting Social Media Automation Setup...")

        try:
            self.setup_directories()
            self.create_environment_file()
            self.create_docker_compose()
            self.create_backend_dockerfile()
            self.create_requirements_file()
            self.create_n8n_workflow_files()
            self.create_database_schema()
            self.create_setup_script()
            self.create_readme()

            logger.info("✅ Setup completed successfully!")
            logger.info("")
            logger.info("🚀 Next steps:")
            logger.info("1. Edit .env file with your API credentials")
            logger.info("2. Run ./setup.sh to start the services")
            logger.info("3. Access n8n at http://localhost:5678")
            logger.info("4. Import workflow files and configure OAuth2")
            logger.info("5. Test the automation workflows")

        except Exception as e:
            logger.error(f"❌ Setup failed: {e}")
            sys.exit(1)


def main():
    """Main function to run the setup."""
    setup = SocialMediaAutomationSetup()
    setup.run_setup()


if __name__ == "__main__":
    main()
