# Docker 微服务部署指南

## 🐳 快速启动

### 一键启动所有服务

```bash
cd backend
./start-docker-services.sh
```

这将启动：
- ✅ PostgreSQL 数据库 (5432)
- ✅ Appointments Service (8001)
- ✅ Items Service (8002)
- ✅ API Gateway (8000)

### 一键停止所有服务

```bash
cd backend
./stop-docker-services.sh
```

## 📋 前提条件

1. **安装 Docker**
   - Docker Desktop (Mac/Windows)
   - Docker Engine + Docker Compose (Linux)

2. **配置环境变量** (可选)

   在 `backend/` 目录创建 `.env` 文件：
   ```bash
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=your_secure_password
   POSTGRES_DB=app
   SECRET_KEY=your_secret_key
   FIRST_SUPERUSER=admin@example.com
   FIRST_SUPERUSER_PASSWORD=admin_password
   ```

   如果不创建，将使用默认值。

## 🏗️ 架构说明

### Docker 网络架构

```
┌─────────────────────────────────────────────────┐
│         Docker Network: microservices-network   │
│                                                 │
│  ┌─────────┐  ┌──────────┐  ┌────────┐  ┌────┐│
│  │   API   │→ │Appoint   │  │ Items  │  │ DB ││
│  │ Gateway │→ │ Service  │  │Service │  │    ││
│  │  :8000  │  │  :8001   │  │ :8002  │  │5432││
│  └─────────┘  └──────────┘  └────────┘  └────┘│
│       ↑                                         │
└───────┼─────────────────────────────────────────┘
        │
   [Frontend]
```

### 服务通信

- **外部访问**: 通过 `localhost:8000` (API Gateway)
- **服务间通信**: 使用 Docker 服务名
  - `appointments-service:8001`
  - `items-service:8002`
  - `db:5432`

## 🔧 常用命令

### 查看服务状态

```bash
docker-compose -f backend/docker-compose.microservices.yml ps
```

### 查看日志

```bash
# 所有服务日志
docker-compose -f backend/docker-compose.microservices.yml logs -f

# 特定服务日志
docker-compose -f backend/docker-compose.microservices.yml logs -f api-gateway
docker-compose -f backend/docker-compose.microservices.yml logs -f appointments-service
docker-compose -f backend/docker-compose.microservices.yml logs -f items-service
docker-compose -f backend/docker-compose.microservices.yml logs -f db
```

### 重启服务

```bash
# 重启所有服务
docker-compose -f backend/docker-compose.microservices.yml restart

# 重启单个服务
docker-compose -f backend/docker-compose.microservices.yml restart api-gateway
```

### 重新构建服务

```bash
# 重新构建所有服务
docker-compose -f backend/docker-compose.microservices.yml build

# 重新构建并启动
docker-compose -f backend/docker-compose.microservices.yml up -d --build

# 重新构建特定服务
docker-compose -f backend/docker-compose.microservices.yml build appointments-service
```

### 进入容器

```bash
# 进入 API Gateway 容器
docker-compose -f backend/docker-compose.microservices.yml exec api-gateway bash

# 进入数据库容器
docker-compose -f backend/docker-compose.microservices.yml exec db psql -U postgres -d app
```

### 清理

```bash
# 停止并删除容器
docker-compose -f backend/docker-compose.microservices.yml down

# 停止、删除容器和数据卷（⚠️ 会删除数据库数据）
docker-compose -f backend/docker-compose.microservices.yml down -v

# 清理未使用的 Docker 资源
docker system prune -a
```

## 🔍 健康检查

所有服务都配置了健康检查：

```bash
# 检查 API Gateway
curl http://localhost:8000/api/v1/utils/health-check/

# 检查 Appointments Service
curl http://localhost:8001/health

# 检查 Items Service
curl http://localhost:8002/health
```

## 🐛 故障排查

### 服务无法启动

1. **检查日志**
   ```bash
   docker-compose -f backend/docker-compose.microservices.yml logs <service-name>
   ```

2. **检查端口占用**
   ```bash
   lsof -i :8000
   lsof -i :8001
   lsof -i :8002
   lsof -i :5432
   ```

3. **重新构建**
   ```bash
   docker-compose -f backend/docker-compose.microservices.yml down
   docker-compose -f backend/docker-compose.microservices.yml build --no-cache
   docker-compose -f backend/docker-compose.microservices.yml up -d
   ```

### 数据库连接失败

1. **检查数据库容器状态**
   ```bash
   docker-compose -f backend/docker-compose.microservices.yml ps db
   ```

2. **检查数据库健康状态**
   ```bash
   docker-compose -f backend/docker-compose.microservices.yml exec db pg_isready -U postgres
   ```

3. **查看数据库日志**
   ```bash
   docker-compose -f backend/docker-compose.microservices.yml logs db
   ```

### Gateway 无法连接微服务

1. **确认服务都已启动**
   ```bash
   docker-compose -f backend/docker-compose.microservices.yml ps
   ```

2. **检查网络连接**
   ```bash
   docker-compose -f backend/docker-compose.microservices.yml exec api-gateway ping appointments-service
   docker-compose -f backend/docker-compose.microservices.yml exec api-gateway ping items-service
   ```

## 📊 性能优化

### 限制资源使用

在 `docker-compose.microservices.yml` 中添加资源限制：

```yaml
services:
  api-gateway:
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
        reservations:
          cpus: '0.25'
          memory: 256M
```

### 查看资源使用

```bash
docker stats
```

## 🔒 生产环境注意事项

1. **修改默认密码**
   - 更改 `POSTGRES_PASSWORD`
   - 更改 `SECRET_KEY`
   - 更改 `FIRST_SUPERUSER_PASSWORD`

2. **配置 CORS**
   - 在 `.env` 中设置 `BACKEND_CORS_ORIGINS`

3. **使用环境变量文件**
   - 不要将 `.env` 提交到 Git
   - 添加到 `.gitignore`

4. **使用 Docker Secrets** (生产环境)
   ```yaml
   secrets:
     postgres_password:
       external: true
   ```

5. **备份数据库**
   ```bash
   docker-compose -f backend/docker-compose.microservices.yml exec db pg_dump -U postgres app > backup.sql
   ```

## 📝 与本地开发对比

| 特性 | 本地开发 | Docker 部署 |
|------|---------|------------|
| 启动命令 | `./start-gateway-architecture.sh` | `./start-docker-services.sh` |
| 环境隔离 | ❌ | ✅ |
| 依赖管理 | 手动 | 自动 |
| 跨平台 | ⚠️ | ✅ |
| 调试 | 容易 | 需要进入容器 |
| 性能 | 更快 | 略慢（容器开销） |
| 适用场景 | 开发调试 | 测试/生产 |

## 🚀 推荐工作流

**开发阶段**: 使用本地启动（快速迭代）
```bash
./backend/start-gateway-architecture.sh
```

**测试/部署**: 使用 Docker（环境一致性）
```bash
./backend/start-docker-services.sh
```

## 📚 更多资源

- [Docker 官方文档](https://docs.docker.com/)
- [Docker Compose 文档](https://docs.docker.com/compose/)
- [项目架构文档](backend/MICROSERVICES.md)
