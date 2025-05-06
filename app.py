import streamlit as st
import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

INDEX_FILE = "ptp_faiss.index"
METADATA_FILE = "ptp_metadata.json"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

@st.cache_resource
def load_model():
    return SentenceTransformer(EMBEDDING_MODEL)

@st.cache_resource
def load_index():
    return faiss.read_index(INDEX_FILE)

@st.cache_data
def load_metadata():
    with open(METADATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def search(query, top_k=5, versions=None):
    model = load_model()
    index = load_index()
    metadata = load_metadata()

    query_vec = model.encode([query]).astype("float32")
    D, I = index.search(query_vec, top_k)

    results = []
    for idx in I[0]:
        entry = metadata[idx]
        if versions and entry["version"] not in versions:
            continue
        results.append(entry)
    return results

# Streamlit UI
st.title("📘 PTPDiff: OpenShift Networking Doc Search")
query = st.text_input("Enter your question:", placeholder="e.g. How did egress IPs change in 4.15?")

versions = st.multiselect("Filter by OpenShift version (optional):", options=["4.13", "4.14", "4.15", "4.16", "4.17", "4.18"])

if st.button("🔍 Search") and query:
    results = search(query, top_k=10, versions=versions if versions else None)
    if results:
        st.subheader("🔍 Retrieved Chunks")
        combined_context = ""
        for res in results:
            st.markdown(f"**Version {res['version']} - Chunk {res['chunk_id']}**")
            st.write(res["text"])
            combined_context += f"\n\n---\n{res['text']}"

        if st.button("🧠 Summarize with Mistral"):
            with st.spinner("Thinking..."):
                summary_prompt = f"""You are a technical assistant. Based on the following OpenShift documentation excerpts, summarize or answer the question:

    Question: {query}

    Documentation:
    {combined_context}

    Answer:"""
                llm_response = query_ollama(summary_prompt)
                st.success("✅ Summary from Mistral:")
                st.write(llm_response)
    else:
        st.warning("No matching results found.")
    #results = search(query, top_k=10, versions=versions if versions else None)
    #if results:
    #    for res in results:
    #        st.markdown(f"**Version {res['version']} - Chunk {res['chunk_id']}**")
    #        st.write(res["text"])
    #        st.divider()
    #else:
    #    st.warning("No matching results found.")

def query_ollama(prompt, model="mistral"):
    response = requests.post("http://localhost:11434/api/generate", json={
        "model": model,
        "prompt": prompt,
        "stream": False
    })
    return response.json()["response"]