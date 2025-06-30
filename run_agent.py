#!/usr/bin/env python3
"""
营养师AI Agent启动脚本
"""
import asyncio
import os
import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

async def main():
    """主函数"""
    print("🥗 启动营养师AI Agent...")
    
    # 检查环境变量
    if not os.getenv("DASHSCOPE_API_KEY"):
        print("❌ 错误: 请设置 DASHSCOPE_API_KEY 环境变量")
        sys.exit(1)
    
    print("✅ 环境检查通过")
    
    # 启动API服务器
    import uvicorn
    from prc.api_server import app
    
    print("🚀 启动API服务器在 http://localhost:8000")
    print("📱 打开浏览器访问 http://localhost:8000 使用Web界面")
    print("📚 API文档地址: http://localhost:8000/docs")
    
    config = uvicorn.Config(
        app=app,
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
    
    server = uvicorn.Server(config)
    await server.serve()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 服务已停止")
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        sys.exit(1)