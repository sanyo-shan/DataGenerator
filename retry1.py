import streamlit as st

st.title("Dynamic Synthetic Data Prompt Builder")

# Initialize session state
if "headers" not in st.session_state:
    st.session_state.headers = [{"header": "", "dtype": "String", "desc": ""}]
if "rules" not in st.session_state:
    st.session_state.rules = [""]

# Functions to add new rows
def add_header():
    st.session_state.headers.append({"header": "", "dtype": "String", "desc": ""})

def add_rule():
    st.session_state.rules.append("")

# Form
with st.form("prompt_form"):
    num_records = st.number_input("Number of records to generate", min_value=1, step=1)

    st.subheader("Headers")
    for i, h in enumerate(st.session_state.headers):
        st.text_input(f"Header Name {i+1}", value=h["header"], key=f"header_{i}")
        st.selectbox(
            f"Data Type {i+1}",
            ["Integer", "Bool", "String", "Date of Birth"],
            index=["Integer", "Bool", "String", "Date of Birth"].index(h["dtype"]),
            key=f"dtype_{i}"
        )
        st.text_input(f"Short Description {i+1}", value=h["desc"], key=f"desc_{i}")
        st.markdown("---")

    st.form_submit_button("➕ Add Header", on_click=add_header)

    st.subheader("Rules")
    for i, r in enumerate(st.session_state.rules):
        st.text_area(f"Rule {i+1}", value=r, key=f"rule_{i}")
    st.form_submit_button("➕ Add Rule", on_click=add_rule)

    submitted = st.form_submit_button("Generate Prompt")

    if submitted:
        # Build headers section
        headers_text = "\n".join(
            [f"- {st.session_state[f'header_{i}']}: {st.session_state[f'desc_{i}']}" 
             for i in range(len(st.session_state.headers))]
        )

        # Build rules section
        rules_text = "\n".join(
            [f"{i+1}. {st.session_state[f'rule_{i}']}" 
             for i in range(len(st.session_state.rules)) if st.session_state[f'rule_{i}']]
        )

        # Final prompt
        prompt = f"""
Generate {num_records} rows of realistic synthetic healthcare data.
Output ONLY a CSV format with the following headers:
{headers_text}
Rules:
{rules_text}
        """

        st.subheader("Generated Prompt")
        st.code(prompt, language="text")
        print(prompt)
