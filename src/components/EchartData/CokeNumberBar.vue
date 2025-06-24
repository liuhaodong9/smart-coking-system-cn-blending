<template>
  <div >
    <!-- 不同图表id名字需要取成不同的，否则只能显示一个图表-->
      <div class="echart" id="echart-bar_2" :style="{position:'absolute',left:'1%',top:'8%', width: '100%', height: '100%'}"></div>
  </div>
</template>

<script>

export default {
  data () {
    return {
      xData: ['2015年', '2016年', '2017年', '2018年', '2019年', '2020年', '2021年'],
      coalData: [4.83, 4.36, 4.46, 4.35, 4.7, 4.85, 4.9],
      cokeData: [4.48, 4.49, 4.31, 4.38, 4.71, 4.71, 4.64, 2.40]
    }
  },
  mounted () {
    this.initChart()
  },
  methods: {
    initChart(Data) {
      const getchart = this.$echarts.init(document.getElementById('echart-bar_2'))
      var option = {
        title: { // 通用配置 1
          text: '中国近7年炼焦煤和焦炭产量(亿吨)',
          x: 'center', // 标题居中对齐
          textStyle: {
            color: 'white',
            fontSize: 15
          }
        },
        tooltip: { // 提示框组件
          trigger: 'axis',
          formatter: '{b0} 炼焦煤产量：{c0}亿吨  焦炭产量：{c1}亿吨', // 对提示框的内容进行格式化
          confine: true // 限制tootip在容器内
        },
        toolbox: { // 内置的工具栏
          feature: {
            saveAsImage: {}, // 导出图片
            dataView: {} // 数据视图
          },
          right: '4%' // 距离右边多远
        },
        xAxis: { // x轴
          show: true,
          type: 'category', // 类目轴，类别
          data: this.xData,
          axisLine: {
            show: true
          },
          axisLabel: {
            interval: 0, // 显示全部标签
            color: 'white'
          }
        },
        yAxis: { // y轴
          type: 'value', // 数值轴
          axisLabel: {
            interval: 0, // 显示全部标签
            color: 'white'
          }
        },
        dataZoom: { // 区域缩放
          show: false
        },
        series: [
          {
            name: '炼焦煤产量',
            type: 'bar',
            barWidth: 17,
            data: this.coalData,
            itemStyle: {
              color: {
                type: 'linear', // 线性渐变，还有radius，为径向渐变, x (0,0) y (0,1), 从下往上
                x: 0,
                y: 0,
                x2: 0,
                y2: 1,
                colorStops: [
                  {
                    offset: 0, color: '#f43b47' // 0%处的颜色
                  },
                  {
                    offset: 1, color: '#96e6a1' // 100%处的颜色
                  }
                ]
              }
            },
            label: { // 显示数值
              show: true,
              position: 'top',
              textStyle: {
                fontSize: 11,
                color: '#9565F4'
              }
            }
          },
          {
            name: '焦炭产量',
            type: 'bar',
            barWidth: 17, // bar的宽度
            data: this.cokeData,
            itemStyle: {
              color: {
                type: 'linear', // 线性渐变，还有radius，为径向渐变, x (0,0) y (0,1), 从下往上
                x: 0,
                y: 0,
                x2: 0,
                y2: 1,
                colorStops: [
                  {
                    offset: 0, color: '#30cfd0' // 0%处的颜色
                  },
                  {
                    offset: 1, color: '#330867' // 100%处的颜色
                  }
                ]
              }
            },
            label: { // 显示数值
              show: true,
              position: 'top',
              textStyle: {
                fontSize: 11,
                color: '#F24354'
              }
            }
          }
        ],
        legend: {
          data: ['炼焦煤产量', '焦炭产量'], // 需要和series的name保持一致，顺序不用一致
          x: 'left',
          textStyle: {
            color: 'white' // 字体颜色
          }
        }
      }
      getchart.setOption(option)
      window.addEventListener('resize', () => {
        getchart.resize()
      })
    }
  }
}
</script>

<style lang="less" scoped>
</style>
