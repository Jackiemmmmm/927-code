# 微服务架构 - API Gateway 模式

## 架构概览

```
┌─────────────┐
│  Frontend   │
│ (React App) │
└──────┬──────┘
       │
       │ HTTP Requests
       │ (port 8000)
       ▼
┌──────────────────┐
│   API Gateway    │  ← 主应用 (backend/app)
│   (port 8000)    │
└────────┬─────────┘
         │
         ├─────────────────────┬──────────────────────┐
         │                     │                      │
         ▼                     ▼                      ▼
┌─────────────────┐   ┌─────────────────┐   ┌──────────────┐
│  Appointments   │   │  Items Service  │   │  其他服务    │
│    Service      │   │   (port 8002)   │   │  (login等)   │
│  (port 8001)    │   └─────────────────┘   │  在Gateway中  │
└─────────────────┘                         └──────────────┘
         │                     │
         └─────────────────────┘
                   │
                   ▼
         ┌──────────────────┐
         │   PostgreSQL DB  │
         │   (port 5432)    │
         └──────────────────┘
```

## 服务说明

### 1. API Gateway (端口: 8000)
- **位置**: `backend/app`
- **功能**:
  - 作为统一入口，接收所有前端请求
  - 处理用户认证、登录等核心功能
  - 代理转发 `/appointments` 请求到 Appointments Service
  - 代理转发 `/items` 请求到 Items Service
- **URL**: `http://localhost:8000`
- **文档**: `http://localhost:8000/docs`

### 2. Appointments Service (端口: 8001)
- **位置**: `backend/services/appointments-service`
- **功能**:
  - 医院管理
  - 医生管理
  - 预约管理
  - 时间段管理
- **URL**: `http://localhost:8001`
- **文档**: `http://localhost:8001/docs`

### 3. Items Service (端口: 8002)
- **位置**: `backend/services/items-service`
- **功能**:
  - 物品/项目的 CRUD 操作
- **URL**: `http://localhost:8002`
- **文档**: `http://localhost:8002/docs`

## 启动方式

### 推荐：使用启动脚本

```bash
cd backend
./start-gateway-architecture.sh
```

这将启动所有三个服务：
- ✅ API Gateway (8000)
- ✅ Appointments Service (8001)
- ✅ Items Service (8002)

### 手动启动

```bash
# Terminal 1 - Appointments Service
cd backend/services/appointments-service
../../.venv/bin/python main.py

# Terminal 2 - Items Service
cd backend/services/items-service
../../.venv/bin/python main.py

# Terminal 3 - API Gateway
cd backend
.venv/bin/python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## 前端集成

**重要**: 前端只需要连接 API Gateway (port 8000)，无需直接访问微服务。

### 之前的配置 (仍然有效)
```typescript
// frontend/.env
VITE_API_URL=http://localhost:8000
```

### API 端点
所有请求通过 Gateway 转发：

```typescript
// Appointments (自动转发到 8001)
GET  http://localhost:8000/api/v1/appointments/hospitals
GET  http://localhost:8000/api/v1/appointments/hospitals/{id}/doctors
POST http://localhost:8000/api/v1/appointments/

// Items (自动转发到 8002)
GET  http://localhost:8000/api/v1/items
POST http://localhost:8000/api/v1/items/

// 其他服务 (在 Gateway 内部处理)
POST http://localhost:8000/api/v1/login/access-token
GET  http://localhost:8000/api/v1/users/me
```

## 优势

✅ **前端简化**: 前端只需连接一个端点 (8000)
✅ **服务独立**: 每个微服务可以独立部署、扩展
✅ **故障隔离**: 某个服务故障不影响其他服务
✅ **技术灵活**: 每个服务可以使用不同技术栈
✅ **开发效率**: 团队可以并行开发不同服务

## 停止服务

```bash
# 查看进程
ps aux | grep python

# 停止所有服务
kill <GATEWAY_PID> <APPOINTMENTS_PID> <ITEMS_PID>
```

或者使用启动脚本输出的停止命令。

## 日志查看

```bash
# Gateway 日志
tail -f /tmp/api-gateway.log

# Appointments Service 日志
tail -f /tmp/appointments-service.log

# Items Service 日志
tail -f /tmp/items-service.log
```

## 开发注意事项

1. **添加新服务**:
   - 在 `services/` 下创建新服务目录
   - 在 `app/api/routes/gateway.py` 添加代理路由

2. **修改微服务**:
   - 直接修改 `services/*/` 下的代码
   - 重启对应服务即可

3. **数据库迁移**:
   - 所有服务共享同一个数据库
   - 迁移仍在 `backend/app/alembic` 中管理

## 故障排查

### 服务无法启动
```bash
# 检查端口占用
lsof -i :8000
lsof -i :8001
lsof -i :8002

# 查看日志
cat /tmp/api-gateway.log
cat /tmp/appointments-service.log
cat /tmp/items-service.log
```

### Gateway 无法连接微服务
确保微服务先启动，Gateway 后启动。检查 `app/api/routes/gateway.py` 中的服务 URL 配置。
