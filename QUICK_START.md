# 快速启动指南 - API Gateway 微服务架构

## 🎯 启动方式

### 方式 1: Docker 部署（推荐）

```bash
cd backend
./start-docker-services.sh
```

**优势**:
- ✅ 环境完全隔离
- ✅ 无需本地安装依赖
- ✅ 包含数据库
- ✅ 跨平台一致性

### 方式 2: 本地运行

```bash
cd backend
./start-gateway-architecture.sh
```

**优势**:
- ✅ 启动更快
- ✅ 调试更方便
- ✅ 适合开发

---

两种方式都会启动：
- ✅ API Gateway (端口 8000)
- ✅ Appointments Service (端口 8001)
- ✅ Items Service (端口 8002)
- ✅ PostgreSQL Database (端口 5432) - Docker 方式自动包含

## 🔍 验证服务

启动后，你会看到健康检查结果：

```
🔍 Health Checks:
   ✓ Appointments Service is healthy (http://localhost:8001)
   ✓ Items Service is healthy (http://localhost:8002)
   ✓ API Gateway is healthy (http://localhost:8000)
```

## 🌐 访问应用

### 前端
前端继续连接原来的地址，**无需修改**：
```
http://localhost:8000
```

### API 文档
- Gateway (推荐): http://localhost:8000/docs
- Appointments Service: http://localhost:8001/docs
- Items Service: http://localhost:8002/docs

## 📡 API 端点

所有请求通过 Gateway (8000) 自动转发到对应的微服务：

```bash
# Appointments API (转发到 8001)
GET  http://localhost:8000/api/v1/appointments/hospitals
GET  http://localhost:8000/api/v1/appointments/hospitals/{id}/doctors
POST http://localhost:8000/api/v1/appointments/

# Items API (转发到 8002)
GET  http://localhost:8000/api/v1/items
POST http://localhost:8000/api/v1/items/

# 其他 API (Gateway 内部处理)
POST http://localhost:8000/api/v1/login/access-token
GET  http://localhost:8000/api/v1/users/me
```

## ✅ 测试示例

```bash
# 测试获取医院列表
curl http://localhost:8000/api/v1/appointments/hospitals

# 测试获取医生列表
curl http://localhost:8000/api/v1/appointments/hospitals/{hospital_id}/doctors

# 测试获取物品列表
curl http://localhost:8000/api/v1/items/
```

## 🛑 停止服务

### Docker 方式

```bash
cd backend
./stop-docker-services.sh
```

### 本地方式

脚本会输出停止命令，例如：
```bash
kill 59116 59114 59115
```

或者：
```bash
cd backend
./stop-all-services.sh
```

## 📝 查看日志

```bash
# Gateway 日志
tail -f /tmp/api-gateway.log

# Appointments Service 日志
tail -f /tmp/appointments-service.log

# Items Service 日志
tail -f /tmp/items-service.log
```

## 🔧 故障排查

### 端口被占用

```bash
# 检查端口
lsof -i :8000
lsof -i :8001
lsof -i :8002

# 释放端口
kill -9 <PID>
```

### 服务无法启动

1. 检查日志文件：`cat /tmp/api-gateway.log`
2. 确认数据库已启动：`docker ps | grep postgres`
3. 确认虚拟环境已激活：`source backend/.venv/bin/activate`

## 📚 详细文档

- 完整架构说明: [backend/MICROSERVICES.md](backend/MICROSERVICES.md)
- 微服务详情: [backend/services/README.md](backend/services/README.md)

## 🎉 开始开发

现在你可以：
1. 启动前端：`cd frontend && npm run dev`
2. 访问：http://localhost:5173
3. 前端会自动连接到 Gateway (8000)
4. 所有功能正常工作，无需修改前端代码！
