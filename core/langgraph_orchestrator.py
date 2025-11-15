"""
RAG (Retrieval-Augmented Generation) Pipeline for Coffeeverse

Implements a flexible RAG system for semantic search and context retrieval.
"""

from typing import List, Dict, Any, Optional
import faiss
import numpy as np
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQAWithSourcesChain

from core.config import CoffeeverseConfig

class RAGPipeline:
    """
    Implements a comprehensive Retrieval-Augmented Generation pipeline.
    Supports text and multimodal document retrieval.
    """
    
    def __init__(self, 
                 embedding_model: str = None, 
                 llm_model: str = None):
        """
        Initialize RAG pipeline with configurable embedding and language models.
        
        :param embedding_model: Embedding model to use
        :param llm_model: Language model for generation
        """
        # Use config defaults if not specified
        self.embedding_model = embedding_model or CoffeeverseConfig.EMBEDDING_MODEL
        self.llm_model = llm_model or CoffeeverseConfig.DEFAULT_LLM_MODEL
        
        # Initialize embeddings and vector store
        self.embeddings = OpenAIEmbeddings(model=self.embedding_model)
        self.vector_store = None
        
        # Initialize language model for generation
        self.llm = ChatOpenAI(model_name=self.llm_model)
        
        # Custom RAG prompt for more contextual responses
        self.rag_prompt = PromptTemplate(
            template="""Use the following pieces of context to answer the question at the end. 
            If you don't know the answer, just say that you don't know, don't try to make up an answer.

            Context:
            {summaries}

            Question: {question}
            Helpful Answer:""",
            input_variables=["summaries", "question"]
        )
    
    def create_vector_store(self, documents: List[str], metadata: Optional[List[Dict[str, Any]]] = None) -> None:
        """
        Create a FAISS vector store from given documents.
        
        :param documents: List of text documents
        :param metadata: Optional metadata for each document
        """
        if metadata:
            self.vector_store = FAISS.from_texts(
                texts=documents, 
                embedding=self.embeddings, 
                metadatas=metadata
            )
        else:
            self.vector_store = FAISS.from_texts(documents, self.embeddings)
    
    def semantic_search(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        """
        Perform semantic search in the vector store.
        
        :param query: Search query
        :param k: Number of top results to return
        :return: List of semantic search results
        """
        if not self.vector_store:
            raise ValueError("Vector store not initialized. Call create_vector_store first.")
        
        return self.vector_store.similarity_search(query, k=k)
    
    def retrieve_and_generate(self, query: str, k: int = 3) -> Dict[str, Any]:
        """
        Retrieve relevant context and generate an answer using RAG.
        
        :param query: User's query
        :param k: Number of context documents to retrieve
        :return: Generated response with sources
        """
        if not self.vector_store:
            raise ValueError("Vector store not initialized. Call create_vector_store first.")
        
        # Create retrieval QA chain
        chain = RetrievalQAWithSourcesChain.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vector_store.as_retriever(search_kwargs={"k": k}),
            return_source_documents=True
        )
        
        # Generate response
        result = chain({"question": query}, return_only_outputs=False)
        
        return {
            "answer": result.get('answer', ''),
            "sources": result.get('source_documents', []),
            "input": query
        }
    
    def add_documents(self, documents: List[str], metadata: Optional[List[Dict[str, Any]]] = None) -> None:
        """
        Add new documents to the existing vector store.
        
        :param documents: List of text documents to add
        :param metadata: Optional metadata for each document
        """
        if not self.vector_store:
            self.create_vector_store(documents, metadata)
        else:
            if metadata:
                self.vector_store.add_texts(documents, metadatas=metadata)
            else:
                self.vector_store.add_texts(documents)

# Example usage
if __name__ == "__main__":
    # Sample usage demonstrating RAG pipeline capabilities
    rag_pipeline = RAGPipeline()
    
    # Sample documents
    documents = [
        "AI is transforming multiple industries with advanced machine learning techniques.",
        "Machine learning models are becoming more sophisticated and efficient.",
        "Data science requires interdisciplinary skills and continuous learning."
    ]
    
    # Create vector store
    rag_pipeline.create_vector_store(documents)
    
    # Perform semantic search
    print("Semantic Search Results:")
    search_results = rag_pipeline.semantic_search("AI technology", k=2)
    for result in search_results:
        print(result.page_content)
    
    # Retrieve and generate
    print("\nRAG Generation:")
    rag_result = rag_pipeline.retrieve_and_generate("What is the impact of AI?")
    print("Answer:", rag_result['answer'])
    print("Sources:", [doc.page_content for doc in rag_result['sources']])
