## 未量化运行
```
lmdeploy chat /root/models/internlm2_5-7b-chat
```

![[Pasted image 20240829092329.png]](imgs/Pasted%20image%2020240829092329.png)

## 资源占用

![[Pasted image 20240829092248.png]](imgs/Pasted%20image%2020240829092248.png)

# 显存缓存占用设置

### **设置最大kv cache缓存大小**

kv cache是一种缓存技术，通过存储键值对的形式来复用计算结果，以达到提高性能和降低内存消耗的目的。在大规模训练和推理中，kv cache可以显著减少重复计算量，从而提升模型的推理速度。理想情况下，kv cache全部存储于显存，以加快访存速度。

模型在运行时，占用的显存可大致分为三部分：模型参数本身占用的显存、kv cache占用的显存，以及中间运算结果占用的显存。LMDeploy的kv cache管理器可以通过设置`--cache-max-entry-count`参数，控制kv缓存占用**剩余显存**的最大比例。默认的比例为0.8。

![[Pasted image 20240829092539.png]](imgs/Pasted%20image%2020240829092539.png)


## 量化命令
```

lmdeploy lite auto_awq \
   /root/model/internlm2_5-1_8b \
  --calib-dataset 'ptb' \
  --calib-samples 128 \
  --calib-seqlen 2048 \
  --w-bits 4 \
  --w-group-size 128 \
  --batch-size 1 \
  --search-scale False \
  --work-dir /root/model/internlm2_5-1_8b-w4a16-4bit
```
参数含义：
1.  `lmdeploy lite auto_awq`: `lite`这是LMDeploy的命令，用于启动量化过程，而`auto_awq`代表自动权重量化（auto-weight-quantization）。
2.  `/root/models/internlm2_5-7b`: 模型文件的路径。
3.  `--calib-dataset 'ptb'`: 这个参数指定了一个校准数据集，这里使用的是’ptb’（Penn Treebank，一个常用的语言模型数据集）。
4.  `--calib-samples 128`: 这指定了用于校准的样本数量—128个样本
5.  `--calib-seqlen 2048`: 这指定了校准过程中使用的序列长度—2048
6.  `--w-bits 4`: 这表示权重（weights）的位数将被量化为4位。
7.  `--work-dir /root/models/internlm2_5-7b-w4a16-4bit`: 这是工作目录的路径，用于存储量化后的模型和中间结果。
运行耗时：
![[Pasted image 20240829093612.png]](imgs/Pasted%20image%2020240829093612.png)
等待两个小时后：
![[Pasted image 20240829104647.png]](imgs/Pasted%20image%2020240829104647.png)

运行量化后的模型：
```
lmdeploy chat /root/model/internlm2_5-1_8b-w4a16-4bit/ --model-format awq
```

![[Pasted image 20240829104623.png]](imgs/Pasted%20image%2020240829104623.png)

![[Pasted image 20240829105218.png]](imgs/Pasted%20image%2020240829105218.png)

###  权重量化 （W4A16 量化）+ 缓存减小（Kv cache） + 缓存量化(kv 量化)
- 权重量化 显存占用减少为原来的25%
- 缓存设置默认0.8 -> 0.4
- 缓存量化 显存占用较少为原来的25%
```
lmdeploy chat \
    /root/model/internlm2_5-1_8b-w4a16-4bit/ \
    --model-format awq \
    --quant-policy 4 \
    --cache-max-entry-count 0.4\
```

### VL模型量化命令
```
conda activate lmdeploy
lmdeploy lite auto_awq \
   /root/models/InternVL2-26B \
  --calib-dataset 'ptb' \
  --calib-samples 128 \
  --calib-seqlen 2048 \
  --w-bits 4 \
  --w-group-size 128 \
  --batch-size 1 \
  --search-scale False \
  --work-dir /root/models/InternVL2-26B-w4a16-4bit
```