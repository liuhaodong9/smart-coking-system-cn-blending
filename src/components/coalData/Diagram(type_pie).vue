<template>
  <div >
      <div class="echart" id="echart-pie" :style="{position:'absolute',left:'5%',top:'5%', width: '100%', height: '100%'}"></div>
  </div>
</template>

<script>

export default {
  methods: {
    initChart(name, Data) {
      console.log(Data)
      const getchart = this.$echarts.init(document.getElementById('echart-pie'))
      var option = {
        tooltip: {
          trigger: 'item',
          formatter: '{b}<br/> 数量: {c}'
        },
        legend: {
          itemWidth: 10,
          width: 'auto',
          height: 'auto',
          orient: 'vertical',
          left: '-2%',
          top: '4%',
          data: Data.name,
          textStyle: {
            color: 'white',
            fontSize: 10
          }
        },
        title: {
          text: '煤种比例分布图',
          left: 'center',
          top: '-1%',
          textStyle: {
            fontSize: 14,
            fontWeight: 'bold',
            color: 'white',
            textShadowBlur: 5
          }
        },
        series: [
          {
            name: 'name',
            type: 'pie',
            radius: ['32%', '75%'], // 饼图中饼状部分的大小所占整个父元素的百分比，空心圆
            data: Data,
            label: {
              normal: {
                show: true,
                position: 'inside',
                textStyle: {
                  fontFamily: 'Microsoft YaHei',
                  fontSize: 10, // 文字的字体大小
                  textBorderColor: '#FFFFFF',
                  textBorderWidth: 2,
                  textShadowColor: '(255, 255, 255)'
                },
                formatter: '{d}%'
              }
            }
          },
          {
            name: 'name',
            type: 'pie',
            radius: ['40%', '75%'], // 饼图中饼状部分的大小所占整个父元素的百分比, 空心圆
            data: Data,
            label: {
              normal: {
                show: true,
                textStyle: {
                  fontFamily: 'Microsoft YaHei',
                  fontSize: 10, // 文字的字体大小
                  textBorderColor: '#FFFFFF',
                  textBorderWidth: 2,
                  textShadowBlur: 1,
                  textShadowColor: '(255, 255, 255, 0.2)'
                },
                formatter: '{b}'
              }
            }
          }
        ],
        itemStyle: {
          emphasis: {
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowColor: 'rgba(30, 144, 255，0.5)'
          }
        },
        color: ['#FFD54F', '#64B5F6', '#FF8A65', '#AED581', '#F06292', '#BA68C8', '#78909C'] // 300配色卡
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
