from SimplerLLM.tools.generic_loader import load_content
from SimplerLLM.language.llm import LLM, LLMProvider
from resources import text_to_x_thread, text_to_blog_post, text_to_medium_post, text_to_summary, text_to_newsletter, format_to_json
import os , json

LLM_PROVIDER = LLMProvider.OLLAMA
LLM_NAME = 'llama3.3' 
CONTENT_URL = "https://www.pinecone.io/learn/series/rag/rerankers/"

llm_instance = LLM.create(provider=LLM_PROVIDER, model_name=LLM_NAME)

llm_instance = LLM.create(provider=LLM_PROVIDER, model_name=LLM_NAME)

#This can take a youtube video link, a blog post link, a csv file, etc... as input too 
file = load_content(CONTENT_URL) 

#Get the pre-defined prompt
x_prompt = text_to_x_thread.format(input = file.content) 

x_thread = llm_instance.generate_response(prompt = x_prompt, max_tokens=1000)
with open(f"{LLM_NAME}_twitter.txt", "w", encoding='utf-8') as f:
	f.write(x_thread)

summary_prompt = text_to_summary.format(input = file.content)

summary = llm_instance.generate_response(prompt=summary_prompt, max_tokens=1000)
with open(f"{LLM_NAME}_summary.txt", "w", encoding="utf-8") as f:
   f.write(summary)

newsletter_prompt = text_to_newsletter.format(input = file.content) 

newsletter_section = llm_instance.generate_response(prompt = newsletter_prompt, max_tokens=1000)
with open(f"{LLM_NAME}_newsletter.txt", "w", encoding='utf-8') as f:
    f.write(newsletter_section)
