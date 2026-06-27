#!/usr/bin/env python3
"""在 Windows 上用 PyInstaller 打包 Jamscreenshot（需在仓库根目录执行）。"""
from __future__ import annotations

import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOOKS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pyinstaller_hooks")


def main() -> None:
    if sys.platform != "win32":
        print("此脚本仅用于 Windows 打包。", file=sys.stderr)
        sys.exit(1)

    os.chdir(ROOT)
    sep = ";"

    datas: list[str] = [
        os.path.join("PaddleOCRModel", "ppocr_keys_v1.txt") + sep + "PaddleOCRModel",
    ]
    for sub in ("modelv3", "modelv2"):
        model_dir = os.path.join("PaddleOCRModel", sub)
        if os.path.isdir(model_dir):
            datas.append(model_dir + sep + model_dir)

    hidden = [
        "cv2",
        "numpy",
        "PIL",
        "PIL.Image",
        "jamresourse",
        "jamWidgets",
        "jampublic",
        "jamroll_screenshot",
        "jamspeak",
        "jam_transtalater",
        "PaddleOCRModel.PaddleOCRModel",
        "onnxruntime",
        "pyclipper",
        "shapely",
        "shapely.geometry",
        "pynput",
        "pynput.mouse",
        "comtypes",
        "fake_useragent",
        "chardet",
        "requests",
        "pyttsx3",
        "pyttsx3.drivers",
        "pyttsx3.drivers.sapi5",
        "PyQt5.sip",
    ]

    collect_packages = (
        "cv2",
        "numpy",
        "PyQt5",
        "onnxruntime",
        "pyttsx3",
        "PIL",
        "shapely",
        "pyclipper",
    )

    cmd: list[str] = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--noconfirm",
        "--clean",
        "--onefile",
        "--windowed",
        "--name",
        "Jamscreenshot",
        "--paths",
        ROOT,
        "--additional-hooks-dir",
        HOOKS,
    ]
    for item in datas:
        cmd.extend(["--add-data", item])
    for name in hidden:
        cmd.extend(["--hidden-import", name])
    for pkg in collect_packages:
        cmd.extend(["--collect-all", pkg])

    cmd.append("jamscreenshot.py")
    print("Running:", " ".join(cmd))
    subprocess.check_call(cmd, cwd=ROOT)
    print("Build output: dist/Jamscreenshot.exe")


if __name__ == "__main__":
    main()
