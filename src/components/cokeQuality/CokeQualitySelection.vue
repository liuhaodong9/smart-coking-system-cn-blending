<template>
    <div>
        <div class="CoalData_2">
            <div class='selectbutton'>
                <p></p>
                <span class='subtitle_2'>焦炭质量预测</span>
                <el-button id='b14' class='button_2' size="mini" >AI算法焦炭质量预测</el-button>
                <el-button id='b13' class='button_2' size="mini" @click='switchCoalTheory'>炼焦过程基础知识</el-button>
                <!-- <el-button id='b15' class='button_2' size="mini">预测性能对比</el-button> -->
            </div>
            <el-card class="box-card_3">
                <el-button class='button_prediction_1' type="primary" @click='switchCokeQualitySelection_1'>CNN-CQP算法<sup>氢一专利</sup></el-button>
                <el-button class='button_prediction_2' type="primary" @click='switchCokeQualitySelection_2'>人工神经网络算法<sup>文献1</sup></el-button>
                <el-button class='button_prediction_3' type="primary" @click='switchCokeQualitySelection_3'>随机森林算法<sup>文献2</sup></el-button>
                <el-button class='button_prediction_4' type="primary" @click='switchCokeQualitySelection_4'>决策树算法<sup>文献3</sup></el-button>
                <el-button class='button_prediction_5' type="primary" @click='switchCokeQualitySelection_6'>支持向量机算法<sup>文献4</sup></el-button>
                <el-button class='button_prediction_6' type="primary" @click='switchCokeQualitySelection_7'>最近邻算法<sup>文献5</sup></el-button>
                <el-button class='button_prediction_7' type="primary" @click='switchCokeQualitySelection_9'>线性回归算法<sup>文献6</sup></el-button>
                <el-button class='button_prediction_8' type="primary" @click='switchCokeQualitySelection_10'>XGBoost算法<sup>文献7</sup></el-button>
            <p>ㅤ</p>
            <p class='blendNote'>*点击指定算法板块进入到数据库界面，勾选待预测的煤数据后，点击"开始预测"按钮进行计算</p>
            <p class='blendNote'>*待进行焦炭质量预测的煤种数据需带有水分、灰分、挥发分、硫分、粘结指数G，X和Y等参数</p>
            <p class='blendNote'><sup>参考文献1</sup>Maharana, Sulata, et al. "Artificial neural network prediction for coke strength after reaction and data analysis." World Academy of Science, Engineering and Technology 45 (2010): 556-570.</p>
            <p class='blendNote'><sup>参考文献2</sup>Chelgani, S. Chehreh, S. S. Matin, and James C. Hower. "Explaining relationships between coke quality index and coal properties by Random Forest method." Fuel 182 (2016): 754-760.</p>
            <p class='blendNote'><sup>参考文献3</sup>程泽凯, et al. "基于梯度提升决策树的焦炭质量预测模型研究." 重庆工商大学学报 (自然科学版) 38.5 (2021): 55-60.</p>
            <p class='blendNote'><sup>参考文献4</sup> Chen, Hong Jun, and Jin Feng Bai. "A Coke Quality Prediction Model Based on Support Vector Machine." Advanced Materials Research. Vol. 690. Trans Tech Publications Ltd, 2013.</p>
            <p class='blendNote'><sup>参考文献5</sup> 闫立强,雷磊,王保荣,李文超,王杰平,谢全安."基于煤质综合指标的焦炭质量预测" 洁净煤技术.027(2022):175-180.</p>
            <p class='blendNote'><sup>参考文献6</sup>Zhang, Qun, et al. "Prediction of coke quality at Baosteel." Fuel Processing Technology 86.1 (2004): 1-11.</p>
            <p class='blendNote'><sup>参考文献7</sup>Homafar, A., H. Nasiri, and S. Chehreh Chelgani. "Modeling coking coal indexes by SHAP-XGBoost: Explainable artificial intelligence method." Fuel Communications 13 (2022): 100078.</p>
            </el-card>
        </div>
    </div>
</template>

<script>
export default {
  methods: {
    switchCokeQualitySelection_1() {
      this.$router.push('/CokeQualityPredictionCNN') // 点击首页按钮切换到coalDataPresent页面
    },
    switchCokeQualitySelection_2() {
      this.$router.push('/CokeQualityPredictionANN') // 点击首页按钮切换到coalDataPresent页面
    },
    switchCokeQualitySelection_3() {
      this.$router.push('/CokeQualityPredictionRF') // 点击首页按钮切换到coalDataPresent页面
    },
    switchCokeQualitySelection_4() {
      this.$router.push('/CokeQualityPredictionDT') // 点击首页按钮切换到coalDataPresent页面
    },
    switchCokeQualitySelection_5() {
      this.$router.push('/CokeQualityPredictionET') // 点击首页按钮切换到coalDataPresent页面
    },
    switchCokeQualitySelection_6() {
      this.$router.push('/CokeQualityPredictionSVM') // 点击首页按钮切换到coalDataPresent页面
    },
    switchCokeQualitySelection_7() {
      this.$router.push('/CokeQualityPredictionKNN') // 点击首页按钮切换到coalDataPresent页面
    },
    switchCokeQualitySelection_8() {
      this.$router.push('/CokeQualityPredictionAdaboost') // 点击首页按钮切换到coalDataPresent页面
    },
    switchCokeQualitySelection_9() {
      this.$router.push('/CokeQualityPredictionLR') // 点击首页按钮切换到coalDataPresent页面
    },
    switchCokeQualitySelection_10() {
      this.$router.push('/CokeQualityPredictionXGBoost') // 点击首页按钮切换到coalDataPresent页面
    },
    switchCoalTheory() {
      this.$router.push('/CokingTheory')
    }
  },
  created () {
    this.$emit('changeActiveStep', 3)
  }
}
</script>

<style>
.box-card_7{
  width: 100% !important;
  height: 30%;
  /* overscroll-behavior: contain; */
  background-color: rgba(0,0,0,0.3) !important;
  border: 0px !important;
  margin-top: 2% !important;
  display:flex;
  justify-content:center;
  align-items:center;
}
.box-card_8{
  width: 100% !important;
  height: 30%;
  /* overscroll-behavior: contain; */
  background-color: rgba(0,0,0,0.3) !important;
  border: 0px !important;
  display:flex;
  justify-content:center;
  align-items:center;
}
.button_prediction_1{
  background-color: #003B8E !important;
  border-color: #15ea43 !important;
  width: 30%;
  font-size: 120% !important;
  line-height: 187% !important; /*控制按钮的高度*/
  margin-top: 4% !important;
  margin-left: 3% !important;
}
.button_prediction_2{
  background-color: #003B8E !important;
  border-color: #15ea43 !important;
  width: 30%;
  font-size: 120% !important;
  line-height: 150% !important; /*控制按钮的高度*/
  margin-top: 2% !important;
  margin-left: 2% !important;
}
.button_prediction_3{
  background-color: #1564BF !important;
  border-color: #15ea43  !important;
  width: 30%;
  font-size: 120% !important;
  line-height: 150% !important; /*控制按钮的高度*/
  margin-top: 2% !important;
  margin-left: 2% !important;
}
.button_prediction_4{
  background-color: #1564BF !important;
  border-color: #15ea43  !important;
  width: 30%;
  font-size: 120% !important;
  line-height: 150% !important; /*控制按钮的高度*/
  margin-top: 2% !important;
  margin-left: 3% !important;
}
.button_prediction_5{
  background-color: #459cff !important;
  border-color: #15ea43  !important;
  width: 30%;
  font-size: 120% !important;
  line-height: 150% !important; /*控制按钮的高度*/
  margin-top: 2% !important;
  margin-left: 2% !important;
}
.button_prediction_6{
  background-color: #459cff !important;
  border-color: #15ea43  !important;
  width: 30%;
  font-size: 120% !important;
  line-height: 150% !important; /*控制按钮的高度*/
  margin-top: 2% !important;
  margin-left: 2% !important;
}
.button_prediction_7{
  background-color: #5E91F2 !important;
  border-color: #15ea43  !important;
  width: 30%;
  font-size: 120% !important;
  line-height: 150% !important; /*控制按钮的高度*/
  margin-top: 2% !important;
  margin-left: 3% !important;
}
.button_prediction_8{
  background-color: #5E91F2 !important;
  border-color: #15ea43 !important;
  width: 30%;
  font-size: 120% !important;
  line-height: 150% !important; /*控制按钮的高度*/
  margin-top: 2% !important;
  margin-left: 2% !important;
}
.button_prediction_9{
  background-color: #6b9efc !important;
  border-color: #15ea43  !important;
  width: 30%;
  font-size: 120% !important;
  line-height: 150% !important; /*控制按钮的高度*/
  margin-top: 2% !important;
  margin-left: 2% !important;
}
.button_prediction_10{
  background-color: #6b9efc !important;
  border-color: #15ea43 !important;
  width: 30%;
  font-size: 120% !important;
  line-height: 150% !important; /*控制按钮的高度*/
  margin-top: 2% !important;
  margin-left: 3% !important;
}

</style>
