import streamlit as st
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load API key
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

# Page settings
st.set_page_config(
    page_title="AI College Assistant",
    page_icon="🎓"
)

st.title("🎓 AI College Assistant")
st.write("Upload your college timetable and ask questions!")

# Upload image or PDF
uploaded_file = st.file_uploader(
    "📄 Upload College Timetable / Document",
    type=["jpg", "jpeg", "png", "pdf"]
)

# Show uploaded image
if uploaded_file:
    st.success("File uploaded successfully!")

    if uploaded_file.type.startswith("image"):
        st.image(
            uploaded_file,
            caption="College Timetable",
            use_container_width=True
        )

# Question
question = st.chat_input("Ask about your college timetable...")

if question:

    st.write("**You:**", question)

    try:

        if uploaded_file:

            file_data = uploaded_file.getvalue()

            # Image
            if uploaded_file.type.startswith("image"):

                image_part = types.Part.from_bytes(
                    data=file_data,
                    mime_type=uploaded_file.type
                )

                response = client.models.generate_content(
                    model="gemini-3.8-flash",
                    contents=[
                        image_part,
                        f"""
You are an AI College Assistant.

Look carefully at the uploaded college timetable.

Answer the student's question using ONLY
the information present in the timetable.

Student question:
{question}

Give a short and clear answer.
"""
                    ]
                )

            # PDF
            else:

                uploaded = client.files.upload(
                    file=uploaded_file
                )

                response = client.models.generate_content(
                    model="gemini-3.8-flash",
                    contents=[
                        uploaded,
                        f"""
You are an AI College Assistant.

Answer the student's question using ONLY
the information present in this college document.

Student question:
{question}

Give a short and clear answer.
"""
                    ]
                )

            st.success("🤖 Answer")
            st.write(response.text)

        else:

            st.warning("⚠️ First upload your college timetable.")

    except Exception as e:

        st.error(f"Error: {e}")