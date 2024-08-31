import subprocess
import time

def git_push_with_retries(remote='origin', branch='main', max_retries=50, wait_time=5):
    for attempt in range(max_retries):
        try:
            # 执行 git push 命令
            print("Pushing to GitHub...")
            subprocess.run(['git', 'push'], check=True)
            print("Push succeeded!")
            break
        except subprocess.CalledProcessError as e:
            print(f"Push failed: {e}. Retrying {attempt + 1}/{max_retries}...")
            time.sleep(wait_time)
    else:
        print("Exceeded maximum retries. Push failed.")

if __name__ == "__main__":
    git_push_with_retries()