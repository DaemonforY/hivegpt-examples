// 对话示例：go run .
package main

import (
	"context"
	"fmt"
	"os"

	"github.com/openai/openai-go/v3"
	"github.com/openai/openai-go/v3/option"
)

func main() {
	client := openai.NewClient(
		option.WithBaseURL("https://hivegpt.cn/v1"),
		option.WithAPIKey(os.Getenv("HIVEGPT_API_KEY")),
	)
	resp, err := client.Chat.Completions.New(context.Background(), openai.ChatCompletionNewParams{
		Model:    "gpt-6.1-sol",
		Messages: []openai.ChatCompletionMessageParamUnion{openai.UserMessage("用一句话解释什么是 API")},
	})
	if err != nil {
		fmt.Println("请求失败：", err)
		os.Exit(1)
	}
	fmt.Println(resp.Choices[0].Message.Content)
}
