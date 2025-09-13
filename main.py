import json
import re
import xml.etree.ElementTree as ET
import streamlit as st
from spellchecker import SpellChecker

spell = SpellChecker()


def clean_and_fix_text(text: str) -> str:
    text = re.sub(r'\s+', ' ', text).strip()
    text = re.sub(r'[^a-zA-Z0-9.,;?!\s]', '', text)
    words = text.split()
    corrected = [spell.correction(w) if spell.correction(w) else w for w in words]
    fixed_text = " ".join(corrected)
    if fixed_text:
        fixed_text = fixed_text[0].upper() + fixed_text[1:]
    return fixed_text

def split_sentences(text: str):
    return re.split(r'(?<=[.?!])\s+', text)

def local_json(prompt: str):
    clean_prompt = clean_and_fix_text(prompt)
    sentences = split_sentences(clean_prompt)
    constraints = sentences[1:] if len(sentences) > 1 else []

    data = {
        "task": sentences[0] if sentences else "General request",
        "context": clean_prompt,
        "constraints": constraints
    }
    return json.dumps(data, indent=2)

def local_xml(prompt: str):
    clean_prompt = clean_and_fix_text(prompt)
    sentences = split_sentences(clean_prompt)
    constraints = sentences[1:] if len(sentences) > 1 else []

    root = ET.Element("prompt")
    task = ET.SubElement(root, "task")
    task.text = sentences[0] if sentences else "General request"

    context = ET.SubElement(root, "context")
    context.text = clean_prompt

    constraints_el = ET.SubElement(root, "constraints")
    for c in constraints:
        constraint = ET.SubElement(constraints_el, "constraint")
        constraint.text = c

    return ET.tostring(root, encoding="unicode")



st.set_page_config(page_title="Prompt Formatter", page_icon="📝", layout="centered")

st.markdown(
    """
    <style>
    body { background-color: #f7f9fc; }
    .stTextArea textarea { font-size: 1rem; border-radius: 10px; }
    .stRadio > div { flex-direction: row; }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("📝 Prompt Maker")
st.caption("Make ChatGPT or Gemini understand your prompts more effectively. Easily clean your prompts and convert them into JSON or XML with style.")


with st.container():
    prompt = st.text_area("✍️ Enter your prompt:", height=220, placeholder="Type something...")


col1, col2 = st.columns([2, 1])
with col1:
    format_choice = st.radio("📂 Choose output format:", ["JSON", "XML"], horizontal=True)
with col2:
    generate = st.button("🚀 Generate", use_container_width=True)

if generate:
    if prompt.strip():
        if format_choice == "JSON":
            output = local_json(prompt)
            st.subheader("📄 JSON Output")
            st.code(output, language="json")
            st.download_button(
                "⬇️ Download JSON",
                data=output,
                file_name="prompt.json",
                mime="application/json",
            )
        else:
            output = local_xml(prompt)
            st.subheader("📄 XML Output")
            st.code(output, language="xml")
            st.download_button(
                "⬇️ Download XML",
                data=output,
                file_name="prompt.xml",
                mime="application/xml",
            )
    else:
        st.error("Please enter a prompt before generating output!")

st.markdown("---")
st.caption("Made with ❤️ by Harsh Kurware")
