import streamlit as st
import os
from litellm import completion
import time
from datetime import datetime

# System prompt
system_prompt = "Bạn là một trợ lý AI chuyên về lập trình mạng C. Giải thích rõ ràng và chính xác."

# Cấu hình trang
st.set_page_config(page_title="Chatbot Lập Trình Mạng C", layout="wide")
st.title("💬 Chatbot Lập Trình Mạng C (Có Memory)")

# Khởi tạo session state
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": system_prompt}]
if "theme" not in st.session_state:
    st.session_state.theme = "light"
if "input_key" not in st.session_state:
    st.session_state.input_key = 0

# CSS cho giao diện (Cập nhật nút và vị trí chân trang)
theme_css = """
<style>
.stApp {{
    background-color: {bg_color};
    font-family: 'Segoe UI', sans-serif;
    color: {text_color};
    transition: all 0.3s ease;
}}
.chat-container {{
    display: flex;
    flex-direction: column;
    gap: 15px;
    margin-bottom: 25px;
    padding: 20px;
    background-color: {chat_bg};
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}}
.user-message {{
    background: linear-gradient(135deg, #4fd1c5, #38b2ac);
    color: white;
    padding: 12px 16px;
    border-radius: 8px 8px 0 8px;
    max-width: 75%;
    align-self: flex-end;
    margin-right: 10px;
    word-wrap: break-word;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}}
.ai-message {{
    background-color: {ai_msg_bg};
    color: {ai_msg_color};
    padding: 12px 16px;
    border-radius: 8px 8px 8px 0;
    max-width: 75%;
    align-self: flex-start;
    margin-left: 10px;
    word-wrap: break-word;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}}
.message-time {{
    font-size: 11px;
    color: {time_color};
    margin-top: 4px;
}}
.sidebar .sidebar-content {{
    background-color: {sidebar_bg};
    padding: 20px;
    border-radius: 8px;
}}
.stTextInput > div > div > input {{
    border-radius: 8px;
    padding: 12px;
    border: 1px solid {input_border};
    background-color: {input_bg};
    color: {text_color};
}}
.stButton > button {{
    background: linear-gradient(135deg, #ff6a00, #ff9e1b);  /* Màu sắc thay đổi tại đây */
    color: white;
    border-radius: 8px;
    padding: 8px 20px;
    border: none;
    transition: transform 0.2s ease;
}}
.stButton > button:hover {{
    transform: translateY(-2px);
}}
.typing-indicator {{
    font-style: italic;
    color: {time_color};
    margin-left: 10px;
}}
.footer-container {{
    position: fixed;
    bottom: 0;
    left: 0;
    width: 100%;
    background-color: {chat_bg};
    padding: 20px;
    box-shadow: 0 -2px 8px rgba(0, 0, 0, 0.1);
    z-index: 10;
}}
.footer-container input {{
    width: 85%;
    margin-right: 10px;
}}
.footer-button {{
    position: absolute;
    right: 10px;
    bottom: 10px;
    background: linear-gradient(135deg, #ff6a00, #ff9e1b);  /* Màu sắc thay đổi tại đây */
    color: white;
    border-radius: 8px;
    padding: 8px 20px;
    border: none;
    transition: transform 0.2s ease;
}}
.footer-button:hover {{
    transform: translateY(-2px);
}}
</style>
"""

# Áp dụng theme với màu sáng hơn
if st.session_state.theme == "dark":
    css_vars = {
        "bg_color": "#2d3748",  
        "text_color": "#edf2f7", 
        "chat_bg": "#4a5568",  
        "ai_msg_bg": "#4a5568",  
        "ai_msg_color": "#edf2f7", 
        "time_color": "#a0aec0",  
        "sidebar_bg": "#4a5568",  
        "input_border": "#718096",  
        "input_bg": "#4a5568",  
    }
else:
    css_vars = {
        "bg_color": "#ffffff", 
        "text_color": "#2d3748",  # Đen nhạt
        "chat_bg": "#f7fafc",  # Trắng nhạt
        "ai_msg_bg": "#f0f0f0",  # Xám nhạt hơn
        "ai_msg_color": "#2d3748",  # Đen nhạt
        "time_color": "#718096",  # Xám nhạt hơn
        "sidebar_bg": "#edf2f7",  # Xám rất nhạt
        "input_border": "#cbd5e0",  # Xám nhạt hơn
        "input_bg": "#ffffff", 
    }

# Áp dụng CSS
try:
    st.markdown(theme_css.format(**css_vars), unsafe_allow_html=True)
except KeyError as e:
    st.error(f"KeyError in CSS formatting: {e}")
    st.stop()

# Kiểm tra API Key
if not os.getenv("GOOGLE_API_KEY"):
    st.error("❌ GOOGLE_API_KEY chưa được thiết lập. Vui lòng thêm vào biến môi trường.")
    st.stop()

# Sidebar: Cấu hình và lịch sử hội thoại
with st.sidebar:
    st.header("⚙️ Cấu hình")
    model = st.selectbox("Chọn mô hình", ["gemini/gemini-1.5-pro", "gemini/gemini-1.5-flash"])

    # Dark mode toggle
    theme_toggle = st.checkbox("Chế độ tối", value=st.session_state.theme == "dark")
    if theme_toggle != (st.session_state.theme == "dark"):
        st.session_state.theme = "dark" if theme_toggle else "light"
        st.rerun()

    st.markdown("---")
    st.header("📜 Lịch sử hội thoại")
    if len(st.session_state.messages) <= 1:
        st.info("Chưa có cuộc hội thoại nào.")
    else:
        for idx, msg in enumerate(st.session_state.messages[1:], 1):
            if msg["role"] == "user":
                st.markdown(
                    f"**🧑 User {idx // 2 + 1}:** {msg['content'][:50]}{'...' if len(msg['content']) > 50 else ''}")
            elif msg["role"] == "assistant":
                st.markdown(f"**🤖 Bot:** {msg['content'][:50]}{'...' if len(msg['content']) > 50 else ''}")

# Hiển thị lịch sử trò chuyện trong phần chính
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for idx, msg in enumerate(st.session_state.messages[1:], 1):
    timestamp = datetime.now().strftime("%H:%M:%S")
    if msg["role"] == "user":
        st.markdown(
            f'<div class="user-message">{msg["content"]}</div>'
            f'<div class="message-time" style="text-align:right;margin-right:14px;">{timestamp}</div>',
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f'<div class="ai-message">{msg["content"]}</div>'
            f'<div class="message-time" style="text-align:left;margin-left:14px;">{timestamp}</div>',
            unsafe_allow_html=True
        )
st.markdown('</div>', unsafe_allow_html=True)

# Nút nhập và gửi tại chân trang
with st.markdown('<div class="footer-container">', unsafe_allow_html=True):
    col1, col2 = st.columns([5, 1])
    with col1:
        user_input = st.text_input("💬 Nhập câu hỏi về lập trình mạng C:", key=f"input_{st.session_state.input_key}",
                                   label_visibility="collapsed")
    with col2:
        if st.button("Gửi", key="send_button"):
            if user_input:
                # Lưu tin nhắn người dùng
                st.session_state.messages.append({"role": "user", "content": user_input})

                # Hiển thị typing indicator
                typing_placeholder = st.empty()
                typing_placeholder.markdown('<div class="typing-indicator">🤖 Bot đang nhập...</div>',
                                            unsafe_allow_html=True)

                # Gọi LLM và sinh phản hồi
                try:
                    time.sleep(1)
                    response = completion(model=model, messages=st.session_state.messages,
                                          api_key=os.getenv("GOOGLE_API_KEY"))
                    ai_response = response.choices[0].message.content
                except Exception as e:
                    ai_response = f"Lỗi: {str(e)}. Vui lòng kiểm tra API Key, model, hoặc kết nối mạng."
                    st.error(ai_response)

                # Xóa typing indicator
                typing_placeholder.empty()

                # Lưu phản hồi vào lịch sử
                st.session_state.messages.append({"role": "assistant", "content": ai_response})

                # Tăng input_key để reset ô nhập
                st.session_state.input_key += 1
                st.rerun()

# Nút xóa hội thoại (Đặt nó ở chân trang)
if st.button("🗑️ Xóa lịch sử", key="footer_button"):
    st.session_state.messages = [{"role": "system", "content": system_prompt}]
    st.success("Đã xóa toàn bộ hội thoại.")
    st.rerun()
