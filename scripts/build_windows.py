#!/usr/bin/env python3
"""在 Windows 上用 PyInstaller 打包 Jamscreenshot（需在仓库根目录执行）。"""
from __future__ import annotations

import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOOKS_DIR = os.path.join(ROOT, "scripts", "pyinstaller_hooks")


def main() -> None:
    if sys.platform != "win32":
        print("此脚本仅用于 Windows 打包。", file=sys.stderr)
        sys.exit(1)

    os.chdir(ROOT)
    sep = ";"

    cmd: list[str] = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--noconfirm",
        "--clean",
        "--windowed",
        "--name",
        "Jamscreenshot",
        "--paths",
        ROOT,
        "--additional-hooks-dir",
        HOOKS_DIR,
    ]

    cmd.extend(
        [
            "--add-data",
            os.path.join("PaddleOCRModel", "ppocr_keys_v1.txt") + sep + "PaddleOCRModel",
        ]
    )
    for sub in ("modelv3", "modelv2"):
        model_dir = os.path.join("PaddleOCRModel", sub)
        if os.path.isdir(model_dir):
            cmd.extend(["--add-data", model_dir + sep + model_dir])

    hidden = [
        "cv2",
        "jamresourse",
        "jamWidgets",
        "jampublic",
        "jamroll_screenshot",
        "jamspeak",
        "jam_transtalater",
        "PaddleOCRModel.PaddleOCRModel",
        "pyttsx3.drivers",
        "pyttsx3.drivers.sapi5",
        "PyQt5.sip",
        "PIL",
        "PIL.Image",
        "pyclipper",
        "shapely",
        "shapely.geometry",
    ]
    for name in hidden:
        cmd.extend(["--hidden-import", name])

    for pkg in ("PyQt5", "onnxruntime", "numpy", "pyttsx3", "PIL", "pyclipper", "shapely"):
        cmd.extend(["--collect-all", pkg])

    cmd.extend(
        [
            "--exclude-module",
            "pytest",
            "--exclude-module",
            "onnx",
        ]
    )

    cmd.append("jamscreenshot.py")

    print("Running:", " ".join(cmd))
    subprocess.check_call(cmd, cwd=ROOT)
    print("Build output: dist/Jamscreenshot/Jamscreenshot.exe")


if __name__ == "__main__":
    main()
