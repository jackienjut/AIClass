class NLU：
    def __init__(self):
        self.prompt_template = f"{instruction}\n\n{
            output_format}\n\n{examples}\n\n用户输入：\n__INPUT__"
        self.client
        self.messages

    def _get_compoetion(self,client,prompt,model="gpt-3.5-turbo"):
        response = client.ChatCompletion.create(
            model=model,
            messages=messages
            temperature=0
        )
        return response.choices[0].message.content
