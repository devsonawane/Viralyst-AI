import streamlit as st
import sys
import os
import re

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.chatbot import Chatbot

st.set_page_config(page_title="Viralyst AI: Content Strategy Suite", layout="wide")

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
if 'calendar_result' not in st.session_state:
    st.session_state.calendar_result = None
if 'analysis_result' not in st.session_state:
    st.session_state.analysis_result = None
if 'localized_result' not in st.session_state:
    st.session_state.localized_result = None
if 'trend_result' not in st.session_state:
    st.session_state.trend_result = None
if 'reverse_virality_result' not in st.session_state:
    st.session_state.reverse_virality_result = None
if 'feedback_loop_result' not in st.session_state:
    st.session_state.feedback_loop_result = None
if 'niche_suggestions' not in st.session_state:
    st.session_state.niche_suggestions = []
if 'persona_suggestions' not in st.session_state:
    st.session_state.persona_suggestions = []
if 'selected_persona' not in st.session_state:
    st.session_state.selected_persona = None
if 'integrated_calendar' not in st.session_state:
    st.session_state.integrated_calendar = None
if 'integrated_localized' not in st.session_state:
    st.session_state.integrated_localized = None
if 'expanded_localized_idea' not in st.session_state:
    st.session_state.expanded_localized_idea = {}

# --- Callback functions to safely update widget state ---
def update_text_input(widget_key, suggestion):
    st.session_state[widget_key] = suggestion
    if widget_key == "niche_main":
        st.session_state.niche_suggestions = []
    elif widget_key == "persona_main":
        st.session_state.persona_suggestions = []

# --- UI Layout ---
st.title("🚀 Viralyst AI: Content Strategy Suite")
st.markdown("Your AI partner for creating unique, trend-aware, and viral content.")

# --- Tabbed Interface ---
main_tab, calendar_tab, analyzer_tab, trends_tab, reverse_tab, feedback_tab, multilingual_tab = st.tabs([
    "💡 Core Content Generator",
    "🗓️ Content Calendar",
    "🔍 Viral Post Analyzer",
    "🔮 Future Trends",
    "🔄 Reverse Virality",
    "🔁 Feedback Loop",
    "🌍 Multilingual Ideation"
])

# --- MAIN TAB: Core Generator ---
with main_tab:
    st.header("Generate a Content Plan")
    
    with st.container(border=True):
        st.subheader("Step 1: Define Your Core Strategy")
        
        niche = st.text_input("Enter your niche (e.g., 'sustainable fashion'):", key="niche_main")
        if st.button("Suggest Niches", key="suggest_niche"):
            with st.spinner("AI is brainstorming niche ideas..."):
                result = st.session_state.chatbot.get_suggestions(niche, 'niche')
                if "suggestions" in result:
                    st.session_state.niche_suggestions = result["suggestions"]
        
        if st.session_state.niche_suggestions:
            st.write("Click to use a suggestion:")
            for sugg in st.session_state.niche_suggestions:
                st.button(sugg, key=f"niche_{sugg}", on_click=update_text_input, args=("niche_main", sugg))

        audience = st.text_input("Describe your target audience:", "Gen Z interested in eco-friendly products")
        tone_options = ["Authoritative", "Relatable", "Humorous", "Inspirational", "Sarcastic", "Empathetic", "Professional", "Casual"]
        tone = st.selectbox("Select your tone:", tone_options)
        
        st.subheader("Step 2: Select Your Target Persona")
        if st.button("🤖 Generate Audience Personas", key="generate_personas"):
            with st.spinner("AI is building detailed audience personas..."):
                result = st.session_state.chatbot.get_suggestions(None, 'persona', niche=niche)
                if "personas" in result:
                    st.session_state.persona_suggestions = result["personas"]
                    st.session_state.selected_persona = None # Reset selection
        
        if st.session_state.persona_suggestions:
            persona_options = [f"{p.get('name', '')}: {p.get('profile', '')}" for p in st.session_state.persona_suggestions]
            selected_persona_str = st.radio("Select a persona to target:", persona_options, key="persona_select")
            
            for p in st.session_state.persona_suggestions:
                if f"{p.get('name', '')}: {p.get('profile', '')}" == selected_persona_str:
                    st.session_state.selected_persona = p
                    with st.expander("View Persona Details"):
                        st.markdown(f"**Pain Point:** {p.get('pain_point')}")
                        st.markdown(f"**Goal:** {p.get('goal')}")
                    break

    with st.container(border=True):
        st.subheader("Step 3: Choose Your Content Plan")
        platform = st.selectbox("Select Primary Platform:", ["Instagram", "TikTok", "YouTube", "LinkedIn", "Twitter/X", "Facebook", "Blog"])
        plan_type = st.radio("Select Plan Type:", ("Single Idea", "3-Part Content Series", "Monthly Content Theme"), horizontal=True)
        
        if st.button("✨ Generate Plan", type="primary"):
            with st.spinner(f"Generating a {plan_type} for {platform}..."):
                st.session_state.content_plan = st.session_state.chatbot.generate_content_plan(niche, tone, audience, plan_type, platform, st.session_state.selected_persona)
                st.session_state.selected_idea = None
                st.session_state.script = None

    if st.session_state.content_plan:
        st.subheader("Your Generated Content Plan:")
        for i, item in enumerate(st.session_state.content_plan):
            with st.container(border=True):
                idea_text = item.get('idea', 'Error: Could not load idea.')
                st.markdown(f"**Idea {i+1}: {idea_text}**")
                if "An AI API error occurred" in idea_text:
                    st.error(idea_text)
                else:
                    if item.get('images'):
                        st.markdown("##### Visual Mood Board")
                        st.image(item['images'], width=150)
                    with st.expander("Show Research & References"):
                        links = item.get('links', {})
                        # --- THIS IS THE FIX ---
                        # Replaced list comprehensions with standard for loops for stability
                        st.markdown("**Articles:**")
                        for l in links.get('articles', []):
                            st.markdown(f"- [{l.get('title')}]({l.get('link')})")
                        st.markdown("**YouTube Inspiration:**")
                        for l in links.get('youtube', []):
                            st.markdown(f"- [{l.get('title')}]({l.get('link')})")
                        st.markdown("**Instagram Inspiration:**")
                        for l in links.get('instagram', []):
                            st.markdown(f"- [{l.get('title')}]({l.get('link')})")
                        st.markdown("**Reddit Discussions:**")
                        for l in links.get('reddit', []):
                            st.markdown(f"- [{l.get('title')}]({l.get('link')})")
                    if st.button(f"Develop Script for Idea {i+1}", key=f"idea_{i}"):
                        st.session_state.selected_idea = idea_text
                        st.session_state.script = None
                        st.session_state.hook_analysis = None
                        st.rerun()

    if st.session_state.selected_idea:
        st.header(f"Step 4: Develop & Enhance Script for '{st.session_state.selected_idea}'")
        with st.container(border=True):
            if not st.session_state.script:
                with st.spinner("Writing a high-quality script with AI..."):
                    st.session_state.script = st.session_state.chatbot.generate_script(st.session_state.selected_idea, platform, st.session_state.selected_persona.get('profile') if st.session_state.selected_persona else persona)
            if st.session_state.script:
                if "error" in st.session_state.script: st.error(st.session_state.script['error'])
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
                    st.markdown("#### 🎵 Trending Audio Suggestions"); st.info(st.session_state.script.get('audio', 'No audio suggestions available.'))
                    if 'script' in st.session_state.script and st.session_state.script.get('script'):
                        st.subheader("Step 5: Repurpose This Content")
                        target_platforms = st.multiselect("Select platforms:", ["LinkedIn Post", "Twitter Thread"], default=["LinkedIn Post"])
                        if st.button("🚀 Repurpose Content", type="primary"):
                            with st.spinner("Adapting content..."):
                                repurposed = st.session_state.chatbot.repurpose_content(st.session_state.script.get('script', ''), platform, target_platforms)
                                for p, content in repurposed.items(): st.text_area(f"Generated {p}:", value=content, height=200)

    with st.expander("🗓️ Advanced Tools: Calendar & Multilingual"):
        st.subheader("Generate a 7-Day Calendar from above Niche")
        if st.button("Generate Calendar"):
            with st.spinner("Building your strategic content calendar..."):
                st.session_state.integrated_calendar = st.session_state.chatbot.generate_content_calendar(niche, audience)
        if 'integrated_calendar' in st.session_state and st.session_state.integrated_calendar:
            result = st.session_state.integrated_calendar
            if "error" in result: st.error(result['error'])
            else:
                st.markdown(result['plan_text'])
                st.download_button(label="📥 Download Plan as CSV", data=result['csv_data'], file_name="content_calendar.csv", mime="text/csv")

        st.markdown("---")
        st.subheader("Generate Localized Ideas from above Niche")
        col1, col2 = st.columns(2)
        with col1:
            lang_options = ["English", "Marathi", "Spanish", "French", "German", "Hindi", "Japanese", "Portuguese"]
            integrated_lang = st.selectbox("Select Language:", lang_options, key="integ_lang")
        with col2:
            integrated_region = st.text_input("Enter Target Region (e.g., India, USA):", key="integ_region")
        if st.button("Generate Localized Ideas"):
            with st.spinner(f"Generating ideas in {integrated_lang} for {integrated_region}..."):
                st.session_state.integrated_localized = st.session_state.chatbot.generate_localized_ideas(niche, audience, tone, integrated_lang, integrated_region)
                st.session_state.expanded_localized_idea = {} # Reset expanded ideas
        if 'integrated_localized' in st.session_state and st.session_state.integrated_localized:
            result = st.session_state.integrated_localized
            if "error" in result: st.error(result['error'])
            else:
                localized_ideas = [line.strip() for line in re.split(r'\d+\.\s*', result['ideas_text']) if line.strip()]
                for idx, idea in enumerate(localized_ideas):
                    st.info(idea)
                    if st.button(f"Expand Idea {idx+1}", key=f"expand_{idx}"):
                        with st.spinner("AI is elaborating..."):
                            expanded_result = st.session_state.chatbot.expand_localized_idea(integrated_lang, integrated_region, idea)
                            st.session_state.expanded_localized_idea[idx] = expanded_result
                    if idx in st.session_state.expanded_localized_idea:
                        expanded_data = st.session_state.expanded_localized_idea[idx]
                        if "error" in expanded_data:
                            st.warning(expanded_data["error"])
                        else:
                            st.success(expanded_data.get("expanded_idea"))

with calendar_tab:
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
    if 'calendar_result' in st.session_state and st.session_state.calendar_result:
        result = st.session_state.calendar_result
        if "error" in result: st.error(result['error'])
        else:
            st.markdown("### Your 7-Day Content Plan:")
            st.markdown(result['plan_text'])
            st.download_button(label="📥 Download Plan as CSV", data=result['csv_data'], file_name=f"content_calendar.csv", mime="text/csv")

with analyzer_tab:
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
    if 'analysis_result' in st.session_state and st.session_state.analysis_result:
        result = st.session_state.analysis_result
        if "error" in result: st.error(result['error'])
        else:
            st.markdown("### Strategic Analysis:")
            st.markdown(result['analysis_text'])

with trends_tab:
    st.header("The Trend Oracle 🔮")
    st.markdown("Get a playful but insightful prediction of a future viral trend in your niche.")
    with st.container(border=True):
        trend_niche = st.text_input("Enter your niche to get a trend prediction:", key="trend_niche")
        if st.button("👁️ Predict the Future", type="primary"):
            if trend_niche:
                with st.spinner("Gazing into the future of content..."):
                    st.session_state.trend_result = st.session_state.chatbot.predict_future_trend(trend_niche)
            else:
                st.warning("Please enter a niche.")
    if 'trend_result' in st.session_state and st.session_state.trend_result:
        result = st.session_state.trend_result
        if "error" in result: st.error(result['error'])
        else:
            st.markdown("### The Oracle Has Spoken:")
            st.success(result['prediction_text'])

with reverse_tab:
    st.header("Reverse Virality Engine 🔄")
    st.markdown("Paste a URL of a viral post and tell us your niche. The AI will break down its success and remix the format for you.")
    with st.container(border=True):
        viral_url_rv = st.text_input("Enter the URL of the viral post:", key="viral_url_rv")
        user_niche_rv = st.text_input("Enter YOUR niche to adapt the post for:", key="user_niche_rv")
        if st.button("🚀 Reverse Engineer & Remix", type="primary"):
            if viral_url_rv and user_niche_rv:
                with st.spinner("Analyzing and remixing the viral post..."):
                    st.session_state.reverse_virality_result = st.session_state.chatbot.reverse_virality(viral_url_rv, user_niche_rv)
            else:
                st.warning("Please provide both a URL and your niche.")
    if 'reverse_virality_result' in st.session_state and st.session_state.reverse_virality_result:
        result = st.session_state.reverse_virality_result
        if "error" in result: st.error(result['error'])
        else:
            st.markdown("### Strategic Analysis & Remix:")
            st.success(result['analysis_text'])

with feedback_tab:
    st.header("Adaptive Content Feedback Loop 🔁")
    st.markdown("Paste a URL to one of YOUR published posts. The AI will analyze it and provide feedback for future content.")
    with st.container(border=True):
        post_url_fl = st.text_input("Enter the URL of YOUR published post:", key="post_url_fl")
        if st.button("📈 Get Feedback & Suggestions", type="primary"):
            if post_url_fl:
                with st.spinner("Analyzing your post and generating feedback..."):
                    st.session_state.feedback_loop_result = st.session_state.chatbot.get_adaptive_feedback(post_url_fl)
            else:
                st.warning("Please enter a URL.")
    if 'feedback_loop_result' in st.session_state and st.session_state.feedback_loop_result:
        result = st.session_state.feedback_loop_result
        if "error" in result: st.error(result['error'])
        else:
            st.markdown("### Performance Analysis & Future Suggestions:")
            st.info(result['feedback_text'])

with multilingual_tab:
    st.header("Multilingual & Localized Content Ideation")
    st.markdown("Generate ideas in a specific language, adapted with local cultural references.")
    with st.container(border=True):
        col1, col2 = st.columns(2)
        with col1:
            lang_options_tab4 = ["English", "Marathi", "Spanish", "French", "German", "Hindi", "Japanese", "Portuguese"]
            loc_lang = st.selectbox("Select Target Language:", lang_options_tab4)
            loc_niche = st.text_input("Enter your niche:", key="loc_niche")
            loc_tone = st.text_input("Enter your desired tone:", key="loc_tone")
        with col2:
            loc_region = st.text_input("Enter Target Region/Country (e.g., Mexico, France, India):", key="loc_region")
            loc_audience = st.text_input("Describe your target audience:", key="loc_audience")
        if st.button("🌍 Generate Localized Ideas", type="primary"):
            if all([loc_lang, loc_niche, loc_tone, loc_region, loc_audience]):
                with st.spinner(f"Generating ideas in {loc_lang} for {loc_region}..."):
                    st.session_state.localized_result = st.session_state.chatbot.generate_localized_ideas(loc_niche, loc_audience, loc_tone, loc_lang, loc_region)
            else:
                st.warning("Please fill in all fields.")
    if 'localized_result' in st.session_state and st.session_state.localized_result:
        result = st.session_state.localized_result
        if "error" in result:
            st.error(result['error'])
        else:
            st.markdown("### Your Localized Content Ideas:")
            st.info(result['ideas_text'])

