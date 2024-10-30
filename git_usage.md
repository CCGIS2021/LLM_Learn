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

## 4.创建新分支
1. **创建新的本地分支并切换到该分支：**

   首先，创建并切换到你需要的新分支。例如：
   ```bash
   git checkout -b new-feature
   ```

2. **修改并添加指定文件：**

   假设你对文件 `example.txt` 进行了修改，接下来需要将其添加到暂存区：
   ```bash
   git add example.txt
   ```

3. **提交更改：**

   将暂存区中的更改提交到本地分支：
   ```bash
   git commit -m "Update example.txt with the new feature"
   ```

4. **推送提交到远程分支：**

   将本地分支推送到远程仓库，以便在远程创建相应的分支并将提交的更改上传：
   ```bash
   git push -u origin new-feature
   ```

   这里的 `-u` 选项用于在本地分支和远程分支之间设置跟踪关系。这样，以后可以直接在本地分支上使用 `git push` 推送更改。

就这样，你在本地创建的文件更改将被提交并推送到远程仓库的相应分支中。