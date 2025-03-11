import os
import json
from groq import Groq

from openai import OpenAI


template_kie = """You are an honest, helpful AI Assistant in extracting information field. Your goal is to provide the extracted information with JSON format from the input. you must return the same information as the output in the template, and do not add other statements such as the opening sentence: "Here is the extracted information in JSON format:"
Below are the information fields you need to extract and their definitions, the result MUST follow this format:
{schema}

This list specifies that the extracted adjectives must be in the list. When you extract an adjective that is not in the list, check to see if it is a synonym for any word in the list. If so, return the synonym in the list. Otherwise, return "bình thường".
The list of extractable adjectives : 
{extractable_adj}

You will be penalized if:
- Add or omit any information. If you don't find the clue to fill in the field, just leave it blank with "".
- Returns irrelevant results or does not follow json format 
 
EXAMPLES
-----
{examples}
-----
Input:
{content}
Output:```"""

description_dictionary =   { "schema" : """
        {
        "room_adj": "adjective describing room in Vietnamese",
        "furnitures": [
            {
                "bed": {
                    "amount": "number of beds",
                    "adjective": "adjective describing bed in Vietnamese"
                }
            },
            {
                "table": {
                    "amount": "number of tables",
                    "adjective": "adjective describing table in Vietnamese"
                }
            },
            {
                "chair": {
                    "amount": "number of chairs",
                    "adjective": "adjective describing chair in Vietnamese"
                }
            },
            {
                "door": {
                    "amount": "number of doors",
                    "adjective": "adjective describing door in Vietnamese"
                }
            },
            {
                "wardrobe": {
                    "amount": "number of wardrobes",
                    "adjective": "adjective describing wardrobe in Vietnamese"
                }
            },
            {
                "window": {
                    "amount": "number of windows",
                    "adjective": "adjective describing window in Vietnamese"
                }
            },
            {
                "rug": {
                    "amount": "number of rugs",
                    "adjective": "adjective describing rugs in Vietnamese"
                }
            }
        ]
    }
    """ , 
    "sample" : {
        "input" : """
            "input" : "Tôi muốn xây một căn phòng khổng lồ , có một chiếc ghế hiện đại , một chiếc bàn màu xanh , hai chiếc tủ quần áo  , thảm chà chân màu xanh"
         """
        ,
        
        "output" : """
        "output" : {
            "room_adj": "to",
            "furnitures": [
                {
                    "bed": {
                        "amount": "0",
                        "adjective": ""
                    }
                },
                {
                    "table": {
                        "amount": "1",
                        "adjective": "xanh"
                    }
                },
                {
                    "chair": {
                        "amount": "1",
                        "adjective": "hiện đại"
                    }
                },
                {
                    "door": {
                        "amount": "number of doors",
                        "adjective": "adjective describing door in Vietnamese"
                    }
                },
                {
                    "wardrobe": {
                        "amount": "2",
                        "adjective": "bình thường"
                    }
                },
                {
                    "window": {
                        "amount": "0",
                        "adjective": ""
                    }
                },
                {
                "rug": {
                    "amount": "1",
                    "adjective": "xanh"
                }
            }
            ]
        }
         """
        
    }
}
exttractable_adj = [
    "hiện đại",
    "cổ điển",
    "tối giản",
    "phức tạp",
    "độc đáo",
    "bình thường",
    "to",
    "nhỏ",
    "dài",
    "rộng",
    "tròn",
    "vuông",
    "tam giác",
    "gỗ",
    "kim loại",
    "mới",
    "cũ",
    "sạch",
    "bẩn",
    "đẹp",
    "xấu"
]

def extractInfoUser(input):
    text = template_kie.format(schema = description_dictionary["schema"] ,extractable_adj = exttractable_adj , examples = description_dictionary["sample"]["input"] + description_dictionary["sample"]["output"],content = input)

    client = Groq(
        api_key=os.environ.get("GROQ_API_KEY"),
    )

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": text,
            }
        ],
        model="llama3-8b-8192",
    )
    
    dict_return = json.loads(chat_completion.choices[0].message.content)
    return dict_return




# def extractInfoUser(input):
#     # Tạo nội dung yêu cầu API
#     text = template_kie.format(
#         schema=description_dictionary["schema"],
#         extractable_adj=exttractable_adj,
#         examples=description_dictionary["sample"]["input"] + description_dictionary["sample"]["output"],
#         content=input
#     )
    
#     print(text)
    
#     # Gửi yêu cầu tới OpenAI API
#     response = client.chat.completions.create(
#         model="gpt-4o",  # Đảm bảo model hợp lệ
#         messages=[
#             {
#                 "role": "user",
#                 "content": text  
#             }
#         ],
#     )
    
#     print("result" + str(response.choices[0].message.content  ))
#     # Lấy nội dung từ response
#     try:
#         output_text = response.choices[0].message.content  
#         dict_return = json.loads(output_text)  # Parse JSON
#         return dict_return
#     except json.JSONDecodeError as e:
#         print(f"Lỗi khi parse JSON: {e}")
#         return {"error": "Failed to parse JSON from response"}
#     except Exception as e:
#         print(f"Lỗi khác: {e}")
#         return {"error": "Unexpected error"}

# # # Kiểm tra hàm
# print(extractInfoUser("tôi muốn xây một căn phòng hiện đại có một chiếc bàn màu đỏ , một chiếc giường hiện đại , hai chiếc ghế"))
