# 大模型报告生成
- 大模型按照给定的word模板，结合word文档中的标题，生成对应的文本内容，返回一个有标题、有内容的、已整理好的word，提供下载链接


## 1. 运行步骤
1. 激活环境 ```conda activate /group_share/condaenv/llmdemo```
2. 启动word下载服务器 ```python main.py```，启动服务即可，如果只需要下载word文件，则不需要打开网页
3. 启动大模型服务器  ```python -m streamlit run chatui.py```
4. 在浏览器中打开 ```http://localhost:8501```



## 2. 前期安装准备

### 激活conda环境
```bash
conda activate /group_share/condaenv/llmdemo
cd /group_share/demo930/report
```

### pip 环境安装
见当前文件夹下requirements.txt

### npm安装
```bash
apt update
apt install nodejs npm
```
> Note! 如果出现报错 *rollbackFailedOptional: verb npm-session xxx*
```bash
npm config set registry http://registry.npm.taobao.org
npm install webpack -g
```
### docx-preview安装
- 见网址[docx-preview](https://github.com/VolodymyrBaydalka/docxjs)，只能预览docx后缀文件
```bash
npm install docx-preview
```

### 安装python-docx，用于python生成docx文件
```python
pip install python-docx
```

### streamlit运行网页
```bash
python -m streamlit run chatui.py
```


## 3. 代码备忘录

### streamlit 录音功能
需安装 audiorecorder  stylable_container


```python
# streamlit 添加录音功能
import streamlit as st
from audiorecorder import audiorecorder
from streamlit_extras.stylable_container import stylable_container

st.title("Audio Recorder")
# 这个格式适合添加其他功能按钮
with stylable_container(
        key="bottom_content",
        css_styles="""
            {
                position: fixed;
                bottom: 120px;
            }
            """,
    ):
        audio = audiorecorder("🎙️ start", "🎙️ stop")
        print('audio: ', audio)
        if len(audio) > 0:
            audio.export("audio.mp3", format="mp3")

st.chat_input("These are words.")

with stylable_container(
        key="text_input1",
        css_styles="""
            {
                position: fixed;
                bottom: 200px;
            }
            """,
    ):
    st.text_input(label = 'text' ,value = "These are words.")
```

