# app/database.py
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

from app.env import DATABASE_URL


# 加载 .env 文件中的环境变量
load_dotenv()

# 从环境变量获取数据库 URL
# 对比 Spring Boot: 从 application.properties/yml 读取 spring.datasource.url

# 创建 SQLAlchemy 引擎
# echo=True 会打印所有执行的 SQL 语句，方便调试，生产环境应关闭
# 对比 Spring Boot: DataSource 配置
engine = create_engine(DATABASE_URL, echo=True)

# 创建一个 Session Local 类
# 每次请求到来时，我们将使用这个类创建一个独立的数据库 Session
# autoflush=False 可以避免不必要的自定刷新
# autocommit=False 确保我们需要手动 commit 事务
# 对比 Spring Boot: SessionFactory 或 EntityManagerFactory，用于获取 EntityManager/Session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


    
# 创建一个基础类，用于 SQLAlchemy 模型
# 对比 Spring Boot: JPA 的 @Entity 需要继承的基类 (虽然不总是显式)
Base = declarative_base()

# 数据库 Session 依赖项
# 这是一个 FastAPI 的 Depends 函数，用于在每个请求中提供一个数据库 Session
# 对比 Spring Boot: 你通常依赖框架自动注入 EntityManager 或 Transactional 代理方法
def get_db():
    db = SessionLocal()
    try:
        yield db # 使用 yield 会让 FastAPI 在请求结束后关闭 Session
    finally:
        db.close() # 确保 Session 被关闭