import dotenv
from langchain_community.document_loaders import CSVLoader
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings

REVIEWS_CSV_PATH = "data/reviews.csv"
REVIEWS_CHROMA_PATH = "chroma_data"

dotenv.load_dotenv()

loader = CSVLoader(file_path="D:\\Python Projects\\chatbot-pro\\data\\reviews.csv", source_column="review")
reviews = loader.load()

reviews_vector_db = Chroma.from_documents(
    reviews, GoogleGenerativeAIEmbeddings(model="models/text-embedding-004"), persist_directory=REVIEWS_CHROMA_PATH
)
