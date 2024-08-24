# 代码实现

实现一个wordcount函数，统计英文字符串中每个单词出现的次数。返回一个字典，key为单词，value为对应单词出现的次数。

代码：

```
text = """

Got this panda plush toy for my daughter's birthday,

who loves it and takes it everywhere. It's soft and

super cute, and its face has a friendly look. It's

a bit small for what I paid though. I think there

might be other options that are bigger for the

same price. It arrived a day earlier than expected,

so I got to play with it myself before I gave it

to her.

"""

  
  

def word_count(text):

    count_list = [item.lower() for item in text.strip().split() if item not in ',.\'。，；：:']

    count_result = {}

    for word in count_list:

        count_result[word] = count_result.get(word, 0) + 1

  

    print(count_result)

    return count_list

  

if __name__=='__main__':

    word_count(text=text)
```

运行结果：
![[Pasted image 20240824224447.png]]

# 远程调试过程：
- 连接ssh
- 
##  单文件调试
- 点击VSCode侧边栏的“Run and Debug”（运行和调试），然后点击“Run and Debug”（开始调试）按钮
- 选择python file 
- ![[Pasted image 20240824225344.png]]

## 命令行带参数调试

- 点击VSCode侧边栏的“Run and Debug”（运行和调试)，单击"create a lauch.json file"
- 择debugger时选择python debuger。选择debug config时选择remote attach，server地址为localhost:5678。
- pip install debugp
- python -m debugpy --listen 5678 --wait-for-client ./myscript.py
- 点击绿色dubug按钮
- ![[Pasted image 20240824225745.png]]