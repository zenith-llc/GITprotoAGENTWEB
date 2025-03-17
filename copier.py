import os
import shutil
import subprocess
import datetime
import time


# リポジトリのルートに移動
os.chdir("C:\GITprotoAGENTWEB")

def copy_file_with_retry(src, dst, max_retries=5, delay=1):
    for attempt in range(max_retries):
        try:
            # 別の一時ファイルにコピーしてみる
            tmp_dst = dst + ".tmp"
            shutil.copy2(src, tmp_dst)
            os.replace(tmp_dst, dst)  # 一時ファイルから最終ファイルにリネーム
            print(f"Copied successfully: {src} -> {dst}")
            return True
        except PermissionError as e:
            print(f"PermissionError on attempt {attempt+1}/{max_retries}: {e}")
            time.sleep(delay)
    return False

def main():
    while True:
        try:
            #EVOLPATH *SOURCE
            source_dir = r"C:\AlphaEvol2ND\ORIGINALPAGE\DataPlotted"
            #CLONED PATH `shita` IDK WHY BYT IT GOT DELETED SO I REMADE IT *MAYUBE BECAUSE IT WAS BLANK
            dest_dir = r"C:\GITprotoAGENTWEB\DataPlotted"

            if not os.path.exists(source_dir):
                print(f"Source folder {source_dir} does not exist.")
                return

            if not os.path.exists(dest_dir):
                os.makedirs(dest_dir, exist_ok=True)

            for filename in os.listdir(source_dir):
                if filename.lower().endswith((".jpg", ".jpeg", ".png", ".gif")):
                    src_path = os.path.join(source_dir, filename)
                    dst_path = os.path.join(dest_dir, filename)
                    print(f"Copying {src_path} -> {dst_path}")
                    if not copy_file_with_retry(src_path, dst_path):
                        print(f"Failed to copy {src_path} after multiple attempts.")

            now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            commit_message = f"Update images at {now_str}"
            try:
                subprocess.run(["git", "add", "."], check=True)
                subprocess.run(["git", "commit", "-m", commit_message], check=True)
                subprocess.run(["git", "push", "origin", "main"], check=True)
                print("Git push successful.")
            except subprocess.CalledProcessError as e:
                print("An error occurred with Git commands:", e)

            time.sleep(600)
        except Exception as e:
            print(e)
            print("Error")
            time.sleep(600)
        

if __name__ == "__main__":
    main()
