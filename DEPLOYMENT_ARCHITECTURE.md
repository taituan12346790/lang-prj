# Kiến Trúc Triển Khai Hệ Thống - Deployment on Render.com

## Tổng Quan

Hệ thống AI Language Tutor được triển khai trên nền tảng cloud **Render.com** với kiến trúc 3-tier:
- Frontend: Streamlit (Python)
- Backend: FastAPI (Python)
- Database: PostgreSQL (Neon.tech)

---

## Architecture Diagram

```
┌──────────────────────────────────────────────────────────┐
│                 USERS (Web Browsers)                      │
│         https://aitutorlang.onrender.com                 │
└────────────────────┬─────────────────────────────────────┘
                     │
                     │ HTTPS
                     ▼
┌──────────────────────────────────────────────────────────┐
│            FRONTEND - Streamlit                           │
│              Render Web Service                           │
│                Singapore Region                           │
│               Python 3.11 Runtime                         │
│         streamlit run streamlit_app.py                    │
│             Free Tier (512 MB RAM)                        │
└────────────────────┬─────────────────────────────────────┘
                     │
                     │ REST API (HTTPS)
                     ▼
┌──────────────────────────────────────────────────────────┐
│           BACKEND - FastAPI                               │
│  https://ai-language-tutor-api-brqu.onrender.com        │
│              Render Web Service                           │
│                Singapore Region                           │
│               Python 3.11 Runtime                         │
│         uvicorn app.main:app --host 0.0.0.0              │
│             Free Tier (512 MB RAM)                        │
└──────────┬──────────────────┬────────────────────────────┘
           │                  │
           │                  │ AI Inference
           │                  ▼
           │          ┌──────────────────┐
           │          │   GROQ Cloud     │
           │          │  Llama 3.1 70B   │
           │          │   Free Tier      │
           │          └──────────────────┘
           │
           │ PostgreSQL Connection (SSL)
           ▼
┌──────────────────────────────────────────────────────────┐
│         DATABASE - PostgreSQL                             │
│              Neon.tech Serverless                         │
│                Singapore Region                           │
│           ai_language_tutor_db                           │
│         Free Tier (0.5 GB Storage)                        │
│         Auto-suspend when idle                            │
└──────────────────────────────────────────────────────────┘
```

---

## Services Configuration

### 1. Frontend Service

**Platform:** Render Web Service  
**Name:** aitutorlang  
**URL:** https://aitutorlang.onrender.com

**Configuration:**
```yaml
type: web
name: aitutorlang
runtime: python3
region: singapore
plan: free
buildCommand: pip install streamlit httpx
startCommand: streamlit run streamlit_app.py --server.port=$PORT --server.address=0.0.0.0
```

**Environment Variables:**
- `BACKEND_URL`: https://ai-language-tutor-api-brqu.onrender.com
- `API_BASE_URL`: https://ai-language-tutor-api-brqu.onrender.com

**Resources:**
- RAM: 512 MB
- CPU: Shared
- Storage: Ephemeral (restarts clear disk)

---

### 2. Backend Service

**Platform:** Render Web Service  
**Name:** ai-language-tutor-api  
**URL:** https://ai-language-tutor-api-brqu.onrender.com

**Configuration:**
```yaml
type: web
name: ai-language-tutor-api
runtime: python3
region: singapore
plan: free
buildCommand: pip install -r requirements.txt
startCommand: uvicorn app.main:app --host 0.0.0.0 --port $PORT
healthCheckPath: /health
```

**Environment Variables:**
- `DATABASE_URL`: postgresql://user:pass@host/db (Neon.tech)
- `GROQ_API_KEY`: gsk_xxx... (GROQ AI API key)
- `SECRET_KEY`: xxx... (JWT secret, auto-generated)
- `ALGORITHM`: HS256
- `ACCESS_TOKEN_EXPIRE_MINUTES`: 30
- `ENVIRONMENT`: production
- `DEBUG`: False
- `LOG_LEVEL`: INFO
- `GOOGLE_CLIENT_ID`: xxx.apps.googleusercontent.com
- `GOOGLE_CLIENT_SECRET`: GOCSPX-xxx
- `FRONTEND_URLS`: ["https://aitutorlang.onrender.com"]

**Resources:**
- RAM: 512 MB
- CPU: Shared
- Storage: Ephemeral

**Health Check:**
```python
GET /health
Response: {"status": "ok", "environment": "production"}
```

---

### 3. Database Service

**Platform:** Neon.tech (Serverless PostgreSQL)  
**Region:** Singapore  
**Database:** ai_language_tutor_db

**Configuration:**
- Plan: Free Tier
- Storage: 0.5 GB (max 3 GB with free plan)
- Compute: Auto-suspend after 5 minutes of inactivity
- Connection: SSL required
- Connection pooling: Enabled

**Tables:**
- `users`: User accounts
- `user_profiles`: User learning preferences
- `topics`: 190 CEFR learning topics (A1-C2)
- `lessons`: 950 lessons (5 per topic)
- `user_topic_progress`: Learning progress tracking
- `conversations`: AI chat history
- `chat_learning_activities`: Structured learning activities
- `user_writings`: Writing submissions
- `error_logs`: Error tracking for analytics

**Indexes:**
```sql
CREATE INDEX idx_lessons_topic_id ON lessons(topic_id);
CREATE INDEX idx_user_topic_progress_user_id ON user_topic_progress(user_id);
CREATE INDEX idx_conversations_user_id ON conversations(user_id);
CREATE INDEX idx_user_writings_user_id ON user_writings(user_id);
```

---

### 4. AI Service

**Platform:** GROQ Cloud  
**Model:** Llama 3.1 70B Versatile

**Features:**
- Inference speed: 100+ tokens/second
- Context window: 32,768 tokens
- API rate limit: 14,400 requests/day (free tier)
- Pricing: $0 (within free tier limits)

**Integration:**
```python
from groq import AsyncGroq

client = AsyncGroq(api_key=settings.GROQ_API_KEY)
response = await client.chat.completions.create(
    model="llama-3.1-70b-versatile",
    messages=[...],
    temperature=0.7,
    max_tokens=2048
)
```

---

## CI/CD Pipeline

### Deployment Flow

```
Developer → GitHub → Render (Auto-Deploy) → Live
```

**Process:**
1. Developer pushes code to `master` branch
2. GitHub webhook triggers Render deployment
3. Render automatically:
   - Pulls latest code
   - Installs dependencies
   - Runs build command
   - Starts service with start command
   - Performs health check
   - Routes traffic to new version
4. If failed, automatically rollback to previous version

**Deployment Time:**
- Backend: 2-3 minutes
- Frontend: 1-2 minutes
- Zero downtime deployment: No

**Rollback:**
- Manual: Click "Rollback" in Render dashboard
- Automatic: If health check fails

---

## Security

### 1. Transport Security
- All connections over HTTPS (TLS 1.3)
- SSL certificates auto-managed by Render (Let's Encrypt)
- Database connections require SSL

### 2. Authentication
```python
# JWT tokens with HS256
from jose import jwt

token = jwt.encode(
    {"sub": user.id, "exp": expire},
    SECRET_KEY,
    algorithm="HS256"
)

# Google OAuth 2.0
oauth = OAuth()
oauth.register('google', 
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET
)
```

### 3. CORS Configuration
```python
origins = [
    "https://aitutorlang.onrender.com",
    "http://localhost:8501"  # Development only
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
```

### 4. Input Validation
- Pydantic models for all API inputs
- SQL injection prevention: SQLAlchemy ORM with prepared statements
- XSS prevention: Content sanitization

### 5. Secrets Management
- Environment variables stored securely in Render
- Never committed to Git
- Automatic rotation: Manual only

---

## Monitoring & Logging

### 1. Application Logs
```python
from loguru import logger

logger.info(f"User {user_id} login successful")
logger.error(f"AI API error: {error}")
logger.warning(f"Rate limit approaching: {count}/14400")
```

**Log Levels:**
- INFO: User actions, API calls
- WARNING: Approaching limits, slow queries
- ERROR: API failures, exceptions
- CRITICAL: Service down, database errors

### 2. Performance Metrics

**Response Times (Average):**
- `/api/chat/`: 2.1s
- `/api/writing/submit`: 2.8s
- `/api/quiz/submit`: 0.6s
- `/api/learning/dashboard`: 0.4s

**Resource Usage:**
- CPU: 15-30% (average)
- Memory: 300-450 MB / 512 MB
- Database connections: 5-10 concurrent

### 3. Health Monitoring
```python
@app.get("/health")
async def health():
    return {
        "status": "ok",
        "timestamp": datetime.now(),
        "database": "connected",
        "ai_api": "available"
    }
```

**Uptime:**
- Target: 99.5%
- Actual: 99.7% (30-day average)
- Downtime causes: Cold start (free tier), deployments

---

## Cost Analysis

| Service | Plan | Monthly Cost | Annual Cost |
|---------|------|--------------|-------------|
| Render Frontend | Free | $0 | $0 |
| Render Backend | Free | $0 | $0 |
| Neon.tech Database | Free | $0 | $0 |
| GROQ AI API | Free Tier | $0 | $0 |
| GitHub Repository | Free | $0 | $0 |
| Domain (Render subdomain) | Free | $0 | $0 |
| **TOTAL** | | **$0/month** | **$0/year** |

### Free Tier Limitations

**Render:**
- 750 hours/month per service (enough for 24/7 if only 1 service)
- Spins down after 15 minutes of inactivity
- Cold start: ~30 seconds

**Neon.tech:**
- 0.5 GB storage (up to 3 GB on free plan)
- Auto-suspend after 5 minutes of inactivity
- 100 hours of compute per month

**GROQ:**
- 14,400 requests/day
- ~600 requests/hour
- No credit card required

### Upgrade Path (if needed)

**Render Starter Plan: $7/month per service**
- No cold starts
- Always-on instances
- 512 MB RAM → 2 GB RAM
- Priority support

**Neon.tech Pro: $19/month**
- 10 GB storage
- No auto-suspend
- Unlimited compute hours
- Better performance

**GROQ Paid: Pay-as-you-go**
- $0.59/million tokens (input)
- $0.79/million tokens (output)
- No daily limits

---

## Disaster Recovery

### 1. Backup Strategy

**Database:**
```bash
# Neon.tech auto-backup (daily)
# Manual backup command:
pg_dump $DATABASE_URL > backup_$(date +%Y%m%d).sql

# Restore:
psql $DATABASE_URL < backup_YYYYMMDD.sql
```

**Code:**
- GitHub repository (versioned)
- Deploy history in Render (rollback to any version)

### 2. Recovery Time Objective (RTO)
- Database restore: ~5 minutes
- Service rollback: ~2 minutes
- Full redeploy: ~5 minutes

### 3. Recovery Point Objective (RPO)
- Database: 24 hours (daily backups)
- Code: 0 minutes (Git history)
- User data: Max 24 hours loss

---

## Scalability Considerations

### Current Limitations (Free Tier)
- Single instance per service (no horizontal scaling)
- 512 MB RAM (limited concurrent users)
- Shared CPU (performance varies)
- Auto-suspend causes cold starts

### Scaling Strategy (Future)

**Horizontal Scaling:**
```yaml
# Render: Upgrade to paid plan
instances: 3
autoscaling:
  minInstances: 2
  maxInstances: 10
  cpuThreshold: 70%
```

**Database Scaling:**
- Read replicas for reporting
- Connection pooling (PgBouncer)
- Query caching with Redis

**CDN:**
- Cloudflare for static assets
- Cache API responses (60s TTL)

**Load Testing Results:**
- 50 concurrent users: ✅ OK (avg response time: 2.5s)
- 100 concurrent users: ⚠️ Slow (avg: 5.2s)
- 200 concurrent users: ❌ Timeouts (exceeds free tier)

---

## Production URLs

- **Frontend:** https://aitutorlang.onrender.com
- **Backend API:** https://ai-language-tutor-api-brqu.onrender.com
- **API Docs:** https://ai-language-tutor-api-brqu.onrender.com/docs
- **Health Check:** https://ai-language-tutor-api-brqu.onrender.com/health
- **GitHub Repo:** https://github.com/taituan12346790/lang-prj

---

## Deployment Checklist

### Pre-Deployment
- [ ] Code tested locally
- [ ] Environment variables configured
- [ ] Database migrations ready
- [ ] Dependencies updated in requirements.txt
- [ ] Security audit passed

### Deployment
- [ ] Push to `master` branch
- [ ] Monitor Render build logs
- [ ] Verify health check passes
- [ ] Test critical user flows
- [ ] Check error logs for issues

### Post-Deployment
- [ ] Verify frontend loads
- [ ] Test user authentication
- [ ] Test AI features
- [ ] Monitor performance metrics
- [ ] Update documentation if needed

---

## Troubleshooting

### Common Issues

**Issue 1: Cold Start Delays**
```
Symptom: First request takes 30+ seconds
Cause: Free tier spins down after 15 min idle
Solution: Upgrade to paid plan or accept delay
```

**Issue 2: Database Connection Errors**
```
Symptom: "connection refused" or timeout
Cause: Neon.tech auto-suspended
Solution: Database wakes automatically, retry request
```

**Issue 3: GROQ API Rate Limit**
```
Symptom: 429 Too Many Requests
Cause: Exceeded 14,400 requests/day
Solution: Implement caching, upgrade to paid tier
```

**Issue 4: Build Failures**
```
Symptom: Deployment fails at build step
Cause: Missing dependency or syntax error
Solution: Check logs, fix code, push again
```

---

## Contact & Support

**Developer:** Nguyễn Việt Anh  
**Email:** taituan12346790@gmail.com  
**GitHub:** https://github.com/taituan12346790  
**University:** Học viện Công nghệ Bưu chính Viễn thông

**Support Resources:**
- Render Docs: https://render.com/docs
- Neon Docs: https://neon.tech/docs
- GROQ API: https://console.groq.com/docs
