<template>
  <div>
    <div class="CoalData">
      <div class='selectbutton'>
        <p></p>
        <span class='subtitle'>煤数据处理</span>
        <el-button id='b2' class='button_2' size="mini" @click='switchCoalDataPresent'>文本煤数据展示</el-button>
        <el-button id='b3' class='button_2' size="mini" @click='switchCoalDataClassify'>煤数据自动分类</el-button>
        <el-button id='b1' class='button_2' size="mini">煤数据参数解读</el-button>
      </div>
    <el-card class="box-card_2">
      <p class='contenttitle'>煤的工业分析</p>
      <p class='description'>■ 水分：煤的水分主要包括内水分，外水分和全水分。内水分指的是吸附在煤粒的外表面和较大的孔隙中的水分，而内水分则指的是存在于较小的孔隙中的水分，二者质量之和则称为全水分。</p>
      <p class='description'>■ 灰分：是指煤在一定条件下完全燃烧后得到的残渣。残渣量的多少主要与煤中矿物质含量关系密切，也与测定条件有关。</p>
      <p class='description'>■ 挥发分：在高温条件下(900℃)下，将煤样隔绝空气加热一段时间，煤的有机质发生热解反应，形成部分小分子的化合物，在测定条件下呈气态析出，该部分挥发的化合物占煤样质量的百分数称为挥发分。</p>
      <p class='description'>■ 固定碳：从测定挥发分后的煤样残渣中减去灰分后的残留物的有机质占煤样质量的百分数称为固定碳。</p>
      <p class='contenttitle'>煤的元素分析</p>
      <p class='description'>■ 碳元素：碳是构成煤大分子骨架最重要的元素，也是煤燃烧过程中放出热能的最主要的元素之一。随着煤化程度的提高，煤中的碳元素逐渐增加。</p>
      <p class='description'>■ 氢元素：氢是煤中第二重要的元素，主要存在于煤分子的侧链和官能团上，随煤化程度的提高呈下降趋势。</p>
      <p class='description'>■ 氧元素：氧是构成煤有机质的重要元素，主要存在于煤分子的含氧官能团上，随煤化程度的提高，煤中的氧元素迅速下降。</p>
      <p class='description'>■ 氮元素：煤中的氮元素含量较少，一般为0.5%~1.8%，随煤化程度提高而呈下降趋势。</p>
      <p class='description'>■ 硫元素：煤中的硫分为有机硫和无机硫，是煤中的有害元素。</p>
      <p class='contenttitle'>煤的岩相分析</p>
      <p class='description'>■ 镜质组：主要由成煤植物的纤维形成，在结焦过程中能熔融、粘结，是活性物质。</p>
      <p class='description'>■ 丝质组：主要由成煤植物的纤维形成，但和镜质组形成条件不同。在结焦过程中不熔融、粘结，基本上保持原来的形态，是惰性物质。</p>
      <p class='description'>■ 半镜质组：介于镜质组和丝质组之间的一过度性组分。</p>
      <p class='description'>■ 稳定组：由植物的繁殖器官、保护器官等化学性质稳定的部分形成，挥发分高，是一种活性物质。</p>
      <p class='description'>■ 镜质组反射率：该指标可以准确表征煤的变质程度。一般的，该值高，其变质程度高，一般相应的，挥发分低，固定碳含量高，氢含量低。</p>
      <p class='description'>■ 镜质组反射率分布：该指标可以比较准确的反映炼焦煤的质量。在控制炼焦煤质量方面，可以用来鉴定混煤。单一煤有且只有一个峰，由几种煤混配而成，则显示多个峰。</p>
    </el-card>
    </div>
  </div>
</template>

<script>
export default {
  methods: {
    switchCoalDataPresent() {
      this.$router.push('/CoalDataPresent') // 点击首页按钮切换到coalDataPresent页面
    },
    switchCoalDataClassify() {
      this.$router.push('/CoalDataClassifySelection')
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
  height: 140%;
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
#b1{
  color: rgb(248, 182, 0) !important;
  top: -2%;
  border: 1px solid #09927b !important;
}
#b2{
  right: 12.5%;
  top: -2%;
  border: 1px solid #09927b !important;
}
#b3{
  right: 0%;
  top: -2%;
  border: 1px solid #09927b !important;
}
.button_2:hover{
  color: rgb(3, 205, 205) !important;
}
.contenttitle{
  color: rgb(248, 182, 0) !important;
  font-family: '微软雅黑';
  font-weight:bold;
  font-size: 80%;
  text-align: left;
  margin-top: 0%;
  cursor:default;
}
.description{
  color: white;
  font-size: 80%;
}
.subtitle{
  position: absolute;
  color: rgb(248, 182, 0);
  left: 0%;
  font-size: 90%;
}
</style>
