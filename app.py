import streamlit as st
import os
import tempfile
from dotenv import load_dotenv


# 导入自定义模块
from src.document_processor.processor import DocumentProcessor
from src.models.model_factory import ModelFactory
from src.vector_store.vector_store import VectorStore
from src.utils.helpers import get_available_models

# 页面配置
st.set_page_config(
    page_title="DocuMind - 智能文档分析与问答系统",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 初始化会话状态
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []

if "current_document" not in st.session_state:
    st.session_state.current_document = None

if "vector_store" not in st.session_state:
    st.session_state.vector_store = None

if "document_processor" not in st.session_state:
    st.session_state.document_processor = DocumentProcessor()

# 侧边栏
with st.sidebar:
    st.title("📚 DocuMind")
    st.subheader("智能文档分析与问答系统")
    
    # 模型选择
    available_models = get_available_models()
    selected_model = st.selectbox(
        "选择大语言模型",
        options=available_models.keys(),
        index=0,
        help="选择用于回答问题的大语言模型"
    )
    
    # 文档上传
    uploaded_file = st.file_uploader(
        "上传文档", 
        type=["pdf", "docx", "txt"], 
        help="支持PDF、Word和TXT格式"
    )
    
    # 上传文档处理
    if uploaded_file and (st.session_state.current_document == uploaded_file.name):
        with st.spinner("正在处理文档..."):
            # 保存上传的文件到临时目录
            temp_dir = tempfile.mkdtemp()
          
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getvalue())
            
            # 处理文档
            try:
                document_processor = st.session_state.document_processor
                document_chunks = document_processor.process_document(temp_path)
                
                # 创建向量存储
                vector_store = VectorStore()
                vector_store.add_documents(document_chunks)
                
                # 更新会话状态
                st.session_state.current_document = uploaded_file.name
                st.session_state.vector_store = vector_store
                st.session_state.conversation_history = []
                
                st.success(f"文档 '{uploaded_file.name}' 已成功处理！")
            except Exception as e:
                st.error(f"处理文档时出错: {str(e)}")
    
    # 高级设置折叠面板
    with st.expander("高级设置"):
        top_k = st.slider(
            "检索文档数量", 
            min_value=1, 
            max_value=10, 
            value=3,
            help="从文档中检索的相关片段数量"
        )
        
        temperature = st.slider(
            "温度", 
            min_value=0.0, 
            max_value=1.0, 
            value=0.7, 
            step=0.1,
            help="控制回答的创造性，较低的值使回答更确定，较高的值使回答更多样化"
        )
    
    # 清除对话按钮
    if st.button("清除对话历史"):
        st.session_state.conversation_history = []
        st.experimental_rerun()
    
    st.divider()
    st.caption("© 2023 DocuMind - 智能文档分析与问答系统")

# 主界面
st.title("智能文档分析与问答系统")

# 显示当前文档信息
if st.session_state.current_document:
    st.info(f"当前文档: {st.session_state.current_document}")
else:
    st.warning("请先上传文档以开始对话")

# 显示对话历史
for i, (question, answer) in enumerate(st.session_state.conversation_history):
    with st.chat_message("user"):
        st.write(question)
    with st.chat_message("assistant"):
        st.write(answer)

# 问题输入
if st.session_state.current_document:
    question = st.chat_input("请输入您的问题")
    
    if question:
        # 显示用户问题
        with st.chat_message("user"):
            st.write(question)
        
        # 生成回答
        with st.chat_message("assistant"):
            with st.spinner("思考中..."):
                try:
                    # 从向量存储中检索相关文档
                    relevant_docs = st.session_state.vector_store.similarity_search(question, k=top_k)
                    
                    # 初始化模型
                    model_info = available_models[selected_model]
                    model = ModelFactory.get_model(
                        model_type=model_info["type"],
                        model_name=model_info["name"],
                        temperature=temperature
                    )

                    # 生成回答
                    answer_container = st.empty()
                    full_answer = ""

                    # 流式输出
                    for token in model.generate_stream(question, relevant_docs):
                        full_answer += token
                        answer_container.markdown(full_answer + "▌")
                    
                    answer_container.markdown(full_answer)
                    
                    # 保存对话历史
                    st.session_state.conversation_history.append((question, full_answer))
                    
                except Exception as e:
                    st.error(f"生成回答时出错: {str(e)}")
else:
    st.info("请先上传文档以开始对话")