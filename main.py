import json
import os

from dotenv import load_dotenv
from openai import OpenAI

from llm_config import PROVIDERS, DEFAULT_PROVIDER
from tools import TOOLS, TOOLS_FUNCTIONS
from prompts.system_prompt import SYSTEM_PROMPT

load_dotenv()

MAX_ITERATIONS = 10  # 单次对话中,agent loop 最多执行的轮数(防止无限调工具)


def get_client(provider=None):
    provider = provider or DEFAULT_PROVIDER
    if provider not in PROVIDERS:
        raise ValueError(f"不支持的 provider {provider}")

    config = PROVIDERS[provider]
    api_key = os.getenv(config["api_key_env"])
    if not api_key:
        raise ValueError(f"没有找到 api_key: {config['api_key_env']}")

    client = OpenAI(
        api_key=api_key,
        base_url=config["base_url"],
    )
    return client, config["default_model"]


class Agent:
    """最基础的 agent loop:LLM 决策 -> 执行工具 -> 观察结果 -> 再决策"""

    def __init__(self, client, model, system_prompt=SYSTEM_PROMPT, max_iterations=MAX_ITERATIONS):
        self.client = client
        self.model = model
        self.max_iterations = max_iterations
        self.messages = [
            {"role": "system", "content": system_prompt},
        ]

    def run(self, user_input: str) -> str:
        """处理一轮用户输入,返回模型的最终回答(内层循环即 agent loop)"""
        self.messages.append({"role": "user", "content": user_input})

        for _ in range(self.max_iterations):
            response = self.client.chat.completions.create(
                model=self.model,
                messages=self.messages,
                tools=TOOLS,
            )

            message = response.choices[0].message

            # 模型不再调用工具 => 任务完成,返回最终回答
            if not message.tool_calls:
                self.messages.append({
                    "role": "assistant",
                    "content": message.content,
                })
                return message.content

            # 先把 assistant 的 tool_calls 决策加入历史
            self.messages.append(message)

            # 逐个执行工具,并把结果作为 tool 消息加入历史
            for tool_call in message.tool_calls:
                result = self._execute_tool(tool_call)
                self.messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": str(result),
                })

        # 超过最大轮数,强制结束,避免死循环烧钱
        return "抱歉,这个任务我尝试了太多次都没有完成,请换个问法。"

    def _execute_tool(self, tool_call) -> str:
        """执行单个工具调用,任何失败都返回字符串,保证 tool 消息一定会被加入"""
        tool_name = tool_call.function.name
        print(f"[调用工具] {tool_name}")

        try:
            arguments = json.loads(tool_call.function.arguments)
        except json.JSONDecodeError as e:
            return f"工具参数解析失败: {e}"

        tool_function = TOOLS_FUNCTIONS.get(tool_name)
        if tool_function is None:
            return f"不存在工具 {tool_name}"

        try:
            return tool_function(**arguments)
        except Exception as e:
            return f"工具 {tool_name} 执行出错: {e}"


def main():
    client, model = get_client()
    agent = Agent(client, model)
    print("输入 exit 退出")

    # 外层循环:会话循环
    while True:
        user_input = input("\nyou: ").strip()
        if not user_input:
            continue
        if user_input == "exit":
            break

        # 内层循环:agent loop,在这里完成
        answer = agent.run(user_input)
        print(f"\nAI: {answer}")


if __name__ == "__main__":
    main()
