import streamlit as st

def main():
    st.title("Resume Analyzer")
    st.subheader("Upload a PDF or Word Resume")
    uploaded_file = st.file_uploader("Upload Resume", type=["pdf", "docx"])
    if uploaded_file:
        st.write("File uploaded:", uploaded_file.name)
        # Placeholder for text extraction
        st.write("Text extraction coming soon!")

if __name__ == "__main__":
    main()