import os
import json
import traceback
import pandas as pd
from dotenv import load_dotenv
from src.mcqgenerator.utils import read_file, get_table_data
import streamlit as st
from langchain_community.callbacks import get_openai_callback
from src.mcqgenerator.MCQGENERATOR import generate_evaluate_chain
from src.mcqgenerator.logger import logging

# loading file
with open('C:/Users/SUBOMMAS/mcq-llm/Response.json', 'r') as file:
    content = file.read()
    RESPONSE_JSON = json.loads(content)


# creating a title for app
st.title("MCQs Genrator Application with Langchain")

##Create a form using st.form
with st.form("user_inputs"):
    #file upload
    uploaded_file = st.file_uploader("UPload a PDF or text file")

    #imput fields
    mcq_count = st.number_input("No. of MCQS", min_value=3, max_value=50)

    #Subject
    subject = st.text_input("which is th Subject", max_chars=20)

    #Quiz tone
    tone = st.text_input("Complexity level of MCQs", max_chars=20, placeholder ="Simple")

    #Add button
    button = st.form_submit_button("Generate")

    #Check if the button is clicked and all fields have input
    if button and uploaded_file is not None and mcq_count and subject and tone:
        with st.spinner("loading..."):
            try:
                text = read_file(uploaded_file)
                #COunt tokens and the cost of API call
                with get_openai_callback() as cb:
                    response = generate_evaluate_chain(
                        {
                             "text": text,
                             "number": mcq_count,
                             "subject":subject,
                             "tone": tone,
                             "response_json": json.dumps(RESPONSE_JSON)
                        }
                    )
                   # st.write(response)
            except Exception as e:
                traceback.print_exception(type(e), e, e.__traceback__)
                st.error("Error")
            else:
                print(f"Total Tokens:{cb.total_tokens}")
                print(f"Prompt Tokens:{cb.prompt_tokens}")
                print(f"Completion Tokens:{cb.completion_tokens}")
                print(f"Total Cost:{cb.total_cost}")
                if isinstance(response, dict):
                    # Extract data
                    quiz = response.get("quiz", None)
                    if quiz is not None:
                        table_data = get_table_data(quiz)
                        if table_data is not None:
                            df= pd.DataFrame(table_data)
                            df.index = df.index + 1
                            df.to_csv(f"{subject}.csv",index=False)
                            a = st.table(df)
                            # Display the review in text box
                            st.text_area(label="Review", value= response["review"])
                        else:
                            st.error("Error in the table data")
                else:
                    st.write(response)

                
                # #Download
                # quiz = json.loads(quiz)
                # quiz_table_data = []
                # #type(quiz_table_data) format table
                # for key, value in quiz.items():
                #     mcq = value['mcq']
                #     options = "//".join( [
                #             f"{option}: {option_value}"
                #             for option, option_value in value["options"].items()
                #             ])
                #     correct = value["correct"]
                #     quiz_table_data.append({"MCQ": mcq, "Choices": options, "Correct": correct})

                # quiz=pd.DataFrame(quiz_table_data)
                # quiz.to_csv(f"{subject}.csv",index=False)


file_path= f"./{subject}.csv"
file_exits = os.path.isfile(file_path)
if file_exits and st.button("Download Resource File"):
    with open(file_path, "rb") as file:
      file_content= file.read()
    st.download_button(
        label="Click to Download",
        data=file_content,
        file_name="resource_file.csv",
        key="download_button",
                    )
