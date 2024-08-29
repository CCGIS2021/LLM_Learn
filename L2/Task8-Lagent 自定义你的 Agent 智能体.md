## 结构

![[Pasted image 20240829082909.png]](imgs/Pasted%20image%2020240829082909.png)

## 环境配置
继续使用xturner0.1.9
```
conda activate xturner0.1.9
pip install termcolor==2.4.0
mkdir -p /L2/Task2
cd /L2/Task2
git clone https://github.com/InternLM/lagent.git
cd lagent && git checkout 81e7ace && pip install -e . && cd ..
```

## Lagent Web Demo 使用
- 启动demo
	- lmdeploy serve api_server /share/new_models/Shanghai_AI_Laboratory/internlm2_5-7b-chat --model-name internlm2_5-7b-chat
	- cd /root/L2/Task2/lagent
	- vscode中运行：
		- streamlit run examples/internlm2_agent_web_demo.py
		- 自动进行端口映射

UI页面启动报错ModuleNotFoundError: No module named 'griffe.enumerations'
需要安装旧版的griffe
pip install griffe==0.48.0
![[Pasted image 20240829090707.png]](imgs/Pasted%20image%2020240829090707.png)


## 自定义工具

### 工具位置：
/root/L2/Task2/lagent/lagent/actions/magicmaker.py
```
import json
import requests

from lagent.actions.base_action import BaseAction, tool_api
from lagent.actions.parser import BaseParser, JsonParser
from lagent.schema import ActionReturn, ActionStatusCode

class MagicMaker(BaseAction):
    styles_option = [
        'dongman',  # 动漫
        'guofeng',  # 国风
        'xieshi',   # 写实
        'youhua',   # 油画
        'manghe',   # 盲盒
    ]
    aspect_ratio_options = [
        '16:9', '4:3', '3:2', '1:1',
        '2:3', '3:4', '9:16'
    ]

    def __init__(self,
                 style='guofeng',
                 aspect_ratio='4:3'):
        super().__init__()
        if style in self.styles_option:
            self.style = style
        else:
            raise ValueError(f'The style must be one of {self.styles_option}')
        
        if aspect_ratio in self.aspect_ratio_options:
            self.aspect_ratio = aspect_ratio
        else:
            raise ValueError(f'The aspect ratio must be one of {aspect_ratio}')
    
    @tool_api
    def generate_image(self, keywords: str) -> dict:
        """Run magicmaker and get the generated image according to the keywords.
        Args:
            keywords (:class:`str`): the keywords to generate image
        Returns:
            :class:`dict`: the generated image
                * image (str): path to the generated image
        """
        try:
            response = requests.post(
                url='https://magicmaker.openxlab.org.cn/gw/edit-anything/api/v1/bff/sd/generate',
                data=json.dumps({
                    "official": True,
                    "prompt": keywords,
                    "style": self.style,
                    "poseT": False,
                    "aspectRatio": self.aspect_ratio
                }),
                headers={'content-type': 'application/json'}
            )
        except Exception as exc:
            return ActionReturn(
                errmsg=f'MagicMaker exception: {exc}',
                state=ActionStatusCode.HTTP_ERROR)
        image_url = response.json()['data']['imgUrl']
        return {'image': image_url}
```

### 添加工具：
修改/root/L2/Task2/lagent/lagent/examples/internlm2_agent_web_demo.py
```
1.  在 `from lagent.actions import ActionExecutor, ArxivSearch, IPythonInterpreter` 的下一行添加 `from lagent.actions.magicmaker import MagicMaker`

2.  在第27行添加 `MagicMaker()`。

from lagent.actions import ActionExecutor, ArxivSearch, IPythonInterpreter
+ from lagent.actions.magicmaker import MagicMaker
from lagent.agents.internlm2_agent import INTERPRETER_CN, META_CN, PLUGIN_CN, Internlm2Agent, Internlm2Protocol

...
        action_list = [
            ArxivSearch(),
+             MagicMaker(),
        ]
```

![[Pasted image 20240829091204.png]](imgs/Pasted%20image%2020240829091204.png)
![[Pasted image 20240829091222.png]](imgs/Pasted%20image%2020240829091222.png)
