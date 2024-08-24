# 命令行执行：
```
import torch

from transformers import AutoTokenizer, AutoModelForCausalLM

model_name_or_path = "/root/share/new_models/Shanghai_AI_Laboratory/internlm2-chat-1_8b"

tokenizer = AutoTokenizer.from_pretrained(model_name_or_path, trust_remote_code=True, device_map='cuda:0')

model = AutoModelForCausalLM.from_pretrained(model_name_or_path, trust_remote_code=True, torch_dtype=torch.bfloat16, device_map='cuda:0')

model = model.eval()

system_prompt = """You are an AI assistant whose name is InternLM (书生·浦语).

- InternLM (书生·浦语) is a conversational language model that is developed by Shanghai AI Laboratory (上海人工智能实验室). It is designed to be helpful, honest, and harmless.

- InternLM (书生·浦语) can understand and communicate fluently in the language chosen by the user such as English and 中文.

"""

messages = [(system_prompt, '')]

print("=============Welcome to InternLM chatbot, type 'exit' to exit.=============")

while True:

    input_text = input("\nUser  >>> ")

    input_text = input_text.replace(' ', '')

    if input_text == "exit":

        break

    length = 0

    for response, _ in model.stream_chat(tokenizer, input_text, messages):

        if response is not None:

            print(response[length:], flush=True, end="")

            length = len(response)
```

运行结果：
![[Pasted image 20240824230503.png]](imgs/Pasted%20image%2020240824230503.png)

# streamlit 界面显示
- streamlit run /root/demo/Tutorial/tools/streamlit_demo.py --server.address 127.0.0.1 --server.port 6006
- 映射端口
![[Pasted image 20240824230806.png]](imgs/Pasted%20image%2020240824230806.png)
- 打开localhost:6006
![[Pasted image 20240824232333.png]](imgs/Pasted%20image%2020240824232333.png)

# 多模态试用

- 环境不变，使用InternVL2-2B模型
- 执行命令：
		lmdeploy serve gradio /share/new_models/OpenGVLab/InternVL2-2B --cache-max-entry-count 0.1
- 结果如图：
![[Pasted image 20240824232548.png]]

## lmdeploy serve gradio 的参数详解：
usage: lmdeploy serve gradio [-h] [--server-name SERVER_NAME] [--server-port SERVER_PORT]
                             [--share] [--backend {pytorch,turbomind}] [--revision REVISION]
                             [--download-dir DOWNLOAD_DIR] [--meta-instruction META_INSTRUCTION]
                             [--chat-template CHAT_TEMPLATE]
                             [--cap {completion,infilling,chat,python}] [--tp TP]
                             [--model-name MODEL_NAME] [--session-len SESSION_LEN]
                             [--max-batch-size MAX_BATCH_SIZE]
                             [--cache-max-entry-count CACHE_MAX_ENTRY_COUNT]
                             [--cache-block-seq-len CACHE_BLOCK_SEQ_LEN] [--enable-prefix-caching]
                             [--model-format {hf,llama,awq}] [--quant-policy {0,4,8}]
                             [--rope-scaling-factor ROPE_SCALING_FACTOR]
                             model_path_or_server

Serve LLMs with web UI using gradio.
positional arguments:
  model_path_or_server  The path of the deployed model or the tritonserver url or restful api url.
                        for example: - ./workspace - 0.0.0.0:23333 - http://0.0.0.0:23333. Type:
                        str

options:
  -h, --help            show this help message and exit
  --server-name SERVER_NAME
                        The ip address of gradio server. Default: 0.0.0.0. Type: str
  --server-port SERVER_PORT
                        The port of gradio server. Default: 6006. Type: int
  --share               Whether to create a publicly shareable link for the app. Default: False
  --backend {pytorch,turbomind}
                        Set the inference backend. Default: turbomind. Type: str
  --revision REVISION   The specific model version to use. It can be a branch name, a tag name, or
                        a commit id. If unspecified, will use the default version.. Type: str
  --download-dir DOWNLOAD_DIR
                        Directory to download and load the weights, default to the default cache
                        directory of huggingface.. Type: str
  --meta-instruction META_INSTRUCTION
                        System prompt for ChatTemplateConfig. Deprecated. Please use --chat-
                        template instead. Default: None. Type: str
  --chat-template CHAT_TEMPLATE
                        A JSON file or string that specifies the chat template configuration.
                        Please refer to
                        https://lmdeploy.readthedocs.io/en/latest/advance/chat_template.html for
                        the specification. Default: None. Type: str
  --cap {completion,infilling,chat,python}
                        The capability of a model. Deprecated. Please use --chat-template instead.
                        Default: chat. Type: str

PyTorch engine arguments:
  --tp TP               GPU number used in tensor parallelism. Should be 2^n. Default: 1. Type:
                        int
  --model-name MODEL_NAME
                        The name of the to-be-deployed model, such as llama-7b, llama-13b,
                        vicuna-7b and etc. You can run `lmdeploy list` to get the supported model
                        names. Default: None. Type: str
  --session-len SESSION_LEN
                        The max session length of a sequence. Default: None. Type: int
  --max-batch-size MAX_BATCH_SIZE
                        Maximum batch size. Default: 128. Type: int
  --cache-max-entry-count CACHE_MAX_ENTRY_COUNT
                        The percentage of free gpu memory occupied by the k/v cache, excluding
                        weights . Default: 0.8. Type: float
  --cache-block-seq-len CACHE_BLOCK_SEQ_LEN
                        The length of the token sequence in a k/v block. For Turbomind Engine, if
                        the GPU compute capability is >= 8.0, it should be a multiple of 32,
                        otherwise it should be a multiple of 64. For Pytorch Engine, if Lora
                        Adapter is specified, this parameter will be ignored. Default: 64. Type:
                        int
  --enable-prefix-caching
                        Enable cache and match prefix. Default: False

TurboMind engine arguments:
  --tp TP               GPU number used in tensor parallelism. Should be 2^n. Default: 1. Type:
                        int
  --model-name MODEL_NAME
                        The name of the to-be-deployed model, such as llama-7b, llama-13b,
                        vicuna-7b and etc. You can run `lmdeploy list` to get the supported model
                        names. Default: None. Type: str
  --session-len SESSION_LEN
                        The max session length of a sequence. Default: None. Type: int
  --max-batch-size MAX_BATCH_SIZE
                        Maximum batch size. Default: 128. Type: int
  --cache-max-entry-count CACHE_MAX_ENTRY_COUNT
                        The percentage of free gpu memory occupied by the k/v cache, excluding
                        weights . Default: 0.8. Type: float
  --cache-block-seq-len CACHE_BLOCK_SEQ_LEN
                        The length of the token sequence in a k/v block. For Turbomind Engine, if
                        the GPU compute capability is >= 8.0, it should be a multiple of 32,
                        otherwise it should be a multiple of 64. For Pytorch Engine, if Lora
                        Adapter is specified, this parameter will be ignored. Default: 64. Type:
                        int
  --enable-prefix-caching
                        Enable cache and match prefix. Default: False
  --model-format {hf,llama,awq}
                        The format of input model. `hf` meaning `hf_llama`, `llama` meaning
                        `meta_llama`, `awq` meaning the quantized model by awq. Default: None.
                        Type: str
  --quant-policy {0,4,8}
                        Quantize kv or not. 0: no quant; 4: 4bit kv; 8: 8bit kv. Default: 0. Type:
                        int
  --rope-scaling-factor ROPE_SCALING_FACTOR
                        Rope scaling factor. Default: 0.0. Type: float


- 6006端口被占用
更改命令：
lmdeploy serve gradio /share/new_models/OpenGVLab/InternVL2-2B --cache-max-entry-count 0.1 --server-port 6010

- gradio界面显示
- ![[Pasted image 20240824233352.png]](imgs/Pasted%20image%2020240824233352.png)
- 后台显示：
- ![[Pasted image 20240824233431.png]](imgs/Pasted%20image%2020240824233431.png)
## 代码Bug
> 1 点击reset
> 2 上传图片
> 3 进行对话
> 界面和后台均报错：
> 
- 界面错误
![[Pasted image 20240824233849.png]](imgs/Pasted%20image%2020240824233849.png)
后台错误

```
[TM][WARNING] [RejectInvalidRequests] Skipping invalid stop request for id 0, code = 4
[TM][WARNING] [forward] Request failed for 0, code 4
[TM][INFO] [forward] Enqueue requests
[TM][INFO] [forward] Wait for requests to complete ...
[TM][WARNING] [RejectInvalidRequests] Skipping invalid stop request for id 0, code = 4
[TM][WARNING] [forward] Request failed for 0, code 4
2024-08-24 23:38:18,447 - lmdeploy - INFO - prompt: ('这是一幅二维地图，说明地图中建筑物投影的主要形状有哪些，有哪些局部的建筑群呈现了怎样的规则分布。', [<PIL.Image.Image image mode=RGB size=439x525 at 0x7F3FCC06CDC0>])
Traceback (most recent call last):
  File "/root/share/pre_envs/icamp3_demo/lib/python3.10/site-packages/gradio/queueing.py", line 536, in process_events
    response = await route_utils.call_process_api(
  File "/root/share/pre_envs/icamp3_demo/lib/python3.10/site-packages/gradio/route_utils.py", line 276, in call_process_api
    output = await app.get_blocks().process_api(
  File "/root/share/pre_envs/icamp3_demo/lib/python3.10/site-packages/gradio/blocks.py", line 1923, in process_api
    result = await self.call_function(
  File "/root/share/pre_envs/icamp3_demo/lib/python3.10/site-packages/gradio/blocks.py", line 1520, in call_function
    prediction = await utils.async_iteration(iterator)
  File "/root/share/pre_envs/icamp3_demo/lib/python3.10/site-packages/gradio/utils.py", line 663, in async_iteration
    return await iterator.__anext__()
  File "/root/share/pre_envs/icamp3_demo/lib/python3.10/site-packages/gradio/utils.py", line 656, in __anext__
    return await anyio.to_thread.run_sync(
  File "/root/share/pre_envs/icamp3_demo/lib/python3.10/site-packages/anyio/to_thread.py", line 56, in run_sync
    return await get_async_backend().run_sync_in_worker_thread(
  File "/root/share/pre_envs/icamp3_demo/lib/python3.10/site-packages/anyio/_backends/_asyncio.py", line 2177, in run_sync_in_worker_thread
    return await future
  File "/root/share/pre_envs/icamp3_demo/lib/python3.10/site-packages/anyio/_backends/_asyncio.py", line 859, in run
    result = context.run(func, *args)
  File "/root/share/pre_envs/icamp3_demo/lib/python3.10/site-packages/gradio/utils.py", line 639, in run_sync_iterator_async
    return next(iterator)
  File "/root/share/pre_envs/icamp3_demo/lib/python3.10/site-packages/gradio/utils.py", line 801, in gen_wrapper
    response = next(iterator)
  File "/root/share/pre_envs/icamp3_demo/lib/python3.10/site-packages/lmdeploy/serve/gradio/vl.py", line 119, in chat
    inputs = _run_until_complete(
  File "/root/share/pre_envs/icamp3_demo/lib/python3.10/site-packages/lmdeploy/pytorch/engine/request.py", line 78, in _run_until_complete
    return event_loop.run_until_complete(future)
  File "uvloop/loop.pyx", line 1517, in uvloop.loop.Loop.run_until_complete
  File "/root/share/pre_envs/icamp3_demo/lib/python3.10/site-packages/lmdeploy/serve/vl_async_engine.py", line 66, in _get_prompt_input
    features = await self.vl_encoder.async_infer(images)
  File "/root/share/pre_envs/icamp3_demo/lib/python3.10/site-packages/lmdeploy/vl/engine.py", line 171, in async_infer
    self.req_que.put_nowait(item)
  File "/root/share/pre_envs/icamp3_demo/lib/python3.10/site-packages/lmdeploy/vl/engine.py", line 124, in req_que
    raise RuntimeError('Current event loop is different from'
RuntimeError: Current event loop is different from the one bound to loop task!
```