import os
import json
import requests
from typing import List, Dict, Any, Optional, Iterator
import time
import base64
import hmac
import hashlib

from .base_model import BaseModelAdapter

class BaiduModelAdapter(BaseModelAdapter):
    """百度文心一言模型适配器"""
    
    def __init__(self, model_name: str = "ERNIE-Bot-4", temperature: float = 0.7, max_tokens: int = 2048):
        """初始化百度文心一言模型适配器
        
        Args:
            model_name: 模型名称，默认为'ERNIE-Bot-4'
            temperature: 温度参数
            max_tokens: 最大生成长度
        """
        super().__init__(model_name, temperature, max_tokens)
        
        # 获取API密钥
        self.api_key = os.getenv("BAIDU_API_KEY")
        self.secret_key = os.getenv("BAIDU_SECRET_KEY")
        
        if not self.api_key or not self.secret_key:
            print("警告：未设置BAIDU_API_KEY或BAIDU_SECRET_KEY环境变量，将使用模拟模式")
        
        # 模型名称映射
        self.model_map = {
            "ERNIE-Bot": "completions",
            "ERNIE-Bot-4": "completions_pro",
            "ERNIE-Bot-8k": "ernie_bot_8k",
            "ERNIE-Speed": "ernie_speed"
        }
    
    def _get_access_token(self) -> Optional[str]:
        """获取百度API访问令牌
        
        Returns:
            访问令牌，如果获取失败则返回None
        """
        url = "https://aip.baidubce.com/oauth/2.0/token"
        params = {
            "grant_type": "client_credentials",
            "client_id": self.api_key,
            "client_secret": self.secret_key
        }
        
        try:
            response = requests.post(url, params=params)
            result = response.json()
            return result.get("access_token")
        except Exception as e:
            print(f"获取百度访问令牌时出错: {str(e)}")
            return None
    
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
            if self.api_key and self.secret_key:
                # 获取访问令牌
                access_token = self._get_access_token()
                if not access_token:
                    return self._get_fallback_response("无法获取百度API访问令牌")
                
                # 确定API端点
                api_endpoint = self.model_map.get(self.model_name, "completions_pro")
                url = f"https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/{api_endpoint}?access_token={access_token}"
                
                # 构建请求体
                payload = {
                    "messages": [
                        {"role": "user", "content": full_prompt}
                    ],
                    "temperature": self.temperature,
                    "top_p": 0.8,
                    "stream": False
                }
                
                # 发送请求
                headers = {"Content-Type": "application/json"}
                response = requests.post(url, headers=headers, json=payload)
                result = response.json()
                
                # 解析响应
                if "result" in result:
                    return result["result"]
                else:
                    error_msg = f"百度API错误: {result.get('error_msg', '未知错误')}"
                    print(error_msg)
                    return self._get_fallback_response(error_msg)
            else:
                # 模拟模式
                return self._get_mock_response(full_prompt)
        except Exception as e:
            error_msg = f"调用百度API时出错: {str(e)}"
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
            if self.api_key and self.secret_key:
                # 获取访问令牌
                access_token = self._get_access_token()
                if not access_token:
                    yield "[生成出错: 无法获取百度API访问令牌]\n"
                    return
                
                # 确定API端点
                api_endpoint = self.model_map.get(self.model_name, "completions_pro")
                url = f"https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/{api_endpoint}?access_token={access_token}"
                
                # 构建请求体
                payload = {
                    "messages": [
                        {"role": "user", "content": full_prompt}
                    ],
                    "temperature": self.temperature,
                    "top_p": 0.8,
                    "stream": True
                }
                
                # 发送流式请求
                headers = {"Content-Type": "application/json"}
                response = requests.post(url, headers=headers, json=payload, stream=True)
                
                # 解析流式响应
                for line in response.iter_lines():
                    if line:
                        line = line.decode("utf-8")
                        if line.startswith("data: "):
                            data = json.loads(line[6:])
                            if "result" in data:
                                yield data["result"]
            else:
                # 模拟流式响应
                mock_response = self._get_mock_response(full_prompt)
                words = mock_response.split()
                for word in words:
                    yield word + " "
                    time.sleep(0.05)  # 模拟延迟
        except Exception as e:
            error_msg = f"调用百度API流式生成时出错: {str(e)}"
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
            return "文心一言是百度推出的知识增强大语言模型，能够与人对话互动，回答问题，协助创作，高效便捷地帮助人们获取信息、知识和灵感。在本文档问答系统中，文心一言被用于理解文档内容并回答用户问题。"
        elif "如何" in prompt or "怎么" in prompt:
            return "使用文心一言进行文档问答非常简单：首先上传您的文档，然后在对话框中输入您的问题。系统会分析文档内容，找到相关信息，并通过文心一言生成准确、流畅的回答。您还可以根据需要调整参数，如温度值和检索文档数量，以获得更符合您期望的回答。"
        else:
            return "基于您提供的文档内容，我发现了一些相关信息。请注意，我的回答仅基于文档中的内容，如有不准确之处，建议查阅原始文档或调整您的问题。如果需要更深入的分析，可以尝试上传更多相关文档或调整系统参数。"
    
    def _get_fallback_response(self, error_msg: str) -> str:
        """获取备用响应（当API调用失败时使用）
        
        Args:
            error_msg: 错误信息
            
        Returns:
            备用响应文本
        """
        return f"很抱歉，我无法生成回答。发生了以下错误：{error_msg}\n\n请检查您的API密钥设置或稍后再试。"