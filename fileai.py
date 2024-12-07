import streamlit as st
import google.generativeai as genai
import os

genai.configure(api_key="AIzaSyBNFUCw3oIxAPIndacymCIP1MmVsS9G9Ts")
model = genai.GenerativeModel(model_name="gemini-1.5-flash")

st.title("Document Summerizer")

uploaded_file = st.file_uploader("Choose a file", type=["txt", "pdf", "docx", "csv", "py", "js", "html", "md"]) # Expanded file types
user_prompt = st.text_area("Enter Prompt")
button = st.button("Process")

if button and uploaded_file is not None:
    file_content = None
    mime_type = None

    try:
        file_extension = os.path.splitext(uploaded_file.name)[1].lower()

        if file_extension in [".txt", ".py", ".js", ".html", "md", ".csv"]:
             file_content = uploaded_file.read().decode("utf-8")
             mime_type = "text/plain"  # Or more specific if known (e.g., "text/csv" for CSV)

        elif file_extension == ".pdf":
            import PyPDF2  # Make sure to install: pip install PyPDF2
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            file_content = ""
            for page in pdf_reader.pages:
                file_content += page.extract_text()
            mime_type = "text/plain"  # Treat extracted text as plain text

        elif file_extension == ".docx":
            import docx2txt  # Make sure to install: pip install docx2txt
            file_content = docx2txt.process(uploaded_file)  # Directly process the uploaded file object
            mime_type = "text/plain"


        if file_content:  # Proceed only if content extraction was successful
            with open("temp_file", "w") as temp_file:  # Use a general temp file name
                temp_file.write(file_content)


            gemini_file = genai.upload_file(
                path="temp_file", display_name=uploaded_file.name, mime_type=mime_type
            )

            response = model.generate_content([user_prompt, gemini_file])


            st.subheader("Explanation:")
            st.write(response.text)

        else:
            st.error("Could not extract content from the file.")

    except Exception as e:
        st.error(f"An error occurred: {e}")

else:
    st.warning("Please upload a file and enter a prompt.")


    if os.path.exists("temp_file"):  # Check if the temp file exists before deleting
         os.remove("temp_file")
