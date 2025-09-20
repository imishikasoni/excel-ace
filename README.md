# excel-ace

AI-Powered Excel Mock Interviewer for Data Analyst, Financial Analyst, and Operations Analyst roles. Practice Excel interview questions and receive automated feedback and evaluation.

## Features

- Interactive Excel interview simulation via web UI (Streamlit)
- Dynamic question generation and evaluation
- Role selection (Data Analyst, Financial Analyst, Operations Analyst)
- Customizable number of questions
- Structured feedback and scoring
- Conversational AI bot having state management capabilities

## Installation

1. **Clone the repository:**
   ```sh
   git clone <your-repo-url>
   cd excel-ace
   ```

2. **(Optional) Create and activate a virtual environment:**
   ```sh
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

4. **Set your OpenAI API key:**
   - Add your key to `.streamlit/secrets.toml`:
     ```
     OPENAI_API_KEY = "<your-openai-api-key>"
     ```

## Running the App

Start the Streamlit app:

```sh
streamlit run main.py
```

The app will open in your browser at [http://localhost:8501](http://localhost:8501).

## Usage

1. Select the job role and number of questions in the sidebar.
2. Answer the interview questions in the chat interface.
3. Receive automated feedback and evaluation at the end.
4. Optionally, start a new interview.

## Project Structure

- `main.py` — Streamlit app entry point
- `src_crewai/` — Interview logic, agents, and tasks
- `.streamlit/secrets.toml` — API key configuration
- `requirements.txt` — Python dependencies

