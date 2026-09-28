import time
from openai import OpenAI
import os
from dotenv import load_dotenv
from llm_config import PROVIDERS,DEFAULT_PROVIDER
from tools import TOOLS_FUNCTIONS,TOOLS
import json
from prompts.system_prompt import SYSTEM_PROMPT

load_dotenv()

def get_client(provider=None):
    provider = provider or DEFAULT_PROVIDER
    if provider not in PROVIDERS:
        raise ValueError(
            f"不支持的 provider {provider}"
        )

    config = PROVIDERS[provider]
    api_key = os.getenv(config["api_key_env"])
    if not api_key:
        raise ValueError(
            f"没有找到api_key{config['api_key_env']}"
        )
    client = OpenAI(
        api_key=api_key,
        base_url=config["base_url"],
    )
    return client,config["default_model"]


client,model = get_client("zhipu")

messages = [
    {
        "role":"system",
        "content":SYSTEM_PROMPT,
    }
]

while True:

    user_input = input("\nyou:")

    if user_input == "exit":
        break

    messages.append(
            {"role":"user","content":user_input},
        )

    while True:
        # print("\n===== 发送给LLM的messages =====")
        # print(messages)
        # print("==============================")

        response = client.chat.completions.create(
            model = model,
            messages = messages,
            # stream = True,
            tools = TOOLS,
        )

        message = response.choices[0].message

        if not message.tool_calls:
            messages.append({
                "role":"assistant",
                "content":message.content,
            })
            print("AI:")
            print(message.content)
            break

        messages.append(message)

        for tool_call in message.tool_calls:

            tool_name = tool_call.function.name
            arguments = json.loads(
                tool_call.function.arguments
            )
            print(f"调用工具{tool_name}")

            tool_function = TOOLS_FUNCTIONS[tool_name]
            if tool_function is None:
                result = (
                    f"不存在工具{tool_name}"
                )
            else:

                result = tool_function(**arguments)

                messages.append({
                    "role":"tool",
                    "tool_call_id":tool_call.id,
                    "content":str(result),
                })
                print("result已加入messages")



    # messages.append(
    #     {"role": "assistant", "content": full_response},
    # )

    # full_response = ""
    # for chunk in response:
    #     if chunk.choices and chunk.choices[0].delta.content:
    #         text = chunk.choices[0].delta.content
    #         for char in text:
    #             print(char, end="", flush=True)
    #             full_response += char
    #             time.sleep(0.005)

