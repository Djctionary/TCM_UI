from flask import Flask, render_template, request, url_for, jsonify
import subprocess
import os
import shutil

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('main.html')


@app.route('/run_python_script', methods=['POST'])
def run_python_script():
    if request.method == 'POST':
        try:
            # 运行你的 Python 文件，例如这里是运行名为 script.py 的文件
            subprocess.run(['python', 'Audio2Words.py'], check=True)
            subprocess.run(['python', 'Audio2Visual.py'], check=True)
            return 'Success'
        except subprocess.CalledProcessError:
            return 'Error'


@app.route('/get_text')
def get_text():
    with open('F:/Users/Djctionary/Desktop/HACI_Lab/TCM_UI/output/Words/result.txt', 'r', encoding='utf-8') as file:
        text_content = file.read()
    return text_content

@app.route('/record.html')
def record():
    return render_template('record.html')

@app.route('/create_folder', methods=['POST'])
def create_folder():
    try:
        data = request.get_json()
        folder_id = data['id']
        folder_name = f"ID_{folder_id}";
        # 在这里使用 folder_id 创建文件夹
        folder_path = rf'F:\Users\Djctionary\Desktop\HACI_Lab\TCM_UI\output\Result\{folder_name}'
        os.makedirs(folder_path, exist_ok=True)
        print(f"Trying to create folder at: {folder_path}")

        source_audio_path = r'F:\Users\Djctionary\Desktop\HACI_Lab\TCM_UI\output\Audio\audio.wav'
        source_visual_path = r'F:\Users\Djctionary\Desktop\HACI_Lab\TCM_UI\output\Visual\visual_wav.jpg'
        source_words_path = r'F:\Users\Djctionary\Desktop\HACI_Lab\TCM_UI\output\Words\result.txt'

        try:
            shutil.copy(source_audio_path, folder_path)
            shutil.copy(source_visual_path, folder_path)
            shutil.copy(source_words_path, folder_path)
            print(f"已成功复制到目标文件夹: {folder_path}")
        except Exception as e:
            print(f"复制文件时出现错误: {e}")

        file_patterns = ["步态记录", "舌相抓取", "面部识别", "患者自述"]
        base_path = r"C:\Users\Djctionary\Downloads"

        max_files = {}

        for root, dirs, files in os.walk(base_path):
            for file in files:
                for file_pattern in file_patterns:
                    if file.startswith(f"{folder_id}_{file_pattern}") and file.endswith(".mp4"):
                        current_key = (folder_id, file_pattern)
                        current_file_path = os.path.join(root, file)

                        if current_key not in max_files or os.path.getmtime(current_file_path) > os.path.getmtime(
                                max_files[current_key]):
                            max_files[current_key] = current_file_path

        for key, file_path in max_files.items():
            print(f"找到符合条件的文件路径: {file_path}")
            shutil.copy(file_path, folder_path)
            print(f"已复制到目标文件夹: {folder_path}")

        return jsonify({'message': 'Folder created successfully'})
    except Exception as e:
        return jsonify({'error': str(e)})



if __name__ == '__main__':
    app.run(debug=True)
