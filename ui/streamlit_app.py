import streamlit as st
import sys
import os

# Add the parent directory to the path to allow imports from other folders
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.chatbot import Chatbot

st.set_page_config(page_title="Content Ideation Chatbot", layout="wide")

# Initialize the chatbot in session state
if 'chatbot' not in st.session_state:
    with st.spinner("Warming up the creative engine..."):
        st.session_state.chatbot = Chatbot()

# --- UI Layout ---
st.title("🤖 Content Ideation & Repurposing Chatbot")
st.markdown("Your AI partner for creating unique, trend-aware content across all your platforms.")

# --- State Management ---
if 'ideas_with_links' not in st.session_state:
    st.session_state.ideas_with_links = []
if 'selected_idea' not in st.session_state:
    st.session_state.selected_idea = None
if 'script' not in st.session_state:
    st.session_state.script = None

# --- Step 1: Define Creator Profile ---
st.header("Step 1: Define Your Content Strategy")
with st.container(border=True):
    col1, col2 = st.columns(2)
    with col1:
        niche = st.text_input("Enter your niche:", "Home workout for beginners")
        audience = st.text_input("Describe your target audience:", "People in their 20s and 30s looking to get fit")
    with col2:
        tone = st.selectbox("Select your tone:", ["Inspirational", "Educational", "Humorous", "Motivational"])
        persona = st.text_area("Optional: Describe your creator persona:", "A friendly and encouraging fitness coach who makes exercise fun and accessible.")

# --- Step 2: Generate Ideas ---
st.header("Step 2: Generate Content Ideas")
with st.container(border=True):
    if st.button("✨ Generate Ideas & Find References", type="primary"):
        with st.spinner("Brainstorming and searching for references..."):
            st.session_state.ideas_with_links = st.session_state.chatbot.generate_ideas_with_links(niche, tone, audience)
            st.session_state.selected_idea = None
            st.session_state.script = None

if st.session_state.ideas_with_links:
    st.subheader("Your Generated Ideas & References:")
    for i, item in enumerate(st.session_state.ideas_with_links):
        st.markdown(f"**Idea {i+1}: {item['idea']}**")
        
        with st.expander("📄 Show Web Article References"):
            if item['links']['articles']:
                for link in item['links']['articles']:
                    st.markdown(f"- [{link['title']}]({link['link']})")
            else:
                st.write("No articles found.")

        with st.expander("▶️ Show YouTube Shorts Inspiration"):
            if item['links']['youtube']:
                for link in item['links']['youtube']:
                    st.markdown(f"- [{link['title']}]({link['link']})")
            else:
                st.write("No YouTube Shorts found.")
        
        with st.expander("📸 Show Instagram Reels Inspiration"):
            if item['links']['instagram']:
                for link in item['links']['instagram']:
                    st.markdown(f"- [{link['title']}]({link['link']})")
            else:
                st.write("No Instagram Reels found.")

        if st.button(f"Develop this idea", key=f"idea_{i}"):
            st.session_state.selected_idea = item['idea']
            st.session_state.script = None
            st.rerun()

# --- Step 3: Develop the Chosen Idea ---
if st.session_state.selected_idea:
    st.header(f"Step 3: Develop '{st.session_state.selected_idea}'")
    with st.container(border=True):
        st.subheader("Generate a Script")
        platform = st.selectbox("Select a platform for the script:", ["Instagram Reel", "TikTok", "YouTube Short"])
        
        if st.button("📝 Generate AI Script", type="primary"):
            with st.spinner(f"Writing a high-quality script with AI..."):
                st.session_state.script = st.session_state.chatbot.generate_script(st.session_state.selected_idea, platform, persona)

        if st.session_state.script:
            if "error" in st.session_state.script:
                st.error(st.session_state.script['error'])
            else:
                st.markdown("#### 🎣 Hook")
                st.info(st.session_state.script.get('hook', 'N/A'))

                st.markdown("#### 📜 Script")
                st.text_area("Script Body", value=st.session_state.script.get('script', 'N/A'), height=200)

                st.markdown("#### 📣 Call to Action")
                st.info(st.session_state.script.get('cta', 'N/A'))
                
                st.markdown("#### #️⃣ Hashtags")
                st.success(st.session_state.script.get('hashtags', 'N/A'))

            # --- Step 4: Cross-Post (with safety check) ---
            # This block now checks if a valid script exists before showing the button.
            if st.session_state.script and 'script' in st.session_state.script:
                st.subheader("Repurpose This Content")
                target_platforms = st.multiselect(
                    "Select platforms to repurpose for:",
                    ["LinkedIn Post", "Twitter Thread", "Facebook Post"],
                    default=["LinkedIn Post", "Twitter Thread"]
                )
                if st.button("🚀 Repurpose Content", type="primary"):
                    with st.spinner("Adapting content for other platforms..."):
                        script_body_for_repurpose = st.session_state.script.get('script', '')
                        repurposed = st.session_state.chatbot.repurpose_content(
                            script_body_for_repurpose,
                            platform,
                            target_platforms
                        )
                        for p, content in repurposed.items():
                            st.text_area(f"Generated {p}:", value=content, height=200)

