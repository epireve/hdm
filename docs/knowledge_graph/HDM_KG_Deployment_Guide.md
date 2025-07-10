# HDM Knowledge Graph Deployment Guide

**Version**: 1.0.0  
**Last Updated**: January 2025  
**For**: System Administrators and DevOps

## Table of Contents

1. [Local Development Setup](#local-development-setup)
2. [Production Deployment Options](#production-deployment-options)
3. [GitHub Pages Deployment](#github-pages-deployment)
4. [Docker Deployment](#docker-deployment)
5. [Cloud Platform Deployment](#cloud-platform-deployment)
6. [Performance Tuning](#performance-tuning)
7. [Monitoring & Maintenance](#monitoring--maintenance)
8. [Backup & Recovery](#backup--recovery)
9. [Security Considerations](#security-considerations)

---

## Local Development Setup

### 🛠️ Prerequisites

```bash
# Check Python version (3.8+ required)
python --version

# Check npm (for alternative web servers)
npm --version

# Check git
git --version
```

### 📦 Installation Steps

1. **Clone Repository**
   ```bash
   git clone https://github.com/yourusername/hdm.git
   cd hdm
   ```

2. **Python Environment**
   ```bash
   # Create virtual environment
   python -m venv venv
   
   # Activate environment
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   
   # Install dependencies
   pip install -r requirements.txt
   ```

3. **Generate Data**
   ```bash
   # Process research papers
   cd scripts/graph_generation
   python process_hdm_data.py
   ```

4. **Launch Development Server**
   ```bash
   # Option 1: Python script
   python launch_visualization.py
   
   # Option 2: Python HTTP server
   cd visualization
   python -m http.server 8080
   
   # Option 3: Node.js server
   npx http-server visualization -p 8080
   ```

### 🔧 Development Configuration

```python
# config/development.py
DEBUG = True
HOST = 'localhost'
PORT = 8080
AUTO_RELOAD = True
CACHE_ENABLED = False
LOG_LEVEL = 'DEBUG'
```

## Production Deployment Options

### 🌐 Deployment Methods Comparison

| Method | Pros | Cons | Best For |
|--------|------|------|----------|
| GitHub Pages | Free, easy, CDN | Static only, public | Open research |
| Docker | Portable, consistent | Overhead, complexity | Enterprise |
| Cloud (AWS/GCP) | Scalable, flexible | Cost, maintenance | Large scale |
| VPS | Full control | Manual setup | Custom needs |
| Netlify/Vercel | Simple, fast | Limited backend | Static sites |

### 📋 Pre-Deployment Checklist

- [ ] Remove debug code
- [ ] Minify JavaScript/CSS
- [ ] Optimize images
- [ ] Update configuration
- [ ] Test on production data
- [ ] Set up monitoring
- [ ] Configure backups
- [ ] Review security

## GitHub Pages Deployment

### 🚀 Automatic Deployment

1. **Enable GitHub Pages**
   ```
   Repository → Settings → Pages
   Source: Deploy from branch
   Branch: main
   Folder: /visualization
   ```

2. **GitHub Actions Workflow**
   ```yaml
   # .github/workflows/deploy.yml
   name: Deploy to GitHub Pages
   
   on:
     push:
       branches: [main]
     workflow_dispatch:
   
   jobs:
     deploy:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v3
         
         - name: Setup Python
           uses: actions/setup-python@v4
           with:
             python-version: '3.9'
         
         - name: Install dependencies
           run: |
             pip install -r requirements.txt
         
         - name: Generate graph data
           run: |
             cd scripts/graph_generation
             python process_hdm_data.py
         
         - name: Deploy to GitHub Pages
           uses: peaceiris/actions-gh-pages@v3
           with:
             github_token: ${{ secrets.GITHUB_TOKEN }}
             publish_dir: ./visualization
   ```

3. **Custom Domain (Optional)**
   ```
   # visualization/CNAME
   hdm.yourdomain.com
   ```

### 📝 Configuration for GitHub Pages

```javascript
// js/config.js
const CONFIG = {
    // Use relative paths for GitHub Pages
    DATA_PATH: './data/',
    API_ENDPOINT: null, // No backend
    
    // GitHub Pages URL
    BASE_URL: 'https://username.github.io/hdm/',
    
    // Disable features requiring backend
    FEATURES: {
        REAL_TIME_UPDATES: false,
        USER_ANNOTATIONS: false,
        ANALYTICS: true // Use GA
    }
};
```

## Docker Deployment

### 🐳 Dockerfile

```dockerfile
# Dockerfile
FROM python:3.9-slim

# Install dependencies
RUN apt-get update && apt-get install -y \
    nginx \
    supervisor \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Generate data
RUN cd scripts/graph_generation && \
    python process_hdm_data.py

# Configure nginx
COPY deployment/nginx.conf /etc/nginx/sites-available/default

# Expose port
EXPOSE 80

# Start services
CMD ["nginx", "-g", "daemon off;"]
```

### 🏗️ Docker Compose

```yaml
# docker-compose.yml
version: '3.8'

services:
  hdm-viz:
    build: .
    ports:
      - "80:80"
    volumes:
      - ./data:/app/visualization/data
      - ./logs:/var/log
    environment:
      - NODE_ENV=production
    restart: unless-stopped
    
  # Optional: Data processing service
  hdm-processor:
    build: 
      context: .
      dockerfile: Dockerfile.processor
    volumes:
      - ./data:/app/data
      - ./research_papers_complete.csv:/app/input.csv
    environment:
      - PROCESS_INTERVAL=3600 # Process hourly
    restart: unless-stopped
```

### 🚀 Deployment Commands

```bash
# Build and run
docker-compose up -d

# View logs
docker-compose logs -f

# Update data
docker-compose exec hdm-processor python process_hdm_data.py

# Backup data
docker-compose exec hdm-viz tar -czf /backup/hdm-data.tar.gz /app/visualization/data
```

## Cloud Platform Deployment

### ☁️ AWS Deployment

#### S3 + CloudFront (Static)

```bash
# Install AWS CLI
pip install awscli

# Configure credentials
aws configure

# Create S3 bucket
aws s3 mb s3://hdm-visualization

# Enable static hosting
aws s3 website s3://hdm-visualization \
  --index-document index.html \
  --error-document error.html

# Sync files
aws s3 sync visualization/ s3://hdm-visualization \
  --delete \
  --cache-control "max-age=3600"

# Create CloudFront distribution
aws cloudfront create-distribution \
  --origin-domain-name hdm-visualization.s3.amazonaws.com \
  --default-root-object index.html
```

#### EC2 Deployment

```bash
# Launch EC2 instance (Ubuntu 20.04)
# Connect via SSH
ssh -i key.pem ubuntu@ec2-instance

# Install dependencies
sudo apt update
sudo apt install -y python3-pip nginx git

# Clone and setup
git clone https://github.com/yourusername/hdm.git
cd hdm
pip3 install -r requirements.txt

# Generate data
cd scripts/graph_generation
python3 process_hdm_data.py

# Configure nginx
sudo cp deployment/nginx.conf /etc/nginx/sites-available/hdm
sudo ln -s /etc/nginx/sites-available/hdm /etc/nginx/sites-enabled/
sudo systemctl restart nginx
```

### 🌩️ Google Cloud Platform

```bash
# Install gcloud CLI
curl https://sdk.cloud.google.com | bash

# Initialize
gcloud init

# Deploy to App Engine
cat > app.yaml << EOF
runtime: python39
handlers:
- url: /
  static_files: visualization/index.html
  upload: visualization/index.html
- url: /(.*)
  static_files: visualization/\1
  upload: visualization/.*
EOF

gcloud app deploy

# Or use Cloud Run
gcloud run deploy hdm-viz \
  --image gcr.io/PROJECT/hdm-viz \
  --platform managed \
  --port 80
```

### 🔷 Azure Deployment

```bash
# Azure Static Web Apps
az staticwebapp create \
  --name hdm-visualization \
  --resource-group hdm-rg \
  --source https://github.com/yourusername/hdm \
  --location westus2 \
  --branch main \
  --app-location "/visualization" \
  --api-location "" \
  --output-location ""
```

## Performance Tuning

### ⚡ Frontend Optimization

1. **Asset Optimization**
   ```bash
   # Minify JavaScript
   terser js/graph.js -o js/graph.min.js
   terser js/interactions.js -o js/interactions.min.js
   terser js/filters.js -o js/filters.min.js
   
   # Minify CSS
   cssnano css/style.css css/style.min.css
   
   # Compress JSON
   python -m json.tool --compact data/graph_data.json > data/graph_data.min.json
   ```

2. **Lazy Loading**
   ```javascript
   // Load data progressively
   async function loadDataProgressive() {
       // Load essential data first
       const coreData = await fetch('data/core_nodes.json');
       renderInitialGraph(coreData);
       
       // Load additional data
       const fullData = await fetch('data/graph_data.json');
       updateGraph(fullData);
   }
   ```

3. **Caching Strategy**
   ```nginx
   # nginx.conf
   location ~* \.(json)$ {
       expires 1h;
       add_header Cache-Control "public, immutable";
   }
   
   location ~* \.(js|css)$ {
       expires 1y;
       add_header Cache-Control "public, immutable";
   }
   ```

### 🚀 Backend Optimization

1. **Data Processing**
   ```python
   # Parallel processing
   from multiprocessing import Pool
   
   def process_papers_parallel(papers, n_workers=4):
       with Pool(n_workers) as pool:
           results = pool.map(process_single_paper, papers)
       return results
   ```

2. **Memory Management**
   ```python
   # Use generators for large datasets
   def read_papers_chunked(filepath, chunk_size=1000):
       for chunk in pd.read_csv(filepath, chunksize=chunk_size):
           yield process_chunk(chunk)
   ```

3. **Database Optimization** (if using)
   ```sql
   -- Create indexes
   CREATE INDEX idx_papers_year ON papers(year);
   CREATE INDEX idx_papers_relevancy ON papers(relevancy);
   CREATE INDEX idx_authors_name ON authors(name);
   
   -- Optimize queries
   EXPLAIN ANALYZE SELECT * FROM papers WHERE year >= 2020;
   ```

## Monitoring & Maintenance

### 📊 Monitoring Setup

1. **Application Monitoring**
   ```javascript
   // Add performance monitoring
   const observer = new PerformanceObserver((list) => {
       for (const entry of list.getEntries()) {
           console.log(`${entry.name}: ${entry.duration}ms`);
           // Send to analytics
           if (window.ga) {
               ga('send', 'timing', 'Graph', entry.name, Math.round(entry.duration));
           }
       }
   });
   observer.observe({ entryTypes: ['measure'] });
   ```

2. **Server Monitoring**
   ```bash
   # Install monitoring tools
   sudo apt install -y htop iotop nethogs
   
   # Setup logging
   mkdir -p /var/log/hdm
   
   # Log rotation
   cat > /etc/logrotate.d/hdm << EOF
   /var/log/hdm/*.log {
       daily
       rotate 14
       compress
       delaycompress
       notifempty
       create 0640 www-data www-data
   }
   EOF
   ```

3. **Health Checks**
   ```python
   # health_check.py
   import requests
   import json
   
   def check_health():
       checks = {
           'web_server': check_web_server(),
           'data_files': check_data_files(),
           'graph_load': check_graph_load(),
           'performance': check_performance()
       }
       
       return {
           'status': 'healthy' if all(checks.values()) else 'unhealthy',
           'checks': checks,
           'timestamp': datetime.now().isoformat()
       }
   ```

### 🔧 Maintenance Tasks

#### Daily
- [ ] Check application logs
- [ ] Monitor performance metrics
- [ ] Verify data integrity
- [ ] Review error reports

#### Weekly
- [ ] Update dependencies
- [ ] Run security scans
- [ ] Backup data
- [ ] Clean temporary files

#### Monthly
- [ ] Performance analysis
- [ ] Update documentation
- [ ] Review user feedback
- [ ] Plan updates

### 📝 Maintenance Scripts

```bash
#!/bin/bash
# maintenance.sh

# Backup data
backup_data() {
    BACKUP_DIR="/backups/$(date +%Y%m%d)"
    mkdir -p $BACKUP_DIR
    cp -r visualization/data $BACKUP_DIR/
    echo "Backup completed: $BACKUP_DIR"
}

# Clean logs
clean_logs() {
    find /var/log/hdm -name "*.log" -mtime +30 -delete
    echo "Old logs cleaned"
}

# Update data
update_data() {
    cd /app/scripts/graph_generation
    python process_hdm_data.py
    echo "Data updated"
}

# Run all maintenance
backup_data
clean_logs
update_data
```

## Backup & Recovery

### 💾 Backup Strategy

1. **Data Backup**
   ```bash
   # Automated backup script
   #!/bin/bash
   BACKUP_ROOT="/backups"
   DATE=$(date +%Y%m%d_%H%M%S)
   BACKUP_DIR="$BACKUP_ROOT/hdm_$DATE"
   
   # Create backup
   mkdir -p $BACKUP_DIR
   
   # Backup data files
   cp -r visualization/data $BACKUP_DIR/
   
   # Backup configuration
   cp -r config $BACKUP_DIR/
   
   # Backup source CSV
   cp research_papers_complete.csv $BACKUP_DIR/
   
   # Compress
   tar -czf $BACKUP_DIR.tar.gz $BACKUP_DIR
   rm -rf $BACKUP_DIR
   
   # Keep only last 30 days
   find $BACKUP_ROOT -name "hdm_*.tar.gz" -mtime +30 -delete
   ```

2. **Database Backup** (if applicable)
   ```bash
   # PostgreSQL backup
   pg_dump hdm_db > $BACKUP_DIR/database.sql
   
   # MongoDB backup
   mongodump --db hdm --out $BACKUP_DIR/mongodb
   ```

3. **Cloud Backup**
   ```bash
   # AWS S3 backup
   aws s3 sync $BACKUP_ROOT s3://hdm-backups/
   
   # Google Cloud Storage
   gsutil -m rsync -r $BACKUP_ROOT gs://hdm-backups/
   ```

### 🔄 Recovery Procedures

1. **Data Recovery**
   ```bash
   # List available backups
   ls -la /backups/hdm_*.tar.gz
   
   # Extract backup
   tar -xzf /backups/hdm_20250115_120000.tar.gz
   
   # Restore data
   cp -r hdm_20250115_120000/data/* visualization/data/
   
   # Verify integrity
   python scripts/verify_data.py
   ```

2. **Disaster Recovery Plan**
   - **RTO** (Recovery Time Objective): 2 hours
   - **RPO** (Recovery Point Objective): 24 hours
   - **Backup Locations**: Local + Cloud
   - **Test Frequency**: Monthly

## Security Considerations

### 🔒 Security Hardening

1. **Web Server Security**
   ```nginx
   # nginx security headers
   add_header X-Frame-Options "SAMEORIGIN" always;
   add_header X-Content-Type-Options "nosniff" always;
   add_header X-XSS-Protection "1; mode=block" always;
   add_header Referrer-Policy "no-referrer-when-downgrade" always;
   add_header Content-Security-Policy "default-src 'self' https:; script-src 'self' 'unsafe-inline' https://d3js.org; style-src 'self' 'unsafe-inline';" always;
   
   # Disable server tokens
   server_tokens off;
   
   # SSL configuration (if using HTTPS)
   ssl_protocols TLSv1.2 TLSv1.3;
   ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256;
   ssl_prefer_server_ciphers off;
   ```

2. **Access Control**
   ```nginx
   # Basic authentication
   location / {
       auth_basic "HDM Knowledge Graph";
       auth_basic_user_file /etc/nginx/.htpasswd;
   }
   
   # IP whitelist
   location / {
       allow 192.168.1.0/24;
       allow 10.0.0.0/8;
       deny all;
   }
   ```

3. **Input Validation**
   ```javascript
   // Sanitize user input
   function sanitizeInput(input) {
       return input
           .replace(/[<>]/g, '')
           .trim()
           .substring(0, 100);
   }
   
   // Validate file uploads
   function validateCSV(file) {
       const maxSize = 50 * 1024 * 1024; // 50MB
       const allowedTypes = ['text/csv', 'application/csv'];
       
       if (file.size > maxSize) {
           throw new Error('File too large');
       }
       
       if (!allowedTypes.includes(file.type)) {
           throw new Error('Invalid file type');
       }
   }
   ```

### 🛡️ Security Checklist

- [ ] Enable HTTPS
- [ ] Set security headers
- [ ] Implement rate limiting
- [ ] Regular security updates
- [ ] Access logging
- [ ] Input validation
- [ ] Error handling (no stack traces)
- [ ] Secure file permissions
- [ ] Remove debug endpoints
- [ ] API authentication (if applicable)

---

## 🚀 Quick Deployment Commands

### Local Development
```bash
python launch_visualization.py
```

### GitHub Pages
```bash
git push origin main
# Automatic deployment via Actions
```

### Docker
```bash
docker-compose up -d
```

### AWS S3
```bash
aws s3 sync visualization/ s3://hdm-viz --delete
```

### Heroku
```bash
heroku create hdm-viz
git push heroku main
```

---

**Document Control**  
- **Author**: HDM Development Team  
- **Review Cycle**: Quarterly  
- **Next Review**: April 2025  
- **Distribution**: Internal/DevOps