# AI Smart Study & Career Assistant

A Generative AI capstone project built with Streamlit and the OpenAI API. It demonstrates LLM integration, prompt engineering, retrieval-augmented generation (RAG), tools, and a simple tool-using AI agent.

## Features

- **AI Chat:** study, coding, project, and career Q&A.
- **PDF RAG:** extract PDF text, split it into chunks, create embeddings, retrieve relevant sections, and answer with document context.
- **Prompt Engineering:** a dedicated system instruction guides the assistant's tone and behavior; RAG changes the instruction to ground answers in retrieved context.
- **Tools:** safe calculator and word counter.
- **AI Agent:** the model can call the calculator and word-counter tools before producing a final answer.
- **Streamlit UI:** four simple tabs.

## Project structure

```text
AI-Smart-Study-Career-Assistant/
├── app.py
├── ai_engine.py
├── rag.py
├── agent.py
├── tools.py
├── requirements.txt
├── README.md
├── .gitignore
├── .env.example
└── .streamlit/
    └── secrets.toml.example
```

## Requirements

- Python 3.10+
- An OpenAI API key with API access and available billing/credits.

## Run locally (Mac)

1. Open this folder in VS Code.
2. Open Terminal in VS Code.
3. Create a virtual environment:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

4. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

5. Create `.streamlit/secrets.toml` (copy from `.streamlit/secrets.toml.example`) and add your API key:

   ```toml
   OPENAI_API_KEY = "your_real_api_key"
   ```

6. Run:

   ```bash
   streamlit run app.py
   ```

The browser will open the local app, usually at `http://localhost:8501`.

## Deploy on Streamlit Community Cloud

1. Push this project to a GitHub repository.
2. Open https://share.streamlit.io/ and sign in with GitHub.
3. Choose **Create app**, select your repository and branch, and set the main file path to `app.py`.
4. In **Advanced settings → Secrets**, paste:

   ```toml
   OPENAI_API_KEY = "your_real_api_key"
   ```

5. Deploy.

Do not commit `.streamlit/secrets.toml`, `.env`, or any real API key to GitHub.

## GitHub upload commands

```bash
git init
git add .
git commit -m "Build GenAI Smart Study and Career Assistant"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/AI-Smart-Study-Career-Assistant.git
git push -u origin main
```

Replace `YOUR-USERNAME` with your GitHub username. If the repository already exists locally, do not run `git init` again.

## How to test

- Chat tab: ask "Explain Python functions with a simple example."
- PDF RAG tab: upload a text-based PDF, process it, then ask a question answered in the PDF.
- Tools tab: calculate `(25 * 4) + 10 / 2`; expected result is `105`.
- Tools tab: paste a paragraph and click Count words.
- Agent tab: ask "Calculate my percentage if I scored 425 out of 500." The agent should call the calculator.

## Notes and limitations

- OpenAI API calls may incur charges. Check your API usage and limits.
- The default chat model is `gpt-4o-mini`; change it in the sidebar if your account uses another supported model.
- PDF RAG currently handles text-based PDFs. Scanned/image-only PDFs need OCR before upload.
- The RAG index is kept in Streamlit session memory; re-process the PDF after a new session or app restart.
- This is an educational starter project, not a production system. Do not upload confidential or sensitive documents. Verify important AI-generated information.
