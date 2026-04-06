import uiautomation as auto
import time

print("=====================================================")
print("请在接下来的 60 秒内，发起或接听一次微信语音/视频通话")
print("本脚本将自动捕捉微信通话窗口的确切名称和类型，以便精准匹配")
print("=====================================================")

end_time = time.time() + 60
found_windows = set()

with open("call_window_debug.txt", "w", encoding="utf-8") as f:
    while time.time() < end_time:
        for win in auto.GetRootControl().GetChildren():
            try:
                name = win.Name
                cls = win.ClassName
                
                # 过滤掉桌面、任务栏等系统窗口
                if cls in ["CabinetWClass", "Progman", "WorkerW", "Shell_TrayWnd", "Chrome_WidgetWin_1", "ConsoleWindowClass"]:
                    continue
                
                # 如果这个窗口和微信有关，或者是未知的新窗口，我们记录它
                if "wechat" in cls.lower() or "weixin" in cls.lower() or "mmui" in cls.lower() or "video" in cls.lower() or "audio" in cls.lower() or "微信" in name:
                    win_info = f"[{time.strftime('%H:%M:%S')}] Window Name: [{name}], ClassName: [{cls}]"
                    if win_info not in found_windows:
                        found_windows.add(win_info)
                        print(f"找到疑似窗口: {win_info}")
                        f.write(win_info + "\n")
                        
                        # 尝试获取第一层和第二层子控件以查看里面的按钮（如“挂断”）
                        for child in win.GetChildren():
                            child_info = f"   - Child Name: [{child.Name}], Class: [{child.ClassName}]"
                            f.write(child_info + "\n")
                            # for sub_child in child.GetChildren():
                            #     f.write(f"      - SubChild Name: [{sub_child.Name}], Class: [{sub_child.ClassName}]\n")
            except Exception:
                pass
        time.sleep(1)

print("=====================================================")
print("诊断完成！信息已保存到 call_window_debug.txt")
print("=====================================================")
