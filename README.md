#Book Search RAG System

This project implements a **web crawling + semantic search + RAG system**
for searching books from Iranian book websites.

##Features
- Web crawling from real book websites
- Building a knowledge base
- Semantic search using TF-IDF
- Answer generation using an LLM (RAG)

##Project Structure
- crawler_taaghche.py → crawl book data
- merge_data.py → merge crawled data
- rag_system.py → run semantic search + RAG

##How to Run
1. Run crawlers to collect data
2. Run merge_data.py
3. Run rag_system.py and enter a query

##Demo Video
The demo video shows crawling and RAG-based search execution.

##Technologies
- Python
- BeautifulSoup
- Scikit-learn
- Ollama (Qwen2.5)
