import streamlit as st
import requests
import json
import os

'''
Assignment 2: Code Quality Report.
This function uses the Groq API to analyze Python code quality. It reads all Python files in the current directory
and sends them to the API for analysis. The API returns a comprehensive report on the code quality, which is then
displayed to the user.
'''

def assignment2_code_quality_report():
    st.subheader("Code QA Analysis")

    # Streamlit UI
    st.write("Analyze all Python files in the current directory.")

    api_key = st.text_input("Enter your Groq API Key (press ENTER to continue)", type="password")

    def get_python_files():
        return [f for f in os.listdir('.') if os.path.isfile(f) and f.endswith('.py')]

    def get_file_content(filename):
        with open(filename, 'r') as file:
            return file.read()

    if api_key:
        python_files = get_python_files()

        if not python_files:
            st.write("No Python files found in the current directory.")
        else:
            for file in python_files:
                code_content = get_file_content(file)

                # Prepare the API request
                api_url = "https://api.groq.com/openai/v1/chat/completions"
                headers = {
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                }

                request_data = {
                    "model": "llama3-70b-8192",
                    "messages": [
                        {
                            "role": "system",
                            "content": "### Instruction ###\nYou are a code QA tester. You are looking at provided code and give a comprehensive report on the code quality."
                        },
                        {
                            "role": "user",
                            "content": f"### Code ###\n{code_content}"
                        }
                    ],
                    "max_tokens": 500,
                    "temperature": 0.5
                }

                # Show loading spinner while the request is processing
                with st.spinner(f"Analyzing {file}..."):
                    response = requests.post(api_url, headers=headers, data=json.dumps(request_data))

                if response.status_code == 200:
                    result = response.json()
                    report = result["choices"][0]["message"]["content"]

                    # Display the report with filename
                    st.subheader(f"Analysis Report for {file}:")
                    st.markdown(report)
                else:
                    st.error(f"Failed to analyze {file}: {response.status_code}")
