import MapUtils
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())


def get_competion(messages, model="gpt-3.5-turbo"):
    client = OpenAI()
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0,
        max_tokens=1000,
        tool_choice="auto",
        tools=[
            {
                "type": "function",
                "function": {
                    "name": "get_location_coordinate",
                    "description": "get the location coordinate",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "location": {
                                "type": "string",
                                "description": "the location name",
                            },
                            "city": {
                                "type": "string",
                                "description": "the city name",
                            }
                        }
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "search_nearby_poi",
                    "description": "search nearby poi",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "longitude": {
                                "type": "string",
                                "description": "the longitude",
                            },
                            "latitude": {
                                "type": "string",
                                "description": "the latitude",
                            }
                        }
                    }
                }
            }]
    )
    return response.choices[0].message


prompt = "我现在在北京天安门，推荐一下附件的咖啡店"

messages = [
    {"role": "system", "content": "你是一个旅游指南助手，能够根据用户的位置和需求，推荐附近的景点、美食、住宿等。"},
    {"role": "user", "content": prompt}
]

response = get_competion(messages, prompt)

messages.append(response)

while response.tool_calls is not None:
    if response.tool_calls[0].type == "function":
        function_call = response.tool_calls[0].function
        function_name = function_call.name
        function_args = function_call.arguments
        if function_name == "get_location_coordinate":
            location = function_args["location"]
            city = function_args["city"]
            location_coordinate = MapUtils.get_location_coordinate(location, city)
            response = get_competion(messages, prompt)
        elif function_name == "search_nearby_poi":
            longitude = function_args["longitude"]
            latitude = function_args["latitude"]
            response = get_competion(messages, prompt)

        messages.append(response)



print(response.content)

