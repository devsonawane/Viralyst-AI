🚀 Viralyst AI: The AI Content Strategy Suite
Viralyst AI is an all-in-one strategic tool designed to empower content creators and brands. It moves beyond simple idea generation to offer a comprehensive suite of AI-powered features, from planning a full week of content to reverse-engineering viral hits and creating culturally-aware multilingual campaigns.

This application was built with Python, Streamlit, and a suite of powerful external APIs to deliver a fast, reliable, and feature-rich experience.

✨ Features
Viralyst AI is organized into five powerful modules:

💡 1. Idea & Script Generator
The core engine for daily content creation.

AI-Powered Ideation: Generates unique ideas or full content series based on your niche, audience, and tone.

Deep Research: For each idea, it automatically finds relevant web articles, YouTube Shorts, Instagram Reels, and Reddit discussions.

Visual Mood Boards: Instantly creates a visual mood board with high-quality images from Pexels to guide your creative direction.

Advanced Scriptwriting: Produces a complete script package, including a hook, a detailed script body, a call-to-action, and optimized hashtags.

Viral Hook Analyzer: An industry-first tool that provides an AI-generated "Virality Score" and actionable feedback to make your hooks irresistible.

🗓️ 2. Content Calendar Generator
Your strategic planner for long-term consistency.

AIDA Framework: Generates a full 7-day content plan using the Awareness, Interest, Desire, Action marketing model.

Multi-Format Strategy: Suggests a mix of content formats (Reels, Threads, etc.) to keep your feed engaging and diverse.

Exportable: Download your entire content calendar as a .csv file, ready to be imported into Notion, Trello, or Google Sheets.

🔍 3. Viral Post Analyzer
Your personal "cheat code" for understanding what works.

Reverse Engineering: Paste the URL of any successful article or post.

Strategic Breakdown: The AI reverse engineers the content, identifying the hook style, psychological triggers, and core message.

Actionable Remix Ideas: Provides concrete ideas on how you can adapt that successful format for your own niche.

🌍 4. Multilingual Ideation
Go global with culturally-aware content.

Multi-Language Generation: Generate ideas in Spanish, French, German, Hindi, and more.

Cultural Adaptation: The AI adapts the tone and includes local references and slang, making your content feel authentic to a specific region.

🔮 5. Future Trend Predictor
Get ahead of the curve.

The Trend Oracle: A playful but insightful feature that predicts a plausible future viral trend for your niche.

First-Mover Advantage: Provides a creative campaign idea to help you capitalize on the trend before it goes mainstream.

⚙️ Tech Stack
Backend: Python

Frontend: Streamlit

Core AI: Google Gemini API (gemini-1.5-flash)

Research: SerpApi (for Google, YouTube, Instagram, Reddit searches)

Visuals: Pexels API

Deployment: Docker on AWS EC2

🚀 Getting Started
The application is containerized with Docker for easy and reliable deployment.

Clone the repository.

Install Docker.

Build the Docker image:

Run the container with your API keys:
You will need to provide three environment variables (-e) for your API keys from SerpApi, Google AI Studio, and Pexels.

Access the application at http://<your-server-ip>:8501.
