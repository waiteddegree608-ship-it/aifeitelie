import time
import os
import subprocess
import uiautomation as auto
import obsws_python as obs
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# --- 配置部分 (CONFIGURATION) ---
# OBS Studio 的完整路径
OBS_PATH = r"F:\workspace\程序本体bot-3.28\obs-studio\bin\64bit\obs64.exe"
OBS_CWD = r"F:\workspace\程序本体bot-3.28\obs-studio\bin\64bit"

# OBS WebSocket 的连接信息
OBS_HOST = "localhost"
OBS_PORT = 4455
# 请在 OBS 中设置 WebSocket 的密码，或者在 OBS 中关闭身份验证 (并在下面留空)
OBS_PASSWORD = "" 

# 微信通话的识别关键词与类名
CALL_KEYWORDS = ["语音通话", "视频通话", "Voice Call", "Video Call", "通话中"]
CALL_CLASSES = ["AudioWnd", "VideoWnd"]

class CallListener:
    def __init__(self):
        self.is_recording = False
        self.obs_client = None

    def connect_obs(self):
        """尝试连接到 OBS WebSocket"""
        try:
            self.obs_client = obs.ReqClient(host=OBS_HOST, port=OBS_PORT, password=OBS_PASSWORD, timeout=3)
            return True
        except Exception as e:
            return False

    def is_call_active(self):
        """检查是否存在微信通话的窗口"""
        try:
            for win in auto.GetRootControl().GetChildren():
                name = win.Name
                className = win.ClassName
                
                # 直接匹配特征窗口名
                if any(kw in name for kw in CALL_KEYWORDS):
                    return True
                
                # 匹配特征窗口类名
                if any(kw in className for kw in CALL_CLASSES):
                    return True
                
                # 在某些微信版本中，通话属于 mmui:: 或 WeChat 相关的类
                if 'wechat' in className.lower() or '微信' in name or className.startswith('mmui'):
                    # 也可以选择进一步遍历子控件来查找"挂断"等字眼（考虑到性能，默认只查顶层名）
                    pass
        except Exception:
            pass
        return False

    def check_and_start_obs(self):
        """确保 OBS 正在运行且 WebSocket 连通"""
        if not self.connect_obs():
            logging.info("未能连接到 OBS WebSocket，正在尝试启动 OBS...")
            try:
                # 最小化启动 OBS
                subprocess.Popen([OBS_PATH, "--minimize-to-tray"], cwd=OBS_CWD)
                logging.info("OBS 启动中，等待 10 秒钟...")
                time.sleep(10)
                if not self.connect_obs():
                    logging.error("无法连接到 OBS WebSocket！请检查：")
                    logging.error("1. OBS -> 工具 -> WebSocket 服务器设置 是否已开启")
                    logging.error("2. 端口是否为 4455")
                    logging.error("3. 本脚本中的 OBS_PASSWORD 密码是否与 OBS 中相符 (或关闭验证)")
                    return False
            except Exception as e:
                logging.error(f"启动 OBS 失败: {e}")
                return False
        return True

    def start_recording(self):
        """开始录制"""
        if self.is_recording:
            return
        
        logging.info("检测到微信通话进行中！准备开始录制...")
        if self.check_and_start_obs():
            try:
                # 获取当前录制状态，如果已录制则不重复调用
                resp = self.obs_client.get_record_status()
                if not resp.output_active:
                    self.obs_client.start_record()
                self.is_recording = True
                logging.info(">>> 录音/录屏已开启 <<<")
            except Exception as e:
                logging.error(f"开启录制失败: {e}")

    def stop_recording(self):
        """停止录制"""
        if not self.is_recording:
            return
        
        logging.info("微信通话疑似结束。准备停止录制...")
        if self.obs_client:
            try:
                resp = self.obs_client.get_record_status()
                if resp.output_active:
                    self.obs_client.stop_record()
                self.is_recording = False
                logging.info(">>> 录音/录屏已停止 <<<")
            except Exception as e:
                logging.error(f"停止录制失败: {e}")
                # 即使抛异常也认为不再处于我们可控的录制状态
                self.is_recording = False 

    def run(self):
        logging.info("=== 微信通话 OBS 自动录音脚本已启动 ===")
        logging.info(f"OBS 路径配置: {OBS_PATH}")
        logging.info("注意事项: 脚本将每 2 秒检测一次微信通话窗口。如检测到，则自动启动 OBS 开始录制。")
        while True:
            active = self.is_call_active()
            if active and not self.is_recording:
                self.start_recording()
            elif not active and self.is_recording:
                self.stop_recording()
            
            time.sleep(2)

if __name__ == "__main__":
    listener = CallListener()
    try:
        listener.run()
    except KeyboardInterrupt:
        logging.info("脚本已手动停止。")
