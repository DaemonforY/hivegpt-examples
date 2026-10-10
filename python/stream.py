"""流式输出：回答一边生成一边打印"""
import os
from openai import OpenAI

client = OpenAI(base_url="https://hivegpt.cn/v1", api_key=os.environ["HIVEGPT_API_KEY"])

stream = client.chat.completions.create(
    model="gpt-6.1-sol",
    messages=[{"role": "user", "content": "写一首关于秋天的四行短诗"}],
    stream=True,
)
for chunk in stream:
    if chunk.choices and chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="", flush=True)
print()
