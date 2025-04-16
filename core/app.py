import os
import random
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--host', type=str, default='localhost', help='Host address')
parser.add_argument('--port', type=int, default=5000, help='Port number')
parser.add_argument('--debug', action='store_true', help='Enable debug mode')
parser.add_argument('--gpu_id', type=str, default='0', help='GPU ID to use')
args = parser.parse_args()

os.environ["CUDA_VISIBLE_DEVICES"] = args.gpu_id

from flask import Flask, request, jsonify, send_from_directory
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from werkzeug.utils import secure_filename


from utils.utils import *
from run_train import before_training, training, after_training
from run_test import before_testing, testing, after_testing

app = Flask(__name__, static_folder=RESULTS_FOLDER)
socketio = SocketIO(app, cors_allowed_origins="*")
CORS(app)

std_listener = StdOutListener(socketio, emit_event="stdout")
std_listener.start()

# 模拟支持的模型列表
# available_models = ["model1", "model2", "model3"]

# # 模拟模型训练/测试过程的日志
# def run_model(images_dir, selected_model, mode):
#     # 模拟训练或测试的命令（你可以替换为实际模型的训练/测试命令）
#     command = f"echo 'Running {selected_model} in {mode} mode with images from {images_dir}'"
    
#     # 模拟一个长时间运行的进程
#     process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

#     # 实时获取进程输出并通过 WebSocket 发送到前端
#     for line in process.stdout:
#         log_message = line.decode().strip()
#         socketio.emit('training_update', 
#                       {
#                           'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'), 
#                           'message': log_message}
#                       )
#         time.sleep(1)  # 模拟延迟
    
#     # 等待进程结束
#     process.wait()

#     # 模拟训练/测试结果
#     result_path = os.path.join(RESULTS_FOLDER, 'final_result.txt')
#     with open(result_path, 'w') as f:
#         f.write(f"Model {selected_model} finished in {mode} mode.\n")

#     # 完成后通知前端
#     socketio.emit('result', {'message': 'Training/Testing completed!', 'result_path': result_path})


@app.route('/api/get_models', methods=['GET'])
def get_models():
    # 返回支持的模型列表
    models = get_supported_models_name()
    # print(models)
    return jsonify(models)


@app.route('/api/get_local_projects', methods=['GET'])
def get_local_projects():
    # 返回本地项目列表
    return jsonify(os.listdir(RESULTS_FOLDER))


@app.route('/api/get_datasets', methods=['GET'])
def get_datasets():
    # 返回支持的数据集列表
    datasets = get_supported_datasets_name()
    return jsonify(datasets)


@app.route('/api/get_model_config', methods=['POST'])
def get_model_config():
    # 获取前端传来的模型名称
    data = request.get_json()
    model_name = data.get('model_name')
    try:
        config = load_model_config(MAPPER.get(model_name, "null"))
    except FileNotFoundError as e:
        print(e)
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        print(e)
        return jsonify({"error": f"An error occurred while loading the config: {str(e)}."}), 500
    return jsonify(config)


@app.route('/api/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request."}), 400
    
    file = request.files['file']
    file_token = request.form.get('fileToken')
    if not file_token:
        file_token = gen_token()

    if file.filename == '':
        return jsonify({"error": "No selected file."}), 400
    
    root_dir = os.path.join(UPLOAD_FOLDER, file_token)
    os.makedirs(root_dir, exist_ok=True)
    file_path = os.path.join(root_dir, secure_filename(file.filename))
    file.save(file_path)

    return jsonify({"message": "File uploaded successfully.", "file_path": file_path, 'file_token': file_token})


@app.route('/api/remove_file', methods=['POST'])
def remove_uploaded_file():
    data = request.get_json()
    file_path = data.get('file_path')
    if not file_path:
        return jsonify({"error": "No file path provided."}), 400
    if os.path.exists(file_path):
        os.remove(file_path)
        return jsonify({"message": "File removed successfully."})
    else:
        return jsonify({"error": "File not found."}), 404


@app.route('/api/get_dataset_config', methods=['POST'])
def get_dataset_config():
    # 获取前端传来的数据集名称
    data = request.get_json()
    dataset_name = data.get('dataset_name')
    try:
        config = load_dataset_config(MAPPER.get(dataset_name, "null"))
    except FileNotFoundError as e:
        print(e)
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        print(e)
        return jsonify({"error": f"An error occurred while loading the config: {str(e)}."}), 500
    return jsonify(config)


@app.route('/api/train', methods=['POST'])
def start_training():
    data = request.get_json()
    model_name = data.get('model_name')
    dataset_name = data.get('dataset_name')
    model_config = data.get('model_config')
    dataset_config = data.get('dataset_config')

    project_path = before_training(model_name, dataset_name, model_config, dataset_config)
    model_config: dict = json.loads(model_config)
    dataset_config: dict = json.loads(dataset_config)
    # print(project_path)

    try:
        # 启动训练进程
        training_process = socketio.start_background_task(training, model_config, dataset_config, project_path, socketio, std_listener)
        # training(model_config, dataset_config, project_path, socketio)
    except Exception as e:
        print(f"Error starting training: {e}")
        return jsonify({"error": f"An error occurred while starting the training: {str(e)}."}), 500
    
    return jsonify({"status": "processing", "message": "Training started."})


@app.route('/api/test', methods=['POST'])
def start_validation():
    data = request.get_json()
    project_name = data.get('project_name')
    file_token = data.get('file_token')
    
    try:
        model_config, model_weight_path, input_dir, test_dir = before_testing(project_name, file_token)
        testing_process = socketio.start_background_task(testing, model_config, model_weight_path, input_dir, test_dir, socketio, std_listener)
    except FileNotFoundError as e:
        print(e)
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        print(e)
        return jsonify({"error": f"An error occurred while loading the config: {str(e)}."}), 500
    
    return jsonify({"status": "processing", "message": "Testing started."})


@app.route('/api/get_results', methods=['POST'])
def get_results():
    data = request.get_json()
    project_path = data.get('project_path')
    test_path = data.get('test_path')
    host = "http://localhost:5000/"

    try:
        if project_path:
            results = get_validation_results(project_path)
            # print(results)
            results = random.choices(results, k=5)
            results = list(
                map(
                    lambda x: host + x,
                    results
                )
            )
        elif test_path:
            results = get_test_results(test_path)
            results = list(map(lambda x: host + x, results))

        return jsonify({
            "imagePaths": results,
        })
    
    except FileNotFoundError as e:
        print(e)
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        print(e)
        return jsonify({"error": f"An error occurred while loading the config: {str(e)}."}), 500

if __name__ == '__main__':
    app.run(debug=args.debug)
    # 启动 Flask-SocketIO
    socketio.run(app, host=args.host, port=args.port, allow_unsafe_werkzeug=True)

