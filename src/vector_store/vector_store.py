import numpy as np
from typing import List, Dict, Any, Optional
import faiss
import os
import pickle
from datetime import datetime

class VectorStore:
    """向量存储类，用于存储和检索文档的向量表示"""
    
    def __init__(self, embedding_dim: int = 768):
        """初始化向量存储
        
        Args:
            embedding_dim: 嵌入向量的维度
        """
        self.embedding_dim = embedding_dim
        self.index = faiss.IndexFlatL2(embedding_dim)  # 使用L2距离的FAISS索引
        self.documents = []  # 存储文档内容和元数据
        self.embeddings = None  # 存储所有文档的嵌入向量
    
    def _get_embedding(self, text: str) -> np.ndarray:
        """获取文本的嵌入向量
        
        这里使用一个简单的方法来模拟嵌入，实际应用中应该使用预训练模型
        
        Args:
            text: 输入文本
            
        Returns:
            文本的嵌入向量
        """
        # 注意：这只是一个简单的模拟，实际应用中应该使用如下方式获取嵌入：
        # 1. 使用预训练模型如BERT、Sentence-BERT等
        # 2. 使用大模型API提供的嵌入功能
        
        # 这里使用一个简单的哈希函数来模拟嵌入
        import hashlib
        
        # 创建一个固定大小的向量
        embedding = np.zeros(self.embedding_dim, dtype=np.float32)
        
        # 使用文本的哈希值填充向量
        hash_object = hashlib.md5(text.encode())
        hash_bytes = hash_object.digest()
        
        # 将哈希值转换为浮点数并填充向量
        for i in range(min(16, self.embedding_dim)):
            embedding[i] = float(hash_bytes[i]) / 255.0
        
        # 填充剩余位置（如果有）
        if self.embedding_dim > 16:
            for i in range(16, self.embedding_dim):
                embedding[i] = np.sin(i * embedding[i % 16])
        
        # 归一化
        norm = np.linalg.norm(embedding)
        if norm > 0:
            embedding = embedding / norm
        
        return embedding
    
    def add_documents(self, documents: List[Dict[str, Any]]):
        """添加文档到向量存储
        
        Args:
            documents: 文档列表，每个文档是一个字典，包含内容和元数据
        """
        if not documents:
            return
        
        # 提取文档内容
        texts = [doc["content"] for doc in documents]
        
        # 获取嵌入向量
        new_embeddings = np.array(dtype=np.float32)
        
        # 添加到FAISS索引
        self.index.add(new_embeddings)
        
        # 保存文档
        self.documents.extend(documents)
        
        # 更新嵌入向量存储
        if self.embeddings is None:
            self.embeddings = new_embeddings
        else:
            self.embeddings = np.vstack([self.embeddings, new_embeddings])
    
    def similarity_search(self, query: str, k: int = 3) -> List[Dict[str, Any]]:
        """基于相似度搜索文档
        
        Args:
            query: 查询文本
            k: 返回的最相似文档数量
            
        Returns:
            最相似的k个文档
        """
        if not self.documents:
            return []
        
        # 获取查询的嵌入向量
        query_embedding = self._get_embedding(query)
        query_embedding = np.array([query_embedding], dtype=np.float32)
        
        # 搜索最相似的文档
        k = min(k, len(self.documents))  # 确保k不超过文档数量
        distances, indices = self.index.search(query_embedding, k)
        
        # 返回最相似的文档
 
        for i in range(len(indices[0])):
            idx = indices[0][i]
            if idx < len(self.documents):
                doc = self.documents[idx].copy()
                doc["score"] = float(1.0 / (1.0 + distances[0][i]))  # 转换距离为相似度分数
                results.append(doc)
        
        return results
    
    def save(self, directory: str, name: str = None):
        """保存向量存储到磁盘
        
        Args:
            directory: 保存目录
            name: 保存名称，默认使用当前时间戳
        """
        if name is None:
            name = f"vector_store_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        os.makedirs(directory, exist_ok=True)
        
        # 保存FAISS索引
        faiss.write_index(self.index, os.path.join(directory, f"{name}.index"))
        
        # 保存文档和嵌入向量
        with open(os.path.join(directory, f"{name}.pkl"), "wb") as f:
            pickle.dump({
                "documents": self.documents,
                "embeddings": self.embeddings,
                "embedding_dim": self.embedding_dim
            }, f)
    
    @classmethod
    def load(cls, directory: str, name: str) -> "VectorStore":
        """从磁盘加载向量存储
        
        Args:
            directory: 加载目录
            name: 加载名称
            
        Returns:
            加载的向量存储实例
        """
        # 加载文档和嵌入向量
        with open(os.path.join(directory, f"{name}.pkl"), "rb") as f:
            data = pickle.load(f)
        
        # 创建实例
        vector_store = cls(embedding_dim=data["embedding_dim"])
        vector_store.documents = data["documents"]
        vector_store.embeddings = data["embeddings"]
        
        # 加载FAISS索引
        vector_store.index = faiss.read_index(os.path.join(directory, f"{name}.index"))
        
        return vector_store