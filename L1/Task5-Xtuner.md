## 环境配置
- 激活预设虚拟环境
	- conda activate share/pre_envs/icamp3_rag
- 下载并安装Xtuner
	- git clone -b v0.1.21  https://github.com/InternLM/XTuner /root/InternLM/code/XTuner
	- pip install -e '.[deepspeed]' -i https://mirrors.aliyun.com/pypi/simple/
- 验证环境
	- xtuner version
	- xtuner help

## 运行原始模型
- 创建文件夹：
	- cd Xtuner
	- mkdir -p Shanghai_AI_Laboratory
- 软链接模型文件
	- ln -s /root/share/new_models/Shanghai_AI_Laboratory/internlm2-chat-1_8b Shanghai_AI_Laboratory/internlm2-chat-1_8b
- 基于streamlit运行原始模型
	- streamlit run /root/InternLM/Tutorial/tools/xtuner_streamlit_demo.py
- ![[Pasted image 20240827094045.png]](imgs/Pasted%20image%2020240827094045.png)
- 
- ![[Pasted image 20240826205626.png]](imgs/Pasted%20image%2020240826205626.png)
## 安装xtuner时环境崩溃了
表现为：
- 无法conda create 提示环境已存在，但conda info --envs没有该环境
- 云盘存储接近满了
- studio-codna这个是坑，拷贝环境接近2个小时未完成环境拷贝。
解决办法：
- 终端 ssh链接
- rm -rf /root 需要等大约半小时
- 网页重启开发机，需要初始化时间很长，大概半小时
- 安装tmux
- 环境初始化完成

-  重启后可以创建conda环境了
- 
## 继续准备微调数据集
- 运行xtuner_generate_assistant.py，制造假微调对话
- ![[Pasted image 20240827091853.png]]
- 拷贝配置文件
	- xtuner copy-cfg internlm2_chat_1_8b_qlora_alpaca_e3 .
	- 修改相应配置
	- 或直接拷贝修改后的
	- cp /root/InternLM/Tutorial/configs/internlm2_chat_1_8b_qlora_alpaca_e3_copy.py ./
	- 这里可以将配置文件中batchsize修改为3 maxlength 修改为512。
- 启动微调
	- xtuner train ./internlm2_chat_1_8b_qlora_alpaca_e3_copy.py
- 转换lora权重格式到hf:
	- pth_file=`ls -t ./work_dirs/internlm2_chat_1_8b_qlora_alpaca_e3_copy/*.pth | head -n 1`
	- export MKL_SERVICE_FORCE_INTEL=1
	- export MKL_THREADING_LAYER=GNU
	- xtuner convert pth_to_hf ./internlm2_chat_1_8b_qlora_alpaca_e3_copy.py ${pth_file} ./hf
- ![[Pasted image 20240827145244.png]](imgs/Pasted%20image%2020240827145244.png)
- 合并权重到原权重
	- export MKL_SERVICE_FORCE_INTEL=1
	- export MKL_THREADING_LAYER=GNU
	- xtuner convert merge ./Shanghai_AI_Laboratory/internlm2-chat-1_8b ./hf ./merged --max-shard-size 4GB
- ![[Pasted image 20240827150533.png]](imgs/Pasted%20image%2020240827150533.png)
- 运行微调后的结果：
	- streamlit run ./Tutorial/tools/xtuner_streamlit_demo.py
	- （需要修改文件中权重的位置，L18 :
		model_name_or_path = "/root/InternLM/XTuner/merged"）
- ![[Pasted image 20240827150924.png]](imgs/Pasted%20image%2020240827150924.png)
- ![[Pasted image 20240827150949.png]](imgs/Pasted%20image%20240827150949.png)
- 