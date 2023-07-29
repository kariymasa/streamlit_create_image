
import openai
import streamlit as st
from PIL import Image
import requests
from io import BytesIO


# 画像をアップロード
uploaded_image = st.file_uploader("画像（.png）をアップロードしてください ※4MB未満", type=["png"])

# 画像がアップロードされたら、それをPIL Imageとして読み込む
if uploaded_image is not None:
    # Check if the image size is less than 4MB
    if len(uploaded_image.getvalue()) <= 4 * 1024 * 1024:  # 4MB in bytes
        image = Image.open(uploaded_image).convert('RGB')  # Convert the image to RGB
        st.image(image, caption='アップロード画像', use_column_width=True)
    else:
        st.error("アップロードされた画像は4MBを超えています。4MB未満の画像をアップロードしてください。")

# 画像生成
if st.button('画像生成') and uploaded_image is not None:
    with st.spinner('生成中...'):
        image_bytes_list = []

        for _ in range(2):
            buffered = BytesIO()
            image.save(buffered, format="PNG")  # Save the converted image into BytesIO object
            img_byte = buffered.getvalue()  # Get the binary representation

            response = openai.Image.create_variation(
                image=img_byte,
                n=2,
                size="512x512"
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