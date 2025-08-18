🤖 AI Content Strategy Suite
This project has evolved from a simple chatbot into a comprehensive, AI-powered suite for content creators. It goes beyond basic idea generation to provide strategic planning, competitive analysis, and content enhancement tools. Built with a Python backend, a Streamlit UI, and powerful external APIs, this tool is designed to be a creator's indispensable partner.

✨ Core Features
This application is now a multi-faceted tool with three main modules:

💡 1. Idea & Script Generator
AI-Powered Idea Generation: Creates unique, high-quality ideas based on your niche, audience, and tone.

Content Series Planner: Generates a cohesive 3-part or 5-part content series to build a narrative and retain your audience.

Comprehensive Research: For each idea, it automatically finds relevant:

📄 Web Articles

▶️ YouTube Shorts

📸 Instagram Reels

💬 Reddit Discussions

Visual Mood Boards: Fetches images from Pexels to provide instant visual inspiration for your content.

Advanced Scriptwriting: Generates a complete script package including a hook, a detailed script body, a call-to-action, and relevant hashtags.

Viral Hook Analyzer: A unique tool that provides an AI-generated "Virality Score" and actionable feedback to make your hooks more powerful.

🗓️ 2. Content Calendar Generator
Strategic Planning: Generates a full 7-day content plan using the AIDA (Awareness, Interest, Desire, Action) marketing framework.

Multi-Format Ideas: Suggests a mix of content formats (Reels, Threads, etc.) to keep your feed diverse.

Exportable: Download your entire content calendar as a .csv file to import into Notion, Trello, or Google Sheets.

🔍 3. Viral Post Analyzer
"Cheat Code" for Creators: Paste the URL of any successful article or post.

Strategic Breakdown: The AI reverse engineers the content, identifying the hook style, psychological triggers, and core message.

Actionable Remix Ideas: Provides concrete ideas on how you can adapt that successful format for your own niche.

⚙️ Tech Stack
Backend: Python

Frontend: Streamlit

Core AI: Google Gemini API (gemini-1.5-flash)

Research: SerpApi (for Google, YouTube, Instagram, Reddit searches)

Visuals: Pexels API

Deployment: Docker on AWS EC2

🚀 Deployment
The application is containerized with Docker for easy deployment.

Clone the repository.

Install Docker.

Build the Docker image:

docker build -t content-chatbot .

Run the container with your API keys:
You will need to provide three environment variables (-e) for your API keys from SerpApi, Google AI Studio, and Pexels.

docker run -d -p 8501:8501 \
  -e SERPAPI_API_KEY="<YOUR_SERPAPI_API_KEY>" \
  -e GEMINI_API_KEY="<YOUR_GOOGLE_AI_KEY>" \
  -e PEXELS_API_KEY="<YOUR_PEXELS_KEY>" \
  content-chatbot

Access the application at http://<your-server-ip>:8501.
