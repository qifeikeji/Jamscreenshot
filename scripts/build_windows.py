#!/usr/bin/env python3
"""在 Windows 上用 PyInstaller 打包 Jamscreenshot（需在仓库根目录执行）。"""
from __future__ import annotations

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main() -> None:
    if sys.platform != "win32":
        print("此脚本仅用于 Windows 打包。", file=sys.stderr)
        sys.exit(1)

    os.chdir(ROOT)

    from PyInstaller.building.api import COLLECT, EXE, PYZ, Analysis
    from PyInstaller.utils.hooks import collect_all

    datas: list[tuple[str, str]] = [
        (
            os.path.join(ROOT, "PaddleOCRModel", "ppocr_keys_v1.txt"),
            "PaddleOCRModel",
        ),
    ]
    for sub in ("modelv3", "modelv2"):
        model_dir = os.path.join(ROOT, "PaddleOCRModel", sub)
        if os.path.isdir(model_dir):
            datas.append((model_dir, os.path.join("PaddleOCRModel", sub)))

    hiddenimports = [
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
    binaries: list[tuple[str, str, str]] = []

    for pkg in ("cv2", "numpy", "PyQt5", "onnxruntime", "pyttsx3", "PIL", "pyclipper", "shapely"):
        pkg_datas, pkg_binaries, pkg_hidden = collect_all(pkg)
        datas += pkg_datas
        binaries += pkg_binaries
        hiddenimports += pkg_hidden

    a = Analysis(
        [os.path.join(ROOT, "jamscreenshot.py")],
        pathex=[ROOT],
        binaries=binaries,
        datas=datas,
        hiddenimports=hiddenimports,
        hookspath=[],
        hooksconfig={},
        runtime_hooks=[],
        excludes=[],
        noarchive=False,
        optimize=0,
    )
    pyz = PYZ(a.pure)
    exe = EXE(
        pyz,
        a.scripts,
        [],
        exclude_binaries=True,
        name="Jamscreenshot",
        debug=False,
        bootloader_ignore_signals=False,
        strip=False,
        upx=False,
        console=False,
        disable_windowed_traceback=False,
        argv_emulation=False,
        target_arch=None,
        codesign_identity=None,
        entitlements_file=None,
    )
    coll = COLLECT(
        exe,
        a.binaries,
        a.datas,
        strip=False,
        upx=False,
        upx_exclude=[],
        name="Jamscreenshot",
    )

    from PyInstaller.building.build_main import build

    build(coll)
    print("Build output: dist/Jamscreenshot/Jamscreenshot.exe")


if __name__ == "__main__":
    main()
