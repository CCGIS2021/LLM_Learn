## 更新并切换分支

1. **添加原项目为远程仓库：**
   确保你在本地克隆了你的fork，并进入到项目目录。然后添加原项目仓库为一个新的远程仓库，通常命名为`upstream`。
   ```bash
   git remote add upstream https://github.com/InternLM/Tutorial.git
   ```

2. **获取原项目的最新信息：**
   拉取原项目中的所有分支和最新更改。
   ```bash
   git fetch upstream
   ```

3. **检查默认分支：**
   查看原项目中的分支，找到新的默认分支。
   ```bash
   git branch -r
   ```

4. **切换到新的默认分支：**
   如果原项目的新默认分支名为`new-default-branch`，切换到该分支。
   ```bash
   git checkout -b camp4 camp4
   ```

5. **更新你的默认分支：**
   如果你希望你的fork的默认分支也变更为与原项目一致，你可以删除本地原来的默认分支（通常是`main`或`master`），并重命名新分支。
   ```bash
   git branch -d camp3
   git branch -m camp4 camp4
   ```

6. **推送更改到你的GitHub fork：**
   将更新后的分支推送到你GitHub上的fork，并设置为默认分支。
   ```bash
   git push origin camp4
   ```

   如果你不想保留旧的默认分支，还可以执行以下步骤推送删除操作：
   ```bash
   git push origin --delete camp3
   ```

7. **在GitHub上设置新的默认分支：**
   - 在GitHub上进入你的fork仓库。
   - 打开“Settings > Branches”。
   - 在“Default branch”中将默认分支更改为你新同步的分支。

完成这些步骤后，fork与原项目的新默认分支同步。

## 创建class分支
git branch -a
git checkout -b class remotes/upstream/class
![[Pasted image 20241031094121.png]](imgs/Pasted%20image%2020241031100441.png)
git checkout -b class_685
创建id.md
git add .
git commit -m "add git_camp4_685_introduction"
git push origin class_685

github 提交pr
![[Pasted image 20241031100441.png]](imgs/Pasted%20image%2020241031100441.png)
