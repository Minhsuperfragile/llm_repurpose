import streamlit as st
import json
from SimplerLLM.tools.generic_loader import load_content
from SimplerLLM.language.llm import LLM, LLMProvider
from vietnamese.resources import text_to_x_thread, text_to_summary, text_to_newsletter, format_to_json

import os , json

os.environ['GEMINI_API_KEY'] = "AIzaSyDzUs85b_kCq4i850Uof05cEnNBqyArld8" # Variable name is important, don't change it

LLM_PROVIDER = LLMProvider.GEMINI
LLM_NAME = 'gemini-pro'
CONTENT_URL = "https://www.pinecone.io/learn/series/rag/rerankers/"

llm_instance = LLM.create(provider=LLM_PROVIDER, model_name=LLM_NAME)

st.title("Content Generation With A Single Click")

url = st.text_input("Enter the URL or File Name of your input:")

if st.button("Generate Content"):
    if url:
        try:
            file = load_content(url)

            x_prompt = text_to_x_thread.format(input=file.content)
            newsletter_prompt = text_to_newsletter.format(input=file.content)
            summary_prompt = text_to_summary.format(input=file.content)

            x_thread = llm_instance.generate_response(prompt=x_prompt, max_tokens=1000)
            newsletter_section = llm_instance.generate_response(prompt=newsletter_prompt, max_tokens=1000)
            bullet_point_summary = llm_instance.generate_response(prompt=summary_prompt, max_tokens=1000)

            st.subheader("Generated Twitter Thread")
            st.write(x_thread)
            st.markdown("---")

            st.subheader("Generated Newsletter Section")
            st.write(newsletter_section)
            st.markdown("---")

            st.subheader("Generated Bullet Point Summary")
            st.write(bullet_point_summary)
            st.markdown("---")

            final_prompt = format_to_json.format(
                input_1=x_thread, 
                input_2=newsletter_section, 
                input_3=bullet_point_summary
            )
            response = llm_instance.generate_response(prompt=final_prompt, max_tokens=3000)
            
            try:
                json_data = json.loads(response)
                st.markdown("### __Generated JSON Result__")
                st.json(json_data)
                st.download_button(
                    label="Download JSON Result",
                    data=json.dumps(json_data, ensure_ascii=False, indent=4),
                    file_name="Json_Result.json",
                    mime="application/json"
                )
            except json.JSONDecodeError as e:
                st.error(f"Error in JSON format: {e}")
                st.write(response)
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter a valid URL.")