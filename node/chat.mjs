// 对话 + 流式输出：npm i openai，然后 node chat.mjs
import OpenAI from 'openai'

const client = new OpenAI({ baseURL: 'https://hivegpt.cn/v1', apiKey: process.env.HIVEGPT_API_KEY })

const resp = await client.chat.completions.create({
  model: 'gpt-6.1-sol',
  messages: [{ role: 'user', content: '用一句话解释什么是 API' }],
})
console.log(resp.choices[0].message.content)

const stream = await client.chat.completions.create({
  model: 'gpt-6.1-sol',
  messages: [{ role: 'user', content: '写一首关于秋天的四行短诗' }],
  stream: true,
})
for await (const chunk of stream) process.stdout.write(chunk.choices[0]?.delta?.content || '')
process.stdout.write('\n')
