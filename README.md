# DocuMind - 智能文档分析与问答系统

## 项目简介

DocuMind是一个基于大语言模型的智能文档分析与问答系统，能够自动提取文档内容并回答相关问题。

### 核心功能

- **文档解析**：支持PDF、Word、TXT等多种格式文档的上传与解析
- **智能问答**：基于文档内容进行精准问答，支持上下文理解
- **知识库构建**：自动从文档中提取关键信息，构建知识库
- **多模型支持**：默认使用国内开源大模型，同时支持切换到其他模型
- **交互式界面**：基于Streamlit构建的友好用户界面

### 技术亮点

- **向量数据库集成**：使用FAISS实现高效的语义检索
- **文本分块与嵌入**：采用先进的文本分块策略和嵌入技术
- **上下文增强**：通过RAG (Retrieval-Augmented Generation) 技术提升回答质量
- **模型适配层**：灵活支持不同大模型API的统一调用接口
- **流式响应**：支持大模型的流式输出，提升用户体验

## 技术栈

- **前端**：Streamlit
- **后端**：FastAPI
- **大模型**：默认支持智谱ChatGLM、百度文心一言等国内开源模型
- **向量数据库**：FAISS
- **文档处理**：PyPDF2, python-docx, langchain

## 项目演示

开始界面

![开始界面](https://github.com/superY688/DocuMind/blob/master/images/image1.png)

上传文档，问答演示

![上传文档，问答演示](https://github.com/superY688/DocuMind/blob/master/images/image2.png)

支持切换不同的大语言模型进行回答，并且支持自定义添加新的模型

![支持切换不同的大语言模型进行回答，并且支持自定义添加新的模型](https://github.com/superY688/DocuMind/blob/master/images/image3.png)

## 安装指南

### 环境要求

- Python 3.8+
- 足够的内存（推荐8GB以上）

### 安装步骤

1. 克隆项目代码

```bash
git clone https://github.com/superY688/DocuMind.git
cd documind
```

2. 安装依赖

```bash
pip install -r requirements.txt
```

3. 配置模型API密钥（可选）

在项目根目录创建`.env`文件，添加以下内容：

```
ZHIPU_API_KEY=your_zhipu_api_key
BAIDU_API_KEY=your_baidu_api_key
BAIDU_SECRET_KEY=your_baidu_secret_key
```

## 使用教程

### 启动应用

```bash
streamlit run app.py
```

### 使用流程

1. **上传文档**：在首页上传PDF、Word或TXT格式的文档
2. **选择模型**：从下拉菜单中选择要使用的大模型
3. **提问**：在输入框中输入与文档相关的问题
4. **获取回答**：系统会分析文档内容并给出相关回答

### 高级功能

- **知识库管理**：可以管理已上传的文档和构建的知识库
- **对话历史**：保存问答历史记录，支持继续对话
- **参数调整**：可以调整检索参数、上下文窗口大小等

## 项目结构

```
documind/
├── app.py                 # 主应用入口
├── requirements.txt       # 项目依赖
├── .env                   # 环境变量配置
├── README.md              # 项目说明
├── docs/                  # 文档目录
├── src/
│   ├── models/            # 模型适配层
│   ├── document_processor/ # 文档处理模块
│   ├── vector_store/      # 向量存储模块
│   ├── utils/             # 工具函数
│   └── config.py          # 配置文件
└── tests/                 # 测试代码
```

## 开发指南

### 添加新的模型支持

1. 在`src/models`目录下创建新的模型适配器
2. 实现`BaseModelAdapter`接口
3. 在`config.py`中注册新模型

### 自定义文档处理

可以通过修改`src/document_processor`中的代码来支持更多文档格式或优化处理逻辑。

## 贡献指南

欢迎提交Pull Request或Issue来帮助改进项目！

## 许可证

MIT License