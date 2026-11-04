import streamlit as st
from openai import OpenAI
from pypdf import PdfReader

st.title("Deep Sea")
st.write("Upload your documents and ask a question.")

api_key = st.text_input("OpenAI API key", type="password")

files = st.file_uploader(
    "Upload PDF files",
    type="pdf",
    accept_multiple_files=True
)

question = st.text_input("Enter your question")

if st.button("Ask"):
    if not api_key:
        st.write("Please enter your API key.")
    elif not files:
        st.write("Please upload a PDF file.")
    elif not question:
        st.write("Please enter a question.")
    else:
        documents = []

        for file in files:
            try:
                pdf = PdfReader(file)
                pages = []

                for page_number, page in enumerate(pdf.pages, start=1):
                    text = page.extract_text() or ""
                    if text.strip():
                        pages.append(f"Page {page_number}: {text}")

                if pages:
                    documents.append(
                        f"Document: {file.name}\n" + "\n".join(pages)
                    )
                else:
                    st.warning(f"No readable text found in {file.name}.")
            except Exception as error:
                st.error(f"Could not read {file.name}: {error}")

        if documents:
            context = "\n\n".join(documents)[:60000]

            try:
                client = OpenAI(api_key=api_key)

                response = client.responses.create(
                    model="gpt-4o-mini",
                    instructions=(
                        "Answer using only the documents provided. "
                        "If the answer is not in the documents, say so. "
                        "Mention the document and page when possible."
                    ),
                    input=f"Documents:\n{context}\n\nQuestion: {question}"
                )

                st.write(response.output_text)

            except Exception as error:
                st.error(f"Could not get an answer: {error}")
