import os
import time
import subprocess
from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from werkzeug.utils import secure_filename

from utils.utils import *

app = Flask(__name__)
socketio = SocketIO(app)
CORS(app, supports_credentials=True)

# 配置上传文件的目录
UPLOAD_FOLDER = 'uploads'
RESULTS_FOLDER = 'results'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULTS_FOLDER, exist_ok=True)

# 模拟支持的模型列表
# available_models = ["model1", "model2", "model3"]

# 模拟模型训练/测试过程的日志
def run_model(images_dir, selected_model, mode):
    # 模拟训练或测试的命令（你可以替换为实际模型的训练/测试命令）
    command = f"echo 'Running {selected_model} in {mode} mode with images from {images_dir}'"
    
    # 模拟一个长时间运行的进程
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # 实时获取进程输出并通过 WebSocket 发送到前端
    for line in process.stdout:
        log_message = line.decode().strip()
        socketio.emit('log', {'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'), 'message': log_message})
        time.sleep(1)  # 模拟延迟
    
    # 等待进程结束
    process.wait()

    # 模拟训练/测试结果
    result_path = os.path.join(RESULTS_FOLDER, 'final_result.txt')
    with open(result_path, 'w') as f:
        f.write(f"Model {selected_model} finished in {mode} mode.\n")

    # 完成后通知前端
    socketio.emit('result', {'message': 'Training/Testing completed!', 'result_path': result_path})


@app.route('/api/get_models', methods=['GET'])
def get_models():
    # 返回支持的模型列表
    return jsonify(get_supported_models_name())


@app.route('/api/upload', methods=['POST'])
def upload_files():
    # 获取前端上传的文件和配置
    files = request.files.getlist("file")
    config = request.form['config']
    mode = request.form['mode']

    # 保存上传的图片
    images_dir = os.path.join(UPLOAD_FOLDER, 'images')
    os.makedirs(images_dir, exist_ok=True)

    for file in files:
        filename = secure_filename(file.filename)
        file.save(os.path.join(images_dir, filename))

    # 启动训练/测试进程
    socketio.start_background_task(run_model, images_dir, config, mode)

    return jsonify({"status": "processing", "message": "Model is running."})


@app.route('/api/get_results', methods=['GET'])
def get_results():
    # 假设每个任务都将结果保存在一个文本文件中
    result_file = os.path.join(RESULTS_FOLDER, 'final_result.txt')
    if os.path.exists(result_file):
        with open(result_file, 'r') as f:
            result = f.read()
        return jsonify({"result": result})
    return jsonify({"status": "error", "message": "No results found."})


if __name__ == '__main__':
    app.run(debug=True)
    # 启动 Flask-SocketIO
    socketio.run(app, host='0.0.0.0', port=5000)
