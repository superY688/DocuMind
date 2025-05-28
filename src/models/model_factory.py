from typing import List, Dict, Any, Optional, Iterator
from .base_model import BaseModelAdapter
from .zhipu_model import ZhipuModelAdapter
from .baidu_model import BaiduModelAdapter

class ModelFactory:
    """模型工厂类，用于创建不同类型的模型适配器"""
    
    @staticmethod
    def get_model(model_type: str, model_name: str, **kwargs) -> BaseModelAdapter:
        """获取模型适配器实例
        
        Args:
            model_type: 模型类型，如'zhipu'、'baidu'等
            model_name: 模型名称
            **kwargs: 其他参数，如temperature等
            
        Returns:
            模型适配器实例
            
        Raises:
            ValueError: 如果模型类型不支持
        """
        if model_type.lower() == "zhipu":
            return ZhipuModelAdapter(model_name=model_name, **kwargs)
        elif model_type.lower() == "baidu":
            return BaiduModelAdapter(model_name=model_name, **kwargs)
        else:
            raise ValueError(f"不支持的模型类型: {model_type}")