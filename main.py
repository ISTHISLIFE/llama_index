import streamlit as st
from tkinter import Tk, filedialog
import llm
llm = llm.llm()
# Function to open folder selection dialog
def select_folder():
    # Hide Tkinter root window
    root = Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    folder_path = filedialog.askdirectory()  # Open the folder dialog
    root.destroy()
    llm.load_document(folder_path)
    return folder_path

# Function to simulate chatbot response
def get_response(user_input):
    return llm.inference(user_input)
# Streamlit App
def main():
    # Custom CSS for styling
    st.markdown("""
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f9f9f9;
            }
            .stApp {
                background-color: #f2f2f2;
            }
        </style>
    """, unsafe_allow_html=True)

    # App title
    st.title("💬 Chatbot Application with Folder Selection")
    st.markdown("Welcome! Chat with the bot below or select a folder.")

    # Folder selection button
    if st.button("Select a Folder"):
        folder_path = select_folder()
        if folder_path:
            st.success(f"Selected folder: `{folder_path}`")
        else:
            st.warning("No folder selected.")

    # Placeholder for chat history
    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    # Display chat history
    for message in st.session_state["messages"]:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # User input
    user_input = st.chat_input("Type your message...")
    if user_input:
        # Add user message to chat history
        st.session_state["messages"].append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)

        # Generate bot response
        response = str(get_response(user_input))
        st.session_state["messages"].append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.write(response)

if __name__ == "__main__":
    main()
