#!/usr/bin/env python3

"""
WEBM to MP3 Converter
=====================

INPUT:
    D:\Airpita Songs

OUTPUT:
    D:\Airpita Songs\Mp3

Requirements:
    pip install -U imageio-ffmpeg
"""

import os
import sys
import subprocess
from pathlib import Path

# =========================================================
# SETTINGS
# =========================================================

INPUT_FOLDER = r"D:\Airpita Songs"

OUTPUT_FOLDER = r"D:\Airpita Songs\Mp3"

BITRATE = "192k"

# =========================================================
# INSTALL PACKAGE
# =========================================================

def install(package):

    subprocess.check_call([
        sys.executable,
        "-m",
        "pip",
        "install",
        "-U",
        package
    ])


try:
    import imageio_ffmpeg

except ImportError:

    print("📦 Installing imageio-ffmpeg...")

    install("imageio-ffmpeg")

    import imageio_ffmpeg


# =========================================================
# GET FFMPEG
# =========================================================

FFMPEG_EXE = imageio_ffmpeg.get_ffmpeg_exe()

if not os.path.isfile(FFMPEG_EXE):

    print("❌ FFmpeg not found")
    sys.exit(1)

print("\n✅ FFmpeg Found")
print(FFMPEG_EXE)

# =========================================================
# CREATE OUTPUT FOLDER
# =========================================================

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# =========================================================
# FIND WEBM FILES
# =========================================================

webm_files = [
    os.path.join(INPUT_FOLDER, file)
    for file in os.listdir(INPUT_FOLDER)
    if file.lower().endswith(".webm")
]

total = len(webm_files)

if total == 0:

    print("\n❌ No .webm files found")
    sys.exit(0)

print("\n" + "=" * 60)
print(f"🎵 Found {total} WEBM file(s)")
print("=" * 60)

# =========================================================
# CONVERT FILES
# =========================================================

success = 0
failed = 0

for index, webm_path in enumerate(webm_files, start=1):

    try:

        filename = Path(webm_path).stem

        mp3_path = os.path.join(
            OUTPUT_FOLDER,
            f"{filename}.mp3"
        )

        print("\n" + "-" * 60)
        print(f"[{index}/{total}]")
        print(f"🎵 {os.path.basename(webm_path)}")

        command = [
            FFMPEG_EXE,
            "-i",
            webm_path,
            "-vn",
            "-ab",
            BITRATE,
            "-ar",
            "44100",
            "-y",
            mp3_path
        ]

        subprocess.run(
            command,
            check=True
        )

        print("✅ Converted")
        print(f"📁 {mp3_path}")

        success += 1

    except Exception as e:

        print(f"❌ Failed: {e}")

        failed += 1

# =========================================================
# SUMMARY
# =========================================================

print("\n" + "=" * 60)
print("🎉 CONVERSION COMPLETE")
print("=" * 60)

print(f"✅ Success : {success}")
print(f"❌ Failed  : {failed}")

print(f"\n📁 Output Folder:")
print(OUTPUT_FOLDER)