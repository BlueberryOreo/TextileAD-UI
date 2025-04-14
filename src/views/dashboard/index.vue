<template>
    <div class="dashboard-container">
      <el-row :gutter="20">
          <el-card>
            <h3>模型设置</h3>
            <el-form :model="modelConfig" label-width="120px">
              <!-- 选择模型 -->
              <el-form-item label="选择模型">
                <el-select v-model="modelConfig.selectedModel" placeholder="请选择模型">
                  <el-option
                    v-for="(model, index) in availableModels"
                    :key="index"
                    :label="model"
                    :value="model"
                  />
                </el-select>
              </el-form-item>
  
              <!-- 选择模式 -->
              <el-form-item label="模式">
                <el-radio-group v-model="modelConfig.mode">
                  <el-radio label="train">训练</el-radio>
                  <el-radio label="test">测试</el-radio>
                </el-radio-group>
              </el-form-item>
              
              <div v-if="modelConfig.mode === 'train'">
                <!-- <DynamicJsonForm
                  :json="modelConfig"
                  v-model="modelConfig"
                /> -->
                Show DynamicJsonForm
              </div>
              <div v-else>
                <!-- 上传文件 -->
                <el-form-item label="图片上传">
                <el-upload
                  class="upload-demo"
                  action=""
                  :before-upload="beforeUpload"
                  multiple
                  :file-list="fileList"
                  :on-change="handleFileChange"
                >
                  <el-button size="small" type="primary">选择文件</el-button>
                </el-upload>
              </el-form-item>
              </div>
  
              <!-- 提交按钮 -->
              <el-form-item>
                <el-button type="primary" @click="uploadFiles">开始处理</el-button>
              </el-form-item>
            </el-form>
          </el-card>
      </el-row>
    </div>
  </template>
  
  <script>
  import axios from 'axios'
//   import DynamicJsonForm from '@/components/DynamicJsonForm/index'
  
  export default {
    data() {
      return {
        modelConfig: {
          selectedModel: '',  // 选中的模型
          mode: 'train',      // 模式（训练/测试）
        },
        fileList: [], // 存储上传的文件
        availableModels: [], // 存储从后端获取的模型列表
        logData: [], // 存储日志信息
        result: null, // 存储结果
      }
    },
    components: {
        // 引入动态表单组件
        // DynamicJsonForm: () => import('@/components/DynamicJsonForm/index.vue'),
    },
    methods: {
      // 获取支持的模型列表
      fetchModels() {
        axios
          .get('http://localhost:5000/api/get_models') // 调用后端接口获取模型
          .then(response => {
            this.availableModels = response.data
          })
          .catch(error => {
            console.error('获取模型失败:', error)
          })
        // const response = axios.get('http://localhost:5000/api/get_models')
        // console.log("Response:")
        // console.log(response)
      },
  
      // 处理文件上传前的验证
      beforeUpload(file) {
        const isImage = file.type.startsWith('image/')
        if (!isImage) {
          this.$message.error('只能上传图片文件！')
        }
        return isImage
      },
  
      // 处理文件列表变化
      handleFileChange(file, fileList) {
        this.fileList = fileList
      },
  
      // 上传图片和设置
      uploadFiles() {
        if (this.fileList.length === 0) {
          this.$message.error('请上传图片！')
          return
        }
  
        let formData = new FormData()
        for (let i = 0; i < this.fileList.length; i++) {
          formData.append('file', this.fileList[i].raw)
        }
        formData.append('config', JSON.stringify(this.modelConfig))
        
        axios
          .post('http://localhost:5000/api/upload', formData, {
            headers: {
              'Content-Type': 'multipart/form-data',
            },
          })
          .then((response) => {
            this.$message.success('上传成功，模型开始处理！')
            this.listenLogs()
          })
          .catch((error) => {
            this.$message.error('上传失败！')
            console.error(error)
          })
      },
  
      // 监听训练/测试的日志
      listenLogs() {
        const socket = new WebSocket('ws://localhost:5000') // 这里假设后端使用 WebSocket 传输实时日志
        socket.onmessage = (event) => {
          this.logData.push(JSON.parse(event.data))
        }
      },
  
      // 获取训练/测试结果
      getResults() {
        axios
          .get('http://localhost:5000/api/get_results')
          .then((response) => {
            this.result = response.data
          })
          .catch((error) => {
            console.error(error)
          })
      }
    },
  
    mounted() {
      // 获取支持的模型列表
      this.fetchModels()
    }
  }
  </script>
  
  <style scoped>
  .dashboard-container {
    padding: 20px;
  }
  
  .el-card {
    margin-bottom: 20px;
  }
  
  .upload-demo i {
    margin-right: 10px;
  }
  
  .el-button {
    width: 100%;
  }
  </style>
  