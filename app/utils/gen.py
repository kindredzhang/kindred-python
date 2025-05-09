import os
import re
from app.env import USER, PASSWORD, HOST, PORT, DBNAME, ORM_DIR

# 系统表前缀列表，这些表将被排除
SYSTEM_TABLE_PREFIXES = [
    'pg_',
    'information_schema.',
    'sql_'
]

def is_system_table(table_name: str) -> bool:
    """检查是否是系统表"""
    return any(table_name.startswith(prefix) for prefix in SYSTEM_TABLE_PREFIXES)

def get_imports_from_content(content: str) -> set:
    """从内容中提取需要的导入"""
    imports = set()
    
    # 基础导入
    imports.add("import uuid")
    imports.add("from datetime import datetime")
    imports.add("from typing import Optional, List")
    imports.add("from sqlalchemy import Uuid, Double, Index, PrimaryKeyConstraint, Column, Integer, String, Float, DateTime, Boolean, Text, ARRAY, BigInteger, Identity, text")
    imports.add("from sqlalchemy.orm import Mapped, mapped_column")
    imports.add("from app.models.base import Base")
    
    # 根据内容添加特定导入
    if "ARRAY" in content:
        imports.add("from sqlalchemy.dialects.postgresql import ARRAY")
    if "JSON" in content:
        imports.add("from sqlalchemy.dialects.postgresql import JSON")
    if "UUID" in content:
        imports.add("from sqlalchemy.dialects.postgresql import UUID")
    if "Enum" in content:
        imports.add("import enum")
    
    return imports

def generate_models():
    """生成数据库模型文件"""
    # 确保models目录存在
    os.makedirs(ORM_DIR, exist_ok=True)
    
    # 生成基础模型文件
    base_model_content = """from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass
"""
    with open(os.path.join(ORM_DIR, 'base.py'), 'w') as f:
        f.write(base_model_content)

    # 使用sqlacodegen生成所有模型
    temp_file = os.path.join(ORM_DIR, 'temp_models.py')
    command = f"sqlacodegen postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME} --outfile {temp_file}"
    os.system(command)

    # 读取生成的临时文件
    with open(temp_file, 'r') as f:
        content = f.read()

    # 删除临时文件
    os.remove(temp_file)

    # 提取所有表定义
    table_pattern = r'class\s+(\w+)\(Base\):.*?(?=class\s+\w+\(Base\):|$)'
    tables = re.finditer(table_pattern, content, re.DOTALL)

    # 为每个表创建单独的文件
    for table_match in tables:
        table_content = table_match.group(0)
        table_name = table_match.group(1)
        
        # 跳过系统表
        if is_system_table(table_name.lower()):
            continue

        # 获取需要的导入
        imports = get_imports_from_content(table_content)
        
        # 创建表模型文件
        table_file = os.path.join(ORM_DIR, f'{table_name.lower()}.py')
        with open(table_file, 'w') as f:
            # 写入导入语句
            f.write("\n".join(sorted(imports)))
            f.write("\n\n")
            # 写入表定义
            f.write(table_content)
            f.write("\n")

    # 创建__init__.py文件
    init_content = """from app.models.base import Base
"""
    with open(os.path.join(ORM_DIR, '__init__.py'), 'w') as f:
        f.write(init_content)

    print("Models generated successfully!")

if __name__ == "__main__":
    generate_models()