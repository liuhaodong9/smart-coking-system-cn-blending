<template>
  <div>
    <div class="CoalData">
      <div class='selectbutton'>
      <p></p>
      <span class='subtitle_4'>配煤方案辅助决策</span>
      <el-button id='b21' class='button_2' size="mini" @click='switchAIpredict'>AI算法最优配煤方案预测</el-button>
      <el-button id='b20' class='button_2' size="mini" >配煤基本理论知识</el-button>
      <!-- <el-button id='b12' class='button_2' size="mini" @click='switchAIComparison'>预测性能对比</el-button> -->
      </div>
    <el-card class="box-card_2">
      <p class='contenttitle_3'>配煤的目的</p>
      <p class='description_3'>配煤的目的在于使各种煤之间性质上取长补短，符合焦炉的生产要求，生产出满足质量要求的优质焦炭，并副产炼焦化学产品，实现煤炭资源的合理利用。</p>
      <p class='description_3'>冶金焦的质量要求是：灰分低、硫分少、强度高、各向异性程度大。这种要求在常规炼焦方法条件下，用单种煤炼焦难以实现。此外，由于煤种的相对储量、分布和开采能力的制约，不可能进行大规模的单种煤炼焦生产，特别是优质炼焦煤资源有限，工业上必须采用配煤炼焦以确保焦炭质量和合理利用煤炭资源。</p>
      <p class='contenttitle_3'>配煤的原则</p>
      <p class='description_3'>(1) 配煤质量应与煤料的预处理工艺及炼焦条件相适应，使焦炭的质量达到规定的指标，满足用户的质量要求，同时控制配煤的成本，提高经济效益。</p>
      <p class='description_3'>(2) 煤源的数量可靠、质量稳定，符合本区域内煤炭资源的组成，有利于扩大炼焦煤源，同时缩短平均运距。</p>
      <p class='description_3'>(3) 在保证焦炭质量的前提下，尽量多配用高挥发分煤，既有利于降低生产成本又有利于增加化学产品和煤气产量。</p>
      <p class='contenttitle_3'>配煤的质量要求</p>
      <p class='description_3'>(1) 配煤灰分：配煤中的灰分在炼焦后全部残留于焦炭中，成为生产冶金焦的主要质量指标之一，因此应当控制配煤的灰分。煤的成焦率一般在75%左右。由于配煤中灰分全部转入焦炭中，所以焦炭的灰分要比配煤灰分高1.3倍左右。在生产上要求配煤灰分小于10%。</p>
      <p class='description_3'>(2) 配煤硫分：硫分煤中通常以黄铁矿、硫酸盐和硫的有机化合物三种形式存在。通常洗选一般只能除去黄铁矿硫，而配煤中的硫约有85%-90%残留于焦炭中。因此配煤中的硫分越低越好，炼焦配煤的硫分一般应小于1.0%。</p>
      <p class='description_3'>(3) 配煤挥发分：为了满足钢铁工业对冶金焦的需要，又能尽量多生产化学产品，顶装机焦配煤干燥无灰基挥发分一般在25%-30%。受资源限制，我国炼钢焦配煤中的气煤用量一般较高，有的焦化厂配煤挥发分达到32%。近几年来，根据我国肥煤、主焦煤紧俏的资源情况，大力推广捣固炼焦新工艺，气煤配比可以达到 75%，配煤干燥无灰基挥发分超过34%。</p>
      <p class='description_3'>(4) 配煤的胶质层厚度：胶质层是表示煤在加热时产生液体的数量的指标。配煤中必须具有一定的液体物质来粘结其他不能熔融的物质，使之成为坚固的冶金焦炭。配煤对胶质层的要求厚度为15-20毫米。</p>
      <p class='contenttitle_3'>煤岩学在配煤炼焦的应用</p>
      <p class='description_3'>镜质体反射率直方图可以直观反映出不同变质程度煤的混合情况。GB/T 15591-2013规定了商品煤混煤类型的判别方法，以反射率间隔0.05%为半阶，分别统计各间隔的测点数，并计算出其分布频率，以频率为纵坐标，随机反射率为横坐标绘制出反射率分布图，从镜质体反射率间隔为0.05%的频率分布图中统计“凹口数”。根据镜质体反射率标准差和反射率直方图中的凹口数，来判别混煤类型。</p>
      <p class='description_3'>(1) 单煤的反射率直方图应具备的特点为单峰，且反射率分布范围窄，标准差较小，通常小于0.10。</p>
      <p class='description_3'>(2) 两种及以上变质程度相近的煤混合而成的煤其反射率直方图通常也表现为单峰，但是往往具有反射率分布范围大，标准差也较大的特点。</p>
      <p class='description_3'>(3) 两种及以上变质程度相差较大的煤构成的混煤其反射率直方图表现为双峰或多峰，同时反射率分布范围大，标准差较大。</p>
    </el-card>
    </div>
  </div>
</template>

<script>
export default {
  methods: {
    switchAIpredict() {
      this.$router.push('/BlendingPrediction') // 点击首页按钮切换到coalDataPresent页面
    },
    switchAIComparison() {
    }
  }
}
</script>

<style>
.CoalData{
  position: absolute;
  height: 96%;
  width: 95%;
}
.box-card_2{
  width: 100% !important;
  height: 150%;
  /* overscroll-behavior: contain; */
  background-color: rgba(0,0,0,0.3) !important;
  border: 0px !important;
}
.button_2{
  /* background:linear-gradient(to top right,#19968e,#27524f,#011629,#011629) !important; */
  /* border: #22b39a !important;; */
  background-color: rgba(0,0,0,0.3) !important;
  border-radius: 0 !important;
  border: none !important;
  font-family: '微软雅黑';
  font-weight:500 !important;
  color: rgb(255, 255, 255) !important;
}
#b27{
  right: 25%;
  top: -2%;
  border: 1px solid #09927b !important;
}
#b28{
  right: 12.5%;
  top: -2%;
  color: rgb(94, 255, 0) !important;
  border: 1px solid #09927b !important;
}
.button_2:hover{
  color: rgb(3, 205, 205) !important;
}
.contenttitle_3{
  color: rgb(94, 255, 0);
  font-family: '微软雅黑';
  font-weight:bold;
  font-size: 80%;
  text-align: left;
  margin-top: 0%;
  cursor:default;
}
.description_3{
  color: white;
  font-size: 80%;
}
</style>
