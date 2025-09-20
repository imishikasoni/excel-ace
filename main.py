# import streamlit as st
# from interview_simulation import InterviewSimulation

# # Page config
# st.set_page_config(page_title="AI-Powered Excel Mock Interviewer", layout="wide")

# st.title("🧑‍💼 AI-Powered Excel Mock Interviewer")

# # Sidebar
# job_titles = ["Data Analyst", "Financial Analyst", "Operations Analyst"]
# job_title = st.sidebar.selectbox("Select Job Role:", job_titles)
# num_questions = st.sidebar.slider("Number of Questions", 3, 10, 5)

# # Session state
# if "simulation" not in st.session_state:
#     st.session_state.simulation = InterviewSimulation(job_title)
#     st.session_state.history = []
#     st.session_state.current_q = 1
#     st.session_state.finished = False
#     st.session_state.messages = []
#     st.session_state.started = False  # Track if interview has started

# # Reset if job_title changes
# if st.session_state.simulation.job_title != job_title:
#     st.session_state.simulation = InterviewSimulation(job_title)
#     st.session_state.history = []
#     st.session_state.current_q = 1
#     st.session_state.finished = False
#     st.session_state.messages = []
#     st.session_state.started = False
#     st.rerun()

# simulation = st.session_state.simulation

# # Display chat history
# for msg in st.session_state.messages:
#     with st.chat_message(msg["role"]):
#         st.markdown(msg["content"])

# # Default welcome message at the top
# if not st.session_state.messages:
#     welcome = "👋 Welcome to the AI-Powered Excel Mock Interviewer!\n\nShall we start the interview?"
#     st.session_state.messages.append({"role": "assistant", "content": welcome})
#     st.rerun()

# # When user types a message
# if not st.session_state.finished:
#     if user_input := st.chat_input("Type your answer..."):
#         # Append user input immediately
#         st.session_state.messages.append({"role": "user", "content": user_input})
        
#         # Mark that assistant response is pending
#         st.session_state.pending_response = True
        
#         # Do NOT generate AI response yet — just rerun so user input shows
#         st.rerun()

# # After rerun, if assistant response is pending, generate it
# if st.session_state.get("pending_response", False):
#     # Generate AI response (could be first question, or next question)
#         # Normal interview flow
#     st.session_state.history.append({
#         "question": st.session_state.messages[-2]["content"] if st.session_state.current_q > 0 else "Intro",
#         "answer": st.session_state.messages[-1]["content"]
#     })
#     if st.session_state.current_q <= num_questions:
#         ai_response = simulation.get_question(st.session_state.current_q, st.session_state.history)
#         st.session_state.current_q += 1
#     else:
#         st.session_state.finished = True

#     # Append assistant response
#     st.session_state.messages.append({"role": "assistant", "content": ai_response})
#     st.session_state.pending_response = False  # Reset flag
#     st.rerun()



# # Show evaluation after interview
# if st.session_state.finished:
#     evaluation = simulation.evaluate(st.session_state.history)

#     st.session_state.messages.append({"role": "assistant", "content": "📊 The interview is now complete. Here’s your evaluation report:"})
#     st.session_state.messages.append({"role": "assistant", "content": evaluation})

#     # Display evaluation
#     with st.chat_message("assistant"):
#         st.markdown("📊 Here’s your evaluation report:")
#     with st.chat_message("assistant"):
#         st.markdown(evaluation)

#     # Save results
#     filename = simulation.save_results()

#     if st.button("🔄 Start New Interview"):
#         for key in ["simulation", "history", "current_q", "finished", "messages", "started"]:
#             st.session_state.pop(key, None)
#         st.rerun()

import streamlit as st
from interview_simulation import InterviewSimulation

# --- Page config ---
st.set_page_config(page_title="AI-Powered Excel Mock Interviewer", layout="wide")

# --- Custom CSS ---
st.markdown("""
    <style>
    /* Gradient header */
    .header-box {
        padding: 20px; 
        border-radius: 12px; 
        background: linear-gradient(135deg,#500050,#7a1f7a,#b84db8); 
        color: white; 
        font-family: 'Times New Roman', serif;
        margin-bottom: 20px;
    }

    /* User message */
    .user-msg {
        background:#E6CCF5; 
        padding:10px; 
        border-radius:12px; 
        margin:5px 0; 
        max-width:80%; 
        float:right; 
        clear:both; 
        color:#2c2c2c; 
        font-family:'Times New Roman';
    }

    /* Assistant message */
    .assistant-msg {
        background:#E6CCF5; 
        padding:10px; 
        border-radius:12px; 
        margin:5px 0; 
        max-width:80%; 
        float:left; 
        clear:both; 
        color:#2c2c2c; 
        font-family:'Times New Roman';
    }

    /* Evaluation / card style */
    .evaluation-box {
        background:#fef9ff;
        border:2px solid #9C27B0;
        border-radius:12px;
        padding:12px;
        font-family:'Times New Roman';
        margin-top:10px;
        box-shadow:0 2px 8px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown('<div class="header-box"><h2 style="color:white;">🧑‍💼 AI-Powered Excel Mock Interviewer</h2>'
            '<p>Practice Excel interview questions for Data/Finance/Operations roles.</p></div>',
            unsafe_allow_html=True)

# --- Sidebar ---
job_titles = ["Data Analyst", "Financial Analyst", "Operations Analyst"]
job_title = st.sidebar.selectbox("Select Job Role:", job_titles)
num_questions = st.sidebar.slider("Number of Questions", 3, 10, 5)

# --- Session state ---
if "simulation" not in st.session_state or st.session_state.simulation.job_title != job_title:
    st.session_state.simulation = InterviewSimulation(job_title)
    st.session_state.history = []
    st.session_state.current_q = 1
    st.session_state.finished = False
    st.session_state.messages = []
    st.session_state.started = False

simulation = st.session_state.simulation

# --- Display chat history ---
for msg in st.session_state.messages:
    role_class = "user-msg" if msg["role"] == "user" else "assistant-msg"
    st.markdown(f'<div class="{role_class}">{msg["content"]}</div>', unsafe_allow_html=True)

# --- Default welcome message ---
if not st.session_state.messages:
    welcome = "👋 Welcome to the AI-Powered Excel Mock Interviewer!\n\nShall we start the interview?"
    st.session_state.messages.append({"role": "assistant", "content": welcome})
    st.rerun()

# --- User input ---
if not st.session_state.finished:
    if user_input := st.chat_input("Type your answer..."):
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.session_state.pending_response = True
        st.rerun()

# --- AI response generation ---
if st.session_state.get("pending_response", False):
    st.session_state.history.append({
        "question": st.session_state.messages[-2]["content"] if st.session_state.current_q > 0 else "Intro",
        "answer": st.session_state.messages[-1]["content"]
    })
    
    if st.session_state.current_q <= num_questions:
        ai_response = simulation.get_question(st.session_state.current_q, st.session_state.history)
        st.session_state.current_q += 1
    else:
        st.session_state.finished = True
        ai_response = "🎉 That concludes the interview!"

    st.session_state.messages.append({"role": "assistant", "content": ai_response})
    st.session_state.pending_response = False
    st.rerun()

# --- Show evaluation ---
if st.session_state.finished:
    evaluation = simulation.evaluate(st.session_state.history)
    
    st.session_state.messages.append({"role": "assistant", "content": "📊 The interview is now complete. Here’s your evaluation report:"})
    st.session_state.messages.append({"role": "assistant", "content": evaluation})
    
    # Render evaluation with card style
    st.markdown('<div class="evaluation-box">📊 Here’s your evaluation report:</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="evaluation-box">{evaluation}</div>', unsafe_allow_html=True)
    
    # Save results
    filename = simulation.save_results()

    # Start new interview button
    if st.button("🔄 Start New Interview"):
        for key in ["simulation", "history", "current_q", "finished", "messages", "started"]:
            st.session_state.pop(key, None)
        st.rerun()
