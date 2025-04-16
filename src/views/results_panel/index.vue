<template>  
  <!-- 结果展示区域 -->
  <div class="results-container">
    <el-row :gutter="20">
      <el-card>
        <h3>结果</h3>
        <!-- <p>Project Path: {{ projectPath }}</p> -->
         <el-form>
          <el-form-item :label="labelText">
            {{ mode == 'train' ? projectPath : testPath }}
          </el-form-item>
          <el-form-item label="测试结果">
            <div class="scroll-result-container">
              <el-image v-for="url in images" :key="url" :src="url" lazy></el-image>
            </div>
          </el-form-item>
         </el-form>
      </el-card>
    </el-row>
  </div>
</template>

<script>
import axios from 'axios';


export default {
  data(){
    return {
      projectPath: '',
      testPath: '',
      mode: 'train',
      images: [],
    }
  },
  computed: {
    labelText: {
      get(){
        return this.mode === 'train' ? '项目路径' : '测试图片路径'
      }
    }
  },
  mounted() {
    this.images = []
    this.projectPath = this.$route.query.projectPath || ''
    this.testPath = this.$route.query.testPath || ''
    this.mode = this.$route.query.mode || 'train'
    this.getResults()
  },
  methods: {
    getResults(){
      if(this.mode === 'train'){
        if(this.projectPath === ''){
          console.log("Project path is empty")
          return
        }
        const data = {
          project_path: this.projectPath,
        }
        axios
          .post('http://localhost:5000/api/get_results', data)
          .then(response => {
            this.images = response.data.imagePaths
            console.log("Fetched images:", this.images)
          })
          .catch(error => {
            console.error('Error fetching results:', error);
          });
      }else{
        if(this.testPath === ''){
          console.log("Test path is empty")
          return
        }
        const data = {
          test_path: this.testPath,
        }
        axios
          .post('http://localhost:5000/api/get_results', data)
          .then(response => {
            this.images = response.data.imagePaths
            console.log("Fetched images:", this.images)
          })
          .catch(error => {
            console.error('Error fetching results:', error);
          });
      }
    }
  }
}
</script>

<style scoped>
  .results-container {
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

  .scroll-result-container {
    width: 100%;
    height: 50vh;
    overflow-y: auto; /* 设置垂直滚动条 */
    border: 1px solid #ccc;
  }
</style>