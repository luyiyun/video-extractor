import os
import tempfile
import argparse
from time import perf_counter
import subprocess

import torch
import whisper
from yt_dlp import YoutubeDL

from .utils import is_url


def download_audio(url: str) -> None:
    ydl_opts = {
        "format": "m4a/bestaudio/best",
        # ℹ️ See help(yt_dlp.postprocessor) for a list of available Postprocessors and their arguments
        "postprocessors": [
            {  # Extract audio using ffmpeg
                "key": "FFmpegExtractAudio",
                "preferredcodec": "m4a",
            }
        ],
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download(url)


def transcribe(
    fn: str,
    model: str = "turbo",
    device: str = "cuda" if torch.cuda.is_available() else "cpu",
    lang: str | None = None,
) -> list[str]:
    model = whisper.load_model(model, device=device)
    result = model.transcribe(fn, language=lang, verbose=True)
    lines = [item["text"] + "\n" for item in result["segments"]]
    return lines


def extract_audio(
    url: str,
    save_fn: str = "transcription.txt",
    model: str = "turbo",
    device: str = "cuda" if torch.cuda.is_available() else "cpu",
    lang: str | None = None,
):
    outdir = os.getcwd()
    with tempfile.TemporaryDirectory() as tdir:
        os.chdir(tdir)
        if is_url(url):
            download_audio(url)
            fn = os.listdir()[0]
        else:
            command = [
                "ffmpeg",
                "-i",
                url,  # 输入视频文件
                "-vn",  # 禁用视频流
                "-acodec",
                "copy",  # 直接复制音频流（不重新编码）
                "audio.m4a",
            ]
            subprocess.run(command, check=True)
            fn = "audio.m4a"
        start_time = perf_counter()
        lines = transcribe(fn, model=model, device=device, lang=lang)
        end_time = perf_counter()
        print(f"Transcription took {end_time - start_time:.2f} seconds.")
        os.chdir(outdir)  # 返回到原工作目录，否则无法删除临时文件
    with open(save_fn, "w", encoding="utf-8") as f:
        f.writelines(lines)


def cli():
    parser = argparse.ArgumentParser(
        description="Extract audio from a YouTube video and transcribe it using the Whisper API"
    )
    parser.add_argument(
        "url", type=str, help="URL of the YouTube video to extract audio from"
    )
    parser.add_argument(
        "--save_fn",
        type=str,
        default="transcription.txt",
        help="Filename to save the transcription to (default: transcription.txt)",
    )
    parser.add_argument(
        "--model",
        type=str,
        choices=["tiny", "turbo"],
        default="turbo",
        help="Model to use for transcription (default: turbo)",
    )
    parser.add_argument(
        "--device",
        type=str,
        default="cuda" if torch.cuda.is_available() else "cpu",
        help="Device to use for inference (default: cuda if available, else cpu)",
    )
    parser.add_argument(
        "--lang",
        type=str,
        default=None,
        help="Language code to use for transcription (default: None)",
    )
    args = parser.parse_args()
    extract_audio(
        args.url,
        save_fn=args.save_fn,
        model=args.model,
        device=args.device,
        lang=args.lang,
    )
