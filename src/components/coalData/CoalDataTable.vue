<template>
<div class='table'>
      <pl-table id='coalTable' :row-style="tableRowClassName" :data-changes-scroll-top='false' ref='CoalTable' big-data-checkbox highlight-current-row :row-height="35" :data = 'coalList.slice((cur_page-1)*pageSize,cur_page*pageSize)' use-virtual border :header-cell-style="{background:'white',color:'#494949',textAlign:'center', border:'1px solid #BFBFBF',fontSize: '14px'}" :height="height" :key='Math.random()' :default-sort="{prop: 'id', order: 'ascending'}" size='mini' :cell-style="{padding:'0px',fontSize: '14px'}" fixedColumnsRoll>
                <pl-table-column align="center" fixed label='序号' prop='id' key="1" class='order'></pl-table-column>
                <pl-table-column align="center" fixed label='煤样名称' prop='coal_name' key="2"></pl-table-column>
                <pl-table-column align="center" fixed label='煤种' prop='coal_type' key="4"></pl-table-column> <!-- 加prop可以直接渲染值 -->
                <pl-table-column align="center" fixed label='存储量(吨)' width="90px" prop='store_number' key="4"></pl-table-column> <!-- 加prop可以直接渲染值 -->
                <pl-table-column align="center" label='价格(吨)' key="5" prop='coal_price'></pl-table-column>
                <pl-table-column align="center" label='原始试验煤样筛分组成/%' width="110px" v-if='show_1' key="6">
                    <pl-table-column align="center" label='>13mm' width="120px" prop='ori_coal_13mm' key="7"></pl-table-column>
                    <pl-table-column align="center" label='13~10mm' width="120px" prop='ori_coal_13_10mm' key="8"></pl-table-column>
                    <pl-table-column align="center" label='10~8mm' width="120px" prop='ori_coal_10_8mm' key="9"></pl-table-column>
                    <pl-table-column align="center" label='8~6mm' width="110px" prop='ori_coal_8_6mm' key="10"></pl-table-column>
                    <pl-table-column align="center" label='6~5mm' width="110px" prop='ori_coal_6_5mm' key="11"></pl-table-column>
                    <pl-table-column align="center" label='5~4mm' width="110px" prop='ori_coal_5_4mm' key="12"></pl-table-column>
                    <pl-table-column align="center" label='4~3mm' width="110px" prop='ori_coal_4_3mm' key="13"></pl-table-column>
                    <pl-table-column align="center" label='3~2mm' width="110px" prop='ori_coal_3_2mm' key="14"></pl-table-column>
                    <pl-table-column align="center" label='2~1mm' width="110px" prop='ori_coal_2_1mm' key="15"></pl-table-column>
                    <pl-table-column align="center" label='1~0.5mm' width="110px" prop='ori_coal_1_05mm' key="16"></pl-table-column>
                    <pl-table-column align="center" label='<0.5mm' width="110px" prop='ori_coal_05mm' key="17"></pl-table-column>
                    <pl-table-column align="center" label='合计' width="110px" prop='ori_coal_total' key="18"></pl-table-column>
                    <pl-table-column align="center" label='细度/%' width="110px" prop='ori_coal_fineness' key="19"></pl-table-column>
                </pl-table-column>
                <pl-table-column align="center" label='粉碎后筛分组成/%' v-if='show_2' key="20"> <!-- v-if=false或true来显示列和隐藏列 -->
                    <pl-table-column align="center" label='粉碎后水分%' width="110px" prop='sma_coal_moi' key="21"></pl-table-column>
                    <pl-table-column align="center" label='>6mm' width="120px" prop='sma__coal_6mm' key="22"></pl-table-column>
                    <pl-table-column align="center" label='6~5mm' width="120px" prop='sma__coal_6_5mm' key="23"></pl-table-column>
                    <pl-table-column align="center" label='5~4mm' width="120px" prop='sma__coal_5_4mm' key="24"></pl-table-column>
                    <pl-table-column align="center" label='4~3mm' width="120px" prop='sma__coal_4_3mm' key="25"></pl-table-column>
                    <pl-table-column align="center" label='3~2mm' width="120px" prop='sma__coal_3_2mm' key="26"></pl-table-column>
                    <pl-table-column align="center" label='2~1mm' width="120px" prop='sma__coal_2_1mm' key="27"></pl-table-column>
                    <pl-table-column align="center" label='1~0.5mm' width="120px" prop='sma__coal_1_05mm' key="28" ></pl-table-column>
                    <pl-table-column align="center" label='<0.5mm' width="120px" prop='sma__coal_05mm' key="29"></pl-table-column>
                    <pl-table-column align="center" label='合计' width="120px" prop='sma__coal_total' key="30"></pl-table-column>
                    <pl-table-column align="center" label='细度<3mm' width="120px" prop='sma_coal_fineness' key="31"></pl-table-column>
                </pl-table-column>
                <pl-table-column align="center" label='煤样工业分析' v-if='show_3' key="32">
                    <pl-table-column align="center" label='水分(Mad)' width="110px" prop='coal_mad' key="33"></pl-table-column>
                    <pl-table-column align="center" label='灰分(Ad)' width="120px" prop='coal_ad' key="34"></pl-table-column>
                    <pl-table-column align="center" label='挥发分(Vdaf)' width="110px" prop='coal_vdaf' key="35"></pl-table-column>
                    <pl-table-column align="center" label='固定碳(FCd)' width="110px" prop='coal_fcd' key="36"></pl-table-column>
                    <!-- <pl-table-column align="center" label='Vd' prop='coal_vd' key="37"></pl-table-column>
                    <pl-table-column align="center" label='Aad' prop='coal_ada' key="38"></pl-table-column>
                    <pl-table-column align="center" label='Vad' prop='coal_vad' key="39"></pl-table-column>
                    <pl-table-column align="center" label='FCad' prop='coal_fcad' key="40"></pl-table-column> -->
                    <pl-table-column align="center" label='全硫(St,d)' width="110px" prop='coal_std' key="41"></pl-table-column>
                </pl-table-column>
                <!-- <pl-table-column align="center" label='元素分析(分析基)' v-if='show_4' key="42">
                    <pl-table-column align="center" label='氢(Had)' width="110px" prop='coal_ana_had' key="43"></pl-table-column>
                    <pl-table-column align="center" label='碳(Cad)' width="120px" prop='coal_ana_cad' key="44"></pl-table-column>
                    <pl-table-column align="center" label='氮(Nad)' width="110px" prop='coal_ana_nad' key="45"></pl-table-column>
                    <pl-table-column align="center" label='氧(Oad)' width="110px" prop='coal_ana_oad' key="46"></pl-table-column>
                </pl-table-column>
                <pl-table-column align="center" label='元素分析(干基)' v-if='show_4' key="47">
                    <pl-table-column align="center" label='氢(Hd)' width="110px" prop='coal_dry_hd' key="48"></pl-table-column>
                    <pl-table-column align="center" label='碳(Cd)' width="120px" prop='coal_dry_cd' key="49"></pl-table-column>
                    <pl-table-column align="center" label='氮(Nd)' width="110px" prop='coal_dry_nd' key="50"></pl-table-column>
                    <pl-table-column align="center" label='氧(Od)' width="110px" prop='coal_dry_od' key="51"></pl-table-column>
                </pl-table-column> -->
                <pl-table-column align="center" label='元素分析(干燥无灰基)' v-if='show_4' key="52">
                    <pl-table-column align="center" label='氢(Hdaf)' width="110px" prop='coal_drynoash_hdaf' key="53"></pl-table-column>
                    <pl-table-column align="center" label='碳(Cdaf)' width="120px" prop='coal_drynoash_cdaf' key="54"></pl-table-column>
                    <pl-table-column align="center" label='氮(Ndaf)' width="110px" prop='coal_drynoash_ndaf' key="55"></pl-table-column>
                    <pl-table-column align="center" label='氧(Odaf)' width="110px" prop='coal_drynoash_odaf' key="56"></pl-table-column>
                </pl-table-column>
                <pl-table-column align="center" label='粘结指数(G)' width="110px" v-if='show_5' prop='G' key="57"></pl-table-column>
                <pl-table-column align="center" label='胶质层指数/mm' v-if='show_5' key="58">
                    <pl-table-column align="center" label='X' width="110px" prop='X' key="59"></pl-table-column>
                    <pl-table-column align="center" label='Y' width="120px" prop='Y' key="60"></pl-table-column>
                </pl-table-column>
                <pl-table-column align="center" label='奥亚膨胀度' v-if='show_6'>
                    <pl-table-column align="center" label='T1/℃' width="110px" prop='T1'></pl-table-column>
                    <pl-table-column align="center" label='T2/℃' width="120px" prop='T2'></pl-table-column>
                    <pl-table-column align="center" label='T3/℃' width="120px" prop='T3'></pl-table-column>
                    <pl-table-column align="center" label='a/%' width="120px" prop='a'></pl-table-column>
                    <pl-table-column align="center" label='b/%' width="120px" prop='b'></pl-table-column>
                </pl-table-column>
                <pl-table-column align="center" label='基氏流动度' v-if='show_7'>
                    <pl-table-column align="center" label='Tp/℃' width="110px" prop='Tp'></pl-table-column>
                    <pl-table-column align="center" label='Tmax/℃' width="120px" prop='Tmax'></pl-table-column>
                    <pl-table-column align="center" label='Tk/℃' width="120px" prop='Tk'></pl-table-column>
                    <pl-table-column align="center" label='αmax/度/分' width="120px" prop='amax'></pl-table-column>
                    <pl-table-column align="center" label='Tk-Tp' width="120px" prop='Tk_Tp'></pl-table-column>
                </pl-table-column>
                <pl-table-column align="center" label='煤灰熔点/℃' v-if='show_8'>
                    <pl-table-column align="center" label='变形温度(DT)' width="110px" prop='DT'></pl-table-column>
                    <pl-table-column align="center" label='软化温度(ST)' width="120px" prop='ST'></pl-table-column>
                    <pl-table-column align="center" label='半球温度(HT)' width="120px" prop='HT'></pl-table-column>
                    <pl-table-column align="center" label='流动温度(FT)' width="120px" prop='FT'></pl-table-column>
                </pl-table-column>
                <pl-table-column align="center" label='灰成分/%' v-if='show_9'>
                    <pl-table-column align="center" label='SiO2' width="110px" prop='SiO2'></pl-table-column>
                    <pl-table-column align="center" label='Al2O3' width="120px" prop='Al2O3'></pl-table-column>
                    <pl-table-column align="center" label='Fe2O3' width="120px" prop='Fe2O3'></pl-table-column>
                    <pl-table-column align="center" label='CaO' width="120px" prop='CaO'></pl-table-column>
                    <pl-table-column align="center" label='MgO' width="120px" prop='MgO'></pl-table-column>
                    <pl-table-column align="center" label='P2O5' width="120px" prop='P2O5'></pl-table-column>
                    <pl-table-column align="center" label='Na2O' width="120px" prop='Na2O'></pl-table-column>
                    <pl-table-column align="center" label='K2O' width="120px" prop='K2O'></pl-table-column>
                    <pl-table-column align="center" label='TiO2' width="120px" prop='TiO2'></pl-table-column>
                    <pl-table-column align="center" label='SO3' width="120px" prop='SO3'></pl-table-column>
                    <pl-table-column align="center"  label='求和' width="120px" prop='ash_total'></pl-table-column>
                </pl-table-column>
                <pl-table-column align="center" label='煤样显微组分分析' v-if='show_10'>
                    <pl-table-column align="center" label='镜质组(V)' width="110px" prop='V'></pl-table-column>
                    <pl-table-column align="center" label='惰质组(I)' width="120px" prop='I'></pl-table-column>
                    <pl-table-column align="center" label='壳质组(E)' width="120px" prop='E'></pl-table-column>
                    <pl-table-column align="center" label='矿物(M)' width="120px" prop='M'></pl-table-column>
                    <pl-table-column align="center" label='活惰比' width="120px" prop='live_idle_ratio'></pl-table-column>
                    <pl-table-column align="center" label='平均最大反射率(Rmax)' width="180px" prop='Rmax'></pl-table-column>
                    <pl-table-column align="center" label='标准方差' width="120px" prop='micro_var'></pl-table-column>
                    <pl-table-column align="center" label='类型' width="120px" prop='micro_type'></pl-table-column>
                </pl-table-column>
                <pl-table-column align="center" label='炼焦过程参数' v-if='show_11'>
                    <pl-table-column align="center" label='炉型' width="110px" prop='oven_type'></pl-table-column>
                    <pl-table-column align="center" label='炼焦方式' width="120px" prop='coking_style'></pl-table-column>
                    <pl-table-column align="center" label='入炉干基质量/kg' width="150px" prop='dry_quality'></pl-table-column>
                    <pl-table-column align="center" label='堆密度t/m³' width="120px" prop='heap_density'></pl-table-column>
                    <pl-table-column align="center" label='入炉煤水分%' width="120px" prop='oven_moi'></pl-table-column>
                    <pl-table-column align="center" label='升温制度' width="120px" prop='up_temper'></pl-table-column>
                    <pl-table-column align="center" label='落下次数' width="120px" prop='down_number'></pl-table-column>
                    <pl-table-column align="center" label='热态焦炭质量kg' width="150px" prop='hot_coke_qulity'></pl-table-column>
                    <pl-table-column align="center" label='热成焦率%' width="120px" prop='hot_ratio_coke'></pl-table-column>
                    <pl-table-column align="center" label='熄焦后重量kg' width="150px" prop='quench_coke_weight'></pl-table-column>
                    <pl-table-column align="center" label='焦炭水分%' width="120px" prop='coke_moi'></pl-table-column>
                    <pl-table-column align="center" label='成焦率%' width="120px" prop='ratio_coke'></pl-table-column>
                </pl-table-column>
                <pl-table-column align="center" label='炼焦温度参数' v-if='show_12'>
                    <pl-table-column align="center" label='炼焦日期' width="110px" prop='coking_date'></pl-table-column>
                    <pl-table-column align="center" label='入炉时间' width="120px" prop='coking_start_time'></pl-table-column>
                    <pl-table-column align="center" label='中心到100℃时间' width="150px" prop='center_100_time'></pl-table-column>
                    <pl-table-column align="center" label='中心到500℃时间' width="150px" prop='center_500_time'></pl-table-column>
                    <pl-table-column align="center" label='中心到900℃时间' width="150px" prop='center_900_time'></pl-table-column>
                    <pl-table-column align="center" label='出炉时间' width="120px" prop='coking_end_time'></pl-table-column>
                    <pl-table-column align="center" label='出炉中心温度℃' width="150px" prop='coking_end_temp'></pl-table-column>
                </pl-table-column>
                <pl-table-column align="center" label='焦炭工业分析/%' v-if='show_13'>
                    <pl-table-column align="center" label='水分(Mad)' width="120px" prop='coke_mad'></pl-table-column>
                    <pl-table-column align="center" label='灰分(Ad)' width="120px" prop='coke_ad'></pl-table-column>
                    <pl-table-column align="center" label='挥发分(Vdaf)' width="130px" prop='coke_vdaf'></pl-table-column>
                    <pl-table-column align="center" label='固定碳(FCd)' width="130px" prop='coke_fcd'></pl-table-column>
                    <pl-table-column align="center" label='Vd' width="130px" prop='coke_vd'></pl-table-column>
                    <pl-table-column align="center" label='Aad' width="120px" prop='coke_aad'></pl-table-column>
                    <pl-table-column align="center" label='Vad' width="130px" prop='coke_vad'></pl-table-column>
                    <pl-table-column align="center" label='FCad' width="130px" prop='coke_fcad'></pl-table-column>
                    <pl-table-column align="center" label='全硫(St,d)' width="130px" prop='coke_std'></pl-table-column>
                </pl-table-column>
                <pl-table-column align="center" label='焦炭筛分组成/%' v-if='show_14'>
                    <pl-table-column align="center" label='>80mm' width="120px" prop='coke_80mm'></pl-table-column>
                    <pl-table-column align="center" label='80-60mm' width="120px" prop='coke_80_60mm'></pl-table-column>
                    <pl-table-column align="center" label='60-40mm' width="130px" prop='coke_60_40mm'></pl-table-column>
                    <pl-table-column align="center" label='40-25mm' width="130px" prop='coke_40_25mm'></pl-table-column>
                    <pl-table-column align="center" label='25-20mm' width="130px" prop='coke_25_20mm'></pl-table-column>
                    <pl-table-column align="center" label='20-10mm' width="120px" prop='coke_20_10mm'></pl-table-column>
                    <pl-table-column align="center" label='<10mm' width="130px" prop='coke_10mm'></pl-table-column>
                    <pl-table-column align="center" label='<5mm方' width="130px" prop='coke_5mm'></pl-table-column>
                    <pl-table-column align="center" label='加和' width="130px" prop='coke_sum'></pl-table-column>
                    <pl-table-column align="center" label='>60mm' width="130px" prop='coke_60mm'></pl-table-column>
                    <pl-table-column align="center" label='平均粒度/mm' width="130px" prop='coke_fineness'></pl-table-column>
                </pl-table-column>
                <pl-table-column label='机械强度/%' v-if='show_15'>
                    <pl-table-column align="center" label='M40' width="120px" prop='coke_M40'></pl-table-column>
                    <pl-table-column align="center" label='M25' width="120px" prop='coke_M25'></pl-table-column>
                    <pl-table-column align="center" label='M10' width="120px" prop='coke_M10'></pl-table-column>
                </pl-table-column>
                <pl-table-column label='热性质/%' v-if='show_15'>
                    <pl-table-column align="center" label='CRI' width="120px" prop='coke_CRI'></pl-table-column>
                    <pl-table-column align="center" label='CSR' width="120px" prop='coke_CSR'></pl-table-column>
                </pl-table-column>
                <pl-table-column label='焦炭灰熔点' v-if='show_16'>
                    <pl-table-column align="center" label='变形温度(DT)' width="120px" prop='coke_DT'></pl-table-column>
                    <pl-table-column align="center" label='软化温度(ST)' width="120px" prop='coke_ST'></pl-table-column>
                    <pl-table-column align="center" label='半球温度(HT)' width="120px" prop='coke_HT'></pl-table-column>
                    <pl-table-column align="center" label='流动温度(FT)' width="120px" prop='coke_FT'></pl-table-column>
                </pl-table-column>
                <pl-table-column label='粉焦反应性(焦炭二氧化碳化学反应性)' v-if='show_17'>
                    <pl-table-column align="center" label='750' width="110px" prop='coke_750'></pl-table-column>
                    <pl-table-column align="center" label='800' width="120px" prop='coke_800'></pl-table-column>
                    <pl-table-column align="center" label='850' width="120px" prop='coke_850'></pl-table-column>
                    <pl-table-column align="center" label='900' width="120px" prop='coke_900'></pl-table-column>
                    <pl-table-column align="center" label='950' width="120px" prop='coke_950'></pl-table-column>
                    <pl-table-column align="center" label='1000' width="120px" prop='coke_1000'></pl-table-column>
                    <pl-table-column align="center" label='1050' width="120px" prop='coke_1050'></pl-table-column>
                    <pl-table-column align="center" label='1100' width="120px" prop='coke_1100'></pl-table-column>
                    <pl-table-column align="center" label='1150' width="120px" prop='coke_1150'></pl-table-column>
                    <pl-table-column align="center" label='1200' width="120px" prop='coke_1200'></pl-table-column>
                </pl-table-column>
                <pl-table-column label='气孔率' v-if='show_18'>
                    <pl-table-column align="center" label='显气孔率' width="120px" prop='coke_apparent_porosity'></pl-table-column>
                    <pl-table-column align="center" label='真相对密度' width="120px" prop='coke_real_density'></pl-table-column>
                    <pl-table-column align="center" label='假相对密度' width="120px" prop='coke_fake_density'></pl-table-column>
                    <pl-table-column align="center" label='总气孔率' width="120px" prop='coke_total_ratio'></pl-table-column>
                </pl-table-column>
                <pl-table-column
                fixed="right"
                label="操作"
                width="85">
                <template slot-scope="scope">
                    <el-button class='Tablebutton' @click="showDetailedDialog(scope.row.id)" type="text" size="small">查看</el-button>
                    <!-- <el-button class='Tablebutton' type="text" size="small">编辑</el-button> -->
                    <el-button class='Tablebutton' type="text" size="small" @click='removeCoalById(scope.row.id)'>删除</el-button>
                </template>
                </pl-table-column>
            </pl-table>
            <!-- 分页栏 -->
            <span class='note'>*此数据库只适用于当前用户，可进行拓展</span>
            <el-pagination
                @size-change="handleSizeChange"
                @current-change="handleCurrentChange"
                :current-page="cur_page"
                :page-sizes="pageSizes"
                :page-size="pageSize"
                layout="total, sizes, prev, pager, next, jumper"
                :total="total">
          </el-pagination>
          <WatchDetailed :coalDetailedList='coalDetailedList' :editCoalDetailVisible='editCoalDetailVisible' @ChangVisible="ChangeCoalDetailVisible" @ChangStatus='ChangShowStatus'></WatchDetailed>
</div>
</template>

<script>
import WatchDetailed from './WatchDetailed' // 引入组件
export default {
  components: { // 引入组件
    WatchDetailed
  },
  props: {
    editCoalDetailVisible: {
      default: false
    },
    show_1: {
      default: true
    },
    show_2: {
      default: true
    },
    show_3: {
      default: true
    },
    show_4: {
      default: true
    },
    show_5: {
      default: true
    },
    show_6: {
      default: true
    },
    show_7: {
      default: true
    },
    show_8: {
      default: true
    },
    show_9: {
      default: true
    },
    show_10: {
      default: true
    },
    show_11: {
      default: true
    },
    show_12: {
      default: true
    },
    show_13: {
      default: true
    },
    show_14: {
      default: true
    },
    show_15: {
      default: true
    },
    show_16: {
      default: true
    },
    show_17: {
      default: true
    },
    show_18: {
      default: true
    },
    queryInfo_get: {
      default: ''
    }
  },
  data() {
    return {
      // 获取煤数据参数对象
      coalList: [],
      height: 250,
      oldChooseData: [],
      chooseData: [],

      // 分页信息显示
      pageSize: 20,
      total: 0,
      pageSizes: [10, 20, 30, 40],
      cur_page: 1,

      // 查看煤具体数据的对话框

      // 煤进一步的细节信息
      coalDetailedList: [],

      status: 0
    }
  },
  created() {
    this.getCoalList()
    this.height = window.screen.height > 850 ? window.screen.height * 0.60 : window.screen.height * 0.45 // 设置表格在不同分辨率电脑的展示大小
  },
  watch: { // 控制表格滚轮跳转
    status (value, oldvalue) {
      if (value === 1) {
        this.timer = setTimeout(() => {
          this.$refs.CoalTable.$el.children[0].children[2].scrollTop = this.scrollDistance
        }, 3)
        this.status = 0
      }
    }
  },
  methods: {
    async getCoalList() {
      await this.$http.get('coalData', { params: this.queryInfo_get }).then(ret => {
        this.coalList = ret.data.msg // 取具体的数值
        this.coalList.reverse()
        this.total = this.coalList.length
      }
      )
    },
    tableRowClassName ({ row, rowIndex }) {
      if (rowIndex % 2 === 0) {
        return 'background-color:rgba(0, 21, 40, 1) !important;'
      }
      if (rowIndex % 2 === 1) {
        return 'background-color:rgba(0, 21, 40, 0.7) !important;'
      }
    },
    // 分页
    handleSizeChange(val) {
      this.pageSize = val
      this.editCoalDetailVisible = false // 防止点击分页时出现对话框
    },
    // 分页导航
    handleCurrentChange(val) {
      this.editCoalDetailVisible = false // 防止点击分页时出现对话框
      this.cur_page = val
    },

    // 展示细节信息的对话框，这里同时要显示获取对应id的数据过程
    async showDetailedDialog(id) {
      this.scrollDistance = this.$refs.CoalTable.$el.children[0].children[2].scrollTop // 赋值滚轮位置
      this.editCoalDetailVisible = true // 点击按钮展示对话框
      const { data: res } = await this.$http.get('/coalDetailedData', { params: id })
      this.coalDetailedList = res.msg
      this.status = 1
    },

    async removeCoalById(id) {
      const { data: res } = await this.$http.get('/deleteCoalData', { params: id })
      if (res === 'delete successfully') {
        this.$message.success('删除成功！')
      }
      setTimeout(location.reload(), '5000') // 页面刷新
    }
  }
}
</script>

<style>
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
.button_2:hover{
  color: rgb(3, 205, 205) !important;
}
#coalTable th{ /*标题栏背景颜色*/
  background-color: rgb(23, 42, 59)  !important;
  color: white !important;
  font-weight: 500;
}
#coalTable td{
  background-color: rgba(1, 22, 40,0) !important; /*必须要加透明，与方法里的tableRowClassName搭配使用，呈现的是tableRowClassName里的颜色*/
  color: white !important;
}
.Tablebutton{
  color: rgb(248, 182, 0) !important;
}
.el-pager li.active{
  color: rgb(248, 182, 0) !important;
}
.el-pager li:hover{
  color: rgb(248, 182, 0) !important;
}
.el-pagination{
  float: right;
}
.note{
  color: white;
  font-size: 80%;
}
</style>
