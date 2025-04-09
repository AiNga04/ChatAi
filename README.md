# Chatbot Lập Trình Mạng C

Ứng dụng chatbot hỗ trợ lập trình mạng C, sử dụng Streamlit để xây dựng giao diện và tích hợp các mô hình AI để trả lời câu hỏi.

## 🛠️ Các Tính Năng

- **Hỗ trợ lập trình mạng C**: Chatbot được thiết kế để trả lời các câu hỏi liên quan đến lập trình mạng C.
- **Lịch sử hội thoại**: Lưu trữ và hiển thị lịch sử hội thoại giữa người dùng và chatbot.
- **Tùy chỉnh giao diện**: Hỗ trợ chế độ sáng/tối và giao diện thân thiện.
- **Tích hợp API**: Sử dụng các API như `GROQ_API_KEY`, `GOOGLE_API_KEY` để gọi mô hình AI.

## 📂 Cấu Trúc Dự Án

- `chat.py`: Tập tin chính để chạy ứng dụng chatbot.
- `web_chat_groq_memory.py`: Phiên bản chatbot sử dụng mô hình Groq với bộ nhớ hội thoại.
- `web_chat_gemini_memory.py`: Phiên bản chatbot sử dụng mô hình Gemini với bộ nhớ hội thoại.
- `.env`: File chứa các biến môi trường (API keys).
- `.env.example`: File mẫu cho các biến môi trường.
- `.gitignore`: Bỏ qua các file/thư mục không cần thiết như `.env` và `.venv`.

## 🚀 Cách Chạy Ứng Dụng

### 1. **Cài đặt môi trường**:

Trước khi chạy ứng dụng, bạn cần cài đặt môi trường ảo và các thư viện phụ thuộc:

```bash
python -m venv .venv
.venv\Scripts\activate  # Trên Windows
source .venv/bin/activate  # Trên Linux/Mac
pip install -r requirements.txt
```

### 2. **Thiết lập biến môi trường**:

Tạo file .env dựa trên file .env.example có sẵn trong dự án. Sau đó, thêm các API keys vào file .env:

```bash
OPENAI_API_KEY=your_openai_api_key
GROQ_API_KEY=your_groq_api_key
GOOGLE_API_KEY=your_google_api_key
```

Lưu ý: Đảm bảo rằng các API keys hợp lệ và bạn đã có quyền truy cập vào các dịch vụ này.

### 3. **Chạy ứng dụng**:

Sau khi thiết lập môi trường và biến môi trường, bạn có thể chạy ứng dụng bằng lệnh:

```bash
streamlit run fileName.py
```

Ứng dụng sẽ chạy trên địa chỉ: http://localhost:8501.

### **📜 Ghi Chú**:

Đảm bảo các API keys hợp lệ và có quyền truy cập.

Không chia sẻ file .env để bảo mật thông tin nhạy cảm.

Ứng dụng yêu cầu kết nối mạng ổn định để gọi API từ các mô hình AI.
