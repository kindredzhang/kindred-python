#!/bin/bash

# 颜色定义
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 显示帮助信息
show_help() {
    echo -e "${BLUE}开发环境命令:${NC}"
    echo "  start     - 启动开发服务器 (uvicorn)"
    echo "  gen       - 生成数据库模型"
    echo "  help      - 显示此帮助信息"
}

# 启动开发服务器
start_server() {
    echo -e "${GREEN}启动开发服务器...${NC}"
    uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
}

# 生成数据库模型
generate_models() {
    echo -e "${GREEN}生成数据库模型...${NC}"
    python -m app.utils.gen
}

# 主命令处理
case "$1" in
    "start")
        start_server
        ;;
    "gen")
        generate_models
        ;;
    "help"|"")
        show_help
        ;;
    *)
        echo -e "${BLUE}未知命令: $1${NC}"
        show_help
        exit 1
        ;;
esac