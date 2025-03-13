<div align="center">

# 🏥 Hospital System RAG Chatbot

![Chatbot Demo](docs/images/chatbot-demo.gif)

*Một chatbot thông minh sử dụng LangChain và RAG để tương tác với hệ thống bệnh viện*

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.68.0+-00a393.svg)](https://fastapi.tiangolo.com)
[![Made with Neo4j](https://img.shields.io/badge/Made%20with-Neo4j-008CC1.svg)](https://neo4j.com/)

</div>

## 📋 Giới thiệu

Chatbot thông minh này được xây dựng với LangChain và RAG (Retrieval-Augmented Generation) để cung cấp trải nghiệm tương tác tự nhiên với hệ thống bệnh viện. 

### Khả năng chính:

- 🔍 Truy vấn thông tin về bệnh viện, bác sĩ và bệnh nhân
- 📊 Phân tích dữ liệu về lượt khám và chi phí
- 💬 Xử lý đánh giá và phản hồi của bệnh nhân
- ⏱️ Theo dõi thời gian chờ tại các bệnh viện
- 🏦 Quản lý thông tin bảo hiểm và thanh toán

## 🚀 Tính năng

### Core Technologies
- **RAG với LangChain** 
  - Kết hợp dữ liệu có cấu trúc và phi cấu trúc 
  - Tạo câu trả lời chính xác và tự nhiên

- **Neo4j Graph Database**
  - Lưu trữ dữ liệu quan hệ phức tạp
  - Truy vấn hiệu quả với Cypher

- **FastAPI Backend**
  - API hiệu năng cao
  - Tài liệu API tự động với Swagger
  - Dễ dàng mở rộng

- **Streamlit Frontend**
  - Giao diện người dùng thân thiện
  - Tương tác trực quan
  - Cập nhật realtime

- **Xử lý ngôn ngữ tự nhiên**
  - Hỗ trợ tiếng Việt
  - Hiểu ngữ cảnh và ý định người dùng

## 🛠️ Tech Stack

<div align="center">

[![LangChain](https://img.shields.io/badge/LangChain-121212?style=for-the-badge&logo=chainlink&logoColor=white)](https://python.langchain.com/docs/get_started/introduction)
[![Neo4j](https://img.shields.io/badge/Neo4j-008CC1?style=for-the-badge&logo=neo4j&logoColor=white)](https://neo4j.com/)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)

</div>

## ⚙️ Cài đặt

### 1. Clone repository

```bash
git clone https://github.com/LeHuyHongNhat/LLM-RAG-Chatbot-with-LangChain.git
cd LLM-RAG-Chatbot-with-LangChain
```

### 2. Tạo môi trường ảo

```bash
conda create -n chatbot python=3.10
conda activate chatbot
```

### 3. Cài đặt dependencies

```bash
pip install -r requirements.txt
```

### 4. Cấu hình môi trường

```bash
# Tạo file .env từ mẫu
cp .env.example .env

# Cập nhật các biến môi trường trong .env
```

### 5. Khởi động ứng dụng

```bash
# Terminal 1 - Backend
uvicorn chatbot_api.src.main:app --reload --port 8000

# Terminal 2 - Frontend
cd chatbot_frontend
streamlit run src/main.py
```

## 📁 Cấu trúc Project

```
chatbot-pro/
├── chatbot_api/           # Backend FastAPI
│   ├── src/
│   │   ├── main.py       # Entry point
│   │   ├── agents/       # LangChain agents
│   │   ├── models/       # Pydantic models
│   │   └── utils/        # Helper functions
│   └── requirements.txt
├── chatbot_frontend/      # Frontend Streamlit
│   ├── src/
│   │   └── main.py       # UI components
│   └── requirements.txt
├── docs/                  # Documentation
├── tests/                 # Unit tests
└── README.md
```

## 💡 Ví dụ Sử dụng

Chatbot có thể trả lời nhiều loại câu hỏi:

| Loại câu hỏi | Ví dụ |
|--------------|-------|
| 🏥 Thông tin bệnh viện | "Có những bệnh viện nào trong hệ thống?" |
| ⏰ Thời gian chờ | "Thời gian chờ hiện tại ở bệnh viện Wallace-Hamilton là bao lâu?" |
| 💰 Chi phí | "Chi phí trung bình cho các lượt khám bảo hiểm y tế là bao nhiêu?" |
| 👨‍⚕️ Thông tin bác sĩ | "Bác sĩ nào có thời gian điều trị trung bình ngắn nhất?" |
| 📈 Thống kê | "Tỷ lệ lượt khám có đánh giá tại mỗi bệnh viện là bao nhiêu?" |

## 🤝 Đóng góp

Mọi đóng góp đều được chào đón! Quy trình đóng góp:

1. Fork repository
2. Tạo branch mới (`git checkout -b feature/AmazingFeature`)
3. Commit thay đổi (`git commit -m 'Add some AmazingFeature'`)
4. Push lên branch (`git push origin feature/AmazingFeature`)
5. Mở Pull Request

## 📝 License

Distributed under the MIT License. See [`LICENSE`](LICENSE) ([View on GitHub](https://github.com/LeHuyHongNhat/LLM-RAG-Chatbot-with-LangChain/tree/master?tab=MIT-1-ov-file)) for more information.

## 📧 Liên hệ

Lê Huy Hồng Nhật - [@LeHuyHongNhat](https://github.com/LeHuyHongNhat)

Project Link: [https://github.com/LeHuyHongNhat/LLM-RAG-Chatbot-with-LangChain](https://github.com/LeHuyHongNhat/LLM-RAG-Chatbot-with-LangChain)

---
<div align="center">
⭐️ Nếu dự án này hữu ích, hãy cho nó một ngôi sao trên GitHub! ⭐️
</div>
