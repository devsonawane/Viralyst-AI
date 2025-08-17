import streamlit as st
import sys
import os

# Add the parent directory to the path to allow imports from other folders
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.chatbot import Chatbot

st.set_page_config(page_title="Content Ideation Chatbot", layout="wide")

# Initialize the chatbot in session state
if 'chatbot' not in st.session_state:
    with st.spinner("Warming up the creative engine... (This may take a moment on first launch)"):
        st.session_state.chatbot = Chatbot()

# --- UI Layout ---
st.title("🤖 Content Ideation & Repurposing Chatbot")
st.markdown("Your AI partner for creating unique, trend-aware content across all your platforms.")

# --- State Management ---
if 'ideas' not in st.session_state:
    st.session_state.ideas = []
if 'selected_idea' not in st.session_state:
    st.session_state.selected_idea = None
if 'script' not in st.session_state:
    st.session_state.script = None


# --- Step 1: Define Creator Profile ---
st.header("Step 1: Define Your Content Strategy")
with st.container(border=True):
    col1, col2 = st.columns(2)
    with col1:
        niche = st.text_input("Enter your niche:", "Sustainable living for city dwellers")
        audience = st.text_input("Describe your target audience:", "Young professionals aged 25-35")
    with col2:
        tone = st.selectbox("Select your tone:", ["Educational", "Humorous", "Inspirational", "Sarcastic", "Emotional"])
        persona = st.text_area("Optional: Describe your creator persona:", "A friendly, slightly nerdy guide who makes sustainability feel easy and accessible, not preachy.")


# --- Step 2: Generate Ideas ---
st.header("Step 2: Generate Content Ideas")
with st.container(border=True):
    # The trend toggle is removed for simplicity in this new model
    if st.button("✨ Generate Ideas & Find References", type="primary"):
        with st.spinner("Brainstorming and searching for references..."):
            # Note the function call has changed
            st.session_state.ideas_with_links = st.session_state.chatbot.generate_ideas_with_links(niche, tone, audience)
            st.session_state.selected_idea = None
            st.session_state.script = None

# In streamlit_app.py, find and replace this entire 'if' block

if 'ideas_with_links' in st.session_state and st.session_state.ideas_with_links:
    st.subheader("Your Generated Ideas & References:")
    for i, item in enumerate(st.session_state.ideas_with_links):
        st.markdown(f"**Idea {i+1}: {item['idea']}**")

        # Create separate expanders for each link category
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
        
        if st.button("📝 Generate Script", type="primary"):
            with st.spinner(f"Writing a script for {platform}..."):
                st.session_state.script = st.session_state.chatbot.generate_script(st.session_state.selected_idea, platform, persona)

        if st.session_state.script and "error" not in st.session_state.script:
            st.markdown(f"**Hook:** {st.session_state.script.get('hook', 'N/A')}")
            st.text_area("Script:", value=st.session_state.script.get('script', 'N/A'), height=150)
            st.markdown(f"**Call to Action:** {st.session_state.script.get('cta', 'N/A')}")

            # --- Step 4: Cross-Post ---
            st.subheader("Repurpose This Content")
            target_platforms = st.multiselect(
                "Select platforms to repurpose for:",
                ["LinkedIn Post", "Twitter Thread", "Facebook Post", "Blog Post Snippet"],
                default=["LinkedIn Post", "Twitter Thread"]
            )
            if st.button("🚀 Repurpose Content", type="primary"):
                with st.spinner("Adapting content for other platforms..."):
                    repurposed = st.session_state.chatbot.repurpose_content(
                        st.session_state.script['script'],
                        platform,
                        target_platforms
                    )
                    for p, content in repurposed.items():
                        st.text_area(f"Generated {p}:", value=content, height=200)


