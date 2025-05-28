import os
import re
from typing import List, Dict, Any

# 导入文档处理相关库
from PyPDF2 import PdfReader
from docx import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

class DocumentProcessor:
    """文档处理类，负责解析不同格式的文档并将其分割成小块"""
    
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        """初始化文档处理器
        
        Args:
            chunk_size: 文本块大小
            chunk_overlap: 文本块重叠大小
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", "。", "！", "？", ".", "!", "?", " ", ""]
        )
    
    def process_document(self, file_path: str) -> List[Dict[str, Any]]:
        """处理文档，提取文本并分块
        
        Args:
            file_path: 文档路径
            
        Returns:
            包含文本块和元数据的列表
        """
        # 获取文件扩展名
        _, file_extension = os.path.splitext(file_path)
        
        # 根据文件类型提取文本
        if file_extension == ".pdf":
            text = self._extract_text_from_pdf(file_path)
        elif file_extension == ".docx":
            text = self._extract_text_from_docx(file_path)
        elif file_extension == ".txt":
            text = self._extract_text_from_txt(file_path)
        else:
            raise ValueError(f"不支持的文件类型: {file_extension}")
        
        # 清理文本
        text = self._clean_text(text)
        
        # 分割文本
        chunks = self.text_splitter.create_documents([text])
        
        # 转换为字典列表，包含文本和元数据
        document_chunks = []
        for i, chunk in enumerate(chunks):
            document_chunks.append({
                "content": chunk.page_content,
                "metadata": {
                    "source": os.path.basename(file_path),
                    "chunk_id": i
                }
            })
        
        return document_chunks
    
    def _extract_text_from_pdf(self, file_path: str) -> str:
        """从PDF文件中提取文本"""
        text = ""
        with open(file_path, "rb") as file:
            pdf = PdfReader(file)
            for page in pdf.pages:
                text += page.extract_text() + "\n\n"
        return text
    
    def _extract_text_from_docx(self, file_path: str) -> str:
        """从DOCX文件中提取文本"""
        doc = Document(file_path)
        text = ""
        for para in doc.paragraphs:
            text += para.text + "\n"
        return text
    
    def _extract_text_from_txt(self, file_path: str) -> str:
        """从TXT文件中提取文本"""
        with open(file_path, "r", encoding="utf-8") as file:
            text = file.read()
        return text
    
    def _clean_text(self, text: str) -> str:
        """清理文本，去除多余空白字符等"""
        # 替换多个空白字符为单个空格
        text = re.sub(r'\s+', ' ', text)
        # 去除其他可能的噪声
        text = text.strip()
        return text