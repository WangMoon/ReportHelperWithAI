import streamlit as st
from openai import OpenAI
import os
import json
import time
from word_generate import generate_docx_file
from streamlit_extras.stylable_container import stylable_container
from audiorecorder import audiorecorder
import time

st.set_page_config(page_title="晟德瑞自动化报告助手",page_icon="🦜🔗")
st.title("晟德瑞自动化报告助手")
st.caption("科标业项目任务书自动化生成与润色助手")
# Create a chatbot UI with Streamlit and OpenAI
def chat_ui():
    state = st.session_state
    # Set the title of the app
    # st.set_page_config(page_title="晟德瑞自动化报告助手",page_icon="🦜🔗")
    # st.title("晟德瑞自动化报告助手")
    # st.caption("科标业项目任务书自动化生成与润色助手")
    

    # Create a client for the OpenAI API
    if "client" not in state:
        st.info("请配置Chatbot的基本设置，其中API Key和Base URL是必须的。")
        pass
    else:
        # if "message_history" not in state:
        #     state.message_history = []
        #     pass
        # if "system_prompt" in state:
        #     state.message_history.append({"role": "system", "content": state.system_prompt})
        if "messages" not in st.session_state.keys():
            st.session_state.messages = [{"role": "assistant", "content": "你好，我是你的编程助手，有什么我可以帮助你的吗？"}]

        # 录音功能
        # with stylable_container(
        #     key="audio_input",
        #     css_styles="""
        #         {
        #             position: fixed;
        #             bottom: 120px;
        #         }
        #         """,
        #     ):
        #     audio = audiorecorder("🎙️ start", "🎙️ stop")
        #     print('audio: ', audio)
        #     if len(audio) > 0:
        #         audio.export("./config/audio.mp3", format="mp3")
        


        user_input = st.chat_input("输入消息")
        uploaded_file = st.file_uploader("📄 上传文件", type=["docx", "pdf", "txt", "md", "doc"], key="file_upload")

        if uploaded_file:
            # st.write("文件正在读取中...", uploaded_file.name)
            st.write("文件正在读取中...")

        # with stylable_container(
        #         key="file_input",
        #         css_styles="""
        #             {
        #                 position: fixed;
        #                 bottom: 200px;
        #             }
        #             """,
        #     ):
        #     uploaded_file = st.file_uploader("📄 上传文件", type=["docx", "pdf", "txt", "md", "doc"], key="file_upload")
        #     if uploaded_file:
        #         # st.write("文件正在读取中...", uploaded_file.name)
        #         st.write("文件正在读取中...")

                
            # st.chat_input("输入消息")
        if user_input:
            state.message_history.append({"role": "user", "content": user_input})
            # 更新消息历史，显示“正在生成报告，请稍等...”消息
            state.message_history.append({"role": "assistant", "content": "正在生成报告，请稍等..."})
            
            # 显示消息历史
            for message in state.message_history:
                if message["role"] == "system":
                    continue
                else:
                    st.chat_message(message["role"]).write(message["content"])
            
            
            with st.spinner("正在生成报告，请稍等..."):
                project_info =  {
                    'project_type': '科技创新项目',
                    'project_number': 'KJ2024',
                    'project_name': '基于AI图像检测算法和视觉（CV）大模型的抽水蓄能电站质量安全隐患排查和风险预警关键技术研究',
                    'host_department': '三峡建工、上海院',
                    'responsible_person': '张三',
                    'start_year': '2024',
                    'start_month': '1',
                    'end_year': '2026',
                    'end_month': '8',
                    'trend_analysis': '随着人工智能技术的快速发展，AI图像检测算法和视觉（CV）大模型在工业安全领域的应用越来越广泛。特别是在抽水蓄能电站这样的复杂工程中，利用AI技术进行质量安全隐患排查和风险预警具有重要的现实意义和广阔的应用前景。\n\n抽水蓄能电站作为调节电力系统峰谷差的重要设施，其安全运行对保障能源供应和电网稳定至关重要。然而，由于电站建设环境复杂，施工过程中存在多种潜在的风险和隐患，如施工机械作业半径站人、卸料车后方有人员活动、高空作业保护缺失等，这些都可能导致严重的安全事故。因此，迫切需要一种高效、准确的安全监测手段来提高电站的安全运行水平。\n\n本项目旨在研究和开发一套基于AI图像检测算法和视觉（CV）大模型的抽水蓄能电站质量安全隐患排查和风险预警系统，以提高电站的安全运行水平，降低事故发生率，保障人员和设备的安全。通过创新开展以大模型作为“调度大脑”，以小模型作为“复核专家”的AI识别模式，实现对电站建设期的“少人巡检、无人巡检”模式，提升科技兴安水平。\n\n在国内外现状方面，虽然已有一些研究和应用案例，但大多数集中在通用领域，针对抽水蓄能电站这一特定领域的研究还相对较少。因此，本项目的研究具有较高的创新性和应用价值。',
                    'research_content': '本项目的研究内容包括：\n\n1. 抽蓄工程风险、隐患数据集建设方法研究：将对抽蓄工程的风险和隐患进行深入分析，建立一个全面的数据集，包括图像、视频、传感器数据等，用于训练和测试AI模型。\n\n2. 视觉（CV）大模型微调方法研究：将研究如何将通用的视觉大模型微调到特定的抽蓄工程场景，以提高识别的准确性和效率。\n\n3. 视觉大、小模型调度策略研究：将研究如何有效地结合大模型和小模型，以实现更高效的风险隐患排查和预警。\n\n4. 安全风险隐患识别预警平台研究：将开发一个平台，集成上述研究成果，实现实时监控、自动报警和数据分析等功能。\n\n每个研究内容都将深入探讨，以确保项目的成功实施和技术的创新。具体研究内容如下：\n\n1. 数据集建设方法研究：数据是AI模型训练的基础，本项目将首先对抽蓄电站的安全隐患进行分类，然后收集和标注相应的图像和视频数据，构建一个多模态的数据集。此外，还将研究数据增强技术，以提高数据集的多样性和模型的泛化能力。\n\n2. 视觉（CV）大模型微调方法研究：本项目将研究如何利用现有的视觉大模型，通过迁移学习和领域适应等技术，对模型进行微调，使其更好地适应抽蓄电站的安全隐患识别任务。\n\n3. 视觉大、小模型调度策略研究：本项目将研究如何将大模型和小模型结合起来，形成一个高效的隐患排查系统。大模型负责处理常规的、通用的安全隐患识别任务，而小模型则针对特定的、复杂的安全隐患进行识别和分析。\n\n4. 安全风险隐患识别预警平台研究：本项目将开发一个集成了上述研究成果的平台，该平台能够实时接收来自电站现场的图像和传感器数据，通过AI模型进行分析，及时发现安全隐患，并进行预警。',
                    'research_outcome': '本项目预期将达到以下研究成果：\n\n1. 构建一个高质量的抽蓄工程风险、隐患数据集，为AI模型的训练和测试提供丰富的数据资源。\n\n2. 开发出一套适用于抽水蓄能电站的AI图像检测算法，能够准确地识别和预警各种安全隐患。\n\n3. 形成一个有效的视觉（CV）大模型微调方法，提高模型在特定任务上的识别准确率和运算效率。\n\n4. 构建一个安全风险隐患识别预警平台，实现对电站现场的实时监控和自动预警，提高电站的安全运行水平。\n\n这些成果将为抽水蓄能电站的安全运行提供强有力的技术支持，并有望推广到其他工业安全领域。',
                    'annual_plan': '本项目的年度计划如下：\n\n第一年度：\n- 第一季度：项目团队组建，项目启动会议，明确项目目标和研究内容；进行市场调研和需求分析，确定技术路线和研究方案。\n\n- 第二季度：开展数据集建设方法研究，收集和标注抽蓄电站的安全隐患数据；研究视觉（CV）大模型的微调方法，选择合适的大模型进行初步的迁移学习实验。\n\n- 第三季度：继续进行数据集建设和模型微调研究；开展视觉大、小模型调度策略研究，设计模型调度框架和策略。\n\n- 第四季度：进行安全风险隐患识别预警平台的初步开发，集成已有的AI模型和算法；在菜籽坝抽蓄电站进行小规模的现场试验和验证。\n\n第二年度：\n- 第一季度：对平台进行技术优化和系统集成，完善平台的功能和用户体验；在更多的电站场景中进行模型测试和验证。\n\n- 第二季度：对平台进行技术验证和效果评估，收集用户反馈，优化平台性能；准备项目中期报告。\n\n- 第三季度：进行项目总结和成果整理，撰写项目总结报告；准备项目验收材料。\n\n- 第四季度：成果推广和应用，将研究成果应用于其他抽水蓄能电站；撰写学术论文，申请专利和软件著作权。',
                    'expected_benefits': '本项目预期将带来以下效益：\n\n1. 提高电站安全管理水平，降低事故发生率；通过实时监控和自动预警，及时发现和处理安全隐患，减少事故发生的可能性。\n\n2. 减少人力成本，提高隐患排查和风险预警的效率；自动化的隐患排查系统将减少对人工巡检的依赖，降低人力成本。\n\n3. 通过技术创新，提升集团在抽水蓄能电站领域的竞争力；本项目的研究成果将增强集团在新能源领域的技术实力和市场竞争力。\n\n4. 为集团在新能源领域的可持续发展提供技术支持；本项目的技术成果将有助于集团在新能源领域的长期发展。\n\n此外，项目还将产生一系列学术论文、专利和软件著作权，增强集团的知识产权储备。',
                    'risk_analysis': '本项目可能面临的风险包括：\n\n1. 技术风险：新技术的研发可能遇到预期之外的难题；AI模型的训练和优化是一个复杂的过程，可能会遇到数据质量、算法效率等问题。\n\n2. 市场风险：市场需求的变化可能影响项目的推广和应用；如果市场对AI在工业安全领域的应用接受度不高，可能会影响项目的推广。\n\n3. 财务风险：项目成本的超支可能影响项目的经济效益；项目实施过程中可能会遇到预算外的支出，导致成本超支。\n\n4. 法律风险：知识产权保护和合同纠纷可能对项目造成不利影响；项目涉及的技术和产品需要严格的知识产权保护，否则可能会面临侵权风险。\n\n针对这些风险，项目团队将采取相应的风险管理和应对措施，确保项目的顺利进行。具体措施包括：\n\n1. 技术风险管理：通过与高校和研究机构合作，引入专家咨询，确保技术难题得到及时解决；同时，建立技术储备和替代方案，以应对可能的技术挑战。\n\n2. 市场风险管理：通过市场调研，及时调整项目方向和产品功能，以适应市场需求；同时，加强市场推广和用户培训，提高市场接受度。\n\n3. 财务风险管理：通过严格的预算控制和成本管理，确保项目成本不超支；同时，寻求政府补贴和行业资助，降低财务压力。\n\n4. 法律风险管理：通过加强知识产权保护和合同管理，避免法律纠纷；同时，建立法律顾问团队，处理可能的法律问题。'
                    }
                
                result = generate_docx_file(project_info)
                time.sleep(5)

            if result.endswith(".docx"):
                state.message_history.append({"role": "assistant", "content": "报告生成成功，请下载查看。"})
                st.success(f"文件已生成，请下载查看。")
                # filename = result.split("/")[-1]
                url = f'http://127.0.0.1:5000/{result}'
                st.link_button("  🔗   预   览   文   件  ", url)

                # st.markdown(f'''
                # <a href={url}><button style="background-color:GreenYellow;">预览</button></a>
                # ''',
                # unsafe_allow_html=True)
                pass

            else:
                state.message_history.append({"role": "assistant", "content": "报告生成失败，请重试。"})


            # state.message_history.append({"role": "assistant", "content": response.choices[0].message.content})
            pass
        for message in state.message_history:
            if message["role"] == "system":
                continue
            else:
                st.chat_message(message["role"]).write(message["content"])

    # Create a text input for the user to type their message

    pass
# define a side bar for the setting of the chatbot, such as the max token length, temperature, api_key, base_url, system prompt, etc.
def read_json_file(file_path):
    with open(file_path, "r") as f:
        system_prompt = json.load(f)

    return system_prompt["content"]
    

def side_bar():
    st.sidebar.title("设置")
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "message_history" not in st.session_state:
        st.session_state.message_history = []

    state = st.session_state
    
    # Set a form of the settings
    with st.sidebar.form(key="settings"):
        # Set the max token length for the chatbot
        max_tokens = st.number_input("最大token长度", min_value=0, max_value=4096, value=1024, step=1)
        # Set the temperature for the chatbot
        temperature = st.number_input("Temperature", min_value=0.0, max_value=1.0, value=0.3, step=0.01)
        # Set the api key for the OpenAI API
        api_key = st.text_input("API Key", value="sk-E1CARH7sAvjVIOUgx1UkYn3pvzFX5c75oHhuULeNE6pCO3n1")
        # Set the base url for the OpenAI API
        base_url = st.text_input("Base URL",value="https://api.moonshot.cn/v1")
        # Set the system prompt for the chatbot
        system_prompt = st.text_area("系统提示", value="")
        # Add a submit button to the form
        submit = st.form_submit_button("保存设置")
        # If the submit button is pressed, save the settings
        if submit:
            welcome_message = "欢迎使用科标业项目任务书自动化生成与润色助手。请提供项目基本信息，包括项目类型、编号、名称、主持部门和负责人等，我将为您生成一个可供修改的文档，便于您查看和整理。"
            st.session_state.messages = [{"role": "assistant", "content": welcome_message}]
            st.session_state.message_history.append({"role": "assistant", "content": welcome_message})
    
            if max_tokens != 0:
                state.max_tokens = max_tokens
            state.temperature = temperature
            state.api_key = api_key
            state.base_url = base_url
            # state.message_history = []
            if system_prompt != "":
                state.system_prompt = system_prompt
                state.message_history.append({"role": "system", "content": system_prompt})
            
            state.client = OpenAI(api_key=state.api_key, base_url=state.base_url)
            pass
        
    if st.sidebar.button("开启新对话"):
        if not os.path.exists("chat_history"):
            os.mkdir("chat_history")
            pass
        with open(f"chat_history/{time.time()}.json", "w") as f:
            json.dump(state.message_history, f, ensure_ascii=False)
            pass

        state.message_history = []
        st.rerun()
    
    pass

if __name__ == "__main__":
    side_bar()
    chat_ui()
    pass