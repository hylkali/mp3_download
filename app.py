import streamlit as st
import requests
from bs4 import BeautifulSoup
import yt_dlp
import os

def get_free_https_proxies():
    url = 'https://www.sslproxies.org/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    proxy_list = []

    for row in soup.select("table#proxylisttable tbody tr"):
        cols = row.find_all("td")
        ip = cols[0].text
        port = cols[1].text
        https = cols[6].text
        if https.lower() == "yes":
            proxy_list.append(f"http://{ip}:{port}")

    return proxy_list

def test_proxy(proxy):
    try:
        res = requests.get("https://www.youtube.com", proxies={"http": proxy, "https": proxy}, timeout=3)
        return res.status_code == 200
    except:
        return False

def get_working_proxy():
    proxies = get_free_https_proxies()
    for proxy in proxies:
        if test_proxy(proxy):
            return proxy
    return None

def download_audio(url, proxy):
    with yt_dlp.YoutubeDL({
        'format': 'bestaudio/best',
        'outtmpl': '%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'proxy': proxy,
        'quiet': False,
        'http_headers': {
            'User-Agent': 'Mozilla/5.0',
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': 'https://www.youtube.com/',
        },
    }) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info_dict).replace(".webm", ".mp3").replace(".m4a", ".mp3")

# Streamlit UI
st.title("유튜브 mp3 다운로드 with 자동 프록시")

video_url = st.text_input("유튜브 영상 링크를 입력하세요")
if st.button("MP3 다운로드"):
    if video_url:
        with st.spinner("프록시 찾는 중..."):
            proxy = get_working_proxy()
        if proxy:
            st.success(f"사용 중인 프록시: {proxy}")
            try:
                with st.spinner("다운로드 중..."):
                    file_path = download_audio(video_url, proxy)
                with open(file_path, "rb") as f:
                    st.download_button(
                        label="MP3 다운로드",
                        data=f,
                        file_name=os.path.basename(file_path),
                        mime="audio/mpeg"
                    )
                os.remove(file_path)
            except Exception as e:
                st.error(f"다운로드 실패: {e}")
        else:
            st.error("사용 가능한 프록시를 찾을 수 없습니다.")

# import streamlit as st
# import yt_dlp
# import uuid
# import os

# st.set_page_config(page_title="YouTube MP3 변환기", layout="centered")
# st.title("🎵 YouTube MP3 변환기")
# st.caption("유튜브 링크를 입력하면 MP3 파일로 변환해 다운로드할 수 있어요.")

# url = st.text_input("🔗 유튜브 링크를 입력하세요")

# if st.button("MP3 다운로드") and url:
#     with st.spinner("MP3로 변환 중입니다..."):
#         video_id = str(uuid.uuid4())
#         output_file = f"{video_id}.mp3"
#         ydl_opts = {
#             'format': 'bestaudio/best',
#             'outtmpl': f'{video_id}.%(ext)s',
#             'postprocessors': [{
#                 'key': 'FFmpegExtractAudio',
#                 'preferredcodec': 'mp3',
#                 'preferredquality': '192',
#             }],
#             'quiet': True,
#             'http_headers': {
#                 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
#                 'Accept-Language': 'en-US,en;q=0.9',
#                 'Referer': 'https://www.youtube.com/',
#             },
#             'nocheckcertificate': True,
#         }



#         try:
#             with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#                 ydl.download([url])
#             with open(output_file, 'rb') as f:
#                 st.success("변환 완료! 아래 버튼을 눌러 다운로드하세요.")
#                 st.download_button(
#                     label="📥 MP3 다운로드",
#                     data=f,
#                     file_name="youtube_audio.mp3",
#                     mime="audio/mpeg"
#                 )
#             os.remove(output_file)
#         except Exception as e:
#             st.error(f"오류 발생: {e}")
