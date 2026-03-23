import streamlit as st
from crewai import Agent, Task, Crew, Process
import os

# ⚠️ Yahan apni OpenAI ya kisi aur LLM ki API key dalein
# os.environ["OPENAI_API_KEY"] = "your-api-key-here" 

# --- SESSION STATE SETUP (Freemium Logic) ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'credits' not in st.session_state:
    st.session_state.credits = 2  # 2 Free Trials

st.title("🚀 AI Instagram Carousel Generator")

# --- LOGIN SIMULATION ---
if not st.session_state.logged_in:
    st.subheader("Login to your account")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        if username and password:
            st.session_state.logged_in = True
            st.rerun()

# --- MAIN DASHBOARD ---
if st.session_state.logged_in:
    st.sidebar.success("Logged In Successfully!")
    st.sidebar.write(f"🪙 Credits Remaining: **{st.session_state.credits}**")
    
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    st.write("Apna topic batayein aur AI aapke liye 5-slide ka carousel likhega.")
    topic = st.text_input("Topic (e.g., 'Data Cleaning Tools', 'Freelancing Tips'):")

    if st.button("Generate Carousel"):
        if st.session_state.credits > 0:
            if topic:
                with st.spinner("AI Agents are researching and writing... Please wait!"):
                    
                    # --- CREWAI AGENTS SETUP ---
                    researcher = Agent(
                        role='Data Researcher',
                        goal=f'Find 3 key insights about {topic}',
                        backstory='You are an expert at finding viral data points.',
                        verbose=False
                    )

                    writer = Agent(
                        role='Carousel Writer',
                        goal='Write a 5-slide Instagram carousel script based on the research.',
                        backstory='You write short, punchy, and engaging Instagram content.',
                        verbose=False
                    )

                    # --- TASKS ---
                    research_task = Task(
                        description=f'Research the latest trends for the topic: {topic}.',
                        expected_output='A bulleted list of 3 key insights.',
                        agent=researcher
                    )
                    
                    write_task = Task(
                        description='Convert the research into a 5-slide carousel text (Slide 1: Hook, Slide 2-4: Value, Slide 5: CTA).',
                        expected_output='Text formatted slide by slide.',
                        agent=writer
                    )

                    # --- CREW KICKOFF ---
                    carousel_crew = Crew(
                        agents=[researcher, writer],
                        tasks=[research_task, write_task],
                        process=Process.sequential
                    )

                    try:
                        # Ye asal mein LLM ko call karega
                        result = carousel_crew.kickoff()
                        
                        st.success("✅ Carousel Content Generated!")
                        st.markdown("### 📝 Your Carousel Script:")
                        st.write(result.raw) # Output show karega
                        
                        # Credit Deduct
                        st.session_state.credits -= 1
                        st.sidebar.info(f"1 Credit used! Remaining: {st.session_state.credits}")
                        
                    except Exception as e:
                        st.error(f"Error aagaya! API Key check karein. Details: {e}")
            else:
                st.warning("Please ek topic zaroor likhein.")
        else:
            # Paywall
            st.error("⚠️ Aapke free trials khatam ho gaye hain!")
            st.warning("Mazeed generate karne ke liye credits khareedein ($0.50 per carousel).")
            if st.button("Buy Credits via Lemon Squeezy"):
                st.success("Redirecting to payment gateway... (Here you will link your Lemon Squeezy checkout)")
