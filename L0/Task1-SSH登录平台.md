Step1:  
ssh-keygen -t rsa  
Step2:  
打开pub文件，复制到网页  
[https://studio.intern-ai.org.cn/user/access](https://link.segmentfault.com/?enc=ftQsKTIUBpyUlfowUDxFfw%3D%3D.Sgg42y6sfT0iUQgGfzZbOe%2BHUHP%2FieAfhIkKWhDpO1Ye0h7e%2Bf%2Bc6ZKb4000Ho0g)  
![image.png](https://segmentfault.com/img/bVddPIC "image.png")  
Step3:  
vscode中 ssh登录命令：  
ssh -p 34802 [root@ssh.intern](mailto:root@ssh.intern)-ai.org.cn -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null  
选择默认config文件，登录成功。  
![image.png](https://segmentfault.com/img/bVddPIF "image.png")

Step4:  
映射端口  
ssh -p 37367 [root@ssh.intern](mailto:root@ssh.intern)-ai.org.cn -CNg -L {本地机器_PORT}:127.0.0.1:{开发机_PORT} -o StrictHostKeyChecking=no  
参数含义：  
-p 37367：是指定 SSH 连接的端口为 37367，这个前面提到过。  
[root@ssh.intern](mailto:root@ssh.intern)-ai.org.cn：表示要以 root 用户身份连接到 ssh.intern-ai.org.cn 这个主机。  
-CNg：  
-C 通常用于启用压缩。  
-N 表示不执行远程命令，仅建立连接用于端口转发等。  
-g 允许远程主机连接到本地转发的端口。  
-L {本地机器_PORT}:127.0.0.1:{开发机_PORT}：这是设置本地端口转发，将本地机器的指定端口（由 {本地机器_PORT} 表示）转发到远程主机（这里即 ssh.intern-ai.org.cn）的 127.0.0.1 （即本地回环地址）和指定的开发机端口（由 {开发机_PORT} 表示）。  
-o StrictHostKeyChecking=no：关闭严格的主机密钥检查，这样可以避免第一次连接时因为未知主机密钥而产生的提示或错误。

关闭端口映射：停止运行该命令的cmd即可。

Step5:运行hello_world  
命令行安装gradio  
pip install gradio  
root目录新建文件hello_world.py：

import socket
import re
import gradio as gr
 
# 获取主机名
def get_hostname():
    hostname = socket.gethostname()
    match = re.search(r'-(\d+)$', hostname)
    name = match.group(1)
    
    return name
 
# 创建 Gradio 界面
with gr.Blocks(gr.themes.Soft()) as demo:
    html_code = f"""
            <p align="center">
            <a href="https://intern-ai.org.cn/home">
                <img src="https://intern-ai.org.cn/assets/headerLogo-4ea34f23.svg" alt="Logo" width="20%" style="border-radius: 5px;">
            </a>
            </p>
            <h1 style="text-align: center;">☁️ Welcome {get_hostname()} user, welcome to the ShuSheng LLM Practical Camp Course!</h1>
            <h2 style="text-align: center;">😀 Let’s go on a journey through ShuSheng Island together.</h2>
            <p align="center">
                <a href="https://github.com/InternLM/Tutorial/blob/camp3">
                    <img src="https://oss.lingkongstudy.com.cn/blog/202406301604074.jpg" alt="Logo" width="20%" style="border-radius: 5px;">
                </a>
            </p>

            """
    gr.Markdown(html_code)

demo.launch()

![image.png](https://segmentfault.com/img/bVddPI0 "image.png")  
执行python helloworld.py

端口映射原理：  
![image.png](https://segmentfault.com/img/bVddPI8 "image.png")

运行结果  
![image.png](https://segmentfault.com/img/bVddPI9 "image.png")