# OpenCV (opencv-contrib-python) 在 Windows 上需显式收集二进制与数据文件
from PyInstaller.utils.hooks import collect_all

datas, binaries, hiddenimports = collect_all("cv2")
