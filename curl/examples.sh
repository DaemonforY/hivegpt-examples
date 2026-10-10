#!/usr/bin/env bash
# 先 export HIVEGPT_API_KEY=sk-你的Key
set -e

# 查看你的 Key 能用哪些模型
curl -s https://hivegpt.cn/v1/models -H "Authorization: Bearer $HIVEGPT_API_KEY"
echo

# 对话
curl -s https://hivegpt.cn/v1/chat/completions \
  -H "Authorization: Bearer $HIVEGPT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"gpt-6.1-sol","messages":[{"role":"user","content":"用一句话解释什么是 API"}]}'
echo

# Responses 接口
curl -s https://hivegpt.cn/v1/responses \
  -H "Authorization: Bearer $HIVEGPT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"gpt-6.1-sol","input":"用一句话解释什么是 API"}'
echo
