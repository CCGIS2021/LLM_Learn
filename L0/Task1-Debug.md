## [Leetcode 383](https://leetcode.cn/problems/ransom-note/description/)
![[Pasted image 20241030111413.png]](imgs/Pasted%20image%2020241030111413.png)

## debug
开始调试：

![[Pasted image 20241030111816.png]](imgs/Pasted%20image%2020241030111816.png)
单步调试，发现返回值为：
response.choices[0].message.content

'```json\n{\n "model_name": "书生浦语InternLM2.5",\n "developer": "上海人工智能实验室",\n "parameter_versions": [1.8B, 7B, 20B],\n "context_length": "1M"\n}\n```'

res_json = json.loads(res)
会报错，需要对res进行处理。

修改代码后运行：
![[Pasted image 20241030113112.png]](imgs/Pasted%20image%2020241030113112.png)