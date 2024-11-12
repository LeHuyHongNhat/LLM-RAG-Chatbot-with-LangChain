# 🏥 Hospital System RAG Chatbot

<p align="center">
  <img src="docs/images/chatbot-demo.gif" alt="Chatbot Demo" width="600"/>
</p>

## 📋 Giới thiệu

Một chatbot thông minh được xây dựng với LangChain và RAG (Retrieval-Augmented Generation) để trả lời các câu hỏi về hệ thống bệnh viện. Chatbot có thể:

- 🔍 Truy vấn thông tin về bệnh viện, bác sĩ và bệnh nhân
- 📊 Phân tích dữ liệu về lượt khám và chi phí
- 💬 Xử lý đánh giá và phản hồi của bệnh nhân
- ⏱️ Theo dõi thời gian chờ tại các bệnh viện
- 🏦 Quản lý thông tin bảo hiểm và thanh toán

## 🚀 Tính năng

- **RAG với LangChain**: Kết hợp dữ liệu có cấu trúc và phi cấu trúc để tạo câu trả lời chính xác
- **Neo4j Graph Database**: Lưu trữ và truy vấn dữ liệu quan hệ phức tạp
- **FastAPI Backend**: API hiệu năng cao, dễ mở rộng
- **Streamlit Frontend**: Giao diện người dùng thân thiện, tương tác trực quan
- **Xử lý ngôn ngữ tự nhiên**: Hiểu và trả lời câu hỏi bằng tiếng Việt

## 🛠️ Công nghệ sử dụng

- [LangChain](https://python.langchain.com/docs/get_started/introduction)
- [Neo4j](https://neo4j.com/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Streamlit](https://streamlit.io/)
- [Python 3.10+](https://www.python.org/)

## ⚙️ Cài đặt

1. **Clone repository**
   bash
   git clone https://github.com/LeHuyHongNhat/LLM-RAG-Chatbot-with-LangChain.git
   cd LLM-RAG-Chatbot-with-LangChain

2. **Tạo môi trường ảo**

bash
conda create -n chatbot python=3.10
conda activate chatbot

3. **Cài đặt dependencies**

bash
pip install -r requirements.txt

4. **Cấu hình môi trường**

bash
Tạo file .env từ mẫu
cp .env.example .env

Cập nhật các biến môi trường trong .env

5. **Khởi động ứng dụng**

bash
Terminal 1 - Backend
cd chatbot_api
uvicorn src.main:app --reload --port 8000
Terminal 2 - Frontend
cd chatbot_frontend
streamlit run src/main.py

## 📁 Cấu trúc Project

chatbot-pro/
├── chatbot_api/ # Backend FastAPI
│ ├── src/
│ │ ├── main.py # Entry point
│ │ ├── agents/ # LangChain agents
│ │ ├── models/ # Pydantic models
│ │ └── utils/ # Helper functions
│ └── requirements.txt
├── chatbot_frontend/ # Frontend Streamlit
│ ├── src/
│ │ └── main.py # UI components
│ └── requirements.txt
├── docs/ # Documentation
├── tests/ # Unit tests
└── README.md

## 💡 Ví dụ Sử dụng

Chatbot có thể trả lời nhiều loại câu hỏi:

- 🏥 "Có những bệnh viện nào trong hệ thống?"
- ⏰ "Thời gian chờ hiện tại ở bệnh viện Wallace-Hamilton là bao lâu?"
- 💰 "Chi phí trung bình cho các lượt khám bảo hiểm y tế là bao nhiêu?"
- 👨‍⚕️ "Bác sĩ nào có thời gian điều trị trung bình ngắn nhất?"
- 📈 "Tỷ lệ lượt khám có đánh giá tại mỗi bệnh viện là bao nhiêu?"

## 🤝 Đóng góp

Mọi đóng góp đều được chào đón! Hãy:

1. Fork repository
2. Tạo branch mới (`git checkout -b feature/AmazingFeature`)
3. Commit thay đổi (`git commit -m 'Add some AmazingFeature'`)
4. Push lên branch (`git push origin feature/AmazingFeature`)
5. Mở Pull Request

## 📝 License

Distributed under the MIT License. See `LICENSE` for more information.

## 📧 Liên hệ

Lê Huy Hồng Nhật - [@LeHuyHongNhat](https://github.com/LeHuyHongNhat)

Project Link: [https://github.com/LeHuyHongNhat/LLM-RAG-Chatbot-with-LangChain](https://github.com/LeHuyHongNhat/LLM-RAG-Chatbot-with-LangChain)
