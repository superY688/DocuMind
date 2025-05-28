import os
import json
from typing import List, Dict, Any, Optional, Iterator
import time
import zhipuai
from zhipuai import ZhipuAI  # 导入 ZhipuAI 客户端

from .base_model import BaseModelAdapter

class ZhipuModelAdapter(BaseModelAdapter):
    """智谱AI模型适配器"""
    
    def __init__(self, model_name: str = "chatglm_turbo", temperature: float = 0.7, max_tokens: int = 2048):
        """初始化智谱AI模型适配器
        
        Args:
            model_name: 模型名称，默认为'chatglm_turbo'
            temperature: 温度参数
            max_tokens: 最大生成长度
        """
        super().__init__(model_name, temperature, max_tokens)
        
        # 获取API密钥
        api_key = os.getenv("ZHIPU_API_KEY")
        if not api_key:
            print("警告：未设置ZHIPU_API_KEY环境变量，将使用模拟模式")
        
        # 将 API Key 存储在实例变量中
        self.api_key = api_key
    
    def generate(self, prompt: str, context_docs: List[Dict[str, Any]] = None) -> str:
        """生成文本
        
        Args:
            prompt: 提示文本
            context_docs: 上下文文档
            
        Returns:
            生成的文本
        """
        # 构建带有上下文的提示
        full_prompt = self._build_prompt_with_context(prompt, context_docs)
        
        try:
            if self.api_key: # 检查实例变量 self.api_key
                client = ZhipuAI(api_key=self.api_key) # 初始化客户端时传入 API Key
                # 调用智谱AI API (v2)
                response = client.chat.completions.create(
                    model=self.model_name,
                    messages=[ # 使用 messages 参数
                        {"role": "user", "content": full_prompt}
                    ],
                    temperature=self.temperature,
                    top_p=0.7, # top_p 参数可能需要根据模型支持情况调整
                    # max_tokens=self.max_tokens # 确认 max_tokens 是否支持或需要调整
                )
                
                # 解析响应 (v2)
                # 检查 response 结构是否包含 choices 且不为空
                if response and response.choices:
                     return response.choices[0].message.content.strip()
                else:
                     # 处理可能的空响应或不同结构
                     error_msg = f"智谱AI API 返回了无效的响应结构: {response}"
                     print(error_msg)
                     return self._get_fallback_response(error_msg)

            else:
                # 模拟模式
                return self._get_mock_response(full_prompt)
        except Exception as e:
            # 捕获并记录更详细的异常信息
            import traceback
            error_msg = f"调用智谱AI API时出错: {str(e)}\n{traceback.format_exc()}"
            print(error_msg)
            return self._get_fallback_response(error_msg)
    
    def generate_stream(self, prompt: str, context_docs: List[Dict[str, Any]] = None) -> Iterator[str]:
        """流式生成文本
        
        Args:
            prompt: 提示文本
            context_docs: 上下文文档
            
        Returns:
            生成文本的迭代器
        """
        # 构建带有上下文的提示
        full_prompt = self._build_prompt_with_context(prompt, context_docs)
        
        try:
            if self.api_key: # 检查实例变量 self.api_key
                client = ZhipuAI(api_key=self.api_key) # 初始化客户端时传入 API Key
                # 调用智谱AI API（流式模式 v2）
                response = client.chat.completions.create(
                    model=self.model_name,
                    temperature=self.temperature,
                    top_p=0.7, # top_p 参数可能需要根据模型支持情况调整
                    # max_tokens=self.max_tokens, # 确认 max_tokens 是否支持或需要调整
                    stream=True # 启用流式输出
                )
                
                # 解析流式响应 (v2)
                for chunk in response:
                    # 检查 chunk 结构和内容
                    print("chunk")

            else:
                # 模拟流式响应
                mock_response = self._get_mock_response(full_prompt)
                words = mock_response.split()
                for word in words:
                    yield word + " "
                    time.sleep(0.05)  # 模拟延迟
        except Exception as e:
             # 捕获并记录更详细的异常信息
            import traceback
            error_msg = f"调用智谱AI API流式生成时出错: {str(e)}\n{traceback.format_exc()}"
            print(error_msg)
            yield f"[生成出错: {str(e)}]\n"
    
    def _get_mock_response(self, prompt: str) -> str:
        """获取模拟响应（当API密钥未设置时使用）
        
        Args:
            prompt: 提示文本
            
        Returns:
            模拟的响应文本
        """
        # 简单的模拟响应，实际应用中应该使用真实API
        if "介绍" in prompt or "是什么" in prompt:
            return "这是一个文档问答系统，可以基于上传的文档回答问题。系统使用了先进的文本分析和检索技术，能够理解文档内容并提供准确的回答。"
        elif "如何" in prompt or "怎么" in prompt:
            return "您可以按照以下步骤使用本系统：1. 上传PDF、Word或TXT格式的文档；2. 在输入框中输入您的问题；3. 系统会分析文档内容并给出相关回答。如果回答不准确，您可以尝试调整侧边栏中的参数设置。"
        else:
            return "根据您上传的文档内容，我找到了一些相关信息。请注意，我的回答仅基于文档中包含的内容。如果需要更准确的回答，请尝试调整问题或上传更多相关文档。"
    
    def _get_fallback_response(self, error_msg: str) -> str:
        """获取备用响应（当API调用失败时使用）
        
        Args:
            error_msg: 错误信息
            
        Returns:
            备用响应文本
        """
        return f"很抱歉，我无法生成回答。发生了以下错误：{error_msg}\n\n请检查您的API密钥设置或稍后再试。"