from flask import Flask, render_template, request, url_for, jsonify
import subprocess

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('1.26.html')


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


@app.route('/get_visual')
def get_visual():
    # 生成图片的 URL
    image_url = url_for('static', filename='visual_wav.jpg')

    # 返回 JSON 格式的响应，包含图片的 URL
    return jsonify({"image_url": image_url})


@app.route('/record.html')
def record():
    return render_template('record.html')


if __name__ == '__main__':
    app.run(debug=True)
