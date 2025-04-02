# 使用yt-dlp下载视频
import os
import subprocess


def download_video(url, output_dir):
    # 下载视频
    subprocess.run(["yt-dlp", "-o", os.path.join(output_dir, "%(title)s.%(ext)s"), url])
