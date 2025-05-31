from langchain_groq import ChatGroq
from Backend.config import PARAMS

# Initializes the language model using parameters defined in config.
llm = ChatGroq(
    model=PARAMS["model"],
    temperature=PARAMS["temperature"],
    max_tokens=PARAMS["max_tokens"],
)
