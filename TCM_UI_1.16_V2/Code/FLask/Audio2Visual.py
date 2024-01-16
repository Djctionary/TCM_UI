import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
import os

def get_unique_input_path(output_path):
    base_dir = os.path.dirname(output_path)
    base_name, ext = os.path.splitext(os.path.basename(output_path))

    numbered_output_path = output_path
    number = 1
    while os.path.exists(numbered_output_path):
        numbered_output_path = os.path.join(base_dir, f"{base_name}_{number}{ext}")
        number += 1

    number -= 2
    numbered_output_path = os.path.join(base_dir, f"{base_name}_{number}{ext}")

    return numbered_output_path

def convert_video_to_audio(output_audio_path):

    if os.path.exists(output_audio_path):
        output_audio_path = get_unique_input_path(output_audio_path)

    return output_audio_path

def visualize_wav(input_file, output_file):
    # 读取 WAV 文件
    sample_rate, data = wavfile.read(input_file)

    # 获取音频数据
    signal = data  # 如果是单声道，使用 data；如果是多声道，使用 data[:, 0] 获取其中一个声道的数据

    # 创建时间轴
    time = np.arange(0, len(signal)) / sample_rate

    # 绘制波形图
    plt.figure(figsize=(10, 4))
    plt.plot(time, signal, color='b')
    plt.title('Waveform Visualization')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Amplitude')
    plt.grid(True)

    # 保存图形到本地文件
    plt.savefig(output_file)
    print("音频可视化成功！")
    #plt.show()

if __name__ == "__main__":
    input_wav = r"F:\Users\Djctionary\Desktop\HACI_Lab\TCM_UI\output\Audio\audio.wav"  # 替换成你的音频文件路径
    output_image = r"F:\Users\Djctionary\Desktop\HACI_Lab\TCM_UI\Code\FLask\static\visual_wav.jpg" # 替换成你想保存的图像文件路径
    unique_input_path = convert_video_to_audio(input_wav)
    visualize_wav(unique_input_path, output_image)
