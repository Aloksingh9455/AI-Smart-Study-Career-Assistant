import streamlit as st
from openai import OpenAI
from ai_engine import get_client, ask_ai
from rag import extract_pdf_text, split_text, embed_texts, retrieve_context
from agent import run_agent
from tools import calculate, count_words

st.set_page_config(page_title="AI Smart Study & Career Assistant", page_icon="🎓", layout="wide")

st.markdown("""
<style>
.main {background-color: #f7f9fc;}
.block-container {padding-top: 2rem; max-width: 1150px;}
.hero {padding: 1.5rem; border-radius: 18px; background: linear-gradient(120deg,#101a35,#315b9a); color: white;}
.small-muted {color: #64748b;}
</style>
""", unsafe_allow_html=True)

def get_api_key():
    try:
        return st.secrets.get("OPENAI_API_KEY", "")
    except Exception:
        return ""

st.title("🎓 AI Smart Study & Career Assistant")
st.caption("Your AI companion for learning, documents, coding, and career preparation.")
api_key = get_api_key()
if not api_key:
    api_key = st.sidebar.text_input("OpenAI API Key", type="password", help="Only for this session. For deployment, use Streamlit Secrets.")
    st.sidebar.caption("Your key is not saved by this app.")
else:
    st.sidebar.success("OpenAI API key loaded from Streamlit Secrets.")

model = st.sidebar.text_input("Chat model", value="gpt-4o-mini")
st.sidebar.markdown("---")
st.sidebar.info("Upload a PDF in the RAG tab to ask questions about your own notes.")
if not api_key:
    st.warning("Add your OpenAI API key in the sidebar to enable AI features. You can still test the calculator and word counter.")

tab_chat, tab_rag, tab_tools, tab_agent = st.tabs(["💬 AI Chat", "📚 PDF RAG", "🧰 Tools", "🤖 AI Agent"])

with tab_chat:
    st.subheader("AI Study & Career Chat")
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
    prompt = st.chat_input("Ask about studies, coding, projects, or career...")
    if prompt:
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        if api_key:
            try:
                with st.chat_message("assistant"):
                    with st.spinner("Thinking..."):
                        answer = ask_ai(api_key, model, prompt, st.session_state.chat_history[:-1])
                        st.markdown(answer)
                st.session_state.chat_history.append({"role": "assistant", "content": answer})
            except Exception as e:
                st.error(f"AI request failed: {e}")
        else:
            st.error("Enter your OpenAI API key in the sidebar first.")

with tab_rag:
    st.subheader("Ask questions from your PDF")
    st.write("Upload class notes, assignment PDFs, or project documentation. The app extracts text, creates embeddings, and retrieves relevant sections.")
    uploaded = st.file_uploader("Choose a PDF file", type=["pdf"], key="pdf_upload")
    if uploaded and st.button("Process PDF", type="primary"):
        if not api_key:
            st.error("Enter your OpenAI API key in the sidebar first.")
        else:
            try:
                with st.spinner("Reading PDF and building search index..."):
                    raw_text = extract_pdf_text(uploaded)
                    chunks = split_text(raw_text)
                    if not chunks:
                        st.error("No readable text found. If this is a scanned PDF, run OCR first.")
                    else:
                        vectors = embed_texts(get_client(api_key), chunks)
                        st.session_state.rag_chunks = chunks
                        st.session_state.rag_vectors = vectors
                        st.success(f"Processed {len(chunks)} text sections successfully.")
            except Exception as e:
                st.error(f"PDF processing failed: {e}")
    question = st.text_input("Ask a question about the uploaded PDF")
    if st.button("Get answer from PDF"):
        if not api_key:
            st.error("Enter your OpenAI API key first.")
        elif not st.session_state.get("rag_chunks"):
            st.warning("Upload and process a PDF first.")
        elif not question.strip():
            st.warning("Enter a question.")
        else:
            try:
                client = get_client(api_key)
                context = retrieve_context(client, question, st.session_state.rag_chunks, st.session_state.rag_vectors)
                answer = ask_ai(api_key, model, question, [], extra_context=context,
                                system_prompt="Answer using the provided document context. If the answer is not in the context, say that the uploaded document does not contain enough information.")
                st.markdown("### Answer")
                st.write(answer)
                with st.expander("Retrieved context"):
                    st.write(context)
            except Exception as e:
                st.error(f"RAG question failed: {e}")

with tab_tools:
    st.subheader("Useful built-in tools")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Calculator")
        expression = st.text_input("Enter a math expression", placeholder="(25 * 4) + 10 / 2")
        if st.button("Calculate"):
            try:
                st.success(f"Result: {calculate(expression)}")
            except Exception as e:
                st.error(str(e))
    with col2:
        st.markdown("#### Word Counter")
        text_value = st.text_area("Paste text here", height=130)
        if st.button("Count words"):
            result = count_words(text_value)
            st.info(f"Words: {result['words']} | Characters: {result['characters']} | Sentences: {result['sentences']}")

with tab_agent:
    st.subheader("AI Agent")
    st.write("The agent can decide when to use the calculator or word-count tool before preparing its response.")
    task = st.text_area("Give the agent a task", placeholder="Calculate my score percentage if I got 425 out of 500, and explain it.")
    if st.button("Run AI Agent", type="primary"):
        if not api_key:
            st.error("Enter your OpenAI API key in the sidebar first.")
        elif not task.strip():
            st.warning("Enter a task.")
        else:
            try:
                with st.spinner("Agent is planning and using tools..."):
                    result = run_agent(api_key, model, task)
                st.markdown("### Agent result")
                st.write(result)
            except Exception as e:
                st.error(f"Agent failed: {e}")

st.markdown("---")
st.caption("Built as a learning capstone. Verify important answers and never upload confidential documents.")
