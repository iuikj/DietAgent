"""
营养师Agent API服务 - 基于FastAPI的Web服务
"""
import base64
import io
import json
from pathlib import Path
from typing import Optional, Dict

import uvicorn
from PIL import Image
from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel


from langgraph_sdk import get_client

app = FastAPI(
    title="营养师AI Agent API",
    description="基于LangGraph和Qwen模型的智能营养分析服务",
    version="1.0.0"
)
static_dir = Path(__file__).resolve().parent.parent / "static"
# 挂载静态文件
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


client = get_client(url="http://127.0.0.1:2024")


class ImageAnalysisRequest(BaseModel):
    """图片分析请求模型"""
    image_data: str
    user_preferences: Optional[Dict] = None


class UserPreferences(BaseModel):
    """用户偏好设置"""
    dietary_restrictions: Optional[list] = []  # 饮食限制
    health_goals: Optional[list] = []  # 健康目标
    allergies: Optional[list] = []  # 过敏信息
    activity_level: Optional[str] = "moderate"  # 运动水平
    age: Optional[int] = None
    gender: Optional[str] = None
    weight: Optional[float] = None
    height: Optional[float] = None


@app.get("/")
async def root():
    """提供主页HTML文件"""
    return FileResponse(static_dir / "index.html")


@app.get("/api")
async def api_info():
    """API信息"""
    return {
        "message": "营养师AI Agent API",
        "version": "1.0.0",
        "endpoints": {
            "upload_image": "/analyze/upload",
            "analyze_base64": "/analyze/base64",
            "health_check": "/health"
        }
    }


@app.get("/health")
async def health_check():
    """健康检查端点"""
    return {"status": "healthy", "service": "nutrition-agent"}


@app.post("/analyze/upload")
async def analyze_uploaded_image(
        file: UploadFile = File(...),
        preferences: Optional[str] = Form(None)
):
    """
    上传图片进行营养分析

    Args:
        file: 上传的图片文件
        preferences: 用户偏好设置(JSON字符串)

    Returns:
        营养分析结果
    """
    try:
        # 验证文件类型
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="上传的文件必须是图片格式")

        # 读取并编码图片
        image_data = await file.read()
        image_base64 = base64.b64encode(image_data).decode('utf-8')

        # 解析用户偏好
        user_prefs = {}
        if preferences:
            try:
                user_prefs = json.loads(preferences)
            except json.JSONDecodeError:
                raise HTTPException(status_code=400, detail="用户偏好设置格式错误")

        # 调用营养师Agent进行分析
        assistant = await client.assistants.create(
            graph_id="nutrition_agent",
            config={
                "configurable": {
                    "vision_model_provider": "openai",
                    "vision_model": "gpt-4.1-nano-2025-04-14",
                    "analysis_model_provider": "openai",
                    "analysis_model": "o3-mini-2025-01-31"
                }
            }
        )
        thread = await client.threads.create()
        run = await client.runs.create(
            assistant_id=assistant["assistant_id"],
            thread_id=thread['thread_id'],
            input={
                "image_data": image_base64,
                "user_preferences": user_prefs
            }
        )
        print("Processing...")
        while True:
            result = await client.threads.get_state(thread["thread_id"])
            current_step = result.get('values').get("current_step")
            print(f"Current step: {current_step}")
            if result.get('values').get("error_message") is not None:
                print(result.get('values').get("error_message"))
                raise HTTPException(status_code=500, detail=result["error_message"])
            if current_step == "completed":
                print(json.dumps(result,indent=2))
                break
        # result = await client.threads.get_state(thread["thread_id"])
        print(result)

        result=result.get("values")

        # 格式化返回结果
        response = {
            "success": True,
            "filename": file.filename,
            "analysis": {
                "image_description": result["image_analysis"],
                "nutrition_facts": result["nutrition_analysis"] if result["nutrition_analysis"] else None,
                "recommendations": result["nutrition_advice"] if result["nutrition_advice"] else None
            },
            "processing_step": result["current_step"]
        }

        return JSONResponse(content=response)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"处理图片时发生错误: {str(e)}")







@app.get("/models/available")
async def get_available_models():
    """获取可用的AI模型列表"""
    return {
        "vision_models": ["qwen-vl-max", "qwen-vl-plus"],
        "analysis_models": ["qwen-plus-latest", "qwen-max", "qwen3-235b-a22b"],
        "current_config": {
            "vision_model": "qwen-vl-max",
            "analysis_model": "qwen-plus-latest"
        }
    }


@app.post("/preferences/validate")
async def validate_user_preferences(preferences: UserPreferences):
    """验证用户偏好设置"""
    try:
        # 这里可以添加偏好验证逻辑
        validated_prefs = preferences.dict(exclude_unset=True)

        return {
            "valid": True,
            "preferences": validated_prefs,
            "recommendations": [
                "偏好设置已验证",
                "建议定期更新健康目标"
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"偏好验证失败: {str(e)}")


if __name__ == "__main__":
    uvicorn.run(
        "server:app",
        # host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
