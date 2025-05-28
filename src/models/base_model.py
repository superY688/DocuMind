from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, Iterator

class BaseModelAdapter(ABC):
    """大模型适配器基类，定义所有模型适配器必须实现的接口"""
    
    def __init__(self, model_name: str, temperature: float = 0.7, max_tokens: int = 2048):
        """初始化模型适配器
        
        Args:
            model_name: 模型名称
            temperature: 温度参数，控制生成文本的随机性
            max_tokens: 生成文本的最大长度
        """
        self.model_name = model_name
        self.temperature = temperature
        self.max_tokens = max_tokens
    
    @abstractmethod
    def generate(self, prompt: str, context_docs: List[Dict[str, Any]] = None) -> str:
        """生成文本
        
        Args:
            prompt: 提示文本
            context_docs: 上下文文档，用于增强生成
            
        Returns:
            生成的文本
        """
        pass
    
    @abstractmethod
    def generate_stream(self, prompt: str, context_docs: List[Dict[str, Any]] = None) -> Iterator[str]:
        """流式生成文本
        
        Args:
            prompt: 提示文本
            context_docs: 上下文文档，用于增强生成
            
        Returns:
            生成文本的迭代器
        """
        pass
    
    def _build_prompt_with_context(self, prompt: str, context_docs: List[Dict[str, Any]]) -> str:
        """构建带有上下文的提示
        
        Args:
            prompt: 原始提示
            context_docs: 上下文文档
            
        Returns:
            带有上下文的完整提示
        """
        if not context_docs:
            return prompt
        
        # 构建上下文字符串
        context_str = "\n\n相关文档内容：\n"
        for i, doc in enumerate(context_docs):
            context_str += f"[文档 {i+1}]\n{doc['content']}\n\n"
        
        # 构建完整提示
        full_prompt = f"{context_str}\n根据以上文档内容，{prompt}"
        
        return full_prompt