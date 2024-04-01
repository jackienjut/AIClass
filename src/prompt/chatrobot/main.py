import json
import copy
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())
client = OpenAI()
instructions = """

"""


class NLU:
    def __init__(self):
        self.prompt_template = f"""{instruction}\n\n
        {output_format}\n\n{examples}\n\n用户输入：\n__INPUT__"""

    def _get_compoetion(self, prompt, model="gpt-3.5-turbo"):
        messages = [{"role": "user", "content": prompt}]
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0
        )
        semamtics = json.loads(response.choices[0].message.content)
        return {k: v for k, v in semamtics.items() if v}

    def parse(self, input):
        prompt = self.prompt_template.replace("__INPUT__", input)
        return self._get_compoetion(prompt)


class DST:
    def __init__(self):
        pass

    def update(self, state, nlu_semantics):
        if "name" in nlu_semantics:
            state.clear()
        if "sort" in nlu_semantics:
            slot = nlu_semantics["sort"]["value"]
            if slot in state and state[slot]["operation"] == "==":
                del state[slot]

        for k, v in nlu_semantics.items():
            state[k] = v
        return state


class MockedDB:
    def __init__(self):
        self.data = {
            "name": [
                {"name": "经济套餐", "price": 50, "data": 10, "requirement": None},
                {"name": "畅游套餐", "price": 180, "data": 100, "requirement": None},
                {"name": "无限套餐", "price": 300, "data": 1000, "requirement": None},
                {"name": "校园套餐", "price": 150, "data": 200, "requirement": "在校生"},
            ]
        }

    def retrieve(self, **kwargs):
        records = []
        for r in self.data:
            select = True
            if r["requirement"]:
                if "status" not in kwargs or kwargs["status"] != r["requirement"]:
                    continue
            for k, v in kwargs.items():
                if k == "sort":
                    continue
                if k == "data" and v["value"] == "无上限":
                    if r[k] != 1000:
                        select = False
                        break
                if "operator" in v:
                    if not eval(str(r[k]) + v["operator"] + str(v["value"])):
                        select = False
                        break
                elif str(r[k]) != str(v):
                    select = False
                    break
            if select:
                records.append(r)
        if len(records) <= 1:
            return records
        key = "price"
        reverse = False
        if "sort" in kwargs:
            key = kwargs["sort"]["value"]
            reverse = kwargs["sort"]["ordering"] == "descend"
        return sorted(records, key=lambda x: x[key], reverse=reverse)

class DialogManager:
    def __init__(self , prompt_templates):
        self.state = {}
        self.session = [
            {
                "role": "system",
                "content": "你是一个手机流量套餐的客服代表，你叫小瓜。可以帮助用户选择最合适的流量套餐产品。"
            }
        ]
        self.nlu = NLU()
        self.dst = DST()
        self.db = MockedDB()
        self.prompt_templates = prompt_templates

    def _wrap(selfself,user_input , records):
