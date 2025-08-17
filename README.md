# 🤖 Content Ideation & Repurposing Chatbot

This project is a Python-based chatbot designed to help content creators generate unique, trend-aware ideas and repurpose them across multiple social media platforms. It is built entirely with free and open-source tools.

## ✨ Core Features

-   **Niche-Aware Idea Generation**: Get ideas tailored to your specific niche, audience, and tone.
-   **Trend Integration**: Pulls data from Google Trends, YouTube, and Twitter/X to keep your content relevant.
-   **Script Generation**: Automatically creates a viral hook, a short script, and an engaging call-to-action (CTA).
-   **Cross-Posting Assistant**: Repurposes a single script into optimized posts for LinkedIn, Twitter, and more.

## ⚙️ Tech Stack

-   **Backend**: Python
-   **Frontend**: Streamlit
-   **NLP/LLM**: Hugging Face `transformers` (using a local, open-source model like `google/flan-t5-small`)
-   **Trend Analysis**: `pytrends`, `yt-dlp`, `snscrape`
-   **Containerization**: Docker

## 🚀 Getting Started

### Prerequisites

-   Python 3.8+
-   `pip` for package management
-   Docker (for containerized deployment)

### Local Installation

1.  **Clone the repository:**
    
    git clone <your-repo-url>
    cd content-ideation-chatbot
    

2.  **Create a virtual environment:**
    
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    

3.  **Install dependencies:**
    
    pip install -r requirements.txt
    
    *Note: The first time you run the app, the `transformers` library will download the language model, which may take a few minutes.*

4.  **Run the Streamlit app:**
    
    streamlit run ui/streamlit_app.py
    

### Running with Docker

1.  **Build the Docker image:**
    
    docker build -t content-chatbot .
    

2.  **Run the Docker container:**
    
    docker run -p 8501:8501 content-chatbot

    The app will be available at `http://localhost:8501`.

## ⚠️ Disclaimer

The web scraping tools (`yt-dlp`, `snscrape`) rely on the structure of the target websites. If those websites change, the scrapers may break and will require updates.

