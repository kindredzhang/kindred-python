# app/api/v1/endpoints/products.py
import uuid
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.repositories.product_repository import ProductRepository
from app.schemas.product import (ProductCreate, ProductList, ProductResponse,
                                 ProductUpdate)

# 创建一个 API 路由器实例
# 对比 Spring Boot: @RequestMapping 在 Controller 类上
router = APIRouter(
    prefix="/products", # 定义这个路由器下的所有路径前缀
    tags=["products"], # 用于 OpenAPI 文档中的分组
)

# 创建商品 API
# 对比 Spring Boot: @PostMapping("/products") 方法
@router.post("/", response_model=ProductResponse)
def create_product(
    product: ProductCreate, # 请求体自动验证为 ProductCreate Schema
    db: Session = Depends(get_db) # 注入数据库 Session 依赖
):
    """Create a new product."""
    product_repo = ProductRepository(db)
    return product_repo.create(product)

# 获取所有商品 API
# response_model=List[schemas.Product] 表示返回一个 Product Schema 的列表
# 对比 Spring Boot: @GetMapping("/products") 方法
@router.get("/", response_model=ProductList)
def read_products(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all products with pagination."""
    product_repo = ProductRepository(db)
    products = product_repo.get_all(skip=skip, limit=limit)
    return ProductList(
        items=products,
        total=len(products),  # 注意：这里应该从数据库获取总数
        page=skip // limit + 1,
        size=limit
    )

# 根据 ID 获取单个商品 API
# 对比 Spring Boot: @GetMapping("/products/{product_id}") 方法
@router.get("/{product_id}", response_model=ProductResponse)
def read_product(
    product_id: str,
    db: Session = Depends(get_db)
):
    """Get a product by ID."""
    product_repo = ProductRepository(db)
    db_product = product_repo.get_by_id(product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

# 更新商品 API (PUT)
@router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: str,
    product: ProductUpdate,
    db: Session = Depends(get_db)
):
    """Update a product."""
    product_repo = ProductRepository(db)
    db_product = product_repo.update(product_id, product)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

# 删除商品 API
@router.delete("/{product_id}", response_model=ProductResponse)
def delete_product(
    product_id: str,
    db: Session = Depends(get_db)
):
    """Delete a product."""
    product_repo = ProductRepository(db)
    db_product = product_repo.delete(product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product