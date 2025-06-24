<template>
  <div >
    <!-- 不同图表id名字需要取成不同的，否则只能显示一个图表-->
      <div class="echart" id="echart-bar_1" :style="{position:'absolute',left:'1%',top:'5%', width: '100%', height: '110%'}"></div>
  </div>
</template>

<script>

export default {
  data () {
    return {
      xData: ['17年', '18年', '19年', '20年', '21年'],
      yData: [35.24, 36.98, 38.46, 39.02, 41.26, 21.94]
    }
  },
  mounted () {
    this.initChart()
  },
  methods: {
    initChart(Data) {
      const getchart = this.$echarts.init(document.getElementById('echart-bar_1'))
      var option = {
        title: { // 通用配置 1
          text: '中国近5年原煤产量(亿吨)',
          x: 'center', // 标题居中对齐
          textStyle: {
            color: 'white',
            fontSize: 15
          }
        },
        tooltip: { // 提示框组件
          trigger: 'axis',
          formatter: '20{b}原煤产量：{c}亿吨', // 对提示框的内容进行格式化
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
          type: 'value', // 类目轴，类别
          axisLine: {
            show: true
          },
          axisLabel: {
            interval: 0, // 显示全部标签
            color: 'white'
          }
        },
        yAxis: { // y轴
          type: 'category', // 数值轴
          inverse: true, // 倒叙
          data: this.xData,
          axisLabel: {
            interval: 0, // 显示全部标签
            color: 'white'
          }
        },
        series: [
          {
            type: 'bar',
            data: this.yData,
            barMaxWidth: 28, // 每一个都要设置
            itemStyle: {
              color: {
                type: 'linear', // 线性渐变，还有radius，为径向渐变, x (0,0) y (1,0), 从左往右
                x: 0,
                y: 0,
                x2: 1,
                y2: 0,
                colorStops: [
                  {
                    offset: 0, color: 'blue' // 0%处的颜色
                  },
                  {
                    offset: 1, color: '#08FBEE' // 100%处的颜色
                  }
                ]
              }
            },
            label: { // 显示数值
              show: true,
              position: 'right',
              textStyle: {
                fontSize: 11,
                color: '#F19E34'
              }
            }
          }

        ]
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
