import requests
import streamlit as st
import streamlit.components.v1 as components

URLS = [
    "https://dlptest.com/api/http-post/",
    "https://httpbin.org/post",
    "https://postman-echo.com/post",
    "https://httpbingo.org/post",
]
BLOCK_KEYS = ["Access Denied", "content_filter_denied", "Transaction ID:"]

st.set_page_config(page_title="DLP Test", layout="wide")

# EdgeSWG 例外ページ表示
if st.session_state.get("block_html"):
    components.html(st.session_state["block_html"], height=600, scrolling=True)
    if st.button("戻る"):
        st.session_state["block_html"] = None
        st.rerun()
    st.stop()

st.title("DLP テストページ")

url = st.selectbox("送信先URL", URLS, index=0)
custom = st.text_input("任意URL（入力時はこちらを優先）")
text = st.text_area("テキスト", height=150)
file = st.file_uploader("ファイル")

with st.expander("接続設定"):
    proxy = st.text_input("プロキシ (例: http://edgeswg.example.local:8080)", "")
    verify = st.checkbox("SSL証明書を検証する", value=False)
    ca = st.text_input("CA証明書パス（EdgeSWGのSSLインターセプトCA、任意）", "")

if st.button("送信", type="primary"):
    target = custom.strip() or url
    data = {"text": text}
    files = {"file": (file.name, file.getvalue(), file.type or "application/octet-stream")} if file else None
    proxies = {"http": proxy, "https": proxy} if proxy else None
    try:
        r = requests.post(target, data=data, files=files, proxies=proxies,
                          verify=(ca or verify), timeout=30)
        body = r.text
        if any(k in body for k in BLOCK_KEYS):
            st.session_state["block_html"] = body
            st.rerun()
        if r.ok:
            st.success(f"正常に送信しました（HTTP {r.status_code}）")
        else:
            st.error(f"送信失敗（HTTP {r.status_code}）")
        st.code(body[:3000])
    except Exception as e:
        st.error(f"通信エラー: {e}")
