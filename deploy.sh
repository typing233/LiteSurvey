#!/bin/bash
set -e

echo "╔══════════════════════════════════════╗"
echo "║   轻问 LiteSurvey - 一键部署脚本     ║"
echo "╚══════════════════════════════════════╝"
echo ""

# Check Docker
if ! command -v docker &> /dev/null; then
    echo "❌ 未检测到 Docker，请先安装 Docker"
    echo "   安装指南: https://docs.docker.com/engine/install/"
    exit 1
fi

if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo "❌ 未检测到 Docker Compose，请先安装"
    exit 1
fi

echo "1️⃣  创建数据目录..."
mkdir -p data uploads

echo "2️⃣  构建并启动服务..."
if docker compose version &> /dev/null 2>&1; then
    docker compose up -d --build
else
    docker-compose up -d --build
fi

echo "3️⃣  等待服务就绪..."
sleep 5

# Check backend health
echo "4️⃣  检查服务状态..."
for i in $(seq 1 10); do
    if curl -s http://localhost:8000/api/v1/surveys?page=1\&page_size=1 > /dev/null 2>&1; then
        break
    fi
    if [ $i -eq 10 ]; then
        echo "⚠️  后端服务启动较慢，请稍后手动检查"
    fi
    sleep 2
done

echo ""
echo "✅ 部署完成！"
echo ""
echo "┌──────────────────────────────────────┐"
echo "│  前端地址: http://localhost           │"
echo "│  后台管理: http://localhost/admin/surveys │"
echo "│  API文档:  http://localhost:8000/docs │"
echo "└──────────────────────────────────────┘"
echo ""
echo "提示: 使用 'docker compose logs -f' 查看日志"
echo "      使用 'docker compose down' 停止服务"
