import os

from dotenv import load_dotenv
from langchain_community.vectorstores import Neo4jVector
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.chains import RetrievalQA
from langchain.prompts import (
    PromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
)

load_dotenv()

HOSPITAL_QA_MODEL = os.getenv("HOSPITAL_QA_MODEL")

neo4j_vector_index = Neo4jVector.from_existing_graph(
    embedding=GoogleGenerativeAIEmbeddings(model="models/text-embedding-004"),
    url=os.getenv("NEO4J_URI"),
    username=os.getenv("NEO4J_USERNAME"),
    password=os.getenv("NEO4J_PASSWORD"),
    index_name="reviews",
    node_label="Review",
    text_node_properties=[
        "physician_name",
        "patient_name",
        "text",
        "hospital_name",
    ],
    embedding_node_property="embedding",
)

review_template = """Công việc của bạn là sử dụng các đánh giá của bệnh nhân để trả lời bằng tiếng  các câu hỏi 
về trải nghiệm của họ tại bệnh viện. Sử dụng ngữ cảnh sau để trả lời các câu hỏi. Hãy trình bày càng chi tiết càng 
tốt, nhưng đừng bịa ra bất kỳ thông tin nào không nằm trong ngữ cảnh. Nếu bạn không biết câu trả lời, hãy nói rằng 
bạn không biết. Chỉ trả lời những câu hỏi thuộc về ngữ cảnh mà bạn đang thực hiện không trả lời bất kì thông tin nào 
khác dù bạn biết. Hãy khéo léo điều hướng người dùng đặt lại câu hỏi liên quan tới công việc bạn đang đảm nhiệm.
{context}
"""

review_system_prompt = SystemMessagePromptTemplate(
    prompt=PromptTemplate(input_variables=["context"], template=review_template)
)

review_human_prompt = HumanMessagePromptTemplate(
    prompt=PromptTemplate(input_variables=["question"], template="{question}")
)
messages = [review_system_prompt, review_human_prompt]

review_prompt = ChatPromptTemplate(
    input_variables=["context", "question"], messages=messages
)

reviews_vector_chain = RetrievalQA.from_chain_type(
    llm=ChatGoogleGenerativeAI(model=HOSPITAL_QA_MODEL, temperature=0.7),
    chain_type="stuff",
    retriever=neo4j_vector_index.as_retriever(k=12),
)
reviews_vector_chain.combine_documents_chain.llm_chain.prompt = review_prompt
