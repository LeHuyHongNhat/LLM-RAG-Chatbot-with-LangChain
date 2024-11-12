import dotenv
from chatbot_api.src.chains.hospital_cypher_chain import hospital_cypher_chain

dotenv.load_dotenv()

question = """What is the average visit duration for
emergency visits in North Carolina?"""
response = hospital_cypher_chain.invoke(question)

print(response.get("result"))
