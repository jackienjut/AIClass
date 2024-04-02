import  json
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv

_=load_dotenv(find_dotenv())

def print_json(data):
    print (data)

client = OpenAI()

message = [
    {
        "role": "system",
        "content": """
你是一个性感的女导游，回答用户的问题，一些旅游的建议。
"""
    }
]


def get_completion(prompt):
    message.append({"role": "user", "content": prompt})
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=message,
        temperature=0.5,
        max_tokens=1000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    msg = completion.choices[0].message.content
    message.append({"role": "assistant", "content": msg})


get_completion("上海有没有什么好玩的景点？")
get_completion("我只有一天的时间，给我推荐一个景点")
print_json(message)

