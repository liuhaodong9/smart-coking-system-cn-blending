import Vue from 'vue'
import VueRouter from 'vue-router'
import Login from '../components/Login.vue'
import CokeDigitalTwin from '../components/DigitalTwin/cokeDigitalTwin.vue'
import Quenching from '../components/AutoCokingDevice/quenching.vue'
import HomeNew from '../components/Home_new.vue'
import EchartPage from '../components/EchartData/EchartPage.vue' // 导入echart 数据的页面
import CoalDataProcessing from '../components/coalData/CoalDataProcessing'
import BlendingRatioPrediction from '../components/coalBlending/BlendingRatioPrediction'
import CokingStandard from '../components/CokingStandard/CokingStandard'
import coalDataPresent from '../components/coalData/CoalDataPresent'
import coalDataClassify from '../components/coalData/CoalDataClassify'
import CokingTheory from '../components/cokeQuality/CokingTheory'
import BlendingTheory from '../components/coalBlending/BlendingTheory'
import CoalDataClassifySelection from '../components/coalData/CoalDataClassifySelection'
import CokeQualitySelection from '../components/cokeQuality/CokeQualitySelection'
import CokeQualityPredictionAdaboost from '../components/cokeQuality/CokeQualityPredictionAdaboost'
import CokeQualityPredictionANN from '../components/cokeQuality/CokeQualityPredictionANN'
import CokeQualityPredictionCNN from '../components/cokeQuality/CokeQualityPredictionCNN'
import CokeQualityPredictionDT from '../components/cokeQuality/CokeQualityPredictionDT'
import CokeQualityPredictionET from '../components/cokeQuality/CokeQualityPredictionET'
import CokeQualityPredictionKNN from '../components/cokeQuality/CokeQualityPredictionKNN'
import CokeQualityPredictionLasso from '../components/cokeQuality/CokeQualityPredictionLasso'
import CokeQualityPredictionLR from '../components/cokeQuality/CokeQualityPredictionLR'
import CokeQualityPredictionRF from '../components/cokeQuality/CokeQualityPredictionRF'
import CokeQualityPredictionSVM from '../components/cokeQuality/CokeQualityPredictionSVM'
import BlendingPrediction from '../components/coalBlending/BlendingPrediction'
import CokingForeignStandard from '../components/CokingStandard/CokingForeignStandard'

Vue.use(VueRouter)

const router = new VueRouter({
  routes: [
    { path: '/', redirect: '/login' }, // 访问/时重定向到login路径
    { path: '/login', component: Login },
    {
      path: '/home_new',
      component: HomeNew,
      redirect: '/EchartPage',
      // 子路由的路径配置
      children: [
        { path: '/EchartPage', component: EchartPage },
        { path: '/cokeDigitalTwin', component: CokeDigitalTwin },
        { path: '/quenching', component: Quenching },
        { path: '/CoalDataProcessing', component: CoalDataProcessing },
        { path: '/CokingTheory', component: CokingTheory },
        { path: '/BlendingRatioPrediction', component: BlendingRatioPrediction },
        { path: '/BlendingTheory', component: BlendingTheory },
        { path: '/CokingStandard', component: CokingStandard },
        { path: '/CokingForeignStandard', component: CokingForeignStandard },
        { path: '/CoalDataPresent', component: coalDataPresent },
        { path: '/CoalDataClassify', component: coalDataClassify },
        { path: '/CoalDataClassifySelection', component: CoalDataClassifySelection },
        { path: '/CokeQualitySelection', component: CokeQualitySelection },
        { path: '/CokeQualityPredictionAdaboost', component: CokeQualityPredictionAdaboost },
        { path: '/CokeQualityPredictionANN', component: CokeQualityPredictionANN },
        { path: '/CokeQualityPredictionCNN', component: CokeQualityPredictionCNN },
        { path: '/CokeQualityPredictionDT', component: CokeQualityPredictionDT },
        { path: '/CokeQualityPredictionET', component: CokeQualityPredictionET },
        { path: '/CokeQualityPredictionKNN', component: CokeQualityPredictionKNN },
        { path: '/CokeQualityPredictionXGBoost', component: CokeQualityPredictionLasso },
        { path: '/CokeQualityPredictionLR', component: CokeQualityPredictionLR },
        { path: '/CokeQualityPredictionRF', component: CokeQualityPredictionRF },
        { path: '/CokeQualityPredictionSVM', component: CokeQualityPredictionSVM },
        { path: '/BlendingPrediction', component: BlendingPrediction }] // EchartPage是home_new组件的el-main的children子组件
    }]
})

// 挂载路由导航守卫, 用户直接访问不是login的页面，会强制跳转至登录界面
router.beforeEach((to, from, next) => {
  // to 将要访问的路径
  // from 代表从哪个路径跳转而来
  // next 是一个函数，表示放行

  if (to.path === '/login') return next()
  // 获取token,等之后添加
  const tokenStr = window.sessionStorage.getItem('token')
  if (!tokenStr) return next('login')
  next()
})

export default router
