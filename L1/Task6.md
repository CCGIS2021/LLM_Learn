## 环境配置

- 暂时继续使用xtuner的环境
- 软件安装
```
cd /root
git clone -b 0.2.4 https://github.com/open-compass/opencompass
cd opencompass
pip install -e .
```

更新下cmake和安装依赖：
```
apt-get update
apt-get install cmake
pip install -r requirements.txt
pip install protobuf
```

## 解包评测数据集
```
cp /share/temp/datasets/OpenCompassData-core-20231110.zip /root/opencompass/
unzip OpenCompassData-core-20231110.zip
```

## 编辑测试代码
- opencompass文件夹下configs/models/hf_internlm/的`hf_internlm2_chat_1_8b.py`

```
from opencompass.models import HuggingFaceCausalLM


models = [
    dict(
        type=HuggingFaceCausalLM,
        abbr='internlm2-1.8b-hf',
        path="/share/new_models/Shanghai_AI_Laboratory/internlm2-chat-1_8b",
        tokenizer_path='/share/new_models/Shanghai_AI_Laboratory/internlm2-chat-1_8b',
        model_kwargs=dict(
            trust_remote_code=True,
            device_map='auto',
        ),
        tokenizer_kwargs=dict(
            padding_side='left',
            truncation_side='left',
            use_fast=False,
            trust_remote_code=True,
        ),
        max_out_len=100,
        min_out_len=1,
        max_seq_len=2048,
        batch_size=8,
        run_cfg=dict(num_gpus=1, num_procs=1),
    )
]
```

## 启动测试
```
#环境变量配置
export MKL_SERVICE_FORCE_INTEL=1
#或
export MKL_THREADING_LAYER=GNU
python run.py --datasets ceval_gen --models hf_internlm2_chat_1_8b --debug
```
评测结果：
![[Pasted image 20240827104803.png]](imgs/Pasted%20image%2020240827104803.png)

![[Pasted image 20240827160849.png]](imgs/Pasted%20image%2020240827160849.png)
![[Pasted image 20240827173443.png]](imgs/Pasted%20image%2020240827173443.png)