# backend.py - AI Tutor with PDF support

from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

# Works both locally and on Streamlit Cloud
try:
    import streamlit as st
    api_key = st.secrets["GROQ_API_KEY"]
except:
    api_key = os.getenv("GROQ_API_KEY")

client = Groq(api_key=api_key)

def get_ai_response(user_message, chat_history, pdf_context=""):
    try:
        # System prompt with optional PDF context
        system_prompt = """You are an expert tutor who teaches any topic in a simple, 
        easy-to-understand way. Follow these rules:
        - Always explain concepts step by step
        - Use simple language, avoid complex jargon
        - Give real-life examples to explain concepts
        - Encourage the student and be patient
        - End every answer with a follow-up question
        - Use emojis to make learning fun 📚"""

        # If PDF was uploaded, add its content to system prompt
        if pdf_context:
            system_prompt += f"""
            
        The student has uploaded a document. Here is the content:
        ---
        {pdf_context[:3000]}
        ---
        Answer questions based on this document when relevant."""

        messages = [{"role": "system", "content": system_prompt}]

        for chat in chat_history:
            messages.append({
                "role": chat["role"],
                "content": chat["content"]
            })

        messages.append({
            "role": "user",
            "content": user_message
        })

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            max_tokens=1024
        )

        return response.choices[0].message.content

    except Exception as e:
        if "429" in str(e):
            return "⚠️ Rate limit reached! Please wait a minute and try again."
        return f"❌ Error: {str(e)}"


def extract_pdf_text(pdf_file):
    """Extract text from uploaded PDF file"""
    try:
        import PyPDF2
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        return f"Error reading PDF: {str(e)}"