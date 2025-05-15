# Mô tả Hệ thống Chatbot Bệnh viện

Tài liệu này mô tả chi tiết kiến trúc, các thành phần và cách chúng liên kết với nhau trong hệ thống chatbot bệnh viện.

## 1. Kiến trúc Hệ thống Tổng quan

Hệ thống được thiết kế theo kiến trúc microservices và được container hóa bằng Docker, bao gồm các thành phần chính sau:

- **Frontend (`chatbot_frontend`):** Giao diện người dùng web được xây dựng bằng Streamlit, cho phép người dùng tương tác với chatbot.
- **Backend API (`chatbot_api`):** Một API service được xây dựng bằng FastAPI, xử lý logic của chatbot, bao gồm việc điều phối agent, tương tác với LLM (Gemini) và cơ sở dữ liệu.
- **VectorDB & Graph Database (Neo4j):** Sử dụng Neo4j cho cả hai mục đích:
  - Lưu trữ dữ liệu có cấu trúc về bệnh viện, bệnh nhân, bác sĩ, lượt khám, bảo hiểm dưới dạng graph.
  - Lưu trữ vector embeddings của các đánh giá (reviews) của bệnh nhân để phục vụ tìm kiếm ngữ nghĩa (semantic search) trong RAG.
- **ETL Service (`hospital_neo4j_etl`):** Một service chịu trách nhiệm trích xuất, chuyển đổi và tải (Extract, Transform, Load) dữ liệu từ các file CSV vào cơ sở dữ liệu Neo4j.
- **LLM (Google Gemini):** Được sử dụng làm bộ não của chatbot, tích hợp thông qua Langchain, để hiểu câu hỏi, quyết định hành động và tạo ra câu trả lời.

Các service này được quản lý và kết nối với nhau thông qua `docker-compose`.

```mermaid
graph TD
    User -->|Tương tác| Frontend[Frontend (Streamlit)]
    Frontend -->|HTTP Request (Hỏi)| API[Backend API (FastAPI)]
    API -->|Xử lý & Điều phối| Agent[Langchain Agent (Gemini)]
    Agent -->|Chọn Tool| Tools[Công cụ (Tools)]
    Tools -->|Tìm kiếm ngữ nghĩa| ReviewChain[Review Chain (Vector Search)]
    Tools -->|Truy vấn Graph| CypherChain[Cypher Chain (Graph Query)]
    Tools -->|Thông tin thời gian chờ| WaitTimeTools[Wait Time Tools]
    ReviewChain -->|Truy vấn Vector| Neo4j[Neo4j (Vector Embeddings)]
    CypherChain -->|Thực thi Cypher| Neo4jGraph[Neo4j (Graph Data)]
    WaitTimeTools -->|Lấy dữ liệu| ExternalOrDB[(Có thể là DB/API khác)]
    Neo4j -->|Dữ liệu Review| ReviewChain
    Neo4jGraph -->|Kết quả Graph| CypherChain
    Agent -->|Tổng hợp & Tạo câu trả lời (Gemini)| API
    API -->|HTTP Response (Trả lời)| Frontend
    User

    ETL[ETL Service (Python Script)] -->|Nạp dữ liệu & Embeddings?| Neo4j
    CSVs[Nguồn dữ liệu CSV] --> ETL
```

## 2. Backend (`chatbot_api`) Hoạt động Như Thế Nào?

Backend được xây dựng bằng **FastAPI** và chịu trách nhiệm chính cho việc xử lý logic của chatbot.

- **File chính:** `chatbot_api/src/main.py`
- **Framework:** FastAPI
- **Chức năng chính:**
  - Cung cấp một endpoint API chính: `/hospital-rag-agent` (POST).
  - Nhận câu hỏi từ frontend dưới dạng `HospitalQueryInput`.
  - Sử dụng `hospital_rag_agent_executor` (một Langchain Agent) để xử lý câu hỏi.
  - Trả về câu trả lời và các bước trung gian (intermediate steps) dưới dạng `HospitalQueryOutput`.
  - Có endpoint `/` (GET) để kiểm tra trạng thái hoạt động.
- **Langchain Agent (`hospital_rag_agent_executor`):**
  - Được định nghĩa trong `chatbot_api/src/agents/hospital_rag_agent.py`.
  - Sử dụng mô hình **Google Gemini** (thông qua `ChatGoogleGenerativeAI`) làm LLM chính để suy luận và ra quyết định.
  - Được trang bị các **Tools** để tương tác với dữ liệu và dịch vụ:
    - **`Experiences` Tool:** Sử dụng `reviews_vector_chain` để trả lời các câu hỏi định tính dựa trên đánh giá của bệnh nhân (tìm kiếm vector trên Neo4j).
    - **`Graph` Tool:** Sử dụng `hospital_cypher_chain` để trả lời các câu hỏi về dữ liệu có cấu trúc (bệnh nhân, bác sĩ, bệnh viện, v.v.) bằng cách tạo và thực thi các truy vấn Cypher lên Neo4j.
    - **`Waits` Tool:** Lấy thông tin thời gian chờ hiện tại ở một bệnh viện cụ thể.
    - **`Availability` Tool:** Tìm bệnh viện có thời gian chờ ngắn nhất.
  - Agent quyết định tool nào sẽ sử dụng dựa trên câu hỏi của người dùng, sau đó gọi tool đó và sử dụng kết quả để tạo câu trả lời (với sự trợ giúp của Gemini).
  - Sử dụng prompt từ Langsmith (`hwchase17/openai-functions-agent`) để điều khiển hành vi của agent.

## 3. Frontend (`chatbot_frontend`) Hoạt động Như Thế Nào?

Frontend là một ứng dụng web được xây dựng bằng **Streamlit**, cung cấp giao diện người dùng cho chatbot.

- **File chính:** `chatbot_frontend/src/main.py`
- **Framework:** Streamlit
- **Chức năng chính:**
  - Hiển thị giao diện chat.
  - Hiển thị các câu hỏi mẫu và giới thiệu về chatbot.
  - Gửi câu hỏi của người dùng đến endpoint `/hospital-rag-agent` của backend API.
  - Nhận và hiển thị câu trả lời từ backend.
  - Hiển thị các bước trung gian (`intermediate_steps`) mà agent đã thực hiện để người dùng hiểu được quá trình tạo ra câu trả lời.
  - Lưu trữ lịch sử chat trong `st.session_state`.
  - Địa chỉ backend API được cấu hình qua biến môi trường `CHATBOT_URL` (mặc định là `http://api:8000/hospital-rag-agent` khi chạy trong Docker).

## 4. VectorDB (Neo4j) Hoạt động Như Thế Nào?

Neo4j được sử dụng như một cơ sở dữ liệu đa năng, vừa là Graph Database vừa là Vector Store.

- **Là Graph Database:**
  - Lưu trữ dữ liệu có cấu trúc về bệnh viện, bệnh nhân, bác sĩ, lượt khám, thanh toán, bảo hiểm và các mối quan hệ giữa chúng.
  - Dữ liệu này được nạp từ các file CSV thông qua service `hospital_neo4j_etl`.
  - `hospital_cypher_chain` trong backend tương tác với graph này bằng cách:
    1.  Sử dụng LLM (Gemini) để dịch câu hỏi của người dùng thành một truy vấn Cypher.
    2.  Thực thi truy vấn Cypher trên Neo4j.
    3.  Sử dụng LLM (Gemini) để diễn giải kết quả truy vấn thành câu trả lời tự nhiên.
- **Là Vector Store (cho RAG):**
  - Lưu trữ vector embeddings của các đánh giá (`Review`) của bệnh nhân.
  - Chain `reviews_vector_chain` trong backend chịu trách nhiệm:
    1.  Kết nối tới một index vector trong Neo4j có tên là "reviews" trên các node `Review`.
    2.  Sử dụng `GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")` để tạo vector embedding cho câu hỏi của người dùng (khi truy vấn) và (theo lý thuyết) cho các review (khi tạo index).
    3.  Tìm kiếm các review có vector embedding gần giống nhất với vector của câu hỏi (tìm kiếm tương đồng ngữ nghĩa).
    4.  Các review này sau đó được đưa vào prompt cùng với câu hỏi gốc để LLM (Gemini) tạo ra câu trả lời dựa trên ngữ cảnh.
- **Quá trình ETL (`hospital_neo4j_etl`):**
  - Script `hospital_neo4j_etl/src/hospital_bulk_csv_write.py` đọc dữ liệu từ các file CSV và tải vào Neo4j, bao gồm các node (Hospital, Patient, Physician, Review, v.v.) và các mối quan hệ giữa chúng.
  - **Lưu ý quan trọng:** Script ETL hiện tại (`hospital_bulk_csv_write.py`) chỉ tải dữ liệu text của các review mà **không có bước rõ ràng để tạo và lưu trữ vector embeddings** cho các review này vào thuộc tính `embedding` của node `Review`. Tuy nhiên, `reviews_vector_chain` lại mong đợi thuộc tính này chứa sẵn embeddings. Điều này có thể là một điểm cần xem xét hoặc có một bước xử lý embedding bị thiếu/ẩn. `Neo4jVector.from_existing_graph` trong `reviews_vector_chain` chỉ định `embedding_node_property="embedding"`, ngụ ý rằng embeddings đã được tính toán và lưu trữ trước đó.

## 5. Gemini Được Implement Như Thế Nào?

Google Gemini là mô hình ngôn ngữ lớn (LLM) cốt lõi được sử dụng trong hệ thống này, tích hợp chủ yếu thông qua thư viện Langchain.

- **Trong Backend Agent (`hospital_rag_agent`):**
  - `ChatGoogleGenerativeAI` (wrapper của Langchain cho Gemini) được sử dụng làm LLM chính của agent.
  - Model cụ thể được chỉ định qua biến môi trường `HOSPITAL_AGENT_MODEL`.
  - Gemini chịu trách nhiệm:
    - Hiểu ý định của người dùng từ câu hỏi.
    - Quyết định sử dụng tool nào trong số các tool có sẵn (Experiences, Graph, Waits, Availability) để thu thập thông tin.
    - Tạo đầu vào phù hợp cho tool được chọn.
    - Tổng hợp thông tin từ các tool và tạo ra câu trả lời cuối cùng bằng ngôn ngữ tự nhiên.
- **Trong `reviews_vector_chain`:**
  - `ChatGoogleGenerativeAI` (với model `HOSPITAL_QA_MODEL`) được sử dụng để tạo câu trả lời dựa trên các review được truy xuất từ Neo4j (sau bước tìm kiếm vector).
- **Trong `hospital_cypher_chain`:**
  - Sử dụng hai instance của `ChatGoogleGenerativeAI`:
    1.  Một LLM (`cypher_llm` với model `HOSPITAL_CYPHER_MODEL`) để dịch câu hỏi của người dùng thành truy vấn Cypher.
    2.  Một LLM khác (`qa_llm` với model `HOSPITAL_QA_MODEL`) để chuyển đổi kết quả từ truy vấn Cypher thành câu trả lời dễ hiểu.
- **Tạo Embeddings:**
  - `GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")` được sử dụng trong `reviews_vector_chain` để (ít nhất là) tạo embedding cho câu hỏi của người dùng lúc truy vấn. Model này cũng được giả định là đã được sử dụng để tạo embeddings cho các review lưu trong Neo4j.

## 6. API Backend Cung Cấp

Backend API (`chatbot_api`) cung cấp các endpoint sau:

1.  **`GET /`**

    - **Mô tả:** Endpoint kiểm tra trạng thái hoạt động của service API.
    - **Request Body:** Không có.
    - **Response Body (JSON):**
      ```json
      {
        "status": "running"
      }
      ```
    - **Hoạt động:** Trả về trạng thái `running` nếu API hoạt động bình thường.

2.  **`POST /hospital-rag-agent`**
    - **Mô tả:** Endpoint chính để tương tác với chatbot. Nhận câu hỏi và trả về câu trả lời được xử lý bởi Langchain agent.
    - **Request Body (JSON - `HospitalQueryInput`):**
      ```json
      {
        "text": "Câu hỏi của người dùng ở đây"
      }
      ```
    - **Response Body (JSON - `HospitalQueryOutput`):**
      ```json
      {
        "input": "Câu hỏi của người dùng (lặp lại)",
        "output": "Câu trả lời của chatbot",
        "intermediate_steps": [
          "Bước 1: Agent đã làm gì...",
          "Bước 2: Agent đã sử dụng tool X với input Y...",
          "Bước 3: Kết quả từ tool X..."
        ]
      }
      ```
    - **Hoạt động:**
      1.  Nhận `text` (câu hỏi) từ request.
      2.  Gọi hàm `invoke_agent_with_retry` để thực thi `hospital_rag_agent_executor.ainvoke({"input": query.text})`.
      3.  Agent sẽ xử lý câu hỏi, có thể gọi một hoặc nhiều tools.
      4.  Kết quả từ agent (bao gồm câu trả lời `output` và các bước trung gian `intermediate_steps`) được trả về.
      5.  Các bước trung gian được chuyển thành chuỗi trước khi trả về.

## 7. Các Điểm Cần Lưu Ý và Cải Thiện Tiềm Năng

- **Tạo Embedding trong ETL:** Cần làm rõ hoặc bổ sung bước tạo và lưu trữ vector embeddings cho các review trong quá trình ETL. Nếu không, chức năng tìm kiếm ngữ nghĩa trên review sẽ không hoạt động đúng.
- **Health Check Endpoint:** `docker-compose.yml` định nghĩa một health check cho `api` service tại `/health`, nhưng endpoint này không được định nghĩa trong `chatbot_api/src/main.py`. Cần đồng bộ hóa điều này.
- **`allow_dangerous_requests=True` trong `GraphCypherQAChain`:** Cài đặt này nên được xem xét cẩn thận về mặt bảo mật. Mặc dù prompt cố gắng ngăn chặn các truy vấn sửa đổi dữ liệu, việc cho phép các yêu cầu nguy hiểm tiềm ẩn rủi ro.
- **Quản lý Biến Môi trường:** Hệ thống phụ thuộc nhiều vào các biến môi trường (`.env` file). Cần đảm bảo file `.env` được quản lý an toàn và đúng cách.
- **Xử lý Lỗi và Độ Tin Cậy:** Cơ chế `async_retry` trong API là một điểm tốt. Có thể mở rộng thêm các chiến lược xử lý lỗi và giám sát chi tiết hơn.

```

```
