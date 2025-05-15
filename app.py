import streamlit as st
import yt_dlp
import uuid
import os

st.set_page_config(page_title="YouTube MP3 변환기", layout="centered")
st.title("🎵 YouTube MP3 변환기")
st.caption("유튜브 링크를 입력하면 MP3 파일로 변환해 다운로드할 수 있어요.")

url = st.text_input("🔗 유튜브 링크를 입력하세요")

if st.button("MP3 다운로드") and url:
    with st.spinner("MP3로 변환 중입니다..."):
        video_id = str(uuid.uuid4())
        output_file = f"{video_id}.mp3"
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': f'{video_id}.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'quiet': True,
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
                'Accept-Language': 'en-US,en;q=0.9',
                'Referer': 'https://www.youtube.com/',
            },
            'nocheckcertificate': True,
        }



        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            with open(output_file, 'rb') as f:
                st.success("변환 완료! 아래 버튼을 눌러 다운로드하세요.")
                st.download_button(
                    label="📥 MP3 다운로드",
                    data=f,
                    file_name="youtube_audio.mp3",
                    mime="audio/mpeg"
                )
            os.remove(output_file)
        except Exception as e:
            st.error(f"오류 발생: {e}")
