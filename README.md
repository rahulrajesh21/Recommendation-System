# 🎬 CineMatch AI — Semantic Movie Recommendation System

[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688.svg?style=flat&logo=FastAPI&logoColor=white)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Google Gemini](https://img.shields.io/badge/Embeddings-Gemini%20v2-4285F4.svg?style=flat&logo=google&logoColor=white)](https://ai.google.dev/)
[![Pydantic v2](https://img.shields.io/badge/Pydantic-v2-E92063.svg?style=flat&logo=pydantic&logoColor=white)](https://docs.pydantic.dev/)

An AI-powered movie recommendation engine and semantic search API built with **FastAPI**, **Google Gemini vector embeddings**, and **Cosine Similarity**. 

Search for movies by concept, vibe, or plot description (e.g., *"astronaut fighting for survival in deep space"*) or find *"More Like This"* recommendations for any title in the catalog.

---

## ✨ Features

- **🧠 Concept-Based Semantic Search:** Go beyond keyword search. Uses Google's 3072-dimensional Gemini embeddings (`gemini-embedding-2`) to understand the plot, themes, and emotional tone of user queries.
- **⚡ Instant "More Like This" Recommendations:** Computes in-memory vector cosine similarity across pre-embedded titles in sub-5ms with zero external network overhead.
- **🏗️ Production-Grade Architecture:** Clean separation of concerns across route controllers, Pydantic schemas, embedding wrappers, and data access layers.
- **🔄 Modern FastAPI Lifespan:** Non-blocking async initialization of in-memory catalogs and clients on server startup.
- **🎨 Modern Responsive UI:** A responsive, Netflix-inspired dark-mode frontend featuring interactive search chips, similarity percentage badges, and recommendation modals.
- **📚 Interactive API Documentation:** Auto-generated interactive OpenAPI / Swagger UI documentation at `/docs`.

---

## 🏛️ System Architecture

```
[ Client Request ] (Search / Recommendations)
       │
       ▼
[ FastAPI App ] (main.py)
       │  (prefix: /api/v1)
       ▼
[ API Router ] (api/v1/movies.py)
       ├── /search?query=...  ──> [ Embedding Service ] ──> Google Gemini API (Query Vector)
       │                                │
       │                                ▼
       └── /{title}/similar   ──> [ Cosine Similarity Engine ] 
                                        │
                                        ▼
                               [ Movie Database ] (In-Memory Catalog)
                                        │
                                        ▼
                             [ Ranked Top-K Results ]
```

---

## 📁 Project Structure

```
recommendation_system/
├── .env.example                 # Template for required environment variables
├── .gitignore                   # Excludes .env, .venv, __pycache__, etc.
├── requirements.txt             # Pinned project dependencies
├── index.html                   # Modern glassmorphism frontend application
├── main.py                      # FastAPI app entrypoint, CORS, lifespan handler
│
├── api/
│   └── v1/
│       └── movies.py            # API routes (search, catalog, similar movies)
│
├── db/
│   ├── db.py                    # MovieDatabase class and async JSON loader
│   └── movies.json              # Movie catalog with titles, plots, and posters
│
├── models/
│   └── movie.py                 # Pydantic v2 schemas (MovieData, MovieSearchResult)
│
└── services/
    ├── embedding_service.py     # Google Generative AI embeddings client wrapper
    ├── consine_simlarity.py     # Pure vector cosine similarity math calculation
    └── similar_movies.py        # Recommendation & semantic search business logic
```

---

## 🚀 Quickstart Guide

### 1. Prerequisites
- **Python 3.11+** installed
- A **Google Gemini API Key** (Get one for free at [Google AI Studio](https://aistudio.google.com/))

### 2. Clone the Repository
```bash
git clone https://github.com/your-username/recommendation-system.git
cd recommendation-system
```

### 3. Create a Virtual Environment
```bash
python3 -m venv .venv
source .venv/bin/activate    # On Windows use: .venv\Scripts\activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Set Up Environment Variables
Create a `.env` file in the project root based on `.env.example`:
```bash
cp .env.example .env
```
Open `.env` and add your Google Gemini API key:
```env
GOOGLE_API_KEY=your_actual_gemini_api_key_here
```

### 6. Run the FastAPI Server
```bash
uvicorn main:app --reload --port 8080
```
On startup, the app will compute 3072-dimensional vector embeddings for all movies in the catalog:
```text
INFO:     Uvicorn running on http://127.0.0.1:8080 (Press CTRL+C to quit)
Computing embeddings and loading catalog...
Movies loaded successfully: {'size': 25, 'Embedding Size': 3072}
Application startup complete.
```

### 7. Open the Frontend
- If using VS Code: Right-click `index.html` and choose **"Open with Live Server"** (runs on `http://localhost:5500`).
- Or open a separate terminal and run:
  ```bash
  python3 -m http.server 5500
  ```
  Then visit [http://localhost:5500](http://localhost:5500) in your web browser!

---

## 📡 API Endpoints Reference

| Method | Endpoint | Description | Sample Query |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/v1/movies/` | Returns all movies in the catalog | `/api/v1/movies/` |
| `GET` | `/api/v1/movies/search` | Semantic vector search by plot or concept | `/api/v1/movies/search?query=astronaut+stranded` |
| `GET` | `/api/v1/movies/{title}/similar` | Top 3 similar movies based on vector similarity | `/api/v1/movies/Interstellar/similar` |
| `GET` | `/docs` | Interactive Swagger UI API documentation | `/docs` |

### Sample Response: `GET /api/v1/movies/Interstellar/similar`
```json
{
  "movies": [
    {
      "title": "Gravity",
      "description": "Two astronauts are stranded in deep space after the mid-orbit destruction of their space shuttle...",
      "imageUrl": "https://image.tmdb.org/t/p/w500/kZ2nZw8D681aphje8NJi8EfbL1U.jpg",
      "similarity_score": 0.8842
    },
    {
      "title": "The Martian",
      "description": "During a manned mission to Mars, an astronaut is presumed dead after a fierce storm and left behind...",
      "imageUrl": "https://image.tmdb.org/t/p/w500/5BHuvQ6p9kfc091Z8RiFNhCwL4b.jpg",
      "similarity_score": 0.8315
    },
    {
      "title": "Inception",
      "description": "A skilled thief who steals corporate secrets through the use of dream-sharing technology...",
      "imageUrl": "https://image.tmdb.org/t/p/w500/oYuLEt3zVCKq57qu2F8dT7NIa6f.jpg",
      "similarity_score": 0.7410
    }
  ]
}
```

---

## 🔒 Security & Best Practices

- **Zero Secret Exposure:** `.env` is explicitly ignored in `.gitignore`. Only `.env.example` with dummy values is committed to git.
- **Thread-Safe Memory State:** In-memory catalogs are immutable during request handling; similarity scores are returned in dedicated response schemas without mutating underlying catalog objects.
- **CORS Configured:** Secure origin restrictions configured for local development (`http://localhost:5500`).

---

## 📄 License
This project is licensed under the MIT License. Feel free to use, modify, and distribute!
