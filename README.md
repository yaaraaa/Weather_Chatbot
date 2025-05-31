# 🌦️ Travel and Weather Assistant

This project is a modular, conversational assistant that helps users with weather-based queries and travel recommendations. It combines **LLM-driven responses**, **real-time weather data**, and **vector search over knowledge store** to produce intelligent, helpful replies.

---

### Overview

The assistant performs four main tasks:

1. **Document Upload & Indexing**  
   Users can upload a PDF document, which is parsed and stored in a vector database for semantic retrieval.

2. **Intelligent Chat Interface**  
   The assistant understands user intent—whether they're asking about the weather or seeking travel recommendations—and generates relevant responses using both external APIs and internal knowledge store search.

3. **Weather Integration**  
   Real-time weather data is fetched and classified into intuitive categories (sunny, rainy, snowy, windy, cloudy) derived from the provided input document. This information is used in searching for specific documents through milvus data filtering.

4. **Vector Search**  
   The assistant performs search on vector embedded documents, filtered by weather category and country, to retrieve the most relevant content.
---
#### System Architecture

_A diagram visualizing the overall system architecture of the chatbot._
![Blank diagram (9)](https://github.com/user-attachments/assets/e2b7acfa-9ef7-4a74-9c4f-89158c5f9765)

---
### Design Decisions

- **Separation of Concerns:**  
  Backend logic is modular and cleanly divided, ensuring maintainability and ease of extension.

- **Vector Search with Milvus:**  
  Documents are embedded and indexed in a collection. The search uses cosine similarity and applies metadata filtering (weather, country).

- **OpenWeatherMap API Integration:**  
  Live weather conditions are fetched using the `OpenWeatherMapAPIWrapper` from langchain.

- **LLM-Powered Intent Routing:**  
  A system prompt guides the assistant in deciding whether to respond with a weather update, or a document-based recommendation.

- **Tooling for extended capability:**  
  Core features like `get_weather_info` and `search_knowledge_base` for seamless use with LLMs.

---

### Used Technologies and Models

#### Language Model
- **Groq LLaMA 3.3 70B (Versatile)** via `langchain_groq`: A high-speed, low-latency large language model used to classify user intent, classify weather, and generate detailed responses.
- Integrated with LangChain and configured with parameters such as temperature and token limits.

#### Weather Data
- **OpenWeatherMap API** via langchain's `OpenWeatherMapAPIWrapper`: Fetches real-time weather conditions based on user-provided location to guide assistant behavior and contextual retrieval.

#### Embeddings
- **Cohere Embed-v4.0**: Used for transforming both user queries and parsed document text into semantic vector embeddings, enabling high-quality similarity-based retrieval in the vector database.

#### Document Parsing
- **LlamaParse Extractor Agent**: Used to extract structured, semantically rich content from uploaded documents. The parsed output is saved in JSON format and indexed into the vector database.

#### Vector Store
- **Zilliz Cloud (Milvus)**: A cloud-hosted vector database accessed via `pymilvus`. Stores embedded documents and enables semantic search filtered by weather conditions and country.

#### Conversational Workflow
- **LangGraph**: Orchestrates the assistant’s logic through a dynamic state graph. Nodes represent tasks like intent classification, weather retrieval, document lookup, and response generation.
- Conditional edges allow flexible routing based on user intent and data availability.

#### Backend API
- **Flask**: Serves two endpoints:
  - `/upload` for parsing and indexing documents
  - `/chat` for handling multi-turn conversational sessions

#### Frontend Interface
- **Streamlit**: Provides an intuitive and lightweight web interface for user interaction with the assistant, including file upload and real-time chatting.


### LangGraph Workflow

The assistant’s reasoning and action pipeline is implemented using **LangGraph**, a library for building deterministic, LLM-driven state machines. The state graph enables modular, traceable, and interruptible decision flows, perfect for multi-step logic like intent classification, weather analysis, and document retrieval.

#### Node Flow Overview

The assistant graph consists of the following nodes:

1. **classify_intent** – Identifies the user’s intent (e.g., weather inquiry vs. recommendation).
2. **check_or_extract_location** – Extracts or verifies the user's mentioned location.
3. **fetch_weather** – Fetches weather data using OpenWeatherMap.
4. **classify_weather** – Converts raw weather data into a weather category (sunny, rainy, snowy, windy, cloudy).
5. **retrieve_documents** – Searches the document knowledge base using vector search with weather category and country filters.
6. **generate_weather_only_response** – Generates a direct weather response (used when no further action is needed).
7. **generate_response** – Combines weather and document insights into a final response.

#### Conditional Routing

A key conditional transition occurs **after weather fetch**. The function `route_after_weather` inspects whether weather data is available and the user's intent:

- If the weather fetch fails → go to `generate_weather_only_response`, where a fallback response telling the user that llm doesn't know the location is provided.
- If the user only asked for weather → go to `generate_weather_only_response`, where a user friendly weather report is provided.
- Otherwise → continue to `classify_weather` → `retrieve_documents` → `generate_response`, where a recommendation on activities or what to wear given a location and a certain weather condition is provided.

#### Visual Diagram

_A diagram visualizing the LangGraph state machine and transitions between nodes will be included here for better clarity._

![graph](https://github.com/user-attachments/assets/e0731747-8bbe-4b35-9eeb-b07977977ef8)

---


### Setup Instructions

#### 1. **Clone the Repository**

```bash
git clone https://github.com/yaaraaa/Weather_Chatbot.git
cd Weather_Chatbot
```

#### 2. **Install Dependencies**

Make sure you have Python 3.9+ installed.

```bash
pip install -r Backend/requirements.txt
pip install -r Frontend/requirements.txt
```

#### 3. **Environment Configuration**

Create a `.env` file at the Backend folder of the project with:

```
LLAMA_CLOUD_API_KEY=your_llama_cloud_key
COHERE_API_KEY=your_cohere_key
MILVUS_ZILLIZ_URI=your_milvus_zilliz_uri
MILVUS_ZILLIZ_TOKEN=your_milvus_zilliz_token
GROQ_API_KEY=your_groq_key
OPENWEATHERMAP_API_KEY=your_openweathermap_key
```

#### 4. **Run the Backend**

```bash
python -m Backend.app
```

The backend Flask API will be available at `http://localhost:5000/api`.

#### 5. **Launch the Frontend (Streamlit)**

```bash
streamlit run Frontend/app.py
```

---

### Example Queries
- “I’m bored, what can I do outside?”
- “What’s the weather like in Egypt?”
- “I’m traveling to Russia, what should I wear?”
---

### Future Improvements

- Chat sessions persistance.
- Enhanced UI components (e.g., weather widgets, document previews).
- Multi-session support.
- Authentication for multi-user support.
