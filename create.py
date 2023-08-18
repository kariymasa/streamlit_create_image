# 必要なモジュールのインポート
import os
import streamlit as st
# 環境変数の設定
os.environ["OPENAI_API_KEY"] = st.secrets["OpenAIAPI"]["OPENAI_API_KEY"]

import openai
from PIL import Image
import requests
from io import BytesIO



# Streamlitの設定
st.set_page_config(page_title='text2image', page_icon=":smiley:", layout='centered', initial_sidebar_state='auto')
st.title('「アートの瞬間、あなたの手中に」')

st.sidebar.image('data/image_1.png')

# スタイルの選択
style_list = ['Anime','Photographic','Digital Art', 'Comic Book', 'Fantasy Art', 'Analog Film', 'Neon Punk', 
              'Isometric', 'Low Poly', 'Origami', 'Line Art', 'Cinematc', '3D Model', 'Pixel Art']
style = st.sidebar.selectbox('スタイルを選択してください。', style_list)

# Qualityリストの選択
quality_list = ['Masterpiece', 'high quality', 'epic high quality', 'best quality', 'detailed', 'highly detailed', 
                'insanely detailed', 'hyper realistic', '4K']
quality = st.sidebar.selectbox('クオリティを選択してください。', quality_list)

# 画像のサイズを選択
size_list = ["512x512", "1024x1024", "256x256"]
size = st.sidebar.radio('画像のサイズを選択してください。', size_list, index=0)

# プロンプトの入力
text_input = st.text_input('生成したい画像を日本語で入力してください。')

## Session state for translated text
if "translated_text" not in st.session_state or st.session_state.prev_text_input != text_input:
    # 日本語を英語に翻訳
    prompt_translation = f'''日本語を英語に翻訳します。

日本語: {text_input}
英語:'''
    response_translation = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt_translation,
        temperature=0
    )
    st.session_state.translated_text = response_translation["choices"][0]["text"].strip()
    st.session_state.prev_text_input = text_input

prompt = style + "," + quality + "," + st.session_state.translated_text

# 翻訳結果の表示
st.text("翻訳結果（プロンプト）: " + prompt)

# 画像生成数の選択
num_images = st.sidebar.slider('生成枚数を選択してください。', 1, 10)

# 画像生成
if st.button('画像生成'):
    with st.spinner('生成中...'):
        image_bytes_list = []

        for _ in range(num_images):
            response = openai.Image.create(
                prompt=prompt,
                size=size
            )
            image_url = response["data"][0]["url"]

            # 画像をダウンロードし、ストリームリットで表示
            image_response = requests.get(image_url)
            image_bytes = BytesIO(image_response.content).read()
            image_bytes_list.append(image_bytes)
            st.image(image_bytes, caption=f'生成画像 {len(image_bytes_list)}', use_column_width=True)
            
        for i, img_bytes in enumerate(image_bytes_list):
            st.download_button(
                label=f"画像 {i+1} ダウンロード",
                data=img_bytes,
                file_name=f'image_{i+1}.png',
                mime="image/png"
            )
