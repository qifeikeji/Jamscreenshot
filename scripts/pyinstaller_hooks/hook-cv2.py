# OpenCV 在 Windows 上有时是扩展模块，collect_all('cv2') 会失效；按安装目录手动收集。
import os

import cv2

hiddenimports = ["cv2", "numpy.core._multiarray_umath"]

binaries: list[tuple[str, str]] = []
datas: list[tuple[str, str]] = []

cv2_root = os.path.dirname(cv2.__file__)
if os.path.isdir(cv2_root):
    for name in os.listdir(cv2_root):
        path = os.path.join(cv2_root, name)
        if not os.path.isfile(path):
            continue
        if name.endswith((".pyd", ".dll", ".so", ".dylib")):
            binaries.append((path, "cv2"))
        elif name.endswith((".py", ".pyi", ".xml", ".json")) or name.startswith("config"):
            datas.append((path, "cv2"))
else:
    binaries.append((cv2.__file__, "cv2"))
