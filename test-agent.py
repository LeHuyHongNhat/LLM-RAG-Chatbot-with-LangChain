import dotenv
from chatbot_api.src.agents.hospital_rag_agent import hospital_rag_agent_executor

dotenv.load_dotenv()


def test_agent():
    try:
        # response = hospital_rag_agent_executor.invoke(
        #     {
        #         "input": (
        #             "What have patients said about their "
        #             "quality of rest during their stay?"
        #         )
        #     }
        # )

        # print(response.get("output"))
        # response = hospital_rag_agent_executor.invoke(
        #     {
        #         "input": (
        #             "Which physician has treated the "
        #             "most patients covered by Cigna?"
        #         )
        #     }
        # )

        # print(response.get("output"))

        response = hospital_rag_agent_executor.invoke(
            {"input": "Xin chào."}
        )

        print(response.get("output"))
    except Exception as e:
        print(f"Error occurred: {str(e)}")


if __name__ == "__main__":
    test_agent()
