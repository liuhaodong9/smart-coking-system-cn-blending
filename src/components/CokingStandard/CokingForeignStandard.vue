<template>
  <div>
    <!-- ChinaStandard -->
    <div class='ChinaStandard'>
      <div class='selectbutton'>
        <p></p>
        <span class='subtitle_5'>煤焦化国标</span>
        <el-button id='b24' class='button_' size="mini" @click='switchChineseStandard'>中国标准</el-button>
        <el-button id='b25' class='button_' size="mini">国际标准</el-button>
      </div>
      <el-card class="box-card">
      <p class='cn_title'>国际煤焦化标准</p>
      <pl-table id='FNstandardtable' :row-style="tableRowClassName" ref='CoalTable' use-virtual border :data='tableData' :header-cell-style="{background:'white',color:'#494949',textAlign:'center', border:'1px solid #BFBFBF',fontSize: '14px'}" big-data-checkbox highlight-current-row fixedColumnsRoll :height="height">
        <pl-table-column align="center" fixed label='序号' prop='id' key="1" width='100'></pl-table-column>
        <pl-table-column align="left" fixed label='文件名称' prop='name' key="1" ></pl-table-column>
        <pl-table-column fixed="right" label="链接" width="350" prop='link' align='center'>
          <template slot-scope="scope">
            <a :href="scope.row.link" target="_blank" class="buttonText" style="color:rgb(255, 90, 219)">{{scope.row.link}}</a>
          </template>
        </pl-table-column>
      </pl-table>
    </el-card>
    </div>
    <el-dialog :lock-scroll="false" destroy-on-close='true' class='abow_dialog' top='7vh' center :close-on-click-modal="false" :visible.sync="editCoalDetailVisible" :append-to-body="true" width="75%" height='40%'>
      <el-button class='Exitbutton' plain icon="el-icon-arrow-left" @click="editCoalDetailVisible=false"></el-button>
      <img :src='document' style="width:100%">
    </el-dialog>
  </div>
</template>

<script>
export default {
  created() {
    this.height = window.screen.height > 850 ? window.screen.height * 0.60 : window.screen.height * 0.45 // 设置表格在不同分辨率电脑的展示大小
    this.$emit('changeActiveStep', 5)
  },
  data() {
    return {
      tableData: [{
        id: 1,
        name: 'ISO 15238:2016 Solid mineral fuels — Determination of total cadmium content of coal',
        link: 'https://www.iso.org/standard/70206.html'
      }, {
        id: 2,
        name: 'ISO 23604:2022 Method of determining specific surface area of coal',
        link: 'https://www.iso.org/standard/81085.html'
      }, {
        id: 3,
        name: 'ISO 7404-1:2016 Methods for the petrographic analysis of coals — Part 1: Vocabulary',
        link: 'https://www.iso.org/standard/67682.html'
      }, {
        id: 4,
        name: 'ISO 7404-2:2009 Methods for the petrographic analysis of coals — Part 2: Methods of preparing coal samples',
        link: 'https://www.iso.org/standard/42798.html'
      }, {
        id: 5,
        name: 'ISO 7404-3:2009 Methods for the petrographic analysis of coals — Part 3: Method of determining maceral group composition',
        link: 'https://www.iso.org/standard/42831.html'
      }, {
        id: 6,
        name: 'ISO 14180:2017 Solid mineral fuels — Guidance on the sampling of coal seams',
        link: 'https://www.iso.org/standard/66498.html'
      }, {
        id: 7,
        name: 'ISO 11724:2019 Solid mineral fuels — Determination of total fluorine in coal, coke and fly ash',
        link: 'https://www.iso.org/standard/75881.html'
      }, {
        id: 8,
        name: 'ISO 15237:2016 Solid mineral fuels — Determination of total mercury content of coal',
        link: 'https://www.iso.org/standard/70207.html'
      }, {
        id: 9,
        name: 'ISO 11760:2018 Classification of coals',
        link: 'https://www.iso.org/standard/75705.html'
      }, {
        id: 10,
        name: 'ISO 8858-1:2019 Hard coal — Froth flotation testing — Part 1: Laboratory procedure',
        link: 'https://www.iso.org/standard/75885.html'
      }, {
        id: 11,
        name: 'ISO 8858-2:2004 Hard coal — Froth flotation testing — Part 2: Sequential evaluation',
        link: 'https://www.iso.org/standard/34310.html'
      }, {
        id: 12,
        name: 'ISO 8858-3:2004 Hard coal — Froth flotation testing — Part 3: Release evaluation',
        link: 'https://www.iso.org/standard/34311.html'
      }, {
        id: 13,
        name: 'ISO/TS 20362:2022 Hard coal — Determination of plastometric indices — Automated Sapozhnikov penetration plastometer method',
        link: 'https://www.iso.org/standard/67785.html'
      }, {
        id: 14,
        name: 'ISO/TS 4699:2022 Hard Coal — Determination of plastometric indices — Manual method',
        link: 'https://www.iso.org/standard/80675.html'
      }, {
        id: 15,
        name: 'ISO 349:2020 Hard coal — Audibert-Arnu dilatometer test',
        link: 'https://www.iso.org/standard/71376.html'
      }, {
        id: 16,
        name: 'ISO 10086-1:2019 Coal — Methods for evaluating flocculants for use in coal preparation — Part 1: Basic parameters',
        link: 'https://www.iso.org/standard/75884.html'
      }, {
        id: 17,
        name: 'ISO 1018:2019 Hard coal — Determination of moisture-holding capacity',
        link: 'https://www.iso.org/standard/74448.html'
      }, {
        id: 18,
        name: 'ISO 15585:2019 Hard coal — Determination of caking index',
        link: 'https://www.iso.org/standard/70839.html'
      }, {
        id: 19,
        name: 'ISO 12900:2018 Hard coal — Determination of abrasiveness',
        link: 'https://www.iso.org/standard/75882.html'
      }, {
        id: 20,
        name: 'ISO 8264:1989 Hard coal — Determination of the swelling properties using a dilatometer',
        link: 'https://www.iso.org/standard/15378.html'
      }, {
        id: 21,
        name: 'ISO 5073:2021 Brown coals and lignites — Determination of humic acids',
        link: 'https://www.iso.org/standard/79744.html'
      }, {
        id: 22,
        name: 'ISO 5072:2021 Brown coals and lignites — Determination of true relative density and apparent relative density',
        link: 'https://www.iso.org/standard/79743.html'
      }, {
        id: 23,
        name: 'ISO 5074:2015 Hard coal — Determination of Hardgrove grindability index',
        link: 'https://www.iso.org/standard/63236.html'
      }, {
        id: 24,
        name: 'ISO 562:2010 Hard coal and coke — Determination of volatile matter',
        link: 'https://www.iso.org/standard/55943.html'
      }
      ],
      url: '/GBT.pdf',
      editCoalDetailVisible: false,
      // 展示显示的煤标准文件
      document: ''
    }
  },
  methods: {
    switchChineseStandard() {
      this.$router.push('/CokingStandard')
    },
    tableRowClassName ({ row, rowIndex }) {
      if (rowIndex % 2 === 0) {
        return 'background-color:rgba(0, 21, 40, 1) !important;'
      }
      if (rowIndex % 2 === 1) {
        return 'background-color:rgba(0, 21, 40, 0.7) !important;'
      }
    },
    // 展示在线预览pdf
    showStanard(id) {
      this.editCoalDetailVisible = true
      if (id === 1) {
        this.document = this.tableData[0].position
      } else if (id === 2) {
        this.document = this.tableData[1].position
      } else if (id === 3) {
        this.document = this.tableData[2].position
      } else if (id === 4) {
        this.document = this.tableData[3].position
      } else if (id === 5) {
        this.document = this.tableData[4].position
      } else if (id === 6) {
        this.document = this.tableData[5].position
      } else if (id === 7) {
        this.document = this.tableData[6].position
      } else if (id === 8) {
        this.document = this.tableData[7].position
      } else if (id === 9) {
        this.document = this.tableData[8].position
      } else if (id === 10) {
        this.document = this.tableData[9].position
      } else if (id === 11) {
        this.document = this.tableData[10].position
      } else if (id === 12) {
        this.document = this.tableData[11].position
      } else if (id === 13) {
        this.document = this.tableData[12].position
      } else if (id === 14) {
        this.document = this.tableData[13].position
      } else if (id === 15) {
        this.document = this.tableData[14].position
      } else if (id === 16) {
        this.document = this.tableData[15].position
      } else if (id === 17) {
        this.document = this.tableData[16].position
      } else if (id === 18) {
        this.document = this.tableData[17].position
      } else if (id === 19) {
        this.document = this.tableData[18].position
      } else if (id === 20) {
        this.document = this.tableData[19].position
      } else if (id === 21) {
        this.document = this.tableData[20].position
      } else if (id === 22) {
        this.document = this.tableData[21].position
      } else if (id === 23) {
        this.document = this.tableData[22].position
      } else if (id === 24) {
        this.document = this.tableData[23].position
      }
    }
  }
}
</script>

<style>
/* ::-webkit-scrollbar {display:none !important} 隐藏滚轮 */

.cn_title{
  text-align: center;
  margin: 0;
  margin-bottom: 1%;
  padding-top: 0;
  color: white;
  font-family: '微软雅黑';
  font-weight:600 !important;
}
.selectbutton{
  margin-top: -2%;
  text-align: right;
}
.button_{
  /* background:linear-gradient(to top right,#19968e,#27524f,#011629,#011629) !important; */
  /* border: #22b39a !important;; */
  background-color: rgba(0,0,0,0.3) !important;
  border-radius: 0 !important;
  border: none !important;
  font-family: '微软雅黑';
  font-weight:500 !important;
  color: rgb(255, 255, 255) !important;
}
.button_:hover{
  color: rgb(3, 205, 205) !important;
}
.ChinaStandard{
  position: absolute;
  height: 90%;
  width: 95%;
}
.box-card{
    position: absolute;
    width: 100% !important;
    height: 100%;
    overscroll-behavior: contain;
    background-color: rgba(0,0,0,0.3) !important;
    border: 0px !important;
}
#FNstandardtable th{ /*标题栏背景颜色*/
  background-color: rgb(23, 42, 59)  !important;
  color: white !important;
}
#FNstandardtable td{
  background-color: rgba(1, 22, 40,0) !important; /*必须要加透明，与方法里的tableRowClassName搭配使用，呈现的是tableRowClassName里的颜色*/
  color: white !important;
}
.lookbutton{
  color: rgb(255, 90, 219) !important;
  font-weight: bold !important;
}
.next_button{
  position: absolute;
  width: 1%;
  height: 10%;
  right: 2.3%;
  top: 42%;
  font-size:40px !important;
  background-color: transparent !important;
  border: 0px !important;
  /* background-color: #23978f !important;
  border: 0px !important; */
}
.switch{
  position: absolute;
  color: white;
  font-size: 12px;
  right: 0.5%;
  top: 50%;
}
.Exitbutton{
  position:fixed;
  margin:auto;
  left:0;
  top:0;
  bottom:0;
  width: 1%;
  padding: 0;
  border-radius: 0;
  opacity: 0.50;
  border-color: none;
}
#b24{
  right: 25%;
  top: -2%;
  border: 1px solid #09927b !important;
}
#b25{
  right: 12.5%;
  top: -2%;
  color: rgb(255, 90, 219) !important;
  border: 1px solid #09927b !important;
}
.subtitle_5{
  position: absolute;
  color: rgb(255, 90, 219);
  left: 0%;
  font-size: 90%;
}
.el-table_24_column_72 is-center {
  color: rgb(255, 90, 219) !important;
}
</style>
