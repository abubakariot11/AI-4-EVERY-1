import os
import streamlit as st
from PyPDF2 import PdfReader

# Function to get information about a PDF file
def get_pdf_info(file_path: str):
    with open(file_path, "rb") as f:
        reader = PdfReader(f)
        num_pages = len(reader.pages)
        num_words = 0
        num_letters = 0
        num_lines = 0
        file_size = os.path.getsize(file_path)
        for page in reader.pages:
            text = page.extract_text()
            num_words += len(text.split())
            num_letters += len(text.replace(" ", "").replace("\n", ""))
            num_lines += text.count('\n')
    return {
        "file_name": os.path.basename(file_path),
        "num_pages": num_pages,
        "num_words": num_words,
        "num_letters": num_letters,
        "num_lines": num_lines,
        "file_size": file_size
    }

# Main function to run the Streamlit app
def main():
    st.title("PDF Sorter App")
    
    # File uploader
    uploaded_files = st.file_uploader("Upload PDF files", accept_multiple_files=True)
    
    if uploaded_files:
        # Display uploaded file names
        st.write("Uploaded Files:")
        file_paths = []
        for file in uploaded_files:
            file_paths.append(file.name)
            st.write(file.name)
        
        # Get information about a specific PDF file
        pdf_name = st.text_input("Enter the name of the PDF file you want to get information about:")
        if pdf_name:
            pdf_name = pdf_name.strip()
            if pdf_name in file_paths:
                st.write(f"Information about '{pdf_name}':")
                pdf_info = get_pdf_info(pdf_name)
                st.write(f"Number of pages: {pdf_info['num_pages']}")
                st.write(f"Number of words: {pdf_info['num_words']}")
                st.write(f"Number of letters: {pdf_info['num_letters']}")
                st.write(f"Number of lines: {pdf_info['num_lines']}")
                st.write(f"File size: {pdf_info['file_size']} bytes")
            else:
                st.write("PDF file not found. Please make sure you entered the correct file name.")

if __name__ == "__main__":
    main()