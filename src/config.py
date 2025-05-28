import os
from typing import Dict, Any

# 项目根目录
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 临时文件目录
TEMP_DIR = os.path.join(ROOT_DIR, "temp")
os.makedirs(TEMP_DIR, exist_ok=True)

# 知识库目录
KNOWLEDGE_BASE_DIR = os.path.join(ROOT_DIR, "knowledge_base")
os.makedirs(KNOWLEDGE_BASE_DIR, exist_ok=True)

# 向量存储目录
VECTOR_STORE_DIR = os.path.join(KNOWLEDGE_BASE_DIR, "vector_stores")
os.makedirs(VECTOR_STORE_DIR, exist_ok=True)

# 文档处理配置
DOCUMENT_PROCESSING = {
    "chunk_size": 1000,  # 文本块大小
    "chunk_overlap": 200,  # 文本块重叠大小
    "supported_extensions": [".pdf", ".docx", ".txt"]  # 支持的文件扩展名
}

# 模型配置
MODEL_CONFIG = {
    "default_model": "智谱 ChatGLM Turbo",  # 默认模型
    "temperature": 0.7,  # 默认温度
    "max_tokens": 2048,  # 默认最大生成长度
    "top_k": 3  # 默认检索文档数量
}

# 模型类型映射
MODEL_TYPE_MAP = {
    "zhipu": {
        "display_name": "智谱AI",
        "models": {
            "chatglm_turbo": "ChatGLM Turbo",
            "chatglm_pro": "ChatGLM Pro",
            "chatglm_std": "ChatGLM 标准版"
        }
    },
    "baidu": {
        "display_name": "百度文心一言",
        "models": {
            "ERNIE-Bot": "文心一言",
            "ERNIE-Bot-4": "文心一言Pro",
            "ERNIE-Bot-8k": "文心一言8K",
            "ERNIE-Speed": "文心一言Speed"
        }
    }
}

# 应用配置
APP_CONFIG = {
    "title": "DocuMind - 智能文档分析与问答系统",
    "description": "上传文档，提问问题，获取智能回答",
    "version": "1.0.0",
    "author": "DocuMind Team"
}