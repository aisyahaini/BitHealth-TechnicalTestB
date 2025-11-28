# Refactored Code
In this file, I will refactor the code in the `main.py` file with the aim of improving separation of concerns, avoiding global state, and making the code easier to test and develop. Here I will explain the main design decisions, the trade-offs considered, and how this improves maintainability

## 1. ✏️ Design Decisions 
In this design decisions section, I made improvements to the structure, readability, and maintainability without changing the features of the application. Therefore, I made several design decisions:

**a. Separating Responsibilities** 

The initial code in the `main.py` file consisted of a lot of global state, so I refactored it into several modules: 
- app/services/ is used for embedding and storage logic (Qdrant / in-memory fallback). 
- app/workflows/ is used for the RAG process: retrieve and answer. 
- app/api/ is used for HTTP routes (controller layer). 
- app/models/ is used for request/response schemas in Pydantic.
- app/main.py is used for the application entrypoint.

**b. Encapsulation & Abstraction**

At this stage, I implemented encapsulation and abstraction with the following details: 
- `EmbeddingService` handles embedding creation (still deterministic fake embeddings, as in the initial code).
- `DocumentStore` (abstract class) is used to allow for free replacement of the store. 
- `InMemoryStore` and `QdrantStore` for concrete implementations. 
- `RagWorkflow` to summarize the retrieval and generation steps.


## 2. ⚖️ Trade-off Considered
In this Trade-Off Considered section, I've kept the fake embedding and simple retrieval logic because it doesn't add any new features to this refactored code. This trade-off is divided into two parts: positive and negative. Here's a more detailed breakdown: 
- Positive (+) - The application becomes easier and faster, keeping the code lightweight and easy to understand during review. 
- Negative (-) - It doesn't use a real embedding model or a more realistic RAG pipeline.

But the current structure allows the embedder or store to be replaced without major refactoring, simply by changing the dependency injection.

## 3. 📈 How this improves maintainability
This section explains the changes after this code refactoring is done, as follows: 
- The code is easier to test because it is tested per unit test without running the server. 
- It is easier to develop, for example, in advanced RAG pipelines that can be done without modifying the API layer. 
- The code is easier to read because it is separated according to structure and needs, for example, app/api/, app/services/, app/workflows/, and app/models/.