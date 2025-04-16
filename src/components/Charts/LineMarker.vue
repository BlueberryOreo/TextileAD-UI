<template>
  <div :id="id" :class="className" :style="{height:height,width:width}" />
</template>

<script>
import echarts from 'echarts'
import resize from './mixins/resize'

export default {
  mixins: [resize],
  props: {
    className: {
      type: String,
      default: 'chart'
    },
    id: {
      type: String,
      default: 'chart'
    },
    width: {
      type: String,
      default: '200px'
    },
    height: {
      type: String,
      default: '200px'
    },
    chartData: {
      type: Object,
      default: () => ({ loss: 0 })
    },
    epoch: {
      type: Number,
      default: 0
    }
  },
  data() {
    return {
      chart: null,
      localChartData: JSON.parse(JSON.stringify(this.chartData)),
    }
  },
  watch: {
    chartData(newData) {
      console.log(newData)
      this.localChartData = JSON.parse(JSON.stringify(newData))
      this.updatechartData()
    }
  },
  mounted() {
    this.initChart()
  },
  beforeDestroy() {
    if (!this.chart) {
      return
    }
    this.chart.dispose()
    this.chart = null
  },
  methods: {
    initChart() {
      // console.log(this.ChartData)
      this.chart = echarts.init(document.getElementById(this.id))

      this.chart.setOption({
        backgroundColor: '#394056',
        title: {
          top: 20,
          text: '损失可视化',
          textStyle: {
            fontWeight: 'normal',
            fontSize: 16,
            color: '#F1F1F3'
          },
          left: '1%'
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            lineStyle: {
              color: '#57617B'
            }
          }
        },
        legend: {
          top: 20,
          icon: 'rect',
          itemWidth: 14,
          itemHeight: 5,
          itemGap: 13,
          data: ['loss'],
          right: '4%',
          textStyle: {
            fontSize: 12,
            color: '#F1F1F3'
          }
        },
        grid: {
          top: 100,
          left: '2%',
          right: '2%',
          bottom: '2%',
          containLabel: true
        },
        xAxis: [{
          type: 'category',
          name: 'epoch',
          boundaryGap: false,
          axisLine: {
            lineStyle: {
              color: '#57617B'
            }
          },
          data: [0]
        }],
        yAxis: [{
          type: 'value',
          name: 'loss',
          axisTick: {
            show: false
          },
          axisLine: {
            lineStyle: {
              color: '#57617B'
            }
          },
          axisLabel: {
            margin: 10,
            textStyle: {
              fontSize: 14
            }
          },
          splitLine: {
            lineStyle: {
              color: '#57617B'
            }
          }
        }],
        // series: Object.entries(this.ChartData).map(([key, value]) => ({
        //       name: key,
        //       type: 'line',
        //       smooth: true,
        //       symbol: 'circle',
        //       symbolSize: 3,
        //       showSymbol: false,
        //       data: value
        //   })),
        // series: this.ChartData
      })
    },

    updatechartData(){
      const epochsArray = Array.from({ length: this.epoch + 1 }, (_, i) => i);
      this.chart.setOption({
          xAxis: [{
              type: 'category',
              name: 'epoch',
              boundaryGap: false,
              axisLine: {
                  lineStyle: {
                  color: '#57617B'
                  }
              },
              data: epochsArray,
          }],
          legend: {
            top: 20,
            icon: 'rect',
            itemWidth: 14,
            itemHeight: 5,
            itemGap: 13,
            data: Object.entries(this.localChartData).map(([key]) => key),
            right: '4%',
            textStyle: {
              fontSize: 12,
              color: '#F1F1F3'
            }
          },
          series: Object.entries(this.localChartData).map(([key, value]) => ({
              name: key,
              type: 'line',
              smooth: true,
              symbol: 'circle',
              symbolSize: 3,
              showSymbol: false,
              data: value
          }))
      })
    },
  }
}
</script>
