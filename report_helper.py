import streamlit as st
from openai import OpenAI
import os
import subprocess


# 设置 Streamlit 页面
st.set_page_config(page_title="Web for SIDRI PYAUTOCAD", page_icon="🦜🔗")
st.title("科标业项目任务书自动化生成与润色助手")

# 设置 OpenAI API 密钥
client = OpenAI(
    # This is the default and can be omitted
    api_key = "sk-E1CARH7sAvjVIOUgx1UkYn3pvzFX5c75oHhuULeNE6pCO3n1" ,
    base_url = "https://api.moonshot.cn/v1" ,
)

# 单轮对话
# completion = client.chat.completions.create(
#     model = "moonshot-v1-8k",
#     messages = [
#         {"role": "system", "content": "你是 Kimi，由 Moonshot AI 提供的人工智能助手，你更擅长中文和英文的对话。你会为用户提供安全，有帮助，准确的回答。同时，你会拒绝一切涉及恐怖主义，种族歧视，黄色暴力等问题的回答。Moonshot AI 为专有名词，不可翻译成其他语言。"},
#         {"role": "user", "content": "你好，我叫李雷，1+1等于多少？"}
#     ],
#     temperature = 0.3,
# )
 
# print(completion.choices[0].message.content)



# 多轮对话
history = [
    {"role": "system", "content": "你是 Kimi，由 Moonshot AI 提供的人工智能助手，你更擅长中文和英文的对话。你会为用户提供安全，有帮助，准确的回答。同时，你会拒绝一切涉及恐怖主义，种族歧视，黄色暴力等问题的回答。Moonshot AI 为专有名词，不可翻译成其他语言。"}
]
 
def chat(query, history):
    history.append({
        "role": "user", 
        "content": query
    })
    completion = client.chat.completions.create(
        model="moonshot-v1-auto",
        messages=history,
        temperature=0.3,
    )
    result = completion.choices[0].message.content
    history.append({
        "role": "assistant",
        "content": result
    })
    return result
 
print(chat("地球的自转周期是多少？", history))
print(chat("月球呢？", history))

# 初始化 OpenAI 模型
@st.cache_resource
def init_models():
    return None

# 检查是否需要初始化模型
if 'query_engine' not in st.session_state:
    st.session_state['query_engine'] = init_models()

# 函数：使用 OpenAI 的 API 生成响应
def greet2(question):
    try:
        chat_completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": question}
            ],
            max_tokens=4000,
            temperature=0.7,          
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

# 保存 LLM 生成的响应
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "你好，我是你的编程助手，有什么我可以帮助你的吗？"}]

# 显示或清除聊天消息
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# 函数：清除聊天记录
def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "你好，我是你的助手，有什么我可以帮助你的吗？"}]

    # 删除 chat_log.py 文件
    try:
        os.remove('chat_log.py')  # 确保路径正确
    except FileNotFoundError:
        st.warning("已删除")

st.sidebar.button('清除聊天历史', on_click=clear_chat_history)

# 函数：生成 ChatGPT 响应
def generate_llama_index_response(prompt_input):
    return greet2(prompt_input)

# 用户输入的提示
if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

# 生成 OpenAI API 响应
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = generate_llama_index_response(prompt)
            placeholder = st.empty()
            placeholder.markdown(response)
    message = {"role": "assistant", "content": response}
    st.session_state.messages.append(message)

# 函数：保存聊天记录到文件          
def save_to_file():
    file_content = ""
    
    for msg in st.session_state.messages:
        content = msg['content']
        
        # 检查是否是代码块（假设代码块使用三个反引号 ``` 包裹）
        code_blocks = content.split("```")
        if len(code_blocks) >= 3:
            # 过滤掉解释性文字，只提取反引号包裹的代码部分
            for i in range(1, len(code_blocks), 2):  # 跳过非代码部分
                code_content = code_blocks[i].strip()

                # 如果代码块以某些编程语言前缀（如 python）开头，删除该前缀,并抓取该代码
                if code_content.startswith("python"):
                    code_content = code_content[len("python"):].strip()  # 删除 "python" 前缀并去掉多余的空格
                    file_content += f"{code_content}\n"  # 将代码内容添加到文件中

    file_path = "chat_log.py"
    
    if file_content:  # 如果 file_content 不为空
        # 使用 UTF-8 编码写入文件
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(file_content)
        st.success(f"文件已生成: {file_path}")
    else:
        st.warning("没有提取到任何代码块")
    
    return file_path

# 函数：运行生成的文件
def run_file(file_path):
    try:
        result = subprocess.run(['python', file_path], capture_output=True, text=True)
        st.text(f"运行结果: \n{result.stdout}")
    except Exception as e:
        st.error(f"运行文件时出错: {str(e)}")

# 添加按钮，生成并运行文件
if st.sidebar.button('生成模型'):
    file_path = save_to_file()
    run_file(file_path)