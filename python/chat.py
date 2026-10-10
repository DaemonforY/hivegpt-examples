"""最简单的对话：pip install -U openai，然后 python chat.py"""
import os
from openai import OpenAI

client = OpenAI(base_url="https://hivegpt.cn/v1", api_key=os.environ["HIVEGPT_API_KEY"])

resp = client.chat.completions.create(
    model="gpt-6.1-sol",
    messages=[
        {"role": "system", "content": "你是简洁的中文助手"},
        {"role": "user", "content": "用一句话解释什么是 API"},
    ],
)
print(resp.choices[0].message.content)
print("用量：", resp.usage.total_tokens, "token")
