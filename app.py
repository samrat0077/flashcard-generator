import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize session state
if 'flashcards' not in st.session_state:
    st.session_state.flashcards = []

def main():
    st.title("ShellEx Flashcard Generator")
    st.write("Convert educational content into flashcards using AI")
    
    # Input options
    input_method = st.radio("Input method:", ("Upload file", "Paste text"))
    subject = st.selectbox("Subject (optional):", 
                         ["", "Biology", "History", "Computer Science"])
    
    content = ""
    if input_method == "Upload file":
        file = st.file_uploader("Upload file", type=["txt", "pdf"])
        if file:
            if file.name.endswith('.pdf'):
                import PyPDF2
                reader = PyPDF2.PdfReader(file)
                content = "\n".join([page.extract_text() for page in reader.pages])
            else:
                content = file.getvalue().decode("utf-8")
            st.text_area("Extracted content", content, height=200)
    else:
        content = st.text_area("Paste content here:", height=200)
    
    # Generate flashcards
    if st.button("Generate Flashcards") and content:
        with st.spinner("Generating flashcards..."):
            try:
                client = OpenAI(api_key="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")  # Loads from .env
                
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You create educational flashcards."},
                        {"role": "user", "content": f"Convert this into 10 Q&A flashcards:\n{content}"}
                    ],
                    temperature=0.7
                )
                
                # Parse the response
                content = response.choices[0].message.content
                qa_pairs = [line.strip() for line in flashcards_text.split('\n') if line.strip()]
                
                # Store in session state
                st.session_state.flashcards = []
                for i in range(0, len(qa_pairs), 2):
                    if i+1 < len(qa_pairs):
                        st.session_state.flashcards.append({
                            "question": qa_pairs[i].replace("Q:", "").strip(),
                            "answer": qa_pairs[i+1].replace("A:", "").strip()
                        })
                
                st.success(f"Generated {len(st.session_state.flashcards)} flashcards!")
            except Exception as e:
                st.error(f"Error: {str(e)}")
    
    # Display flashcards
    if st.session_state.flashcards:
        st.subheader("Generated Flashcards")
        for i, card in enumerate(st.session_state.flashcards):
            with st.expander(f"Card {i+1}: {card['question'][:50]}..."):
                st.write(f"**Q:** {card['question']}")
                st.write(f"**A:** {card['answer']}")
        
        # Export options
        st.subheader("Export Flashcards")
        if st.button("Export as JSON"):
            st.download_button(
                label="Download JSON",
                data=st.json(st.session_state.flashcards),
                file_name="flashcards.json",
                mime="application/json"
            )

if __name__ == "__main__":
    main()