# HiveGPT API 示例代码

[HiveGPT](https://hivegpt.cn/?utm_source=github&utm_medium=readme&utm_campaign=hivegpt-examples)（hivegpt.cn）是兼容 OpenAI 接口的 AI 模型 API 平台：一个 API Key 即可调用 GPT、Codex、gpt-image-2 等模型，按实际用量计费，出错不扣费。

这个仓库收集了调用 HiveGPT 的可运行示例：Python、Node.js、Go、curl，以及字幕翻译、文档批量总结等实用脚本，和 Codex、OpenCode、Continue 的配置模板。所有代码都在 hivegpt.cn 上实际跑过。

## 三行接入

任何支持 OpenAI 接口的 SDK 或工具，只改两处：

| 配置 | 填什么 |
|---|---|
| Base URL | `https://hivegpt.cn/v1` |
| API Key | 在 [API 密钥](https://hivegpt.cn/keys?utm_source=github&utm_medium=readme&utm_campaign=hivegpt-examples) 页创建，分组选 GPT 类分组 |
| 模型 | `gpt-6.1-sol`、`gpt-5.5`、`gpt-6-luna` 等，以 `GET /v1/models` 返回的为准 |

```python
from openai import OpenAI

client = OpenAI(base_url="https://hivegpt.cn/v1", api_key="sk-你的Key")
resp = client.chat.completions.create(model="gpt-6.1-sol", messages=[{"role": "user", "content": "你好"}])
print(resp.choices[0].message.content)
```

## 快速开始

```bash
git clone https://github.com/DaemonforY/hivegpt-examples.git
cd hivegpt-examples
export HIVEGPT_API_KEY="sk-你的Key"     # Windows CMD：set HIVEGPT_API_KEY=sk-你的Key

pip install -U openai
python python/chat.py
```

## 示例列表

| 文件 | 内容 | 详细教程 |
|---|---|---|
| [python/chat.py](python/chat.py) | 最简单的对话 | [Python 完整示例](https://hivegpt.cn/learn/connect/python.html) |
| [python/stream.py](python/stream.py) | 流式输出 | [Python 完整示例](https://hivegpt.cn/learn/connect/python.html) |
| [python/structured_output.py](python/structured_output.py) | JSON Schema 结构化输出 | [Responses API 教程](https://hivegpt.cn/learn/connect/responses-api.html) |
| [python/function_calling.py](python/function_calling.py) | 函数调用（Function Calling） | [Python 完整示例](https://hivegpt.cn/learn/connect/python.html) |
| [python/vision.py](python/vision.py) | 看图识图 | [看图识图 / 读 PDF](https://hivegpt.cn/learn/connect/vision.html) |
| [python/image_generate.py](python/image_generate.py) | gpt-image-2 生成图片 | [图片 API 教程](https://hivegpt.cn/learn/connect/image-api.html) |
| [python/translate_srt.py](python/translate_srt.py) | 批量翻译 SRT 字幕，可输出双语 | [批量翻译字幕](https://hivegpt.cn/learn/connect/subtitle-translate.html) |
| [python/summarize_docs.py](python/summarize_docs.py) | 批量总结 PDF / Word，导出 CSV | [批量总结文档](https://hivegpt.cn/learn/connect/summarize-docs.html) |
| [node/chat.mjs](node/chat.mjs) | Node.js 对话 + 流式 | [Node.js 完整示例](https://hivegpt.cn/learn/connect/nodejs.html) |
| [go/main.go](go/main.go) | Go（openai-go v3） | [Go 调用 GPT API](https://hivegpt.cn/learn/connect/go.html) |
| [curl/examples.sh](curl/examples.sh) | curl：模型列表、对话、Responses | [用 SDK 调用](https://hivegpt.cn/learn/connect/sdk.html) |
| [configs/codex-config.toml](configs/codex-config.toml) | Codex CLI 配置 | [Codex 接入 HiveGPT](https://hivegpt.cn/learn/codex/hivegpt.html) |
| [configs/opencode.json](configs/opencode.json) | OpenCode 配置 | [OpenCode 配置教程](https://hivegpt.cn/learn/connect/opencode.html) |
| [configs/continue-config.yaml](configs/continue-config.yaml) | Continue 插件配置 | [Continue 配置教程](https://hivegpt.cn/learn/connect/continue.html) |

## 在常用工具里使用

Cherry Studio、Chatbox、沉浸式翻译、Dify、n8n、Obsidian、Zotero、Open WebUI、LobeChat、AstrBot 等工具的填法见 [接入教程](https://hivegpt.cn/learn/connect/?utm_source=github&utm_medium=readme&utm_campaign=hivegpt-examples)。Base URL 末尾要不要加 `/v1`，见 [对照表](https://hivegpt.cn/learn/connect/base-url.html)。

## 常见问题

- **404，提示接口地址少了或多了 /v1**：Base URL 写成 `https://hivegpt.cn/v1`。
- **401**：Key 复制不全或已停用，到 API 密钥页重新复制。
- **提示分组不支持模型**：模型不在你的 Key 所在分组里，用 `/v1/models` 查可用模型。
- 更多报错见 [报错速查](https://hivegpt.cn/learn/connect/errors/)。

模型价格见 [模型广场](https://hivegpt.cn/model-plaza)，各模型怎么选见 [GPT 模型怎么选](https://hivegpt.cn/learn/connect/models.html)。

## License

MIT
