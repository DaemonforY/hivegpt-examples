"""用 gpt-image-2 生成图片并保存。按张计费，价格见 https://hivegpt.cn/model-plaza"""
import base64, os
from openai import OpenAI

client = OpenAI(base_url="https://hivegpt.cn/v1", api_key=os.environ["HIVEGPT_API_KEY"], timeout=600)

img = client.images.generate(
    model="gpt-image-2",
    prompt="一只在图书馆看书的橘猫，水彩风格",
    size="1024x1024",
)
with open("cat.png", "wb") as f:
    f.write(base64.b64decode(img.data[0].b64_json))
print("已保存 cat.png，尺寸", img.size)
