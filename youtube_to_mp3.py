#!/usr/bin/env python3

"""
YouTube to MP3 Converter
========================

Requirements:
    pip install -U yt-dlp imageio-ffmpeg

Run:
    python youtube_to_mp3.py
"""

import os
import sys
import subprocess

# ╔══════════════════════════════════════════════════════════════╗
# ║                    ✏️ EDIT ONLY THIS                        ║
# ╚══════════════════════════════════════════════════════════════╝

YOUTUBE_URLS = [
    "https://www.youtube.com/watch?v=B1DGKaZRDMA&list=PLfP6i5T0-DkKSs8G6YbPHYAR70-f5tP9S&index=2",
]

OUTPUT_PATH = r"D:\Airpita Songs"

# ╔══════════════════════════════════════════════════════════════╗
# ║                🚫 DO NOT EDIT BELOW                         ║
# ╚══════════════════════════════════════════════════════════════╝


def auto_install(package):
    print(f"📦 Installing {package} ...")

    subprocess.check_call([
        sys.executable,
        "-m",
        "pip",
        "install",
        "-U",
        package
    ])


def ensure_packages():

    try:
        import yt_dlp
    except ImportError:
        auto_install("yt-dlp")

    try:
        import imageio_ffmpeg
    except ImportError:
        auto_install("imageio-ffmpeg")


def get_ffmpeg_dir():
    """
    Returns FFmpeg directory path.
    yt-dlp needs the DIRECTORY, not the exe file.
    """

    try:
        import imageio_ffmpeg

        ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()

        if not os.path.isfile(ffmpeg_exe):
            raise RuntimeError("FFmpeg executable not found")

        ffmpeg_dir = os.path.dirname(ffmpeg_exe)

        print("\n✅ FFmpeg detected")
        print(f"📁 {ffmpeg_dir}")

        return ffmpeg_dir

    except Exception as e:
        print(f"\n❌ FFmpeg setup failed: {e}")
        sys.exit(1)


def download_as_mp3(url, output_path, ffmpeg_dir):

    import yt_dlp

    os.makedirs(output_path, exist_ok=True)

    ydl_opts = {
        "format": "bestaudio/best",

        # IMPORTANT FIX
        "ffmpeg_location": ffmpeg_dir,

        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],

        "outtmpl": os.path.join(
            output_path,
            "%(title)s.%(ext)s"
        ),

        "restrictfilenames": True,

        "quiet": False,
        "no_warnings": False,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:

        try:
            info = ydl.extract_info(
                url,
                download=True
            )

        except yt_dlp.utils.DownloadError as e:
            raise RuntimeError(str(e))

    title = info.get("title", "audio")

    safe_title = yt_dlp.utils.sanitize_filename(
        title,
        restricted=True
    )

    mp3_path = os.path.join(
        output_path,
        f"{safe_title}.mp3"
    )

    if os.path.isfile(mp3_path):
        return mp3_path

    raise RuntimeError("MP3 conversion failed")


def main():

    print("=" * 60)
    print("🎵 YouTube → MP3 Converter")
    print("=" * 60)

    print("\n🔍 Checking dependencies...\n")

    ensure_packages()

    ffmpeg_dir = get_ffmpeg_dir()

    total = len(YOUTUBE_URLS)

    success = []
    failed = []

    print("\n" + "=" * 60)
    print(f"📋 Total URLs: {total}")
    print(f"📁 Output: {OUTPUT_PATH}")
    print("=" * 60)

    for idx, url in enumerate(YOUTUBE_URLS, start=1):

        print(f"\n[{idx}/{total}] {url}")
        print("-" * 60)

        try:
            saved = download_as_mp3(
                url,
                OUTPUT_PATH,
                ffmpeg_dir
            )

            size_mb = os.path.getsize(saved) / (1024 * 1024)

            print(f"✅ Saved: {os.path.basename(saved)}")
            print(f"📦 Size : {size_mb:.2f} MB")

            success.append(saved)

        except Exception as e:

            print(f"❌ Failed: {e}")

            failed.append((url, str(e)))

    print("\n" + "=" * 60)
    print("🎉 DOWNLOAD COMPLETE")
    print("=" * 60)

    print(f"\n✅ Success: {len(success)}")
    print(f"❌ Failed : {len(failed)}")

    if failed:

        print("\nFailed URLs:\n")

        for url, reason in failed:

            print(url)
            print(reason)
            print()


if __name__ == "__main__":
    main()