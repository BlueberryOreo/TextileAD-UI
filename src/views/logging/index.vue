<template>
    <div class="chart-container">
      <!-- 顶部进度条 -->
      <el-form style="margin-bottom: 10px;">
        <el-form-item :label="progressLabel" style="margin-bottom: 0;">
          <el-progress :percentage="progressPercentage" />
        </el-form-item>
      </el-form>
  
      <!-- 图表容器 -->
      <div class="chart-box">
        <chart ref="chart" :chartData="lossDict" :epoch="epoch" height="100%" width="100%" />
      </div>
  
      <!-- 测试按钮 -->
      <!-- <el-button type="primary" @click="updateChartData" style="margin: 10px 0;">更新</el-button> -->
  
      <!-- 日志文本框 -->
      <el-input
        id="logTextArea"
        type="textarea"
        :rows="10"
        v-model="logTextLines"
        placeholder="日志内容"
        readonly
      />
    </div>
  </template>

<script>
import Chart from '@/components/Charts/LineMarker'
import io from 'socket.io-client'
import router from '@/router'

export default {
    name: 'Logging',
    components: {
        Chart
    },
    data(){
        return {
            training: true,
            inference: false,
            logText: '',
            epoch: 0,
            totalEpoch: 1000,
            // lossArray: [],
            lossDict: {},
            socket: null,
            mode: 'train',
        }
    },
    computed: {
        logTextLines: {
            get(){
                // this.scrollToBottom()
                return this.logText
            }
        },
        progressLabel: {
            get(){
                return this.training ? "训练中..." : "测试中..."
            }
        },
        progressPercentage: {
            get(){
                if(this.totalEpoch == 0) totalEpoch = 1
                return +(this.epoch / this.totalEpoch * 100).toFixed(1)
            }
        }
    },
    watch: {
        logTextLines(newData){
            this.scrollToBottom()
        }
    },
    mounted() {
        this.mode = this.$route.query.mode || 'train'
        this.training = this.mode == 'train'
        this.inference = this.mode == 'test'

        this.socket = io('http://localhost:5000')
        this.socket.on('training_progress', (data) => {
            console.log(data)
            this.epoch = data.epoch
            this.totalEpoch = data.total_epochs
            if(this.training){
                if(data.loss != undefined){
                    let newDict = { ...this.lossDict }
                    for(let key in data.loss){
                        if(newDict[key] == undefined){
                            newDict[key] = []
                        }
                        newDict[key].push(data.loss[key])
                    }
                    this.lossDict = newDict
                }
            }
            
            if(data.training_complete){
                if(this.training){
                    this.logText += `训练完成！\n`
                    this.training = false
                }
                if(data.inference_complete){
                    this.logText += `测试完成！\n`
                    this.socket.disconnect()
                    router.push({'name': 'Results', 
                        query: { 
                            projectPath: data.project_path, 
                            testPath: data.test_path,
                            mode: this.mode
                        }
                    })
                }else{
                    if(!this.inference){
                        this.inference = true
                        this.logText += '开始测试\n'
                        this.epoch = 0
                    }
                }
            }
            // this.logText += `Epoch: ${this.epoch}, Loss: ${data.loss}\n`
        })
        this.socket.on('stdout', (data) => {
            this.logText += data.data + "\n"
        })
    },
    methods: {
        scrollToBottom() {
            // 使用 $nextTick 确保 DOM 更新后再滚动
            this.$nextTick(() => {
                // console.log("scrollToBottom")
                let logTextArea = document.getElementById('logTextArea')
                logTextArea.scrollTop = logTextArea.scrollHeight;
            })
        },
        updateChartData(){
            this.progressLabel = "测试中..."
        }
    }
}
</script>

<style scoped>
.chart-container {
  display: flex;
  flex-direction: column;
  height: 100%;
  padding: 20px;
  gap: 10px;
}

.chart-box {
  height: 300px; /* 或者用 max-height: 40vh 等，根据页面结构灵活调整 */
  width: 100%;
}
</style>