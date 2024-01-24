from flask import Flask, render_template, request
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('demo.html')

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
    with open('/Users/zhangqi/TCM_UI/TCM_UI/output/Words/result.txt', 'r', encoding='utf-8') as file:
        text_content = file.read()
    return text_content



if __name__ == '__main__':
    app.run(debug=True)
