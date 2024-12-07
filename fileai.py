import streamlit as st
import google.generativeai as genai
import os
import tempfile

genai.configure(api_key="AIzaSyDLofaqW5zrabBkvv4LtURSeQYM6MSoOz0")  # Replace with your actual API key
model = genai.GenerativeModel(model_name="gemini-1.5-flash")

st.title("Document Explanation with Gemini")

uploaded_file = st.file_uploader("Choose a file", type=["txt", "pdf", "docx", "csv", "py", "js", "html", "md"])
user_prompt = st.text_area("Enter Prompt")

if uploaded_file is not None and user_prompt:  # Check for both file and prompt
    try:
        file_content = None
        mime_type = "text/plain"  # Default mime type

        with tempfile.NamedTemporaryFile(delete=False) as temp_file:  # Use tempfile for better cleanup
            temp_file_path = temp_file.name
            temp_file.write(uploaded_file.read())

        file_extension = os.path.splitext(uploaded_file.name)[1].lower()

        if file_extension == ".pdf":
            import PyPDF2
            with open(temp_file_path, "rb") as f:
                pdf_reader = PyPDF2.PdfReader(f)
                file_content = ""
                for page in pdf_reader.pages:
                    file_content += page.extract_text()

        elif file_extension == ".docx":
            import docx2txt
            file_content = docx2txt.process(temp_file_path)

        elif file_extension in [".txt", ".py", ".js", ".html", "md", ".csv"]:
            with open(temp_file_path, "r", encoding="utf-8") as f:  # Handle encoding explicitly
                file_content = f.read()
                if file_extension == ".csv":
                    mime_type = "text/csv"


        if file_content:
            gemini_file = genai.upload_file(
                path=temp_file_path, display_name=uploaded_file.name, mime_type=mime_type
            )

            response = model.generate_content([user_prompt, gemini_file])

            st.subheader("Explanation:")
            st.write(response.text)
            #Consider adding: st.write(response) to see the full response object for debugging

        else:
            st.error("Could not extract content from the file or file type not supported.")


    except Exception as e:
        st.error(f"An error occurred: {e}")

    finally:  # Ensure cleanup even if an error occurs
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
else:
    st.warning("Please upload a file and enter a prompt.")
