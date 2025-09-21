import chromadb
import chromadb.utils.embedding_functions as embedding_functions

# Setup embedding function with Gemini
google_ef = embedding_functions.GoogleGenerativeAiEmbeddingFunction(
    api_key="AIzaSyBSUjnGo14-Mn_o8BhjFhjP6HsYHHCu9Gg"
)

# Initialize persistent ChromaDB client
chroma_client = chromadb.PersistentClient(path="./chroma_storage")

# Get or create collection with embedding function
collection = chroma_client.get_or_create_collection(
    name="user_learning_memory",
    embedding_function=google_ef
)

# Function to store memory
def store_learning_memory(topic, feedback, answers):
    try:
        doc_id = f"{topic}-{len(answers)}"
        document = f"Topic: {topic}\nAnswers: {answers}\nFeedback: {feedback}"
        collection.add(
            documents=[document],
            ids=[doc_id],
            metadatas=[{"topic": topic}]
        )
        print(f"Stored: {doc_id}")
    except Exception as e:
        print(f"Error storing memory: {e}")

# Function to retrieve memory
def retrieve_related_memory(topic, n_results=2):
    try:
        query_text = f"Recent feedback on {topic}"
        results = collection.query(
            query_texts=[query_text],
            n_results=n_results
        )
        return results.get("documents", [])
    except Exception as e:
        print(f"Error retrieving memory: {e}")
        return []
