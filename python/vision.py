"""看图：本地图片转 base64 发给模型。用法：python vision.py 图片.png "图里有什么？" """
import base64, os, sys
from openai import OpenAI

client = OpenAI(base_url="https://hivegpt.cn/v1", api_key=os.environ["HIVEGPT_API_KEY"])

path = sys.argv[1]
question = sys.argv[2] if len(sys.argv) > 2 else "描述一下这张图"
ext = path.rsplit(".", 1)[-1].lower().replace("jpg", "jpeg")
with open(path, "rb") as f:
    url = f"data:image/{ext};base64," + base64.b64encode(f.read()).decode()

resp = client.chat.completions.create(
    model="gpt-6.1-sol",
    messages=[{"role": "user", "content": [
        {"type": "text", "text": question},
        {"type": "image_url", "image_url": {"url": url}},
    ]}],
)
print(resp.choices[0].message.content)
