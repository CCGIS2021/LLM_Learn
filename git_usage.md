## 1.初始化项目
- git init
- git add .
- git commit -m "Initial commit"
- git remote add origin https://github.com/CCGIS2021/LLM_Learn.git
- git push -u origin master
  
## 2.更新项目
- git add .
- git commit -m "update"
- git push

## 3.删除文件
- git rm --cached <file_name> # 删除文件跟踪
- 或者 git rm <file_name> # 删除文件
- git commit -m "delete <file_name>"
- git push