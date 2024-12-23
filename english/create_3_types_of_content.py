from SimplerLLM.tools.generic_loader import load_content
from SimplerLLM.language.llm import LLM, LLMProvider
from resources import text_to_x_thread, text_to_blog_post, text_to_medium_post, text_to_summary, text_to_newsletter, format_to_json
import os , json
from dotenv import load_dotenv
load_dotenv()

#os.environ['GEMINI_API_KEY'] = "your key" # Variable name is important, don't change it

LLM_PROVIDER = LLMProvider.GEMINI
LLM_NAME = 'gemini-1.5-flash'
CONTENT_URL = "https://www.pinecone.io/learn/series/rag/rerankers/"

llm_instance = LLM.create(provider=LLM_PROVIDER, model_name=LLM_NAME)

#This can take a youtube video link, a blog post link, a csv file, etc... as input too 
file = load_content(CONTENT_URL) 

#Getting the 3 inputs
x_prompt = text_to_x_thread.format(input = file.content) 
newsletter_prompt = text_to_newsletter.format(input = file.content) 
summary_prompt = text_to_summary.format(input = file.content) 

#Generating the 3 types of social posts
x_thread = llm_instance.generate_response(prompt = x_prompt, max_tokens=1000)
with open("twitter.txt", "w", encoding='utf-8') as f:
    f.write(x_thread)

newsletter_section = llm_instance.generate_response(prompt = newsletter_prompt, max_tokens=1000)
with open("newsletter.txt", "w", encoding='utf-8') as f:
    f.write(newsletter_section)

bullet_point_summary = llm_instance.generate_response(prompt = summary_prompt, max_tokens=1000)
with open("summary.txt", "w", encoding='utf-8') as f:
    f.write(bullet_point_summary)

#Converting them into json format
final_prompt = format_to_json.format(input_1 = x_thread, 
                                     input_2 = newsletter_section, 
                                     input_3 = bullet_point_summary) 

response = llm_instance.generate_response(prompt = final_prompt, max_tokens=3000)

# Validate and write JSON with indentation for readability
try:
    json_data = json.loads(response)
    with open("Json_Result.json", "w", encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=4)
    print("JSON saved successfully.")
except json.JSONDecodeError as e:
    print(f"Gemini is bad at creating responses in json format")
    print("Error in JSON format:", e)
    with open("Json_Result.json", "w", encoding='utf-8') as f:
        f.write(response) 