import subprocess
import os


def get_unique_output_path(output_path):
    base_dir = os.path.dirname(output_path)
    base_name, ext = os.path.splitext(os.path.basename(output_path))

    numbered_output_path = output_path
    number = 1
    while os.path.exists(numbered_output_path):
        numbered_output_path = os.path.join(base_dir, f"{base_name}_{number}{ext}")
        number += 1

    return numbered_output_path


def convert_video_to_audio(video_path, output_audio_path):
    try:
        # 检查输出路径是否已存在
        if os.path.exists(output_audio_path):
            output_audio_path = get_unique_output_path(output_audio_path)

        # 使用 ffmpeg 将视频转成音频
        subprocess.run(['ffmpeg', '-i', video_path, '-vn', '-acodec', 'pcm_s16le', '-ar', '44100', output_audio_path],
                       check=True)

        print(f"成功将视频转成音频：{output_audio_path}")
    except subprocess.CalledProcessError as e:
        print(f"视频转音频过程中出错：{e}")


# 用法示例
video_path = "ch.mp4"
output_audio_path = "audio.wav"

convert_video_to_audio(video_path, output_audio_path)
