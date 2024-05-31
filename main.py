import streamlit as st
from langchain.memory import ConversationBufferMemory

from utils import qa_agent

st.title("AI智能PDF问答工具")
with st.sidebar:
    openai_api_key = st.text_input("请输入OpenAI API密钥", type="password")
    st.markdown("[获取OpenAI API密钥](https://platform.openai.com/account/api-keys)")

if "memory" not in st.session_state:
    st.session_state["memory"] = ConversationBufferMemory(
        return_messages=True,   # 设置这个参数才返回的是消息列表，而不是字符串
        memory_key="chat_history", # 在ConversationRetrievalChain中，记忆对应的键是chat_history
        output_key="answer"   # 输出对应的键是answer
    )

uploaded_file = st.file_uploader("上传你的PDF文件：", type="pdf")  # type="pdf"表示除了pdf文件以外的文件都不行
question = st.text_input("对PDF的内容进行提问", disabled=not uploaded_file) # disabled表是示没有上传文件时，输入框不可用

if uploaded_file and question and not openai_api_key:
    st.info("请输入你的OpenAI API密钥")

if uploaded_file and question and openai_api_key:
    with st.spinner("AI正在思考中，请稍等..."):
        response = qa_agent(openai_api_key, st.session_state["memory"],
                            uploaded_file, question)  # 返回的是字典
    print(response)
    st.write("### 答案")
    st.write(response["answer"])
    # 历史消息放在会话状态中
    st.session_state["chat_history"] = response["chat_history"]

if "chat_history" in st.session_state:
    with st.expander("历史消息"):   # 折叠框
        # 每两条消息是一个对话，直到所有对话
        for i in range(0, len(st.session_state["chat_history"]), 2):
            human_message = st.session_state["chat_history"][i]
            ai_message = st.session_state["chat_history"][i + 1]
            st.write(human_message)
            st.write(ai_message)
            # 一轮对话结束就画一个分割线
            if i < len(st.session_state["chat_history"]) - 2:
                st.divider()


