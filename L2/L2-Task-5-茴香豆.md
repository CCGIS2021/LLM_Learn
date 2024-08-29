[**茴香豆**](https://github.com/InternLM/HuixiangDou/) 是由书生·浦语团队开发的一款开源、专门针对国内企业级使用场景设计并优化的知识问答工具。在基础 RAG 课程中我们了解到，RAG 可以有效的帮助提高 LLM 知识检索的相关性、实时性，同时避免 LLM 训练带来的巨大成本。在实际的生产和生活环境需求，对 RAG 系统的开发、部署和调优的挑战更大，如需要解决群应答、能够无关问题拒答、多渠道应答、更高的安全性挑战。因此，根据大量国内用户的实际需求，总结出了**三阶段Pipeline**的茴香豆知识问答助手架构，帮助企业级用户可以快速上手安装部署。

**茴香豆特点**：

-   三阶段 Pipeline （前处理、拒答、响应），提高相应准确率和安全性
    
-   打通微信和飞书群聊天，适合国内知识问答场景
    
-   支持各种硬件配置安装，安装部署限制条件少
    
-   适配性强，兼容多个 LLM 和 API
    
-   傻瓜操作，安装和配置方便

## 环境配置
- 使用base环境
		git clone https://github.com/internlm/huixiangdou && cd huixiangdou
		git checkout 79fa810
		pip install BCEmbedding==0.1.5 cmake==3.30.2 lit==18.1.8 sentencepiece==0.2.0 protobuf==5.27.3 accelerate==0.33.0
		# 这里BCEmbedding版本号是0.1.5不是教程中的0.15
		pip install -r requirements.txt
		# 此处faiss-gpu安装不上，单独安装了
		conda install -c conda-forge faiss-gpu
- 链接模型
		ln -s /root/share/new_models/maidalun1020/bce-embedding-base_v1 /root/model/bce-embedding-base_v1
		ln -s /root/share/new_models/maidalun1020/bce-reranker-base_v1 /root/model/bce-reranker-base_v1
		ln -s /root/share/new_models/Shanghai_AI_Laboratory/internlm2-chat-7b /root/model/internlm2-chat-7b
此时model下：
![[Pasted image 20240829153743.png]](imgs/Pasted%20image%2020240829153743.png)

## 修改茴香豆配置文件
/root/huixiangdou/config.ini
L9:embedding_model_path = "/root/model/bce-embedding-base_v1"
L15:reranker_model_path = "/root/model/bce-reranker-base_v1"
L43:local_llm_path = "/root/model/internlm2-chat-7b"

## 创建知识库索引
此处放置知识库：
	cd /root/huixiangdou && mkdir repodir
此处创建索引：
	mkdir workdir
	python3 -m huixiangdou.service.feature_store

## 正反例设置

本地版也可以通过编辑正反例来调整茴香豆的拒答和响应，正例位于 `/root/huixiangdou/resource/good_questions.json` 文件夹中，反例位于`/root/huixiangdou/resource/bad_questions.json`。

需要注意的是，每次更新原始知识文档和正反例，都需要重新运行 `python3 -m huixiangdou.service.feature_store` 命令进行向量知识库的重新创建和应答阈值的更新。

## 测试

1.   命令行运行
```
conda activate huixiangdou
cd /root/huixiangdou
python3 -m huixiangdou.main --standalone
```
2.  Gradio UI 界面测试

```
conda activate huixiangdou
cd /root/huixiangdou
python3 -m huixiangdou.gradio
```

- 运行结果
![[Pasted image 20240829173534.png]](imgs/Pasted%20image%2020240829173534.png)
- 
![[Pasted image 20240829173914.png]](imgs/Pasted%20image%2020240829173914.png)
