import streamlit as st
import os
import re
from docx import Document
from io import StringIO

def extract_dois_from_text(text):
    # Regular expression to find DOIs starting with "10."
    doi_pattern = r'10\.\d{4,9}/[^\s\)\]\[]+(?:\([^\s\)\]\[]+\))?'
    matches = re.findall(doi_pattern, text)

    # Clean up DOIs by removing extraneous characters
    cleaned_matches = []
    for match in matches:
        match = re.sub(r'[\[\]\)]', '', match)  # Remove '[', ']', ')'
        match = match.strip('.')
        cleaned_matches.append(match)
    
    return cleaned_matches

def extract_dois_from_paragraphs(paragraphs):
    full_text = []
    for para in paragraphs:
        full_text.append(para.text)
    text = '\n'.join(full_text)
    return extract_dois_from_text(text)

def extract_dois_from_tables(tables):
    full_text = []
    for table in tables:
        for row in table.rows:
            for cell in row.cells:
                full_text.append(cell.text)
    text = '\n'.join(full_text)
    return extract_dois_from_text(text)

def extract_dois_from_word(docx_file):
    # Load the Word document
    doc = Document(docx_file)
    
    # Extract DOIs from paragraphs
    dois = extract_dois_from_paragraphs(doc.paragraphs)
    
    # Extract DOIs from tables
    dois += extract_dois_from_tables(doc.tables)
    
    return dois

def save_dois_to_text(dois):
    # Create a StringIO object to store DOIs
    output = StringIO()
    for doi in sorted(set(dois)):  # Remove duplicates and sort
        output.write(doi.strip() + '\n')
    return output.getvalue()

# Streamlit app layout
st.title("DOI Extractor from Word Documents")
st.write("Upload multiple .docx files to extract DOIs. The extracted DOIs will be saved in a text file for download.")

# File uploader for multiple files
uploaded_files = st.file_uploader("Upload .docx files", type='docx', accept_multiple_files=True)

if uploaded_files:
    all_dois = set()  # Use a set to collect DOIs and automatically remove duplicates
    
    for uploaded_file in uploaded_files:
        # Read the uploaded Word file
        st.write(f"Processing file: {uploaded_file.name}")
        dois = extract_dois_from_word(uploaded_file)
        all_dois.update(dois)

    # Save the extracted DOIs to a text string
    extracted_dois = save_dois_to_text(all_dois)

    # Prepare the text for download
    if extracted_dois:
        st.download_button(
            label="Download Extracted DOIs",
            data=extracted_dois,
            file_name='extracted_dois.txt',
            mime='text/plain'
        )
        st.success(f"Extracted {len(all_dois)} unique DOIs.")
    else:
        st.warning("No DOIs were extracted from the uploaded files.")
else:
    st.info("Please upload .docx files to extract DOIs.")

st.info("Created by Dr. Satyajeet Patil")
st.info("For more cool apps like this visit: https://patilsatyajeet.wixsite.com/home/python")




# Display custom "Buy Me a Coffee" button
bmc_button = """
<div align="center">
    <a href="https://www.buymeacoffee.com/researcher13" target="_blank">
        <img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Support our Research" style="height: 50px; width: 217px;">
    </a>
</div>
"""
