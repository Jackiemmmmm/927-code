# Microservices Architecture

这个项目已被拆分为微服务架构，每个服务独立运行。

## 服务列表

### 1. Appointments Service (端口: 8001)
处理医疗预约相关的所有功能：
- 医院管理
- 医生管理
- 预约管理
- 时间段管理

**API 端点**: `http://localhost:8001/api/v1/appointments`

### 2. Items Service (端口: 8002)
处理物品/项目管理功能：
- 创建、读取、更新、删除物品

**API 端点**: `http://localhost:8002/api/v1/items`

## 安装依赖

```bash
# 在 services 目录下
pip install -r requirements.txt
```

或者使用项目的虚拟环境：

```bash
cd ..
source .venv/bin/activate  # 或者在 Windows: .venv\Scripts\activate
cd services
pip install -r requirements.txt
```

## 如何运行

### 方式 1: 分别启动每个服务

```bash
# 启动 Appointments Service
cd services/appointments-service
python main.py

# 在另一个终端启动 Items Service
cd services/items-service
python main.py
```

### 方式 2: 使用启动脚本

```bash
cd services
./start-all.sh
```

### 方式 3: 使用 Docker Compose

```bash
docker-compose -f docker-compose.microservices.yml up
```

## 健康检查

- Appointments Service: `http://localhost:8001/health`
- Items Service: `http://localhost:8002/health`

## API 文档

- Appointments Service: `http://localhost:8001/docs`
- Items Service: `http://localhost:8002/docs`

## 目录结构

```
services/
├── shared/                 # 共享代码
│   ├── config.py          # 数据库配置
│   └── database.py        # 数据库连接
├── appointments-service/   # 预约服务
│   ├── main.py
│   ├── models.py
│   └── routes.py
├── items-service/          # 物品服务
│   ├── main.py
│   ├── models.py
│   └── routes.py
└── README.md
```

## 注意事项

1. 所有服务共享同一个数据库
2. 确保数据库迁移已经运行
3. 需要在项目根目录有 `.env` 文件配置数据库连接
4. 前端需要配置多个 API 端点，或使用 API Gateway
