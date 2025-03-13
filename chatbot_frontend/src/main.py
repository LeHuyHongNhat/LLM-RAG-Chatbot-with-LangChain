import os
import requests
import streamlit as st

CHATBOT_URL = os.getenv("CHATBOT_URL", "http://127.0.0.1:8000/hospital-rag-agent")

# Khởi tạo session state
if "messages" not in st.session_state:
    st.session_state["messages"] = []  # Khởi tạo rõ ràng với dictionary syntax

# Phần sidebar
with st.sidebar:
    st.header("Giới thiệu")
    st.markdown(
        """
        Chatbot này được tích hợp với 
        [LangChain](https://python.langchain.com/docs/get_started/introduction),
        một agent được thiết kế để trả lời các câu hỏi về bệnh viện, bệnh nhân,
        lượt khám, bác sĩ và bảo hiểm trong một hệ thống bệnh viện mô phỏng.
        Agent sử dụng công nghệ RAG (Retrieval-Augmented Generation) để xử lý 
        cả dữ liệu có cấu trúc và phi cấu trúc được tạo tự động.
        """
    )

    st.header("Các câu hỏi mẫu")
    st.markdown("- Có những bệnh viện nào trong hệ thống?")
    st.markdown("- Thời gian chờ hiện tại ở bệnh viện Wallace-Hamilton là bao lâu?")
    st.markdown(
        "- Bệnh viện nào đang có nhiều khiếu nại về hóa đơn và "
        "vấn đề bảo hiểm?"
    )
    st.markdown("- Thời gian trung bình của các ca cấp cứu đã hoàn thành là bao nhiêu ngày?")
    st.markdown(
        "- Bệnh nhân nói gì về đội ngũ điều dưỡng tại "
        "bệnh viện Castaneda-Hardy?"
    )
    st.markdown("- Tổng số tiền thanh toán cho mỗi đơn vị bảo hiểm trong năm 2023 là bao nhiêu?")
    st.markdown("- Chi phí trung bình cho các lượt khám bảo hiểm y tế là bao nhiêu?")
    st.markdown("- Bác sĩ nào có thời gian điều trị trung bình ngắn nhất?")
    st.markdown("- Chi phí điều trị của bệnh nhân số 789 là bao nhiêu?")
    st.markdown(
        "- Tiểu bang nào có tỷ lệ tăng cao nhất về số lượt khám bảo hiểm y tế "
        "từ 2022 đến 2023?"
    )
    st.markdown("- Chi phí điều trị trung bình mỗi ngày cho bệnh nhân bảo hiểm Aetna là bao nhiêu?")
    st.markdown("- Có bao nhiêu đánh giá được viết bởi bệnh nhân ở Florida?")
    st.markdown(
        "- Đối với các lượt khám có ghi nhận triệu chứng chính, "
        "tỷ lệ có đánh giá là bao nhiêu?"
    )
    st.markdown(
        "- Tỷ lệ lượt khám có đánh giá tại mỗi bệnh viện là bao nhiêu?"
    )
    st.markdown(
        "- Bác sĩ nào nhận được nhiều đánh giá nhất cho các ca khám "
        "mà họ phụ trách?"
    )
    st.markdown("- ID của bác sĩ James Cooper là gì?")
    st.markdown(
        "- Liệt kê tất cả đánh giá về các ca khám do bác sĩ 270 điều trị, không bỏ sót ca nào."
    )

st.title("Chatbot Hệ thống Bệnh viện")
st.info(
    "Hãy hỏi tôi về bệnh nhân, lượt khám, bảo hiểm, bệnh viện, "
    "bác sĩ, đánh giá và thời gian chờ!"
)

# Hiển thị tin nhắn từ session state
for message in st.session_state["messages"]:  # Sử dụng dictionary syntax
    with st.chat_message(message["role"]):
        if "output" in message:
            st.markdown(message["output"])
        if "explanation" in message:
            with st.status("How was this generated", state="complete"):
                st.info(message["explanation"])

# Xử lý input
if prompt := st.chat_input("What do you want to know?"):
    st.chat_message("user").markdown(prompt)
    
    # Thêm tin nhắn vào session state
    st.session_state["messages"].append({"role": "user", "output": prompt})

    data = {"text": prompt}

    with st.spinner("Searching for an answer..."):
        try:
            response = requests.post(CHATBOT_URL, json=data)
            response.raise_for_status()  # Raise exception for bad status codes
            
            output_text = response.json()["output"]
            explanation = response.json()["intermediate_steps"]
        except Exception as e:
            output_text = f"""An error occurred while processing your message.
            Please try again or rephrase your message. Error: {str(e)}"""
            explanation = output_text

    st.chat_message("assistant").markdown(output_text)
    with st.status("How was this generated", state="complete"):
        st.info(explanation)

    # Thêm phản hồi vào session state
    st.session_state["messages"].append({
        "role": "assistant",
        "output": output_text,
        "explanation": explanation,
    })
