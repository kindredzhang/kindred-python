# app/main.py
from fastapi import FastAPI
from app.api.v1.endpoints import products # 导入商品相关的路由器
from app import models # 导入 models 模块，确保 SQLAlchemy 知道模型定义
from app.database import engine # 导入数据库引擎

# 创建 FastAPI 应用实例
app = FastAPI(
    title="My FastAPI Product API", # API 标题，用于文档
    description="A simple API to manage products", # API 描述
    version="1.0.0", # API 版本
    # 可以添加其他元数据
)

# 可选：在应用启动时创建数据库表 (如果它们不存在)
# 在生产环境中，通常会使用数据库迁移工具 (如 Alembic) 来管理 schema 改动
@app.on_event("startup")
def startup_event():
    print("Creating database tables...")
    # 创建所有继承自 Base 的模型对应的数据库表
    # 对比 Spring Boot: ddl-auto: create 或 create-drop
    models.Base.metadata.create_all(bind=engine)
    print("Database tables created (if they didn't exist).")


# 包含商品相关的路由器
# 所有 /products 相关的路由都会由 products.router 处理
# 对比 Spring Boot: ComponentScan 扫描 Controller，或者手动配置 DispatcherServlet
app.include_router(products.router, prefix="/api/v1") # 添加版本前缀