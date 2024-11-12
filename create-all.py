import os

# Định nghĩa cấu trúc thư mục
directory_structure = {
    "chatbot_api": {
        "src": {
            "agents": ["hospital_rag_agent.py"],
            "chains": ["hospital_cypher_chain.py", "hospital_review_chain.py"],
            "models": ["hospital_rag_query.py"],
            "tools": ["wait_times.py"],
            "utils": ["async_utils.py"],
            ".": ["entrypoint.sh", "main.py"]
        },
        ".": ["Dockerfile", "pyproject.toml"]
    },
    "chatbot_frontend": {
        "src": ["entrypoint.sh", "main.py"],
        ".": ["Dockerfile", "pyproject.toml"]
    },
    "hospital_neo4j_etl": {
        "src": ["entrypoint.sh", "hospital_bulk_csv_write.py"],
        ".": ["Dockerfile", "pyproject.toml"]
    },
    "tests": ["async_agent_requests.py", "sync_agent_requests.py"],
    ".": [".env", "docker-compose.yml"]
}


# Hàm tạo thư mục và tập tin
def create_structure(base_path, structure):
    for name, content in structure.items():
        path = os.path.join(base_path, name)
        os.makedirs(path, exist_ok=True)

        if isinstance(content, dict):
            # Tiếp tục tạo thư mục con
            create_structure(path, content)
        else:
            # Tạo các tập tin rỗng trong thư mục
            for file in content:
                open(os.path.join(path, file), 'a').close()


# Tạo cấu trúc từ thư mục gốc
create_structure(".", directory_structure)
