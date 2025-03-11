
template_text_extract_type = """ 
You are an AI model that classifies descriptions into three categories:

- "new_chat" if the new description introduces a completely different topic or a separate request from previous ones.  
- "new_mess_on_current_chat" if the new description continues, expands, or provides additional details about an existing topic in the previous descriptions.  
- "undefined" if the new description is unclear, random, lacks a clear subject, or does not provide meaningful information.  


**Rules for classification:**  
- If the new description presents a **new, distinct request**, classify it as "new_chat".  
- If the new description **adds details or refines** an existing request, classify it as "new_mess_on_current_chat".  
- If the new description is **random, nonsensical, or unclear**, classify it as "undefined".  

**Important:**  
Your response **must be only one of these three labels**: `"new_chat"`, `"new_mess_on_current_chat"`, or `"undefined"`. Do not include any explanations, additional text, or formatting.

Previous descriptions:  
{previous_descriptions}  

New description:  
"{new_description}"  

Based on the context, respond with only one of these three labels.
"""


from dotenv import load_dotenv
import os

# Tải các biến môi trường từ file .env
load_dotenv()

# Lấy giá trị API Key từ môi trường
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")


from groq import Groq
from openai import OpenAI

# store chat bot and user messages
chatHistory = []
def resert_chat_history():
    global chatHistory
    chatHistory = []

def add_new_chat(mess):   
    global chatHistory 
    chatHistory = []
    chatHistory.append(mess)

def add_new_mess_on_currrent_chat(mess):
    global chatHistory
    chatHistory.append(mess)    

   
def use_groq(input):
    global GROQ_API_KEY
    client = Groq(
        api_key=GROQ_API_KEY,
    )

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": input,
            }
        ],
        model="llama-3.1-8b-instant",
    )
    
    res =  chat_completion.choices[0].message.content
    return str(res)

def use_gpt(prompt):
    client = OpenAI(
    api_key=OPENAI_API_KEY,
    base_url = "https://api.openai.com/v1")

    response = client.chat.completions.create(
        model="gpt-4o",  # Đảm bảo model hợp lệ
        messages=[
            {
                "role": "user",
                "content": prompt  
            }
        ],
    )
    return str(response.choices[0].message.content)

"""
    check_type_of_mess :   input : user's mess , chat history
    return : type of mess new_chat or new_mess_on_current_chat or undefined
"""
def return_type_of_mess(chatHistory,mess):
    prompt = template_text_extract_type.format(
        previous_descriptions = chatHistory,
        new_description = mess
    )
    print("======== \n prompt \n" + prompt + "\n ========") 
    
    return use_groq(prompt)
  
def classify_type_of_mess(mess):
    type = return_type_of_mess(chatHistory=chatHistory , mess=mess)
    if type == "new_chat":
        add_new_chat(mess)
    elif type == "new_mess_on_current_chat":       
        add_new_mess_on_currrent_chat(mess)
    # dont do any if  type == "undefined"
    return type
        
        
        


