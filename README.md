# Video Extractor

使用Python编写的视频内容提取器，可以将视频语音提取为文本文件。依赖于[FFmpeg](https://ffmpeg.org/), [yt-dlp](https://github.com/yt-dlp/yt-dlp), [openai whisper](https://github.com/openai/whisper/tree/main)。


## 安装

```bash
pip install git+https://github.com/luyiyun/video_extractor.git
```

## 使用

```bash
video_extract --save_fn output.txt https://www.youtube.com/watch?v=dQw4w9WgXcQ
video_extract --save_fn output.txt --lang Chinese https://www.youtube.com/watch?v=dQw4w9WgXcQ
```
