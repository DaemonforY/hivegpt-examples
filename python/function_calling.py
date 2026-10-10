"""函数调用：模型决定调用哪个函数，你执行后把结果交回给它"""
import json, os
from openai import OpenAI

client = OpenAI(base_url="https://hivegpt.cn/v1", api_key=os.environ["HIVEGPT_API_KEY"])
MODEL = "gpt-6.1-sol"

tools = [{
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "查询城市当前天气",
        "parameters": {"type": "object", "properties": {"city": {"type": "string"}}, "required": ["city"]},
    },
}]


def get_weather(city):  # 换成真实的天气接口
    return {"city": city, "temp": "18°C", "sky": "晴"}


messages = [{"role": "user", "content": "北京现在天气怎么样？"}]
first = client.chat.completions.create(model=MODEL, messages=messages, tools=tools)
msg = first.choices[0].message
messages.append(msg)
for call in msg.tool_calls or []:
    result = get_weather(**json.loads(call.function.arguments))
    messages.append({"role": "tool", "tool_call_id": call.id, "content": json.dumps(result, ensure_ascii=False)})

final = client.chat.completions.create(model=MODEL, messages=messages, tools=tools)
print(final.choices[0].message.content)
