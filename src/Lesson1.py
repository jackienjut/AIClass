from openai import OpenAI
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

client = OpenAI()

def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message.content

#mission description
instruction="""
你是一名优秀的导游，每当用户输入城市名称的时候，你会输出该城市的简介。有哪些景点，有哪些美食，有哪些历史，和名人。
"""

#用户输入
input_text= """
    南京
"""

out_put_format="""
    以json的格式输出
"""

#prompt模板
prompt_template = f"""
你是一名优秀的导游，每当用户输入城市名称的时候，你会输出该城市的简介。有哪些景点，有哪些美食，有哪些历史，和名人。
    {instruction}
    {out_put_format}
    用户输入：{input_text}
    城市简介：
"""

respose = get_completion(prompt_template, model="gpt-3.5-turbo")
print(respose)
