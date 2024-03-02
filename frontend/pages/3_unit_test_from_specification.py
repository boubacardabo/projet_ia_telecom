import streamlit as st
from langchain.prompts import PromptTemplate
import streamlit as st
import requests
import os


backend_url = os.environ.get("API_URL") or "http://localhost:4000"
st.session_state["is_invoked"] = False
use_case_name = "codewriter_unit_test"

# Create a header element
st.header("Code writer : unit test with specification")




specification_string = st.text_area(
    label="specification",
    value="",
    key="specification")


function_string = st.text_area(
    label="function",
    value="",
    key="function")



setup_button = st.button("invoke output")
if setup_button:
    data = (
        {
            "use_case": use_case_name,
            "specification_string" : specification_string,
            "function_string" : function_string, 
                        }
    )
    with st.spinner(""):
        response = requests.post(f"{backend_url}/invoke_use_case/", json=data)

        if use_case_name in response.text and response.status_code == 200:
            st.session_state["is_invoked"] = True
            st.success("Your output has been successfully invoked")
        else:
            st.session_state["is_invoked"] = False
            st.error(
                f"An error has occurred during invocation: {response.status_code} {response.text}"
            )






