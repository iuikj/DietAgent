#!/usr/bin/env python3
"""
营养师AI Agent测试脚本
"""
import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from prc.nutrition_agent import NutritionAgent, encode_image_to_base64

def test_agent_with_sample():
    """使用示例图片测试Agent"""
    print("🧪 开始测试营养师Agent...")
    
    # 检查是否有示例图片
    sample_image_path = project_root / "test_images" / "sample_food.jpg"
    
    if not sample_image_path.exists():
        print("⚠️  未找到测试图片，将使用base64pic.py中的现有图片路径")
        # 使用现有代码中的图片路径
        existing_image_path = r"D:\电脑管家迁移文件\Downloads\wx_camera_1751172800244.jpg"
        if Path(existing_image_path).exists():
            sample_image_path = existing_image_path
        else:
            print("❌ 未找到测试图片，请提供食物图片进行测试")
            return False
    
    try:
        # 初始化Agent
        print("🔄 初始化营养师Agent...")
        agent = NutritionAgent()
        
        # 编码图片
        print("📷 编码图片...")
        image_data = encode_image_to_base64(str(sample_image_path))
        
        # 设置用户偏好
        user_preferences = {
            "age": 25,
            "gender": "female",
            "weight": 55,
            "height": 165,
            "activity_level": "moderate",
            "dietary_restrictions": ["低盐"],
            "health_goals": ["减脂", "增肌"]
        }
        
        # 处理图片
        print("🔍 开始分析图片...")
        result = agent.process_image(image_data, user_preferences)
        
        # 输出结果
        print("\n" + "="*50)
        print("📊 分析结果:")
        print("="*50)
        
        if result["success"]:
            print("✅ 分析成功!")
            
            # 图片分析
            if result["image_analysis"]:
                print("\n🔍 图片分析:")
                print("-" * 30)
                print(result["image_analysis"])
            
            # 营养分析
            if result["nutrition_analysis"]:
                print("\n📈 营养分析:")
                print("-" * 30)
                nutrition = result["nutrition_analysis"]
                print(f"识别食物: {nutrition.food_items}")
                print(f"总热量: {nutrition.total_calories} 大卡")
                print(f"蛋白质: {nutrition.macronutrients.get('protein', 'N/A')} 克")
                print(f"脂肪: {nutrition.macronutrients.get('fat', 'N/A')} 克")
                print(f"碳水化合物: {nutrition.macronutrients.get('carbohydrates', 'N/A')} 克")
                print(f"健康评分: {nutrition.health_score}/10")
            
            # 营养建议
            if result["nutrition_advice"]:
                print("\n💡 营养建议:")
                print("-" * 30)
                advice = result["nutrition_advice"]
                
                if advice.recommendations:
                    print("具体建议:")
                    for i, rec in enumerate(advice.recommendations, 1):
                        print(f"  {i}. {rec}")
                
                if advice.dietary_tips:
                    print("\n饮食技巧:")
                    for i, tip in enumerate(advice.dietary_tips, 1):
                        print(f"  {i}. {tip}")
                
                if advice.alternative_foods:
                    print("\n推荐替代食物:")
                    for i, food in enumerate(advice.alternative_foods, 1):
                        print(f"  {i}. {food}")
        
        else:
            print("❌ 分析失败:")
            print(result["error_message"])
            return False
        
        print("\n" + "="*50)
        print("✅ 测试完成!")
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
        return False

def test_api_endpoints():
    """测试API端点"""
    print("\n🌐 测试API端点...")
    
    try:
        import requests
        
        # 测试健康检查
        response = requests.get("http://localhost:8000/health", timeout=10)
        if response.status_code == 200:
            print("✅ 健康检查端点正常")
        else:
            print("❌ 健康检查端点异常")
            return False
        
        # 测试模型信息
        response = requests.get("http://localhost:8000/models/available", timeout=10)
        if response.status_code == 200:
            print("✅ 模型信息端点正常")
            models = response.json()
            print(f"当前使用模型: {models['current_config']}")
        else:
            print("❌ 模型信息端点异常")
        
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到API服务器，请确保服务器正在运行")
        return False
    except Exception as e:
        print(f"❌ API测试失败: {str(e)}")
        return False

def main():
    """主测试函数"""
    print("🚀 营养师AI Agent - 功能测试")
    print("=" * 50)
    
    # 测试Agent核心功能
    agent_test_passed = test_agent_with_sample()
    
    # 测试API端点
    api_test_passed = test_api_endpoints()
    
    print("\n" + "=" * 50)
    print("📋 测试总结:")
    print(f"Agent核心功能: {'✅ 通过' if agent_test_passed else '❌ 失败'}")
    print(f"API端点测试: {'✅ 通过' if api_test_passed else '❌ 失败'}")
    
    if agent_test_passed and api_test_passed:
        print("\n🎉 所有测试通过！营养师Agent已准备就绪")
        return True
    else:
        print("\n⚠️  部分测试失败，请检查配置")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)