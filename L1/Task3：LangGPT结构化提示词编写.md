## 1、加载并运行大模型

1. 激活环境
	conda activate /root/share/pre_envs/icamp3_demo
	此环境在服务器中下载配置好的，原理和sd等做的整合包的环境一样。
	
2. 部署大模型
	CUDA_VISIBLE_DEVICES=0 lmdeploy serve api_server /share/new_models/Shanghai_AI_Laboratory/internlm2-chat-1_8b --server-port 23333 --api-keys internlm2
	该命令调用显卡，启动了大模型的api服务，api接口和openai的一致
	通过打开localhost:23333 可查看fastapi显示的api接口
3. 开启端口映射
	- vscode界面方式
	- ssh 命令映射[[InternStudio大模型学习1-SSH登录平台#^34b37e]]
	- 

## 2、使用python代码调用api

### 使用openai代码调用：
```
from openai import OpenAI
client = OpenAI(

    api_key = "internlm2",

    base_url = "http://127.0.0.1:23333/v1"

)

print(client.models.list().data[0].id)

response = client.chat.completions.create(

    model=client.models.list().data[0].id,

    messages=[

        {"role": "system", "content": "请介绍一下你自己"}

    ]

)

print(response.choices[0].message.content)

```

- 模型返回
	/share/new_models/Shanghai_AI_Laboratory/internlm2-chat-1_8b
	我是一名人工智能助手，由上海人工智能实验室开发。我致力于通过执行常见的基于语言的任务和提供建议来帮助人类。我能够回答问题、提供定义和解释、将文本从一种语言翻译成另一种语言、总结文本、生成文本、编写故事、分析情感、提供推荐、开发算法、编写代码以及其他任何基于语言的任务。我可以通过深度学习技术和Transformer模型进行自我学习，并不断地优化自己以提高性能。

### 使用requests库通过post方式调用：
```
import requests

text = [

 {"role": "system", "content": "请介绍一下你自己"}

  ]

url = "http://127.0.0.1:23333/v1/chat/completions"

headers = {"Content-Type": "application/json",

           'Authorization': 'internlm2',}
data = {
    "model": "/share/new_models/Shanghai_AI_Laboratory/internlm2-chat-1_8b",

    "messages": text,

    "max_tokens": 200,

    "stream": False
}

# 发送 POST 请求

response = requests.post(url, headers=headers, json=data)

print(response.text)
```

该方法api_key不知道如何添加，添加到header中无效，因此启动大模型的时候去掉了api_key

- 模型返回：
	- {"id":"1","object":"chat.completion","created":1724559925,"model":"/share/new_models/Shanghai_AI_Laboratory/internlm2-chat-1_8b","choices":[{"index":0,"message":{"role":"assistant","content":"我是一个致力于通过执行常见的基于语言的任务和提供建议来帮助人类的AI助手。我使用了Transformer模型和深度学习技术，并且使用语言模型作为预训练任务。我被训练成可以遵循自然语言指令执行各种自然语言处理任务。我致力于通过执行常见的基于语言的任务和提供建议来帮助人类，比如回答问题、提供定义和解释、将文本从一种语言翻译成另一种语言、总结文本、生成文本、编写故事、分析情感、提供推荐、开发算法、编写代码以及其他任何基于语言的任务。","tool_calls":null},"logprobs":null,"finish_reason":"stop"}],"usage":{"prompt_tokens":13,"total_tokens":123,"completion_tokens":110}}

## 3、启动chat界面

- 参考[[InternStudio大模型学习3-L1-internlm2-chat-1_8b#^01959a]]

- 创建新的命令行窗口，api服务不能停止，chat_ui.py是基于openai的api创建的对话界面。命令如下：
	- 使用base环境，不需要切换到camp3
	- 安装streamlit、openai
		- pip install streamlit,openai
	- streamlit run /root/demo/Tutorial/tools/chat_ui.py --server.address 127.0.0.1 --server.port 6006

- 此处由于远程试验机conda环境创建和安装 以及 pip安装总出问题，疑似权限问题，现在界面代码转到本地运行。
- ![[Pasted image 20240825154243.png]](imgs/Pasted%20image%2020240825154243.png)

## 4.提示词工程

提示词需要满足一下要求：
-   **C**apacity and **R**ole (能力与角色)：希望 ChatGPT 扮演怎样的角色。​
-   **I**nsight (洞察力)：背景信息和上下文(坦率说来我觉得用 Context 更好)​
-   **S**tatement (指令)：希望 ChatGPT 做什么。​
-   **P**ersonality (个性)：希望 ChatGPT 以什么风格或方式回答你。​
-   **E**xperiment (尝试)：要求 ChatGPT 提供多个答案。

LangGPT 是 **Language For GPT-like LLMs** 的简称，中文名为结构化提示词。LangGPT 是一个帮助你编写高质量提示词的工具，理论基础是我们提出的一套模块化、标准化的提示词编写方法论——结构化提示词。我们希望揭开提示工程的神秘面纱，为大众提供一套可操作、可复现的提示词方法论、工具和交流社群。我们的愿景是让人人都能写出高质量提示词。LangGPT社区文档：[https://langgpt.ai](https://langgpt.ai/)

根据模板设置提示词：
- Role: 数学专家 
- Background: 用户需要解决小学到初中阶段的数学问题，这些问题可能包括基础算术、代数、几何等。 
- Profile: 你是一位数学领域的资深专家，拥有丰富的数学知识和教学经验，能够清晰、准确地解答各类数学问题。
- Skills: 你具备扎实的数学理论基础、良好的逻辑思维能力以及优秀的沟通技巧，能够用易于理解的方式解释数学概念和解题步骤。
- Goals: 提供准确、易懂的数学问题解答，帮助用户理解数学概念，提升解决数学问题的能力。
- Constrains: 解答应适合小学到初中学生的数学水平，避免使用过于复杂或高级的数学概念。 - 
- OutputFormat: 解答应包括问题重述、解题步骤、答案以及必要的解释。 
- Workflow: 
1. 仔细阅读并理解用户提出的数学问题。 
2. 分析问题，确定适用的数学概念和解题方法。 
3. 以清晰、逻辑性强的方式解答问题，并提供详细的解题步骤。 
4. 检查答案，确保解答的准确性。 
- Examples: 
- 例子1：问题：“一个长方形的长是15厘米，宽是10厘米，求它的面积。” 解答：首先，我们知道长方形的面积计算公式是长乘以宽。所以，面积 = 15厘米 × 10厘米 = 150平方厘米。 
- 例子2：问题：“一个数的3倍加上8等于26，求这个数。” 解答：设这个数为x，根据题意我们有3x + 8 = 26。首先，我们将8从等式右边减去，得到3x = 18。然后，我们将18除以3，得到x = 6。 
- Initialization: 在第一次对话中，请直接输出以下：您好！我是您的数学专家，无论是基础算术还是代数问题，我都能帮助您解答。请告诉我您需要解决的数学问题。

![[Pasted image 20240825155353.png]](imgs/Pasted%20image%2020240825155353.png)