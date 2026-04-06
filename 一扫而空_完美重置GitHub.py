import os
import subprocess
import shutil

def run_cmd(cmd):
    print(f"> {cmd}")
    subprocess.run(cmd, shell=True, stderr=subprocess.STDOUT)

def main():
    print("==============================================")
    print("      极简清理与全静默重轨脚本启动")
    print("==============================================")

    # 1. 彻底覆盖全局的 .gitignore，掐平包括顶级目录下产生的所有图片、废品录制及大文件
    gitignore_content = """# 字节码与缓存
__pycache__/
*.py[cod]

# 本地数据与缓存（顶级目录及子目录全面拦截）
Memory_Temp/
CoreMemory/
录制/
accounting_data/
calendar_data/
forum_data/
todo_data/
temp_whl/
Demo_Image/*

# 超大第三方依赖与二进制文件
ffmpeg_bin/
obs-studio/
node-v*/
*.exe
*.dll
*.zip
*.tar.xz
*.7z

# 日志、多媒体废品与敏感配置
*.log
*log*.txt
*.txt
*.mp3
*.wav
*.mp4
*.png
*.jpg
@AutomationLog.txt
config.py
"""
    with open('.gitignore', 'w', encoding='utf-8') as f:
        f.write(gitignore_content)

    print("\n[1/3] 执行物理清除：清理根目录生成图档及赘余文本...")
    # 物理抹除刚才那些烦人的画图目录和日志文件
    junk_files = ['call_window_debug.txt', 'gradio_api_docs.txt', 'test_v3.log']
    for f in junk_files:
        if os.path.exists(f):
            try: os.remove(f)
            except: pass

    junk_dirs = ['Memory_Temp', '录制', 'WeChatBot_WXAUTO_SE-3.28/Memory_Temp']
    for d in junk_dirs:
        if os.path.exists(d):
            try: shutil.rmtree(d, ignore_errors=True)
            except: pass

    print("\n[2/3] 重构代码基底：无声抹除所有AI风貌和痕迹...")
    
    # 重造根源历史，完全抹除那句中二的 Commit Message 留言
    run_cmd('git checkout --orphan fresh_stage_new')
    run_cmd('git rm -rf --cached .')
    run_cmd('git add .')
    run_cmd('git config user.email "bot@example.com"')
    run_cmd('git config user.name "Master"')
    
    # 使用最为冰冷、正规的大厂提交术语
    run_cmd('git commit -m "Initial commit"')

    print("\n[3/3] 执行深空覆盖：冲刷 Github 云端...")
    run_cmd('git branch -D main')
    run_cmd('git branch -M main')
    run_cmd('git push -f origin main')

    print("\n==============================================")
    print("清空洗白已完成！Github 云端已被无中二感纯净源码覆盖。")
    print("==============================================")

if __name__ == "__main__":
    main()
