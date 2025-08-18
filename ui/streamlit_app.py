import streamlit as st
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.chatbot import Chatbot

st.set_page_config(page_title="AI Content Strategy Suite", layout="wide")

# --- Initialize Chatbot and State ---
if 'chatbot' not in st.session_state:
    st.session_state.chatbot = Chatbot()
# Initialize all necessary state variables
if 'content_plan' not in st.session_state:
    st.session_state.content_plan = []
if 'selected_idea' not in st.session_state:
    st.session_state.selected_idea = None
if 'script' not in st.session_state:
    st.session_state.script = None
if 'hook_analysis' not in st.session_state:
    st.session_state.hook_analysis = None
if 'calendar_result' not in st.session_state:
    st.session_state.calendar_result = None
if 'analysis_result' not in st.session_state:
    st.session_state.analysis_result = None


# --- UI Layout ---
st.title("🤖 AI Content Strategy Suite")
st.markdown("Go beyond ideas. Generate strategic plans, analyze viral hits, and create standout content.")

# --- Tabbed Interface ---
tab1, tab2, tab3 = st.tabs(["💡 Idea & Script Generator", "🗓️ Content Calendar", "🔍 Viral Post Analyzer"])

# --- TAB 1: Idea & Script Generator ---
with tab1:
    st.header("Generate a Content Plan")
    
    with st.expander("Step 1: Define Your Content Strategy", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            niche = st.text_input("Enter your niche:", "Personal finance for millennials", key="niche_tab1")
            audience = st.text_input("Describe your target audience:", "25-35 year olds saving for major life goals", key="audience_tab1")
        with col2:
            tone = st.selectbox("Select your tone:", ["Authoritative", "Relatable", "Humorous", "Inspirational"], key="tone_tab1")
            persona = st.text_area("Optional: Describe your creator persona:", "A friendly financial advisor who breaks down complex topics simply.", key="persona_tab1")

    st.header("Step 2: Generate Your Content Plan")
    with st.container(border=True):
        plan_type = st.radio("Select Plan Type:", ("Single Idea", "3-Part Content Series"), horizontal=True, key="plan_type_tab1")
        
        if st.button("✨ Generate Plan", type="primary", key="generate_plan_tab1"):
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
                    # --- THIS IS THE FIX ---
                    # Changed from list comprehension to a standard for loop
                    st.markdown("**Articles:**")
                    for l in item['links']['articles']:
                        st.markdown(f"- [{l['title']}]({l['link']})")
                    
                    st.markdown("**YouTube Inspiration:**")
                    for l in item['links']['youtube']:
                        st.markdown(f"- [{l['title']}]({l['link']})")

                    st.markdown("**Instagram Inspiration:**")
                    for l in item['links']['instagram']:
                        st.markdown(f"- [{l['title']}]({l['link']})")

                    st.markdown("**Reddit Discussions:**")
                    for l in item['links']['reddit']:
                        st.markdown(f"- [{l['title']}]({l['link']})")
                
                if st.button(f"Develop Script for Idea {i+1}", key=f"idea_{i}"):
                    st.session_state.selected_idea = item['idea']
                    st.session_state.script = None
                    st.session_state.hook_analysis = None
                    st.rerun()

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
                    st.markdown("#### 🎣 Hook"); st.info(st.session_state.script.get('hook', 'N/A'))
                    if st.button("🧠 Analyze & Enhance Hook"):
                        with st.spinner("AI is analyzing your hook..."):
                            st.session_state.hook_analysis = st.session_state.chatbot.analyze_hook(st.session_state.script.get('hook'))
                    if st.session_state.hook_analysis:
                        if "error" in st.session_state.hook_analysis: st.warning(st.session_state.hook_analysis['error'])
                        else:
                            st.metric("Virality Score", st.session_state.hook_analysis.get('score', 'N/A'))
                            st.markdown("**Feedback:**"); st.write(st.session_state.hook_analysis.get('feedback', 'N/A'))
                            st.markdown("**Suggested Alternatives:**")
                            for alt in st.session_state.hook_analysis.get('alternatives', []):
                                st.success(alt)
                    st.markdown("---")
                    st.markdown("#### 📜 Script"); st.text_area("Script Body", value=st.session_state.script.get('script', 'N/A'), height=200)
                    st.markdown("#### #️⃣ Hashtags"); st.success(st.session_state.script.get('hashtags', 'N/A'))
                    if 'script' in st.session_state.script and st.session_state.script.get('script'):
                        st.subheader("Step 4: Repurpose This Content")
                        target_platforms = st.multiselect("Select platforms:", ["LinkedIn Post", "Twitter Thread"], default=["LinkedIn Post"])
                        if st.button("🚀 Repurpose Content", type="primary"):
                            with st.spinner("Adapting content..."):
                                repurposed = st.session_state.chatbot.repurpose_content(st.session_state.script.get('script', ''), "Instagram Reel", target_platforms)
                                for p, content in repurposed.items(): st.text_area(f"Generated {p}:", value=content, height=200)

# --- TAB 2: Content Calendar Generator ---
with tab2:
    st.header("Strategic Content Calendar Generator")
    st.markdown("Generate a 7-day content plan based on the AIDA marketing framework.")
    
    with st.container(border=True):
        cal_niche = st.text_input("Enter your niche for the calendar:", key="cal_niche")
        cal_audience = st.text_input("Describe your target audience for the calendar:", key="cal_audience")
        
        if st.button("📅 Generate 7-Day Plan", type="primary"):
            if cal_niche and cal_audience:
                with st.spinner("Building your strategic content calendar..."):
                    st.session_state.calendar_result = st.session_state.chatbot.generate_content_calendar(cal_niche, cal_audience)
            else:
                st.warning("Please provide both a niche and an audience.")

    if st.session_state.calendar_result:
        result = st.session_state.calendar_result
        if "error" in result: st.error(result['error'])
        else:
            st.markdown("### Your 7-Day Content Plan:")
            st.markdown(result['plan_text'])
            st.download_button(label="📥 Download Plan as CSV", data=result['csv_data'], file_name=f"content_calendar.csv", mime="text/csv")

# --- TAB 3: Viral Post Analyzer ---
with tab3:
    st.header("Reverse Engineer Viral Posts")
    st.markdown("Paste a URL of a viral post (article, LinkedIn post, etc.) to get a strategic breakdown.")
    
    with st.container(border=True):
        viral_url = st.text_input("Enter the URL of the viral post:")
        
        if st.button("🔬 Analyze Post", type="primary"):
            if viral_url:
                with st.spinner("Reading and analyzing the post..."):
                    st.session_state.analysis_result = st.session_state.chatbot.analyze_viral_post(viral_url)
            else:
                st.warning("Please enter a URL.")

    if st.session_state.analysis_result:
        result = st.session_state.analysis_result
        if "error" in result: st.error(result['error'])
        else:
            st.markdown("### Strategic Analysis:")
            st.markdown(result['analysis_text'])

