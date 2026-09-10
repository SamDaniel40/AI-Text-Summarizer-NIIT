import streamlit as st
from groq import Groq

# 1. Page Configuration
st.set_page_config(
    page_title="AI Text Summarizer", 
    page_icon="📝", 
    layout="centered"
)

# 2. Main Title and Subtitle
st.title("📝 AI Text Summarizer")
st.write("Generate clear, instant summaries from long articles or documents powered by Groq.")

# 3. Sidebar for Configuration
st.sidebar.header("Configuration")

# Secure input field for the Groq API key
api_key = st.sidebar.text_input(
    "Enter Groq API Key:", 
    type="password", 
    help="Get yours from ://groq.com"
)

# Model selection dropdown
model_choice = st.sidebar.selectbox(
    "Choose LLM Model:",
    ["openai/gpt-oss-20b", "openai/gpt-oss-120b", "minimaxai/minimax-m2.7"],
    index=0,
    help="openai/gpt-oss-20b is recommended for lightning-fast summary generation."
)

# Format selection dropdown
summary_length = st.sidebar.selectbox(
    "Select Output Format:", 
    ["Concise (1-2 sentences)", "Standard (1 paragraph)", "Bullet points"]
)

# 4. Main Interface
user_text = st.text_area("Paste your long text here:", height=300, placeholder="Type or paste your text...")

# Display active word count dynamically
if user_text:
    word_count = len(user_text.split())
    st.info(f"Input Word Count: {word_count} words")

# 5. Summarization Execution Block
if st.button("Generate Summary", type="primary"):
    if not api_key:
        st.error("⚠️ Authentication Error: Please provide your Groq API Key in the sidebar.")
    elif not user_text.strip():
        st.error("⚠️ Input Error: Please enter some text to summarize.")
    else:
        try:
            # Initialize the Groq SDK Client
            client = Groq(api_key=api_key)
            
            # Format custom instructions for the LLM based on user selection
            prompt = f"Summarize the following text into a {summary_length} format. Focus only on critical takeaways. Text:\n\n{user_text}"
            
            with st.spinner("Processing text with Groq inference engines..."):
                # Call Groq's high-speed completion endpoint
                chat_completion = client.chat.completions.create(
                    model=model_choice,
                    messages=[
                        {
                            "role": "system", 
                            "content": "You are a precise writing assistant that condenses long text into essential insights without adding external facts."
                        },
                        {
                            "role": "user", 
                            "content": prompt
                        }
                    ],
                    temperature=0.2, # Low temperature ensures strict adherence to the input facts
                )
                
                # Extract response text
                summary_output = chat_completion.choices[0].message.content
                
                # Display final UI output
                st.success("✨ Summary Generated Successfully!")
                st.subheader("Summary Output")
                st.markdown(summary_output)
                
                # Provide download utility for the results
                st.download_button(
                    label="Download Summary as TXT",
                    data=summary_output,
                    file_name="summary.txt",
                    mime="text/plain"
                )
                
        except Exception as e:
            st.error(f"Execution Error: {str(e)}")