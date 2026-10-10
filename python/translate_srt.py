"""把 SRT 字幕翻译成中文（或其他语言），保留编号和时间轴。

用法：
    python translate_srt.py input.srt                 # 输出 input.zh.srt（只有译文）
    python translate_srt.py input.srt --bilingual     # 双语：译文在上，原文在下
    python translate_srt.py input.srt --to 日语 --model gpt-6.1-sol
"""
import argparse, json, os, re, sys, time
from concurrent.futures import ThreadPoolExecutor
from openai import OpenAI

client = OpenAI(base_url="https://hivegpt.cn/v1", api_key=os.environ["HIVEGPT_API_KEY"], timeout=300)

BATCH = 30        # 每次请求翻译多少条字幕
WORKERS = 4       # 同时发几个请求；遇到 429 就调小
EFFORT = "low"    # 推理强度：none / low / medium …，模型不支持 none 时用 low
usage = [0, 0]    # 累计输入、输出 token


def parse_srt(text):
    """返回 [(编号, 时间轴, 字幕文本)]。"""
    blocks = re.split(r"\n\s*\n", text.replace("\r\n", "\n").strip())
    items = []
    for b in blocks:
        lines = b.strip().split("\n")
        if len(lines) >= 2 and "-->" in lines[1]:
            items.append((lines[0].strip(), lines[1].strip(), "\n".join(lines[2:]).strip()))
    return items


SCHEMA = {
    "type": "object",
    "properties": {"items": {"type": "array", "items": {
        "type": "object",
        "properties": {"id": {"type": "integer"}, "text": {"type": "string"}},
        "required": ["id", "text"], "additionalProperties": False,
    }}},
    "required": ["items"], "additionalProperties": False,
}


def translate_batch(batch, target, model, context):
    """batch: [(序号, 原文)]，返回 {序号: 译文}。编号对不上就重试。"""
    payload = [{"id": i, "text": t} for i, t in batch]
    for attempt in range(4):
        try:
            resp = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": (
                        f"你是专业的字幕译者。把每条字幕翻译成{target}，口语化、简洁，适合在屏幕上读。"
                        "每条单独翻译，不要合并或拆分，id 原样返回；人名、品牌名保留原文。"
                        + (f"\n视频背景：{context}" if context else ""))},
                    {"role": "user", "content": json.dumps(payload, ensure_ascii=False)},
                ],
                response_format={"type": "json_schema", "json_schema": {"name": "subs", "strict": True, "schema": SCHEMA}},
                reasoning_effort=EFFORT,  # 翻译不需要深度推理，调低了快很多也省钱
            )
            usage[0] += resp.usage.prompt_tokens
            usage[1] += resp.usage.completion_tokens
            out = {it["id"]: it["text"].strip() for it in json.loads(resp.choices[0].message.content)["items"]}
            if set(out) == {i for i, _ in batch}:
                return out
            print(f"  第 {batch[0][0]} 条起的一批：返回条数不对，重试", file=sys.stderr)
        except Exception as e:  # 429、超时等：等一会儿再试
            print(f"  第 {batch[0][0]} 条起的一批出错：{e}，重试", file=sys.stderr)
        time.sleep(2 ** attempt)
    raise RuntimeError(f"第 {batch[0][0]} 条起的一批翻译失败")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("srt")
    ap.add_argument("--to", default="简体中文")
    ap.add_argument("--model", default="gpt-6-luna")
    ap.add_argument("--bilingual", action="store_true")
    ap.add_argument("--context", default="", help="一句话说明视频内容，帮助统一术语")
    args = ap.parse_args()

    items = parse_srt(open(args.srt, encoding="utf-8-sig").read())
    texts = [(n, t) for n, (_, _, t) in enumerate(items)]
    batches = [texts[i:i + BATCH] for i in range(0, len(texts), BATCH)]
    print(f"{len(items)} 条字幕，分 {len(batches)} 批翻译…", file=sys.stderr)

    translated = {}
    with ThreadPoolExecutor(WORKERS) as pool:
        for part in pool.map(lambda b: translate_batch(b, args.to, args.model, args.context), batches):
            translated.update(part)

    out_path = re.sub(r"\.srt$", "", args.srt) + (".bilingual.srt" if args.bilingual else ".zh.srt")
    with open(out_path, "w", encoding="utf-8") as f:
        for n, (idx, timing, text) in enumerate(items):
            body = translated[n] + ("\n" + text if args.bilingual else "")
            f.write(f"{idx}\n{timing}\n{body}\n\n")
    print(f"完成：{out_path}（输入 {usage[0]} token，输出 {usage[1]} token）", file=sys.stderr)


if __name__ == "__main__":
    main()
