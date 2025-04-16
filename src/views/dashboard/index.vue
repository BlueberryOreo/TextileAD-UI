<template>
    <div class="dashboard-container">
      <el-row :gutter="20">
          <el-card>
            <h3>模型选择与设置</h3>
            <el-form :model="modelConfig" label-width="120px">
              <!-- 选择模式 -->
              <el-form-item label="模式">
                <el-radio-group v-model="modelConfig.mode" @change="handleModeChange">
                  <el-radio label="train">训练模型</el-radio>
                  <el-radio label="test">使用已训练模型</el-radio>
                </el-radio-group>
              </el-form-item>

              <!-- 选择模型 -->
              <el-form-item label="选择模型">
                <el-select v-model="modelConfig.selectedModel" placeholder="请选择模型" @change="fetchModelConfigs">
                  <el-option
                    v-for="(model, index) in (modelConfig.mode == 'train' ? availableModels : availableProjects)"
                    :key="index"
                    :label="model"
                    :value="model"
                  />
                </el-select>
              </el-form-item>
              
              <div v-if="modelConfig.mode === 'train'">
                <!-- <DynamicJsonForm
                  :json="modelConfig"
                  v-model="modelConfig"
                /> -->
                <div style="display: flex; flex-direction: column; gap: 20px;">
                  <!-- 模型配置展示 -->
                  <el-form-item label="模型配置">
                    <el-input
                      type="textarea"
                      :rows="10"
                      v-model="modelConfigText"
                      placeholder="模型参数"
                      :readonly="!modifyingModelConfig"
                      style="margin-bottom: 10px;"
                    />
                    <el-row justify="start" type="flex">
                      <el-col :span="2">
                        <el-button type="primary" icon="el-icon-edit" circle style="width: 40px; height: 40px;" @click="handleEditButtonClick('model', $event)" :disabled="this.configs == null" title="编辑"></el-button>
                      </el-col>
                      <el-col :span="2">
                        <el-button type="success" icon="el-icon-check" circle style="width: 40px; height: 40px;" @click="handleSaveButtonClick('model', $event)" :disabled="this.configs == null" title="保存"></el-button>
                      </el-col>
                      <el-col :span="2">
                        <el-button type="warning" icon="el-icon-refresh-left" circle style="width: 40px; height: 40px;" @click="handleRefreshButtonClick('model', $event)" :disabled="this.configs == null" title="重置"></el-button>
                      </el-col>
                    </el-row>
                  </el-form-item>

                  <!-- 数据集选择 -->
                  <el-form-item label="数据集选择">
                    <el-select
                      v-model="modelConfig.selectedDataset"
                      placeholder="请选择数据集"
                      @change="fetchDatasetConfigs"
                    >
                      <el-option
                        v-for="(dataset, index) in availableDatasets"
                        :key="index"
                        :label="dataset"
                        :value="dataset"
                      />
                    </el-select>
                  </el-form-item>

                  <!-- 数据集参数展示 -->
                  <el-form-item label="数据集参数设置">
                    <el-input
                      type="textarea"
                      :rows="10"
                      v-model="datasetConfigText"
                      placeholder="数据集参数"
                      :readonly="!modifyingDatasetConfig"
                      style="margin-bottom: 10px;"
                    />
                    <el-row justify="start" type="flex">
                      <el-col :span="2">
                        <el-button type="primary" icon="el-icon-edit" circle style="width: 40px; height: 40px;" @click="handleEditButtonClick('dataset', $event)" :disabled="this.datasetConfigs == null" title="编辑"></el-button>
                      </el-col>
                      <el-col :span="2">
                        <el-button type="success" icon="el-icon-check" circle style="width: 40px; height: 40px;" @click="handleSaveButtonClick('dataset', $event)" :disabled="this.datasetConfigs == null" title="保存"></el-button>
                      </el-col>
                      <el-col :span="2">
                        <el-button type="warning" icon="el-icon-refresh-left" circle style="width: 40px; height: 40px;" @click="handleRefreshButtonClick('model', $event)" :disabled="this.datasetConfigs == null" title="重置"></el-button>
                      </el-col>
                    </el-row>
                  </el-form-item>
                </div>
              </div>
              <div v-else>
                <!-- 上传文件 -->
                <el-form-item label="图片上传">
                  <el-upload
                    class="upload-demo"
                    action="http://localhost:5000/api/upload"
                    :data="uploadData"
                    :on-remove="handleUploadRemove"
                    :on-success="handleUploadSuccess"
                    multiple
                    :file-list="fileList">
                    <el-button size="small" type="primary">图片上传</el-button>
                  </el-upload>
                </el-form-item>
              </div>
  
              <!-- 提交按钮 -->
              <el-form-item>
                <el-button type="primary" @click="startProcess">开始处理</el-button>
              </el-form-item>
            </el-form>
          </el-card>
      </el-row>
    </div>
  </template>
  
<script>
  import router from '@/router'
  import axios from 'axios'
//   import DynamicJsonForm from '@/components/DynamicJsonForm/index'
  
  export default {
    data() {
      return {
        modelConfig: {
          selectedModel: '',  // 选中的模型
          selectedDataset: '',  // 选中的数据集
          mode: 'train',      // 模式（训练/测试）
        },
        fileList: [], // 存储上传的文件
        availableModels: [], // 存储从后端获取的模型列表
        availableProjects: [], // 存储从后端获取的项目列表
        availableDatasets: [], // 存储从后端获取的数据集列表
        configs: null, // 存储模型配置
        datasetConfigs: null, // 存储数据集配置
        originConfigs: null, // 存储原始的模型配置
        originDatasetConfigs: null, // 存储原始的数据集配置
        modifyingModelConfig: false, // 是否正在修改模型配置
        modifyingDatasetConfig: false, // 是否正在修改数据集配置
        fileToken: '', // 存储文件的token
      }
    },
    computed: {
      // 计算属性，用于动态生成 JSON 文本
      modelConfigText: {
        get(){
          return this.configs
        },
        set(val){
          this.configs = val
        }
      },
      datasetConfigText: {
        get(){
          return this.datasetConfigs
        },
        set(val){
          this.datasetConfigs = val
        }
      },
      uploadData: {
        get(){
          return {
            fileToken: this.fileToken,
          }
        },
      }
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
      },

      fetchProjects(){
        axios
          .get('http://localhost:5000/api/get_local_projects') // 调用后端接口获取模型
          .then(response => {
            this.availableProjects = response.data
          })
          .catch(error => {
            console.error('获取本地项目失败:', error)
          })
      },

      fetchDataset(){
        axios
          .get('http://localhost:5000/api/get_datasets') // 调用后端接口获取模型
          .then(response => {
            this.availableDatasets = response.data
          })
          .catch(error => {
            console.error('获取数据集失败:', error)
          })
      },
      
      handleModeChange(){
        // console.log("mode change: " + this.modelConfig.mode)
        this.modelConfig.selectedModel = ''
        this.modelConfig.selectedDataset = ''
        for(let idx in this.fileList){
          this.handleUploadRemove(this.fileList[idx], this.fileList, false)
        }
        this.fileList = []
        this.fileToken = ''

        if (this.modelConfig.mode === 'train') {
          this.fetchModelConfigs()
        } else {
          this.configs = null
        }
      },

      handleEditButtonClick(config_name, event){
        if(config_name === "model"){
          this.modifyingModelConfig = true
        }
        if(config_name === "dataset"){
          this.modifyingDatasetConfig = true
        }
      },

      handleSaveButtonClick(config_name, event){
        if(config_name === "model"){
          this.modifyingModelConfig = false
          // 这里可以添加保存模型配置的逻辑
          try{
            const data = JSON.parse(this.configs)
            this.$message.success('模型配置已保存！')
            // 最终配置统一在开始训练的时候发送给后端作为本次训练的参数保存
          }catch(e){
            console.error('JSON 解析错误:', e)
            this.$message.error('模型配置 JSON 格式错误！')
            return
          }
        }
        if(config_name === "dataset"){
          this.modifyingDatasetConfig = false
          // 这里可以添加保存数据集配置的逻辑
          try{
            const data = JSON.parse(this.datasetConfigs)
            this.$message.success('数据集配置已保存！')
            // 最终配置统一在开始训练的时候发送给后端作为本次训练的参数保存
          }catch(e){
            console.error('JSON 解析错误:', e)
            this.$message.error('数据集配置 JSON 格式错误！')
            return
          }
        }
      },

      handleRefreshButtonClick(config_name, event){
        if(config_name === "model"){
          this.configs = this.originConfigs
          this.$message({
            message: "模型配置已重置",
            type: "success",
          })
        }
        if(config_name === "dataset"){
          this.datasetConfigs = this.originDatasetConfigs
          this.$message({
            message: "数据集配置已重置",
            type: "success",
          })
        }
      },

      // 获取模型配置
      fetchModelConfigs(){
        if(this.modelConfig.mode != "train" || this.modelConfig.selectedModel == ''){
          this.configs = null
          return
        }
        const data = {
          model_name: this.modelConfig.selectedModel,
        }
        axios
          .post(`http://localhost:5000/api/get_model_config`, data) // 调用后端接口获取模型
          .then(response => {
            this.configs = JSON.stringify(response.data, null, 2)
            this.originConfigs = this.configs
          })
          .catch(error => {
            console.error('获取模型配置失败:', error)
            if(error.response.status == 400){
              this.$message({
                message: "该模型无特别配置",
                type: "warning",
              })
              this.configs = "无"
            }else{
              this.$message.error('获取模型配置失败! code:' + error.response.status)
              this.configs = null
            }
            this.originConfigs = null
          })
      },
      
      // 获取数据集配置
      fetchDatasetConfigs(){
        if(this.modelConfig.mode != "train" || this.modelConfig.selectedDataset == ''){
          this.datasetConfigs = null
          return
        }
        const data = {
          dataset_name: this.modelConfig.selectedDataset,
        }
        axios
          .post(`http://localhost:5000/api/get_dataset_config`, data) // 调用后端接口获取模型
          .then(response => {
            this.datasetConfigs = JSON.stringify(response.data, null, 2)
            this.originDatasetConfigs = this.datasetConfigs
          })
          .catch(error => {
            console.error('获取数据集配置失败:', error)
            if(error.response.status == 400){
              this.$message({
                message: "该数据集无特别配置",
                type: "warning",
              })
              this.datasetConfigs = "无"
            }else{
              this.$message.error('获取数据集配置失败! code:' + error.response.status)
              this.datasetConfigs = null
            }
            this.originDatasetConfigs = null
          })
      },
      
      handleUploadRemove(file, fileList, popup=true){
        // console.log(file)
        // console.log(file, fileList)
        axios
          .post('http://localhost:5000/api/remove_file', file.response)
          .then(response => {
            console.log(response.data)
            if(popup){
              this.$message.success('文件删除成功！')
            }
          })
          .catch(error => {
            console.error('文件删除失败:', error)
            if(popup){
              this.$message.error('文件删除失败！')
            }
          })
      },

      handleUploadSuccess(response, file, fileList){
        // console.log(fileList)
        this.fileToken = response.file_token
        this.fileList = fileList
      },

      startProcess(){
        // Check if the model is selected
        if (!this.modelConfig.selectedModel) {
          this.$message.error('请选择模型！')
          return
        }

        // Check if the mode is train
        if (this.modelConfig.mode === 'train') {
          // Check if the dataset are selected
          if (!this.modelConfig.selectedDataset) {
            this.$message.error('请选择数据集！')
            return
          }

          const data = {
            model_name: this.modelConfig.selectedModel,
            dataset_name: this.modelConfig.selectedDataset,
            model_config: this.configs,
            dataset_config: this.datasetConfigs,
          }
          axios.post('http://localhost:5000/api/train', data)
            .then(response => {
              this.$message.success('开始训练')
            })
            .catch(error => {
              console.error('训练请求失败:', error)
              this.$message.error('训练请求失败！')
            })
        } else {
          if (this.fileList.length === 0) {
            this.$message.error('请上传图片！')
            return
          }

          const data = {
            project_name: this.modelConfig.selectedModel,
            file_token: this.fileToken,
          }
          axios.post('http://localhost:5000/api/test', data)
            .then(response => {
              this.$message.success('开始测试')
            })
            .catch(error => {
              console.error('测试请求失败:', error)
              this.$message.error('测试请求失败！')
            })
        }

        router.push({ path: '/logging/logging_panel', query: { mode: this.modelConfig.mode } })
      }
    },
  
    mounted() {
      // 获取支持的模型列表
      this.fetchModels()
      this.fetchDataset()
      this.fetchProjects()
      this.fileToken = ''
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
  