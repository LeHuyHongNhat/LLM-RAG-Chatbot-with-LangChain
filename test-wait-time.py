import dotenv
from chatbot_api.src.tools.wait_times import (
    get_current_wait_times,
    get_most_available_hospital,
)

dotenv.load_dotenv()
print(get_current_wait_times("Wallace-Hamilton"))
print(get_current_wait_times("fake hospital"))

print(get_most_available_hospital(None))
