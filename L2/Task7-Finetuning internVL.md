## 环境准备
- conda activate xtuner0.1.9
- 软连接模型
	- ln -s /root/share/new_models/OpenGVLab/InternVL2-2B /root/model/InternVL2
- 可能需要的依赖
	- apt install libaio-dev
	- pip install lmdeploy==0.5.3
	- pip install datasets matplotlib Pillow timm
## 微调前

- 准备代码
```
from lmdeploy import pipeline

from lmdeploy.vl import load_image

  

pipe = pipeline('/root/model/InternVL2/InternVL2-2B')

  

image = load_image('/root/L1/Task4/test.jpg')

response = pipe(('这是一张只包含居民地建筑物的二维地图图像，根据这张图像，分析其中建筑物的形状和分布特征，统计建筑物的数量，并给出建筑物分布的规律。', image))

print(response.text)
```
- python tuning_VL.py
- ![[Pasted image 20240827211931.png]](imgs/Pasted%20image%2020240827211931.png)
- ## 微调cfg
```
path = '/root/model/InternVL2/InternVL2-2B'

  

# Data

data_root = '/root/L1/Task4/'

data_path = data_root + 'data.json'

image_folder = data_root

prompt_template = PROMPT_TEMPLATE.internlm2_chat

max_length = 6656

  

# Scheduler & Optimizer

batch_size = 4  # per_device

accumulative_counts = 4

dataloader_num_workers = 4

max_epochs = 10

optim_type = AdamW

# official 1024 -> 4e-5

lr = 2e-5

betas = (0.9, 0.999)

weight_decay = 0.05

max_norm = 1  # grad clip

warmup_ratio = 0.03

  

# Save

save_steps = 1000

save_total_limit = 5  # Maximum checkpoints to keep (-1 means unlimited)

  

#######################################################################

#            PART 2  Model & Tokenizer & Image Processor              #

#######################################################################

model = dict(

    type=InternVL_V1_5,

    model_path=path,

    freeze_llm=True,

    freeze_visual_encoder=True,

    quantization_llm=True,  # or False

    quantization_vit=False,  # or True and uncomment visual_encoder_lora

    # comment the following lines if you don't want to use Lora in llm

    llm_lora=dict(

        type=LoraConfig,

        r=128,

        lora_alpha=256,

        lora_dropout=0.05,

        target_modules=None,

        task_type='CAUSAL_LM'),

    # uncomment the following lines if you don't want to use Lora in visual encoder # noqa

    # visual_encoder_lora=dict(

    #     type=LoraConfig, r=64, lora_alpha=16, lora_dropout=0.05,

    #     target_modules=['attn.qkv', 'attn.proj', 'mlp.fc1', 'mlp.fc2'])

)

  

#######################################################################

#                      PART 3  Dataset & Dataloader                   #

#######################################################################

llava_dataset = dict(

    type=InternVL_V1_5_Dataset,

    model_path=path,

    data_paths=data_path,

    image_folders=image_folder,

    template=prompt_template,

    max_length=max_length)

  

train_dataloader = dict(

    batch_size=batch_size,

    num_workers=dataloader_num_workers,

    dataset=llava_dataset,

    sampler=dict(

        type=LengthGroupedSampler,

        length_property='modality_length',

        per_device_batch_size=batch_size * accumulative_counts),

    collate_fn=dict(type=default_collate_fn))

  

#######################################################################

#                    PART 4  Scheduler & Optimizer                    #

#######################################################################

# optimizer

optim_wrapper = dict(

    type=AmpOptimWrapper,

    optimizer=dict(

        type=optim_type, lr=lr, betas=betas, weight_decay=weight_decay),

    clip_grad=dict(max_norm=max_norm, error_if_nonfinite=False),

    accumulative_counts=accumulative_counts,

    loss_scale='dynamic',

    dtype='float16')

  

# learning policy

# More information: https://github.com/open-mmlab/mmengine/blob/main/docs/en/tutorials/param_scheduler.md  # noqa: E501

param_scheduler = [

    dict(

        type=LinearLR,

        start_factor=1e-5,

        by_epoch=True,

        begin=0,

        end=warmup_ratio * max_epochs,

        convert_to_iter_based=True),

    dict(

        type=CosineAnnealingLR,

        eta_min=0.0,

        by_epoch=True,

        begin=warmup_ratio * max_epochs,

        end=max_epochs,

        convert_to_iter_based=True)

]

  

# train, val, test setting

train_cfg = dict(type=TrainLoop, max_epochs=max_epochs)

  

#######################################################################

#                           PART 5  Runtime                           #

#######################################################################

# Log the dialogue periodically during the training process, optional

tokenizer = dict(

    type=AutoTokenizer.from_pretrained,

    pretrained_model_name_or_path=path,

    trust_remote_code=True)

  

custom_hooks = [

    dict(type=DatasetInfoHook, tokenizer=tokenizer),

]

  

# configure default hooks

default_hooks = dict(

    # record the time of every iteration.

    timer=dict(type=IterTimerHook),

    # print log every 10 iterations.

    logger=dict(type=LoggerHook, log_metric_by_epoch=False, interval=10),

    # enable the parameter scheduler.

    param_scheduler=dict(type=ParamSchedulerHook),

    # save checkpoint per `save_steps`.

    checkpoint=dict(

        type=CheckpointHook,

        save_optimizer=False,

        by_epoch=False,

        interval=save_steps,

        max_keep_ckpts=save_total_limit),

    # set sampler seed in distributed evrionment.

    sampler_seed=dict(type=DistSamplerSeedHook),

)

  

# configure environment

env_cfg = dict(

    # whether to enable cudnn benchmark

    cudnn_benchmark=False,

    # set multi process parameters

    mp_cfg=dict(mp_start_method='fork', opencv_num_threads=0),

    # set distributed parameters

    dist_cfg=dict(backend='nccl'),

)

  

# set visualizer

visualizer = None

  

# set log level

log_level = 'INFO'

  

# load from which checkpoint

load_from = None

  

# whether to resume training from the loaded checkpoint

resume = False

  

# Defaults to use random seed and disable `deterministic`

randomness = dict(seed=None, deterministic=False)

  

# set log processor

log_processor = dict(by_epoch=False)
```

- 配置不存在
- 发现xtuner在task5中安装的是0.1.21，而这里需要0.1.23
- 因此 pip uninstall 卸载后 重新安装
- pip install -e '.[deepspeed]' 
- 这里有个警告，测试不影响
- DEPRECATION: Legacy editable install of xtuner[deepspeed]==0.1.23 from file:///root/L2/Task4/XTuner (setup.py develop) is deprecated. pip 25.0 will enforce this behaviour change. A possible replacement is to add a pyproject.toml or enable --use-pep517, and use setuptools >= 64. If the resulting installation is not behaving as expected, try using --config-settings editable_mode=compat. Please consult the setuptools documentation for more information. Discussion can be found at https://github.com/pypa/pip/issues/11457
- 
- NPROC_PER_NODE=1 xtuner train /root/L2/Task4/XTuner/xtuner/configs/internvl/v2/internvl_v2_internlm2_2b_qlora_finetune.py  --work-dir /root/L2/Task4/work_dir/internvl_v2_internlm2_2b_qlora_finetune  --deepspeed deepspeed_zero1
- 
```text
# cd /root/L2/Task4/Xtuner 不需要这句

python3 /root/L2/Task4/XTuner/xtuner/configs/internvl/v1_5/convert_to_official.py /root/L2/Task4/XTuner/xtuner/configs/internvl/v2/internvl_v2_internlm2_2b_qlora_finetune.py /root/L2/Task4/work_dir/internvl_v2_internlm2_2b_qlora_finetune/iter_4000.pth /root/model/InternVL2/internvl_v2_internlm2_2b_qlora_finetune
```

微调后：

![[Pasted image 20240828091602.png]](imgs/Pasted%20image%2020240828091602.png)

## 基于lmdeploy serve 启动api服务
```
lmdeploy serve gradio /root/model/InternVL2/internvl_v2_internlm2_2b_qlora_finetune_it7000 --cache-max-entry-count 0.2 --server-port 23333 

lmdeploy serve api_server /root/model/InternVL2/internvl_v2_internlm2_2b_qlora_finetune_it7000 --cache-max-entry-count 0.2 --server-port 23333 

```
