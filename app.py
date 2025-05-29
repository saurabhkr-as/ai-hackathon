import streamlit as st
import openai
import streamlit.components.v1 as components
import os
from dotenv import load_dotenv
load_dotenv(override=True)

api_key = st.secrets["OPENAI_API_KEY"]

st.set_page_config(page_title="Mind-Map Auto-Builder", layout="wide")
st.title("🧠 Mind-Map Auto-Builder")
st.markdown("Paste your notes or paragraph, and let AI generate a structured mind map.")

input_text = st.text_area("✍️ Paste Your Text Below:", height=100)

client = openai.OpenAI(api_key=api_key)

def generate_mindmap_mermaid(text: str) -> str:
    prompt = f"""
You are a mind map generator.
Take the following input text and output a mind map in Mermaid.js syntax using 'mindmap' diagram type.

Input:
{text}

Rules:
- Use at most 3 levels: main topic, subtopic, and detail.
- The first line must be 'mindmap' with NO leading spaces.
- Use exactly 2 spaces per level for indentation, no tabs.
- Do NOT include code block markers or any text except the diagram code.
- Use a generic 'mindmap' root if no clear title is found.
- Return ONLY the Mermaid code, starting with 'mindmap'.

Output:
"""
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5
    )
    return response.choices[0].message.content.strip()


if st.button("🚀 Generate Mind Map") and input_text.strip():
    with st.spinner("Analyzing and building mind map..."):
        mermaid_code = generate_mindmap_mermaid(input_text)

    st.subheader("🗺️ Generated Mind Map")

    # Unique id for the diagram container (useful if multiple renders)
    container_id = "mermaid-mindmap"

    # HTML/JS block for Mermaid 10+ (ESM, modern browsers)
    components.html(f"""
    <div id="{container_id}">
      <pre class="mermaid">
{mermaid_code}
      </pre>
    </div>
    <script type="module">
      import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs";
      // Clean up existing SVG (hot reload safety)
      let el = document.querySelector("#{container_id} .mermaid");
      if (el) {{
        // Initialize mermaid if not already done
        mermaid.initialize({{ startOnLoad: false }});
        mermaid.run({{ nodes: [el] }});
      }}
    </script>
    """, height=500)

    st.subheader("📋 Mermaid Code")
    st.code(mermaid_code, language="markdown")
