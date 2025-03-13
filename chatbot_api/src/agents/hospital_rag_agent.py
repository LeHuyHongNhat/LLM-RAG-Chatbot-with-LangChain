import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import (
    create_tool_calling_agent,
    Tool,
    AgentExecutor,
)
from langsmith import Client
from langchain import hub
from chatbot_api.src.chains.hospital_review_chain import reviews_vector_chain
from chatbot_api.src.chains.hospital_cypher_chain import hospital_cypher_chain
from chatbot_api.src.tools.wait_times import (
    get_current_wait_times,
    get_most_available_hospital,
)

HOSPITAL_AGENT_MODEL = os.getenv("HOSPITAL_AGENT_MODEL")
client = Client(api_key="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")
hospital_agent_prompt = client.pull_prompt("hwchase17/openai-functions-agent", include_model=True)

tools = [
    Tool(
        name="Experiences",
        func=reviews_vector_chain.invoke,
        description="""Hữu ích khi bạn cần trả lời các câu hỏi về trải nghiệm, cảm xúc của bệnh nhân hoặc bất kỳ câu 
        hỏi định tính nào khác có thể được trả lời về bệnh nhân bằng cách sử dụng tìm kiếm ngữ nghĩa. Không hữu ích 
        khi trả lời các câu hỏi khách quan liên quan đến việc đếm, phần trăm, tổng hợp hoặc liệt kê các sự kiện. Sử 
        dụng toàn bộ lời nhắc làm đầu vào cho công cụ. Ví dụ, nếu lời nhắc là "Bệnh nhân có hài lòng với dịch vụ chăm 
        sóc của họ không?", đầu vào phải là "Bệnh nhân có hài lòng với dịch vụ chăm sóc của họ không?". 
        """
    ),
    Tool(
        name="Graph",
        func=hospital_cypher_chain.invoke,
        description="""Hữu ích khi trả lời các câu hỏi về bệnh nhân, bác sĩ, bệnh viện, bên thanh toán bảo hiểm, 
        số liệu thống kê đánh giá của bệnh nhân và thông tin chi tiết về chuyến thăm bệnh viện. Sử dụng toàn bộ lời 
        nhắc làm đầu vào cho công cụ. Ví dụ, nếu lời nhắc là "Đã có bao nhiêu lần khám ?, đầu vào phải là "Đã có bao 
        nhiêu lần khám?".
        """
    ),
    Tool(
        name="Waits",
        func=get_current_wait_times,
        description="""Sử dụng khi được hỏi về thời gian chờ hiện tại tại một bệnh viện cụ thể. Công cụ này chỉ có 
        thể lấy thời gian chờ hiện tại tại một bệnh viện và không có bất kỳ thông tin nào về thời gian chờ tổng hợp 
        hoặc lịch sử. Không truyền từ "bệnh viện" làm đầu vào, chỉ truyền tên bệnh viện. Ví dụ: nếu lời nhắc là "Thời 
        gian chờ hiện tại tại Bệnh viện Jordan Inc là bao lâu?", đầu vào phải là "Jordan Inc". 
        """
    ),
    Tool(
        name="Availability",
        func=get_most_available_hospital,
        description="""Sử dụng khi bạn cần tìm ra bệnh viện nào có thời gian chờ ngắn nhất. Công cụ này không có bất 
        kỳ thông tin nào về tổng hợp hoặc thời gian chờ trong quá khứ. Công cụ này trả về một từ điển có tên bệnh 
        viện làm khóa và thời gian chờ tính bằng phút làm giá trị.
        """
    ),
]

chat_model = ChatGoogleGenerativeAI(
    model=HOSPITAL_AGENT_MODEL,
    temperature=0.7,
)

hospital_rag_agent = create_tool_calling_agent(
    llm=chat_model,
    prompt=hospital_agent_prompt,
    tools=tools,
)

hospital_rag_agent_executor = AgentExecutor(
    agent=hospital_rag_agent,
    tools=tools,
    return_intermediate_steps=True,
    verbose=True,
)
