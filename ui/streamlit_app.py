import streamlit as st
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.chatbot import Chatbot

st.set_page_config(page_title="Content Strategy Suite", layout="wide")

# --- Initialize Chatbot and State ---
if 'chatbot' not in st.session_state:
    st.session_state.chatbot = Chatbot()
if 'content_plan' not in st.session_state:
    st.session_state.content_plan = []
if 'selected_idea' not in st.session_state:
    st.session_state.selected_idea = None
if 'script' not in st.session_state:
    st.session_state.script = None
if 'hook_analysis' not in st.session_state:
    st.session_state.hook_analysis = None

# --- UI Layout ---
st.title("🤖 Content Strategy Suite")
st.markdown("Your AI partner for creating unique, trend-aware, and viral content.")

# --- Step 1: Define Creator Profile ---
with st.expander("Step 1: Define Your Content Strategy", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        niche = st.text_input("Enter your niche:", "Personal finance for millennials")
        audience = st.text_input("Describe your target audience:", "25-35 year olds saving for major life goals")
    with col2:
        tone = st.selectbox("Select your tone:", ["Authoritative", "Relatable", "Humorous", "Inspirational"])
        persona = st.text_area("Optional: Describe your creator persona:", "A friendly financial advisor who breaks down complex topics simply.")

# --- Step 2: Generate Content Plan ---
st.header("Step 2: Generate Your Content Plan")
with st.container(border=True):
    plan_type = st.radio("Select Plan Type:", ("Single Idea", "3-Part Content Series"), horizontal=True)
    
    if st.button("✨ Generate Plan", type="primary"):
        with st.spinner(f"Generating a {plan_type} with visuals..."):
            st.session_state.content_plan = st.session_state.chatbot.generate_content_plan(niche, tone, audience, plan_type)
            st.session_state.selected_idea = None
            st.session_state.script = None
            st.session_state.hook_analysis = None

if st.session_state.content_plan:
    if plan_type == "3-Part Content Series":
        st.subheader("Your 3-Part Content Series Plan:")
    else:
        st.subheader("Your Generated Idea:")

    for i, item in enumerate(st.session_state.content_plan):
        with st.container(border=True):
            st.markdown(f"**Idea {i+1}: {item['idea']}**")

            if item['images']:
                st.markdown("##### Visual Mood Board")
                st.image(item['images'], width=150)

            with st.expander("Show Research & References"):
                st.markdown("**Articles:**")
                for link in item['links']['articles']: st.markdown(f"- [{link['title']}]({link['link']})")
                
                st.markdown("**YouTube Inspiration:**")
                for link in item['links']['youtube']: st.markdown(f"- [{link['title']}]({link['link']})")
                
                st.markdown("**Instagram Inspiration:**")
                for link in item['links']['instagram']: st.markdown(f"- [{link['title']}]({link['link']})")
                
                # --- Reddit Section Included ---
                st.markdown("**Reddit Discussions:**")
                for link in item['links']['reddit']: st.markdown(f"- [{link['title']}]({link['link']})")

            if st.button(f"Develop Script for Idea {i+1}", key=f"idea_{i}"):
                st.session_state.selected_idea = item['idea']
                st.session_state.script = None
                st.session_state.hook_analysis = None
                st.rerun()

# --- Step 3: Develop & Enhance Script ---
if st.session_state.selected_idea:
    st.header(f"Step 3: Develop & Enhance Script for '{st.session_state.selected_idea}'")
    with st.container(border=True):
        if not st.session_state.script:
            with st.spinner("Writing a high-quality script with AI..."):
                st.session_state.script = st.session_state.chatbot.generate_script(st.session_state.selected_idea, "Instagram Reel", persona)

        if st.session_state.script:
            if "error" in st.session_state.script:
                st.error(st.session_state.script['error'])
            else:
                st.markdown("#### 🎣 Hook")
                st.info(st.session_state.script.get('hook', 'N/A'))
                
                if st.button("🧠 Analyze & Enhance Hook"):
                    with st.spinner("AI is analyzing your hook..."):
                        st.session_state.hook_analysis = st.session_state.chatbot.analyze_hook(st.session_state.script.get('hook'))

                if st.session_state.hook_analysis:
                    if "error" in st.session_state.hook_analysis:
                        st.warning(st.session_state.hook_analysis['error'])
                    else:
                        st.metric("Virality Score", st.session_state.hook_analysis.get('score', 'N/A'))
                        st.markdown("**Feedback:**")
                        st.write(st.session_state.hook_analysis.get('feedback', 'N/A'))
                        st.markdown("**Suggested Alternatives:**")
                        for alt in st.session_state.hook_analysis.get('alternatives', []):
                            st.success(alt)

                st.markdown("---")
                st.markdown("#### 📜 Script")
                st.text_area("Script Body", value=st.session_state.script.get('script', 'N/A'), height=200)
                st.markdown("#### #️⃣ Hashtags")
                st.success(st.session_state.script.get('hashtags', 'N/A'))
                
                if 'script' in st.session_state.script and st.session_state.script.get('script'):
                    st.subheader("Step 4: Repurpose This Content")
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
                                "Instagram Reel",
                                target_platforms
                            )
                            for p, content in repurposed.items():
                                st.text_area(f"Generated {p}:", value=content, height=200)

