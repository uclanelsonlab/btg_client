# 🐳 Docker Usage Guide

This guide explains how to use the BTG Virtual Geneticist API Client with Docker.

## 📋 Prerequisites

- Docker installed on your system
- Docker Compose (usually comes with Docker Desktop)
- Your API token file (`token.txt`)
- Your VCF files and CSV data

## 🚀 Quick Start

### Option 1: Using Docker Compose (Recommended)

1. **Prepare your files**:
   ```bash
   # Create directories
   mkdir -p data results
   
   # Place your files
   cp your_vcf_files/*.vcf.gz data/
   cp your_samplesheet.csv data/
   cp your_token.txt token.txt
   ```

2. **Run the container**:
   ```bash
   # Build and run
   docker-compose up --build
   
   # Or run in background
   docker-compose up -d
   ```

3. **Execute commands**:
   ```bash
   # Interactive mode
   docker-compose exec btg-client python btg_client.py --token token.txt
   
   # Batch upload
   docker-compose exec btg-client python btg_client.py batch-upload --token token.txt --csv data/samplesheet.csv
   
   # Single file upload
   docker-compose exec btg-client python btg_client.py upload --token token.txt --file-path data/file.vcf.gz --prefix sample
   ```

### Option 2: Using Docker Directly

1. **Build the image**:
   ```bash
   docker build -t btg-client .
   ```

2. **Run commands**:
   ```bash
   # Interactive mode
   docker run -it --rm \
     -v $(pwd)/data:/app/data:ro \
     -v $(pwd)/token.txt:/app/token.txt:ro \
     -v $(pwd)/results:/app/results \
     btg-client --token token.txt
   
   # Batch upload
   docker run --rm \
     -v $(pwd)/data:/app/data:ro \
     -v $(pwd)/token.txt:/app/token.txt:ro \
     -v $(pwd)/results:/app/results \
     btg-client batch-upload --token token.txt --csv data/samplesheet.csv
   ```

## 📁 Volume Mounts

The Docker setup uses volume mounts to access your files:

| Host Path | Container Path | Purpose | Read/Write |
|-----------|----------------|---------|------------|
| `./data` | `/app/data` | Your VCF files and CSV | Read-only |
| `./token.txt` | `/app/token.txt` | API token | Read-only |
| `./results` | `/app/results` | Output files | Read/Write |

## 🎯 Usage Examples

### Interactive Mode
```bash
docker-compose exec btg-client python btg_client.py --token token.txt
```

### File Upload
```bash
docker-compose exec btg-client python btg_client.py upload \
  --token token.txt \
  --file-path data/sample.vcf.gz \
  --prefix test
```

### Batch Upload
```bash
docker-compose exec btg-client python btg_client.py batch-upload \
  --token token.txt \
  --csv data/samplesheet.csv
```

### Task Creation
```bash
docker-compose exec btg-client python btg_client.py task \
  --token token.txt \
  --task-config examples/task_config.json
```

### Status Check
```bash
docker-compose exec btg-client python btg_client.py status \
  --token token.txt \
  --submission-id <submission_id>
```

## 🔧 Configuration

### Environment Variables

You can set environment variables in `docker-compose.yml`:

```yaml
services:
  btg-client:
    environment:
      - PYTHONUNBUFFERED=1
      - BTG_API_URL=https://vg-api.btgenomics.com:8082/api
```

### Custom Commands

Override the default command:

```bash
# Run with custom command
docker-compose run btg-client python btg_client.py upload --token token.txt --file-path data/file.vcf.gz

# Run interactive shell
docker-compose run btg-client bash
```

## 🛠️ Development

### Building for Development

```bash
# Build with no cache
docker-compose build --no-cache

# Build specific stage
docker build --target development -t btg-client:dev .
```

### Debugging

```bash
# Run with debug output
docker-compose run btg-client python -u btg_client.py --token token.txt

# Access container shell
docker-compose exec btg-client bash
```

## 📊 File Management

### Input Files
- Place your VCF files in the `data/` directory
- Place your CSV files in the `data/` directory
- Place your token file as `token.txt` in the project root

### Output Files
- Results will be saved to the `results/` directory
- Upload results: `results/upload_results.json`
- Task results: `results/task_results.json`
- Batch results: `results/batch_results.json`

## 🔒 Security

- The container runs as a non-root user (`btg_user`)
- Token files are mounted as read-only
- Data directories are mounted as read-only
- Results directory is writable for output files

## 🐛 Troubleshooting

### Common Issues

**Permission Denied**
```bash
# Fix file permissions
chmod 644 token.txt
chmod 755 data/
```

**File Not Found**
```bash
# Check if files are mounted correctly
docker-compose exec btg-client ls -la /app/data
docker-compose exec btg-client ls -la /app/token.txt
```

**Network Issues**
```bash
# Check container network
docker-compose exec btg-client curl -I https://vg-api.btgenomics.com:8082/api
```

### Debug Commands

```bash
# Check container logs
docker-compose logs btg-client

# Check container status
docker-compose ps

# Restart container
docker-compose restart btg-client
```

## 🚀 Production Deployment

For production use, consider:

1. **Multi-stage builds** for smaller images
2. **Health checks** for monitoring
3. **Resource limits** for stability
4. **Secrets management** for tokens
5. **Logging** for debugging

Example production Dockerfile:

```dockerfile
# Multi-stage build
FROM python:3.11-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user -r requirements.txt

FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .
RUN pip install -e .
USER btg_user
ENTRYPOINT ["python", "btg_client.py"]
```

## 📚 Related Documentation

- [Quick Start Guide](QUICK_START.md)
- [Project Structure](PROJECT_STRUCTURE.md)
- [Batch Usage Guide](BATCH_USAGE.md) 