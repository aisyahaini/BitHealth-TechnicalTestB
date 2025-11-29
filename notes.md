# Refactored Code
In this file, I will refactor the code in the `main.py` file with the aim of improving separation of concerns, avoiding global state, and making the code easier to test and develop. Here I will explain the main design decisions, the trade-offs considered, and how this improves maintainability

## 1. ✏️ Design Decisions 
In this design decisions section, I made improvements to the structure, readability, and maintainability without changing the features of the application. Therefore, I made several design decisions:

**a. Separating Responsibilities** 

The initial code in the `main.py` file consisted of a lot of global state, so I refactored it into several modules: 
- app/services/ to logic embedding & storage 
- app/workflows/ to RAG process
- app/api/ to HTTP routing 
- app/models/ to Pydantic schema
- app/main.py to application entrypoint

**b. Encapsulation & Abstraction**

At this stage, I implemented encapsulation and abstraction with the following details: 
- `EmbeddingService` to handles embedding creation
- `DocumentStore` to storage abstraction
- `InMemoryStore` and `QdrantStore` to concrete implementations. 
- `RagWorkflow` to summarize the retrieval and generation steps.


## 2. ⚖️ Trade-off Considered
In this Trade-Off Considered section, I've kept the fake embedding and simple retrieval logic because it doesn't add any new features to this refactored code. This trade-off is divided into two parts: positive and negative. Here's a more detailed breakdown: 
- Positive (+) - The application becomes easier and faster, keeping the code lightweight and easy to understand during review
- Negative (-) - It doesn't use a real embedding model or a more realistic RAG pipeline

But the current structure allows the embedder or store to be replaced without major refactoring, simply by changing the dependency injection.

## 3. 📈 How this improves maintainability
This section explains the changes after this code refactoring is done, as follows: 
- The code is easier to test (unit test per component)
- It is easier to develop for more complex RAGs 
- The code is easier to read and maintain thanks to a clear folder structure