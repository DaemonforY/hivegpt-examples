"""让模型严格按 JSON Schema 返回结构化数据"""
import json, os
from openai import OpenAI

client = OpenAI(base_url="https://hivegpt.cn/v1", api_key=os.environ["HIVEGPT_API_KEY"])

resp = client.chat.completions.create(
    model="gpt-6.1-sol",
    messages=[{"role": "user", "content": "张三，28岁，在杭州做设计师，电话 138-0000-0000。提取信息"}],
    response_format={"type": "json_schema", "json_schema": {
        "name": "person",
        "strict": True,
        "schema": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "integer"},
                "city": {"type": "string"},
                "job": {"type": "string"},
            },
            "required": ["name", "age", "city", "job"],
            "additionalProperties": False,
        },
    }},
)
print(json.loads(resp.choices[0].message.content))
