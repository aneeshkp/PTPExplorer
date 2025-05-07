import streamlit as st
import asyncio
from core.searcher import search, query_ollama
from core.model_manager import list_available_models, query_ollama
# Safe AsyncIO Setup
def ensure_asyncio():
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        asyncio.set_event_loop(asyncio.new_event_loop())

ensure_asyncio()


st.title("📘 PTPExplorer: OpenShift Networking Doc Search")

query = st.text_input("Enter your question:")
versions = st.multiselect("Select versions to compare:", options=["4.13", "4.14", "4.15", "4.16", "4.17", "4.18"])
keyword = st.text_input("Optional: Prioritize keyword (e.g., PTPConfig)")

# Dynamically detect available models
available_models = list_available_models()
if not available_models:
    st.error("No LLM models available. Please start Mistral or LLaMA with Ollama.")
else:
    model_choice = st.selectbox("Choose LLM Model:", available_models)

if st.button("🔍 Search"):
    if query:
        results = search(query, top_k=5, versions=versions, prioritize_keyword=keyword)
        st.session_state.search_results = results
        st.session_state.llm_response = ""  # Reset LLM response

# Display Search Results
if st.session_state.get("search_results"):
    st.subheader("🔍 Retrieved Chunks")
    combined_context = "\n\n".join([res['text'] for res in st.session_state.search_results])
    for res in st.session_state.search_results:
        st.markdown(f"**Version {res['version']} - Chunk {res['chunk_id']}**")
        st.write(res["text"])

    if st.button(f"🧠 Summarize with {model_choice}"):
        if model_choice:
            with st.spinner(f"Thinking with {model_choice}..."):
                summary_prompt = f"""You are a technical assistant. Based on the following OpenShift documentation excerpts, summarize or answer the question:

    Question: {query}

    Versions: {', '.join(versions)}

    Documentation:
    {combined_context}

    Answer:"""
                st.session_state.llm_response = query_ollama(summary_prompt, model=model_choice)
        else:
            st.warning("No model selected.")

        # Display the LLM Response if available
        if st.session_state.llm_response:
            st.success(f"✅ Summary from {model_choice}:")
            st.write(st.session_state.llm_response)
    else:
        st.info("Search results will appear here.")
