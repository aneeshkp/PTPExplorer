import streamlit as st
import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import requests

INDEX_FILE = "ptp_faiss.index"
METADATA_FILE = "ptp_metadata.json"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

def query_ollama(prompt, model="mistral"):
    try:
        response = requests.post("http://localhost:11434/api/generate", json={
            "model": model,
            "prompt": prompt,
            "stream": False
        })
        response.raise_for_status()
        data = response.json()
        return data.get("response", "[No response from model]")
    except Exception as e:
        return f"❌ Error querying LLM: {e}"

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

def search_and_debug(query, top_k=10, versions=None):
    model = load_model()
    index = load_index()
    metadata = load_metadata()

    query_vec = model.encode([query]).astype("float32")

    st.markdown("### 🔢 Query Embedding (first 5 dims):")
    st.code(query_vec[0][:5])

    D, I = index.search(query_vec, top_k)

    results = []
    for idx in I[0]:
        entry = metadata[idx]
        if versions and entry["version"] not in versions:
            continue
        results.append(entry)

    return results, query_vec

# UI
st.title("📘 PTPDiff: OpenShift Version Comparator (Debug Mode)")

query = st.text_input("Enter your comparison question:", placeholder="e.g., What changed about egress IPs?")
col1, col2 = st.columns(2)
with col1:
    version_1 = st.selectbox("Select Version A", ["4.13", "4.14", "4.15", "4.16", "4.17", "4.18"])
with col2:
    version_2 = st.selectbox("Select Version B", ["4.13", "4.14", "4.15", "4.16", "4.17", "4.18"], index=1)

compare_button = st.button("🔍 Compare")

if compare_button and query:
    st.subheader(f"🔍 Comparing OpenShift {version_1} vs {version_2}")

    results_1, _ = search_and_debug(query, top_k=10, versions=[version_1])
    results_2, _ = search_and_debug(query, top_k=10, versions=[version_2])

    if not results_1:
        st.warning(f"No chunks for {version_1}. Using fallback.")
        results_1, _ = search_and_debug("networking changes", top_k=5, versions=[version_1])
    if not results_2:
        st.warning(f"No chunks for {version_2}. Using fallback.")
        results_2, _ = search_and_debug("networking changes", top_k=5, versions=[version_2])

    if results_1 and results_2:
        combined_1 = "\n\n".join(r["text"] for r in results_1)
        combined_2 = "\n\n".join(r["text"] for r in results_2)

        compare_prompt = f"""
You are a technical assistant comparing OpenShift networking documentation.

Compare **Version A: {version_1}** and **Version B: {version_2}** based on the user's question.

Question:
{query}

Context from Version {version_1}:
{combined_1}

---

Context from Version {version_2}:
{combined_2}

Instructions:
- Identify real changes between versions
- Ignore unrelated text
- If no change is found, clearly say so
- Answer in bullet points

Comparison:
"""

        st.markdown("### 📄 Prompt Sent to Mistral:")
        st.code(compare_prompt[:2000] + "\n...")  # Truncate long prompt for display

        with st.spinner("Summarizing differences with Mistral..."):
            response = query_ollama(compare_prompt)
            st.success("✅ Comparison Summary:")
            st.markdown(response)
    else:
        st.error("❌ Not enough data for comparison.")