import os
from typing import Dict, Any

def get_available_models() -> Dict[str, Dict[str, Any]]:
    """获取可用的大语言模型列表
    
    Returns:
        模型名称到模型信息的映射
    """
    # 检查环境变量，确定哪些模型可用
    zhipu_api_key = os.getenv("ZHIPU_API_KEY")
    baidu_api_key = os.getenv("BAIDU_API_KEY")
    baidu_secret_key = os.getenv("BAIDU_SECRET_KEY")
    
    # 定义模型列表
    models = {
        "智谱 ChatGLM Turbo": {
            "type": "zhipu",
            "name": "chatglm_turbo",
            "description": "智谱AI的ChatGLM Turbo模型，适合一般对话和文档问答",
            "available": True  # 即使没有API密钥，也可以使用模拟模式
        },
        "智谱 ChatGLM Pro": {
            "type": "zhipu",
            "name": "chatglm_pro",
            "description": "智谱AI的ChatGLM专业版模型，具有更强的理解和生成能力",
            "available": zhipu_api_key is not None
        },
        "百度文心一言": {
            "type": "baidu",
            "name": "ERNIE-Bot",
            "description": "百度的ERNIE-Bot模型，具有广泛的知识和强大的理解能力",
            "available": baidu_api_key is not None and baidu_secret_key is not None
        },
        "百度文心一言Pro": {
            "type": "baidu",
            "name": "ERNIE-Bot-4",
            "description": "百度的ERNIE-Bot专业版模型，具有更强的推理和分析能力",
            "available": baidu_api_key is not None and baidu_secret_key is not None
        }
    }
    
    return models

def format_document_for_display(doc: Dict[str, Any]) -> str:
    """格式化文档以便于显示
    
    Args:
        doc: 文档字典，包含内容和元数据
        
    Returns:
        格式化后的文档字符串
    """
    content = doc["content"]
    metadata = doc["metadata"]
    source = metadata.get("source", "未知来源")
    
    # 如果内容太长，截断显示
    max_display_length = 300
    if len(content) > max_display_length:
        content = content[:max_display_length] + "..."
    
    return f"**来源:** {source}\n\n{content}"

def create_empty_file(file_path: str) -> None:
    """创建空文件
    
    Args:
        file_path: 文件路径
    """
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w") as f:
        pass