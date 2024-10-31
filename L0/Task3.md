# 激活环境
conda activate /root/share/pre_envs/pytorch2.1.2cu12.1

# 安装 modelscope
pip install modelscope -t /root/env/maas
pip install numpy==1.26.0  -t /root/env/maas
pip install packaging -t /root/env/maas

export PATH=$PATH:/root/env/maas/bin
export PYTHONPATH=/root/env/maas:$PYTHONPATH

mkdir -p /root/ms_demo

modelscope download \
    --model 'Shanghai_AI_Laboratory/internlm2_5-7b-chat' \
    tokenizer.json config.json model.safetensors.index.json \
    --local_dir '/root/ms_demo'

modelscope download \
    --model 'Shanghai_AI_Laboratory/internlm2_5-1_8b-chat' \
    tokenizer.json config.json model.safetensors.index.json \
    --local_dir '/root/ms_demo'

![[Pasted image 20241031100250.png]](imgs/Pasted%20image%2020241031100250.png)
