import streamlit as st
import os
from litellm import completion
import time
from datetime import datetime

# System prompt: điều hướng tính cách và vai trò AI
system_prompt = "Bạn là một trợ lý AI chuyên về lập trình mạng C. Giải thích rõ ràng và chính xác."

# Thiết lập tiêu đề
st.set_page_config(page_title="Chatbot Lập Trình Mạng C", layout="wide")
st.title("💬 Chatbot Lập Trình Mạng C (Có Memory)")

# Thêm CSS tuỳ chỉnh
st.markdown("""
    <style>
    .stApp {
        background-color: #f7f7f7;
        font-family: 'Segoe UI', sans-serif;
    }
    .chat-container {
        display: flex;
        flex-direction: column;
        gap: 12px;
        margin-bottom: 20px;
    }
    .user-message {
        background-color: #34C759;
        color: white;
        padding: 12px 16px;
        border-radius: 16px;
        max-width: 75%;
        align-self: flex-end;
        margin-right: 10px;
        word-wrap: break-word;
    }
    .ai-message {
        background-color: #e0e0e0;
        color: #111;
        padding: 12px 16px;
        border-radius: 16px;
        max-width: 75%;
        align-self: flex-start;
        margin-left: 10px;
        word-wrap: break-word;
    }
    .message-time {
        font-size: 11px;
        color: #888;
        margin-top: 4px;
    }
    .copy-button {
        font-size: 12px;
        margin-left: 12px;
        color: #888;
        cursor: pointer;
    }
    .copy-button:hover {
        color: #555;
    }
    </style>
""", unsafe_allow_html=True)

# Kiểm tra API Key
if not os.getenv("GROQ_API_KEY"):
    st.error("❌ GROQ_API_KEY chưa được thiết lập. Vui lòng thêm vào biến môi trường.")
    st.stop()

# Chọn mô hình từ sidebar
with st.sidebar:
    st.header("⚙️ Cấu hình")
    model = st.selectbox("Chọn mô hình", ["groq/llama3-8b-8192", "groq/qwen-2.5-coder-32b"])
    st.markdown("---")
    st.header("📜 Lịch sử hội thoại")

    if "messages" not in st.session_state or len(st.session_state.messages) <= 1:
        st.info("Chưa có cuộc hội thoại nào.")
    else:
        for idx, msg in enumerate(st.session_state.messages[1:], 1):
            if msg["role"] == "user":
                st.markdown(f"**🧑 User {idx//2 + 1}:** {msg['content']}")
            elif msg["role"] == "assistant":
                st.markdown(f"**🤖 Bot:** {msg['content']}")

# Khởi tạo lịch sử hội thoại nếu chưa có
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": system_prompt}]

# Hiển thị lịch sử hội thoại
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for msg in st.session_state.messages[1:]:
    timestamp = datetime.now().strftime("%H:%M:%S")
    if msg["role"] == "user":
        st.markdown(
            f'<div class="user-message">{msg["content"]}</div>'
            f'<div class="message-time" style="text-align:right;margin-right:14px;">{timestamp}</div>',
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f'<div class="ai-message">{msg["content"]}'
            f'<span class="copy-button" onclick="navigator.clipboard.writeText(`{msg["content"]}`)">📋 Copy</span></div>'
            f'<div class="message-time" style="text-align:left;margin-left:14px;">{timestamp}</div>',
            unsafe_allow_html=True
        )
st.markdown('</div>', unsafe_allow_html=True)

# Ô nhập và xử lý
col1, col2 = st.columns([5, 1])
with col1:
    user_input = st.text_input("💬 Nhập câu hỏi về lập trình mạng C:", key="user_input", label_visibility="collapsed")
with col2:
    if st.button("Gửi"):
        if user_input:
            # Lưu tin nhắn người dùng
            st.session_state.messages.append({"role": "user", "content": user_input})

            # Gọi LLM và sinh phản hồi
            try:
                with st.spinner("🤖 Đang trả lời..."):
                    time.sleep(1)
                    response = completion(model=model, messages=st.session_state.messages)
                    ai_response = response.choices[0].message.content
            except Exception as e:
                ai_response = f"Lỗi: {str(e)}"
                st.error(ai_response)

            # Lưu phản hồi
            st.session_state.messages.append({"role": "assistant", "content": ai_response})
            st.rerun()

# Nút xóa hội thoại
if st.button("🗑️ Xóa lịch sử"):
    st.session_state.messages = [{"role": "system", "content": system_prompt}]
    st.success("Đã xóa toàn bộ hội thoại.")
    st.rerun()
