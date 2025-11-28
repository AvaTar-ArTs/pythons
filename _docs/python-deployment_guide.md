# Deployment Guide
## Production Deployment Options for Advanced Systems

---

## 🎯 **Overview**

This guide covers multiple deployment strategies for the Advanced Systems suite, from local development to enterprise-scale production environments. Choose the approach that best fits your scale, budget, and operational requirements.

---

## 🏠 **Local Development**

### **Basic Setup**
```bash
# Clone or navigate to the directory
cd ~/advanced-systems

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run systems locally
python content_pipeline/advanced_content_pipeline.py
python code_orchestrator/intelligent_code_orchestrator.py
```

### **Development Configuration**
```python
# config/dev_config.py
DEBUG = True
LOG_LEVEL = 'DEBUG'
API_TIMEOUT = 30
MAX_CONCURRENT_REQUESTS = 3

# Development-specific settings
CACHE_ENABLED = False
METRICS_ENABLED = False
```

---

## ☁️ **Cloud Deployment Options**

### **AWS (Amazon Web Services)**

#### **Option 1: Lambda + API Gateway (Serverless)**
```yaml
# template.yaml (SAM template)
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31

Resources:
  ContentPipelineFunction:
    Type: AWS::Serverless::Function
    Properties:
      FunctionName: content-pipeline
      Runtime: python3.11
      Handler: lambda_function.lambda_handler
      MemorySize: 2048
      Timeout: 300
      Environment:
        Variables:
          ENV_FILE_PATH: /opt/env
      Layers:
        - !Ref PythonRequirementsLayer

  PythonRequirementsLayer:
    Type: AWS::Serverless::LayerVersion
    Properties:
      LayerName: python-requirements
      ContentUri: ./requirements/
      CompatibleRuntimes:
        - python3.11
```

**Deployment Steps:**
```bash
# Install AWS SAM CLI
pip install aws-sam-cli

# Build and deploy
sam build
sam deploy --guided

# API Gateway URL will be provided after deployment
```

#### **Option 2: EC2 + Docker**
```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Deployment:**
```bash
# Build and push to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account>.dkr.ecr.us-east-1.amazonaws.com

docker build -t advanced-systems .
docker tag advanced-systems:latest <account>.dkr.ecr.us-east-1.amazonaws.com/advanced-systems:latest
docker push <account>.dkr.ecr.us-east-1.amazonaws.com/advanced-systems:latest

# Deploy to EC2 with user data script
aws ec2 run-instances --image-id ami-12345678 --instance-type t3.medium \
  --user-data file://ec2-setup.sh --security-group-ids sg-123456
```

### **Google Cloud Platform**

#### **Cloud Run (Serverless Containers)**
```yaml
# cloud-run.yaml
apiVersion: serving.knative.dev/v1
kind: Service
metadata:
  name: advanced-systems
spec:
  template:
    spec:
      containers:
      - image: gcr.io/PROJECT-ID/advanced-systems:latest
        ports:
        - containerPort: 8000
        env:
        - name: ENV_FILE_PATH
          value: /secrets/env
        resources:
          limits:
            cpu: 2000m
            memory: 2Gi
```

**Deployment:**
```bash
# Build and deploy
gcloud builds submit --tag gcr.io/PROJECT-ID/advanced-systems
gcloud run deploy advanced-systems --image gcr.io/PROJECT-ID/advanced-systems --platform managed
```

#### **GKE (Kubernetes)**
```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: advanced-systems
spec:
  replicas: 3
  selector:
    matchLabels:
      app: advanced-systems
  template:
    metadata:
      labels:
        app: advanced-systems
    spec:
      containers:
      - name: api
        image: gcr.io/PROJECT-ID/advanced-systems:latest
        ports:
        - containerPort: 8000
        envFrom:
        - secretRef:
            name: api-secrets
        resources:
          requests:
            cpu: 1000m
            memory: 2Gi
          limits:
            cpu: 2000m
            memory: 4Gi
```

### **Azure**

#### **Container Apps**
```bash
# Deploy to Azure Container Apps
az containerapp create \
  --name advanced-systems \
  --resource-group myResourceGroup \
  --image myregistry.azurecr.io/advanced-systems:latest \
  --target-port 8000 \
  --ingress external \
  --query properties.configuration.ingress.fqdn
```

#### **App Service**
```json
// app-service.json
{
  "name": "advanced-systems",
  "type": "Microsoft.Web/sites",
  "properties": {
    "serverFarmId": "/subscriptions/.../serverfarms/myPlan",
    "siteConfig": {
      "linuxFxVersion": "PYTHON|3.11",
      "appSettings": [
        {
          "name": "SCM_DO_BUILD_DURING_DEPLOYMENT",
          "value": "true"
        }
      ]
    }
  }
}
```

---

## 🐳 **Docker Containerization**

### **Multi-Stage Dockerfile**
```dockerfile
# Multi-stage build for optimization
FROM python:3.11-slim as builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --user -r requirements.txt

# Production stage
FROM python:3.11-slim as production

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd --create-home --shell /bin/bash app
USER app

WORKDIR /home/app
COPY --from=builder /root/.local /home/app/.local
COPY . .

# Add local bin to PATH
ENV PATH=/home/app/.local/bin:$PATH

EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### **Docker Compose for Development**
```yaml
# docker-compose.yml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - ENV_FILE_PATH=/app/.env
    volumes:
      - ~/.env.d:/app/.env.d:ro
      - ./logs:/app/logs
    depends_on:
      - redis
      - postgres

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: advanced_systems
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

volumes:
  redis_data:
  postgres_data:
```

---

## 🚀 **FastAPI Server Setup**

### **Main Application**
```python
# main.py
from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import asyncio
from typing import Dict, Any
import logging

from content_pipeline.advanced_content_pipeline import AdvancedContentPipeline
from code_orchestrator.intelligent_code_orchestrator import IntelligentCodeOrchestrator

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Advanced AI Systems API",
    description="Multi-modal content generation and code analysis platform",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global instances (consider dependency injection for production)
content_pipeline = None
code_orchestrator = None

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    global content_pipeline, code_orchestrator
    try:
        content_pipeline = AdvancedContentPipeline()
        code_orchestrator = IntelligentCodeOrchestrator()
        logger.info("Services initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize services: {e}")
        raise

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "services": {
            "content_pipeline": content_pipeline is not None,
            "code_orchestrator": code_orchestrator is not None
        }
    }

@app.post("/api/generate-content")
async def generate_content(request: Dict[str, Any], background_tasks: BackgroundTasks):
    """Generate content using the content pipeline"""
    try:
        if not content_pipeline:
            raise HTTPException(status_code=503, detail="Content pipeline not available")

        result = await content_pipeline.generate_content(**request)

        # Log usage for analytics
        background_tasks.add_task(log_content_generation, request, result)

        return result

    except Exception as e:
        logger.error(f"Content generation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/analyze-codebase")
async def analyze_codebase(request: Dict[str, Any] = None, background_tasks: BackgroundTasks = None):
    """Analyze codebase using the code orchestrator"""
    try:
        if not code_orchestrator:
            raise HTTPException(status_code=503, detail="Code orchestrator not available")

        focus_areas = request.get('focus_areas', ['bug_detection', 'code_quality']) if request else ['bug_detection', 'code_quality']

        result = await code_orchestrator.analyze_codebase(focus_areas=focus_areas)

        # Log usage for analytics
        if background_tasks:
            background_tasks.add_task(log_code_analysis, focus_areas, result)

        return result

    except Exception as e:
        logger.error(f"Code analysis failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/metrics")
async def get_metrics():
    """Get system metrics and usage statistics"""
    return {
        "uptime": "calculate uptime",
        "requests_processed": 0,  # Track with actual metrics
        "active_services": {
            "content_pipeline": content_pipeline is not None,
            "code_orchestrator": code_orchestrator is not None
        }
    }

async def log_content_generation(request: Dict[str, Any], result: Dict[str, Any]):
    """Log content generation for analytics"""
    # Implement logging to your analytics system
    pass

async def log_code_analysis(focus_areas: list, result: Dict[str, Any]):
    """Log code analysis for analytics"""
    # Implement logging to your analytics system
    pass

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Set to False in production
        log_level="info"
    )
```

---

## 🔧 **Production Configuration**

### **Environment Variables**
```bash
# Production environment variables
export ENVIRONMENT=production
export LOG_LEVEL=WARNING
export API_TIMEOUT=60
export MAX_CONCURRENT_REQUESTS=10
export CACHE_ENABLED=true
export METRICS_ENABLED=true
export SENTRY_DSN=your_sentry_dsn
```

### **Secrets Management**
```python
# Use proper secrets management in production
import os
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

# Azure Key Vault example
credential = DefaultAzureCredential()
secret_client = SecretClient(vault_url="https://myvault.vault.azure.net/", credential=credential)

openai_key = secret_client.get_secret("openai-api-key").value
anthropic_key = secret_client.get_secret("anthropic-api-key").value
```

### **Monitoring & Observability**
```python
# Production monitoring setup
from sentry_sdk import init as sentry_init
import structlog

# Sentry error tracking
sentry_init(dsn=os.getenv('SENTRY_DSN'))

# Structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)
```

---

## 📊 **Scaling Strategies**

### **Horizontal Scaling**
```yaml
# Kubernetes HPA for autoscaling
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: advanced-systems-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: advanced-systems
  minReplicas: 3
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

### **Load Balancing**
```nginx
# Nginx load balancer configuration
upstream advanced_systems {
    least_conn;
    server api1.example.com:8000;
    server api2.example.com:8000;
    server api3.example.com:8000;
}

server {
    listen 80;
    server_name api.example.com;

    location / {
        proxy_pass http://advanced_systems;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

---

## 🔒 **Security Hardening**

### **Production Security Checklist**
- [ ] Use HTTPS with valid SSL certificates
- [ ] Implement API rate limiting
- [ ] Add request validation and sanitization
- [ ] Use secrets management (not environment variables)
- [ ] Implement proper authentication/authorization
- [ ] Add request/response logging (without sensitive data)
- [ ] Regular security updates and dependency scanning
- [ ] Database encryption and secure backups
- [ ] Network security (firewalls, VPCs)
- [ ] Regular security audits and penetration testing

### **API Security**
```python
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException, status
import jwt
from datetime import datetime, timedelta

# JWT token validation
SECRET_KEY = os.getenv('JWT_SECRET_KEY')
ALGORITHM = "HS256"

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
```

---

## 📈 **Performance Optimization**

### **Caching Strategies**
```python
from cachetools import TTLCache
from functools import lru_cache

# TTL cache for API responses
api_cache = TTLCache(maxsize=1000, ttl=300)  # 5 minute TTL

@lru_cache(maxsize=128)
def cached_api_call(endpoint, params):
    """Cache expensive API calls"""
    # Implementation with caching
    pass
```

### **Async Optimization**
```python
import asyncio
from asyncio import Semaphore

# Semaphore for controlling concurrency
api_semaphore = Semaphore(10)  # Max 10 concurrent API calls

async def rate_limited_api_call(func, *args, **kwargs):
    """Rate-limited API call with semaphore"""
    async with api_semaphore:
        return await func(*args, **kwargs)
```

### **Database Optimization**
```python
# Connection pooling for database operations
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

engine = create_async_engine(
    "postgresql+asyncpg://user:password@localhost/db",
    pool_size=10,
    max_overflow=20,
    pool_timeout=30,
    pool_recycle=1800
)

AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
```

---

## 📊 **Monitoring & Alerting**

### **Application Metrics**
```python
from prometheus_client import Counter, Histogram, Gauge
import time

# Request metrics
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint', 'status'])
REQUEST_LATENCY = Histogram('http_request_duration_seconds', 'HTTP request latency', ['method', 'endpoint'])
ACTIVE_CONNECTIONS = Gauge('active_connections', 'Number of active connections')

# API usage metrics
API_CALLS = Counter('api_calls_total', 'Total API calls', ['service', 'endpoint'])
API_ERRORS = Counter('api_errors_total', 'Total API errors', ['service', 'error_type'])
```

### **Health Checks**
```python
@app.get("/health/detailed")
async def detailed_health_check():
    """Detailed health check with service status"""
    health_status = {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "services": {},
        "system": {
            "cpu_usage": "get CPU usage",
            "memory_usage": "get memory usage",
            "disk_usage": "get disk usage"
        }
    }

    # Check each service
    services_to_check = [
        ("content_pipeline", content_pipeline),
        ("code_orchestrator", code_orchestrator),
        ("database", check_database_connection()),
        ("external_apis", check_api_connectivity())
    ]

    for service_name, service_check in services_to_check:
        try:
            status = await service_check if asyncio.iscoroutine(service_check) else service_check
            health_status["services"][service_name] = {"status": "healthy", "details": status}
        except Exception as e:
            health_status["services"][service_name] = {"status": "unhealthy", "error": str(e)}
            health_status["status"] = "degraded"

    return health_status
```

---

## 🚨 **Backup & Disaster Recovery**

### **Automated Backups**
```bash
#!/bin/bash
# Daily backup script

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups/advanced_systems"

# Database backup
pg_dump -h localhost -U user dbname > $BACKUP_DIR/db_backup_$DATE.sql

# Configuration backup
cp -r ~/.env.d $BACKUP_DIR/env_backup_$DATE/

# Application data backup
tar -czf $BACKUP_DIR/app_backup_$DATE.tar.gz /app/data/

# Upload to cloud storage
aws s3 cp $BACKUP_DIR/ s3://backups/advanced-systems/ --recursive

# Cleanup old backups (keep last 30 days)
find $BACKUP_DIR -name "*.sql" -mtime +30 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +30 -delete
```

### **Disaster Recovery**
```yaml
# Disaster recovery plan
recovery_procedures:
  - name: "API Key Recovery"
    steps:
      - "Access encrypted backup storage"
      - "Decrypt and validate keys"
      - "Update environment files"
      - "Restart services"
    rto: "2 hours"
    rpo: "1 hour"

  - name: "Database Recovery"
    steps:
      - "Identify last good backup"
      - "Restore from backup"
      - "Replay transaction logs"
      - "Validate data integrity"
    rto: "4 hours"
    rpo: "15 minutes"

  - name: "Application Recovery"
    steps:
      - "Deploy from last stable image"
      - "Restore configuration"
      - "Validate service health"
      - "Gradual traffic ramp-up"
    rto: "1 hour"
    rpo: "N/A"
```

---

## 🎯 **Cost Optimization**

### **Resource Optimization**
- **Auto-scaling** based on load
- **Spot instances** for non-critical workloads
- **CDN integration** for static assets
- **Database connection pooling**

### **API Cost Management**
```python
# Intelligent model selection based on cost
MODEL_COSTS = {
    'openai': {'gpt-4': 0.03, 'gpt-3.5': 0.002},
    'anthropic': {'claude-3-opus': 0.015, 'claude-3-haiku': 0.00025},
    'gemini': {'pro': 0.001, 'flash': 0.0005}
}

def select_cost_effective_model(task_type, max_budget=None):
    """Select most cost-effective model for task"""
    # Implementation logic for cost optimization
    pass
```

---

## 📞 **Support & Maintenance**

### **Regular Maintenance Tasks**
- **Weekly**: Monitor logs, check API usage, update dependencies
- **Monthly**: Security updates, performance optimization, backup validation
- **Quarterly**: Major version updates, infrastructure review, cost analysis
- **Annually**: Security audit, disaster recovery testing, architecture review

### **Monitoring Dashboards**
- **Grafana**: Real-time metrics and alerting
- **Kibana**: Log aggregation and analysis
- **Prometheus**: Service monitoring and alerting
- **Custom dashboards**: Business metrics and KPIs

**Ready to deploy? Choose your platform and follow the specific deployment guide above!** 🚀

*Deployment Guide v1.0 - 2025*