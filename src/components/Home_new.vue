<template>
  <!-- 外层容器：仅负责布局，不承担视频背景 -->
  <div>
    <el-container class="home-container">
      <!-- 顶部栏始终使用纯色渐变背景，不受视频影响 -->
      <el-header class="header-bar">
        <!-- 左上角：用户手册下载 -->
        <a
          class="userguide"
          href="http://1.116.164.66:5000/userguidedownload"
          target="_blank"
        >
          用户手册下载
        </a>

        <!-- 右上角：退出 -->
        <el-button class="exitbuttion" size="mini" @click="returnHome"
          >退出</el-button
        >

        <!-- 标题 + 工具行（用户时间 + 6 个按钮） -->
        <div class="header-title-time">
          <div class="title">智慧焦化 · 数字孪生系统</div>

          <div class="toolbar-line">
            <!-- 左 3 个按钮 -->
            <div class="button-group">
              <el-button
                :class="['selection', activePage === 'echart' ? 'active' : '']"
                @click="switchEchartPage"
                >配煤</el-button
              >
              <el-button
                :class="['selection', activePage === 'mixing' ? 'active' : '']"
                @click="switchMixingRatioPrediction"
                >煤料输送</el-button
              >
              <el-button
                :class="['selection', activePage === 'coke' ? 'active' : '']"
                @click="switchCokeDigitalTwin"
                >装煤</el-button
              >
            </div>

            <!-- 当前用户 + 时间 -->
            <div class="info-line">
              <span class="lab_name">当前用户：Admin</span>
              <span class="currenttime">{{ gettime }}</span>
            </div>

            <!-- 右 3 个按钮 -->
            <div class="button-group">
              <el-button
                :class="['selection', activePage === 'quenching' ? 'active' : '']"
                @click="switchQuenching"
                >炼焦</el-button
              >
              <el-button
                :class="['selection', activePage === 'push' ? 'active' : '']"
                @click="switchPush"
                >推焦</el-button
              >
              <el-button
                :class="['selection', activePage === 'cool' ? 'active' : '']"
                @click="switchCool"
                >熄焦</el-button
              >
            </div>
          </div>
        </div>
      </el-header>

      <!-- ================== 主体区 ================== -->
      <!-- 1. 使用 position:relative; 以便绝对定位的视频仅覆盖主体  -->
      <!-- 2. 视频放在主体内，并通过绝对定位铺满整个 el-main  -->
      <el-main class="main-area">
        <video
          autoplay
          muted
          loop
          playsinline
          class="background-video"
        >
          <source src="../assets/blendingPlant.mp4" type="video/mp4" />
          Your browser does not support the video tag.
        </video>

        <!-- 真正的业务内容 -->
        <div class="charts-wrapper">
          <!-- 左列外框 -->
          <div class="charts-column">
            <div class="chart-container">
              <h1>AI配煤算法</h1>
              <el-card
                class="box-card_6"
                shadow="never"
                :body-style="{ backgroundColor: 'transparent', border: 'none' }">

                <el-form>

                  <!-- ① 气煤 -->
                  <el-row>
                    <!-- 气煤按钮 -->
                    <el-col :span="3">
                      <el-button
                        class="fixed-button-size"
                        type="primary"
                        @click="selectQicoal"
                      >
                        气煤
                      </el-button>
                    </el-col>

                    <!-- 清空按钮，右移 2 格 -->
                    <el-col :span="3" :offset="2">
                      <el-button
                        class="fixed-button-size"
                        type="primary"
                        @click="deleteQicoal"
                      >
                        清空
                      </el-button>
                    </el-col>

                    <!-- 选中结果，右移 1 格 -->
                    <el-col :span="14" :offset="1">
                      <!-- 只在这里加 :model -->
                      <el-form-item class="type_label_1" :model="modifyParametersForm">
                        选择的气煤：
                        <span
                          v-for="item in modifyParametersForm.params"
                          :key="item.key"
                          class="selectedCoal"
                        >
                          &nbsp;{{ item.paramName }}
                        </span>
                      </el-form-item>
                    </el-col>
                  </el-row>

                  <!-- ② 肥煤 -->
                  <el-row>
                    <el-col :span="3">
                      <el-button class="fixed-button-size" type="primary" @click="selectFeicoal">
                        肥煤
                      </el-button>
                    </el-col>
                    <el-col :span="3" :offset="2">
                      <el-button class="fixed-button-size" type="primary" @click="deleteFeicoal">
                        清空
                      </el-button>
                    </el-col>

                    <el-col :span="14" :offset="1">
                      <!-- 加这一行 ↓↓↓ -->
                      <el-form-item class="type_label_1" :model="modifyParametersForm_2">
                        选择的肥煤：
                        <span v-for="item in modifyParametersForm_2.params"
                              :key="item.key"
                              class="selectedCoal_2">
                          &nbsp;{{ item.paramName }}
                        </span>
                      </el-form-item>
                    </el-col>
                  </el-row>

                  <!-- ③ 气肥煤 -->
                  <el-row>
                    <el-col :span="3">
                      <el-button class="fixed-button-size" type="primary" @click="selectQiFeicoal">
                        气肥煤
                      </el-button>
                    </el-col>
                    <el-col :span="3" :offset="2">
                      <el-button class="fixed-button-size" type="primary" @click="deleteQiFeicoal">
                        清空
                      </el-button>
                    </el-col>

                    <el-col :span="14" :offset="1">
                      <el-form-item class="type_label_1" :model="modifyParametersForm_3">
                        选择的气肥煤：
                        <span v-for="item in modifyParametersForm_3.params"
                              :key="item.key"
                              class="selectedCoal_3">
                          &nbsp;{{ item.paramName }}
                        </span>
                      </el-form-item>
                    </el-col>
                  </el-row>

                  <!-- ④ 1/3 焦煤 -->
                  <el-row>
                    <el-col :span="3">
                      <el-button class="fixed-button-size" type="primary" @click="select13jiaocoal">
                        1/3焦煤
                      </el-button>
                    </el-col>
                    <el-col :span="3" :offset="2">
                      <el-button class="fixed-button-size" type="primary" @click="delete13jiaocoal">
                        清空
                      </el-button>
                    </el-col>

                    <el-col :span="14" :offset="1">
                      <el-form-item class="type_label_1" :model="modifyParametersForm_4">
                        选择的1/3焦煤：
                        <span v-for="item in modifyParametersForm_4.params"
                              :key="item.key"
                              class="selectedCoal_4">
                          &nbsp;{{ item.paramName }}
                        </span>
                      </el-form-item>
                    </el-col>
                  </el-row>

                  <!-- ⑤ 焦煤 -->
                  <el-row>
                    <el-col :span="3">
                      <el-button class="fixed-button-size" type="primary" @click="selectjiaocoal">
                        焦煤
                      </el-button>
                    </el-col>
                    <el-col :span="3" :offset="2">
                      <el-button class="fixed-button-size" type="primary" @click="deletetjiaocoal">
                        清空
                      </el-button>
                    </el-col>

                    <el-col :span="14" :offset="1">
                      <el-form-item class="type_label_1" :model="modifyParametersForm_5">
                        选择的焦煤：
                        <span v-for="item in modifyParametersForm_5.params"
                              :key="item.key"
                              class="selectedCoal_5">
                          &nbsp;{{ item.paramName }}
                        </span>
                      </el-form-item>
                    </el-col>
                  </el-row>

                  <!-- ⑥ 瘦煤 -->
                  <el-row>
                    <el-col :span="3">
                      <el-button class="fixed-button-size" type="primary" @click="selectshoucoal">
                        瘦煤
                      </el-button>
                    </el-col>
                    <el-col :span="3" :offset="2">
                      <el-button class="fixed-button-size" type="primary" @click="deletetshoucoal">
                        清空
                      </el-button>
                    </el-col>

                    <el-col :span="14" :offset="1">
                      <el-form-item class="type_label_1" :model="modifyParametersForm_6">
                        选择的瘦煤：
                        <span v-for="item in modifyParametersForm_6.params"
                              :key="item.key"
                              class="selectedCoal_6">
                          &nbsp;{{ item.paramName }}
                        </span>
                      </el-form-item>
                    </el-col>
                  </el-row>

                  <!-- 决策按钮 -->
                  <el-row style="margin-top: 12px;">
                    <el-col :span="4" :offset="16">
                      <el-button class="fixed-button-size" type="primary" @click="MakingDecision">
                        配煤决策
                      </el-button>
                    </el-col>
                  </el-row>

                </el-form>
              </el-card>
            </div>

            <div class="chart-container">
              <h1 class="block-title">配煤预测结果</h1>
              <div class="ring-row">
                <div class="echart" ref="chart1"></div>
                <div class="echart" ref="chart2"></div>
                <div class="echart" ref="chart3"></div>
              </div>
              <div class="ring-row">
                <div class="echart" ref="chart4"></div>
                <div class="echart" ref="chart5"></div>
                <div class="echart" ref="chart6"></div>
              </div>
            </div>
          </div>

          <!-- 右列外框 -->
          <div class="charts-column">
            <div class="chart-container filler-machine" style="flex:0 0 44%;">
              <div class="progress-row">
                <div class="progress-wrap charge-bar">
                  <div
                    class="progress-fill"
                    :style="{ width: loadPercent + '%' }"
                  ></div>
                  <span class="progress-digit">{{ loadPercent }}%</span>
                </div>
              </div>
              <h1 class="block-title">填料机</h1>
              <!-- ① 填料及状态 -->
              <div class="status-row">
                填料机状态：
                  <span :class="['legend-dot run', {active: conveyorRunning}]"></span> 运行
                  <!-- 停止圆点：反之 -->
                  <span :class="['legend-dot stop', {active: !conveyorRunning}]"></span> 停止
              </div>
              <!-- 5 个煤仓进度条：循环渲染 -->
              <div v-for="(p, idx) in bunkerPercents"
                  :key="idx"
                  class="progress-row">
                <span class="label">煤仓&nbsp;{{ idx + 1 }}&nbsp;剩余量</span>：
                <div class="progress-wrap">
                  <div class="progress-fill" :style="{ width: p + '%' }"></div>
                  <span class="progress-digit">{{ p }}%</span>
                </div>
              </div>
              <!-- ④ 按钮 -->
              <div class="btn-group">
                <!-- 新增设置按钮 -->
                <button class="square-btn settings-btn" @click="openSettings">设置</button>
                <button class="square-btn run-btn"  @click="startConveyor">运行</button>
                <button class="square-btn stop-btn" @click="stopConveyor">停止</button>
              </div>
            </div>
            <!-- 传送带 -->
            <div class="chart-container conveyor" style="flex:0 0 23%;">
              <h1 class="block-title">传送带</h1>

              <!-- ① 传送带状态 -->
              <div class="status-row">
                传送带状态：
                  <span :class="['legend-dot run', {active: conveyorRunning}]"></span> 运行
                  <!-- 停止圆点：反之 -->
                  <span :class="['legend-dot stop', {active: !conveyorRunning}]"></span> 停止
              </div>

              <!-- ② 数码管 + 仪表盘 -->
              <div class="meter-inline">
                <span class="status-row">传送带速度：</span>
                <span class="label">PV</span>
                <span class="digit v">{{ pv }}</span><span class="unit">m/s</span>

                <span class="label">SV</span>
                <span class="digit v">{{ sv }}</span><span class="unit">m/s</span>

                <span class="status-row">传送带电流：</span>
                <span class="digit cur">{{ current }}</span><span class="unit">A</span>
              </div>

              <!-- ④ 按钮 -->
              <div class="btn-group">
                <!-- 新增设置按钮 -->
                <button class="square-btn settings-btn" @click="openSettings">设置</button>
                <button class="square-btn run-btn"  @click="startConveyor">运行</button>
                <button class="square-btn stop-btn" @click="stopConveyor">停止</button>
              </div>
            </div>

            <!-- 搅拌机 -->
            <div class="chart-container blender" style="flex:0 0 28%;">
              <!-- ‣ 搅拌进度条 -->
              <div class="progress-row">
                <div class="progress-wrap charge-bar">
                  <div class="progress-fill" :style="{ width: mixPercent + '%' }"></div>
                  <span key="mixPercent" class="progress-digit">{{ mixPercent }}%</span>
                </div>
              </div>
              <h1 class="panel-title">搅拌机</h1>

              <!-- ‣ 状态 + 按钮 -->
              <div class="status-row">
                搅拌机状态：
                <span :class="['legend-dot run', {active: blenderRunning}]"></span> 运行
                <span :class="['legend-dot stop', {active: !blenderRunning}]"></span> 停止
                <div class="btn-group">
                  <button :class="['square-btn', 'run-btn', {active: blenderRunning}]"
                          @click="startBlender">
                    运行
                  </button>
                  <button :class="['square-btn', 'stop-btn', {active: !blenderRunning}]"
                          @click="stopBlender">
                    停止
                  </button>
                </div>
              </div>

              <!-- ‣ 输出质量 / 体积 -->
              <div class="row">
                <span class="status-row">出口流量：</span>
                <span class="label">质量</span>
                <span class="digit v">{{ mass }}</span>
                <span class="unit">t / min</span>
                <span class="label">体积</span>
                <span class="digit v">{{ volume }}</span>
                <span class="unit">m³ / min</span>
              </div>
            </div>
          </div>
        </div>
      </el-main>
    </el-container>

    <!-- 以下是弹窗代码 -->
    <!-- 气煤数据库弹窗 -->
    <el-dialog
      :lock-scroll="true"
      class="abow_dialog1"
      top="2vh"
      title="气煤数据库"
      custom-class="userDig"
      center
      :show-close="true"
      :closeOnPressEscape="true"
      :close-on-click-modal="true"
      :visible.sync="editRatioCoalVisible1"
      :append-to-body="true"
      width="75%"
      height="50%"
    >
      <pl-table
        @selection-change="handleSelectionChange"
        id="CoalTable"
        :data="coalList"
        big-data-checkbox
        highlight-current-row
        :row-height="40"
        use-virtual
        border
        :header-cell-style="{
          background: 'white',
          color: '#494949',
          textAlign: 'center',
          border: '1px solid #BFBFBF',
          fontSize: '14px'
        }"
        :height="height"
        :key="Math.random()"
        :default-sort="{ prop: 'id', order: 'ascending' }"
        size="mini"
        :cell-style="{ padding: '0px', fontSize: '14px' }"
        fixedColumnsRoll
      >
        <pl-table-column type="selection" width="55" align="center" />
        <pl-table-column
          align="center"
          label="序号"
          width="80px"
          prop="id"
          fixed
        />
        <pl-table-column
          align="center"
          label="煤样名称"
          width="140px"
          prop="coal_name"
          fixed
        />
        <pl-table-column align="center" label="煤种" prop="coal_type" fixed />
        <pl-table-column
          align="center"
          label="存储量(吨)"
          width="90px"
          prop="store_number"
          key="4"
        />
        <pl-table-column
          align="center"
          label="价格(吨)"
          key="5"
          prop="coal_price"
          fixed
        />
        <pl-table-column
          align="center"
          label="水分(Mad)"
          width="110px"
          prop="coal_mad"
        />
        <pl-table-column
          align="center"
          label="灰分(Ad)"
          width="120px"
          prop="coal_ad"
        />
        <pl-table-column
          align="center"
          label="挥发分(Vdaf)"
          width="110px"
          prop="coal_vdaf"
        />
        <pl-table-column
          align="center"
          label="全硫(St,d)"
          width="110px"
          prop="coal_std"
        />
        <pl-table-column align="center" label="G" width="110px" prop="G" />
        <pl-table-column align="center" label="X" width="110px" prop="X" />
        <pl-table-column align="center" label="Y" width="110px" prop="Y" />
        <pl-table-column
          align="center"
          label="CRI"
          width="110px"
          prop="coke_CRI"
        />
        <pl-table-column
          align="center"
          label="CSR"
          width="110px"
          prop="coke_CSR"
        />
        <pl-table-column
          align="center"
          label="M10"
          width="110px"
          prop="coke_M10"
        />
        <pl-table-column
          align="center"
          label="M25"
          width="110px"
          prop="coke_M25"
        />
      </pl-table>
      <p class="qiCoalattention">{{ qiCoalattention }}</p>
      <el-button class="Blendingbutton_3" type="primary" @click="sendBlendingData">
        确认选择
      </el-button>
      <div class="heightblank"></div>
    </el-dialog>

    <!-- 肥煤数据库弹窗 -->
    <el-dialog
      :lock-scroll="true"
      class="abow_dialog2"
      top="7vh"
      title="肥煤数据库"
      custom-class="userDig"
      center
      :show-close="true"
      :closeOnPressEscape="true"
      :close-on-click-modal="true"
      :visible.sync="editRatioCoalVisible2"
      :append-to-body="true"
      width="75%"
      height="40%"
    >
      <pl-table
        @selection-change="handleSelectionChange_2"
        id="CoalTable"
        :data="coalList_2"
        big-data-checkbox
        highlight-current-row
        :row-height="40"
        use-virtual
        border
        :header-cell-style="{
          background: 'white',
          color: '#494949',
          textAlign: 'center',
          border: '1px solid #BFBFBF',
          fontSize: '14px'
        }"
        :height="height"
        :key="Math.random()"
        :default-sort="{ prop: 'id', order: 'ascending' }"
        size="mini"
        :cell-style="{ padding: '0px', fontSize: '14px' }"
        fixedColumnsRoll
      >
        <pl-table-column type="selection" width="55" align="center" />
        <pl-table-column
          align="center"
          label="序号"
          width="80px"
          prop="id"
          fixed
        />
        <pl-table-column
          align="center"
          label="煤样名称"
          width="140px"
          prop="coal_name"
          fixed
        />
        <pl-table-column align="center" label="煤种" prop="coal_type" fixed />
        <pl-table-column
          align="center"
          label="存储量(吨)"
          width="90px"
          prop="store_number"
          key="4"
        />
        <pl-table-column
          align="center"
          label="价格(吨)"
          key="5"
          prop="coal_price"
          fixed
        />
        <pl-table-column
          align="center"
          label="水分(Mad)"
          width="110px"
          prop="coal_mad"
        />
        <pl-table-column
          align="center"
          label="灰分(Ad)"
          width="120px"
          prop="coal_ad"
        />
        <pl-table-column
          align="center"
          label="挥发分(Vdaf)"
          width="110px"
          prop="coal_vdaf"
        />
        <pl-table-column
          align="center"
          label="全硫(St,d)"
          width="110px"
          prop="coal_std"
        />
        <pl-table-column align="center" label="G" width="110px" prop="G" />
        <pl-table-column align="center" label="X" width="110px" prop="X" />
        <pl-table-column align="center" label="Y" width="110px" prop="Y" />
        <pl-table-column
          align="center"
          label="CRI"
          width="110px"
          prop="coke_CRI"
        />
        <pl-table-column
          align="center"
          label="CSR"
          width="110px"
          prop="coke_CSR"
        />
        <pl-table-column
          align="center"
          label="M10"
          width="110px"
          prop="coke_M10"
        />
        <pl-table-column
          align="center"
          label="M25"
          width="110px"
          prop="coke_M25"
        />
      </pl-table>
      <p class="qiCoalattention">{{ feiCoalattention }}</p>
      <el-button class="Blendingbutton_3" type="primary" @click="sendBlendingData_2">
        确认选择
      </el-button>
      <div class="heightblank"></div>
    </el-dialog>

    <!-- 气肥煤数据库弹窗 -->
    <el-dialog
      :lock-scroll="true"
      class="abow_dialog3"
      top="7vh"
      title="气肥煤数据库"
      custom-class="userDig"
      center
      :show-close="true"
      :closeOnPressEscape="true"
      :close-on-click-modal="true"
      :visible.sync="editRatioCoalVisible3"
      :append-to-body="true"
      width="75%"
      height="40%"
    >
      <pl-table
        @selection-change="handleSelectionChange_3"
        id="CoalTable"
        :data="coalList_3"
        big-data-checkbox
        highlight-current-row
        :row-height="40"
        use-virtual
        border
        :header-cell-style="{
          background: 'white',
          color: '#494949',
          textAlign: 'center',
          border: '1px solid #BFBFBF',
          fontSize: '14px'
        }"
        :height="height"
        :key="Math.random()"
        :default-sort="{ prop: 'id', order: 'ascending' }"
        size="mini"
        :cell-style="{ padding: '0px', fontSize: '14px' }"
        fixedColumnsRoll
      >
        <pl-table-column type="selection" width="55" align="center" />
        <pl-table-column
          align="center"
          label="序号"
          width="80px"
          prop="id"
          fixed
        />
        <pl-table-column
          align="center"
          label="煤样名称"
          width="140px"
          prop="coal_name"
          fixed
        />
        <pl-table-column align="center" label="煤种" prop="coal_type" fixed />
        <pl-table-column
          align="center"
          label="存储量(吨)"
          width="90px"
          prop="store_number"
          key="4"
        />
        <pl-table-column
          align="center"
          label="价格(吨)"
          key="5"
          prop="coal_price"
          fixed
        />
        <pl-table-column
          align="center"
          label="水分(Mad)"
          width="110px"
          prop="coal_mad"
        />
        <pl-table-column
          align="center"
          label="灰分(Ad)"
          width="120px"
          prop="coal_ad"
        />
        <pl-table-column
          align="center"
          label="挥发分(Vdaf)"
          width="110px"
          prop="coal_vdaf"
        />
        <pl-table-column
          align="center"
          label="全硫(St,d)"
          width="110px"
          prop="coal_std"
        />
        <pl-table-column align="center" label="G" width="110px" prop="G" />
        <pl-table-column align="center" label="X" width="110px" prop="X" />
        <pl-table-column align="center" label="Y" width="110px" prop="Y" />
        <pl-table-column
          align="center"
          label="CRI"
          width="110px"
          prop="coke_CRI"
        />
        <pl-table-column
          align="center"
          label="CSR"
          width="110px"
          prop="coke_CSR"
        />
        <pl-table-column
          align="center"
          label="M10"
          width="110px"
          prop="coke_M10"
        />
        <pl-table-column
          align="center"
          label="M25"
          width="110px"
          prop="coke_M25"
        />
      </pl-table>
      <p class="qiCoalattention">{{ qifeiCoalattention }}</p>
      <el-button class="Blendingbutton_3" type="primary" @click="sendBlendingData_3">
        确认选择
      </el-button>
      <div class="heightblank"></div>
    </el-dialog>

    <!-- 1/3焦煤数据库弹窗 -->
    <el-dialog
      :lock-scroll="true"
      class="abow_dialog4"
      top="7vh"
      title="1/3焦煤数据库"
      custom-class="userDig"
      center
      :show-close="true"
      :closeOnPressEscape="true"
      :close-on-click-modal="true"
      :visible.sync="editRatioCoalVisible4"
      :append-to-body="true"
      width="75%"
      height="40%"
    >
      <pl-table
        @selection-change="handleSelectionChange_4"
        id="CoalTable"
        :data="coalList_4"
        big-data-checkbox
        highlight-current-row
        :row-height="40"
        use-virtual
        border
        :header-cell-style="{
          background: 'white',
          color: '#494949',
          textAlign: 'center',
          border: '1px solid #BFBFBF',
          fontSize: '14px'
        }"
        :height="height"
        :key="Math.random()"
        :default-sort="{ prop: 'id', order: 'ascending' }"
        size="mini"
        :cell-style="{ padding: '0px', fontSize: '14px' }"
        fixedColumnsRoll
      >
        <pl-table-column type="selection" width="55" align="center" />
        <pl-table-column
          align="center"
          label="序号"
          width="80px"
          prop="id"
          fixed
        />
        <pl-table-column
          align="center"
          label="煤样名称"
          width="140px"
          prop="coal_name"
          fixed
        />
        <pl-table-column align="center" label="煤种" prop="coal_type" fixed />
        <pl-table-column
          align="center"
          label="存储量(吨)"
          width="90px"
          prop="store_number"
          key="4"
        />
        <pl-table-column
          align="center"
          label="价格(吨)"
          key="5"
          prop="coal_price"
          fixed
        />
        <pl-table-column
          align="center"
          label="水分(Mad)"
          width="110px"
          prop="coal_mad"
        />
        <pl-table-column
          align="center"
          label="灰分(Ad)"
          width="120px"
          prop="coal_ad"
        />
        <pl-table-column
          align="center"
          label="挥发分(Vdaf)"
          width="110px"
          prop="coal_vdaf"
        />
        <pl-table-column
          align="center"
          label="全硫(St,d)"
          width="110px"
          prop="coal_std"
        />
        <pl-table-column align="center" label="G" width="110px" prop="G" />
        <pl-table-column align="center" label="X" width="110px" prop="X" />
        <pl-table-column align="center" label="Y" width="110px" prop="Y" />
        <pl-table-column
          align="center"
          label="CRI"
          width="110px"
          prop="coke_CRI"
        />
        <pl-table-column
          align="center"
          label="CSR"
          width="110px"
          prop="coke_CSR"
        />
        <pl-table-column
          align="center"
          label="M10"
          width="110px"
          prop="coke_M10"
        />
        <pl-table-column
          align="center"
          label="M25"
          width="110px"
          prop="coke_M25"
        />
      </pl-table>
      <p class="qiCoalattention">{{ jiao13Coalattention }}</p>
      <el-button class="Blendingbutton_3" type="primary" @click="sendBlendingData_4">
        确认选择
      </el-button>
      <div class="heightblank"></div>
    </el-dialog>

    <!-- 焦煤数据库弹窗 -->
    <el-dialog
      :lock-scroll="true"
      class="abow_dialog5"
      top="7vh"
      title="焦煤数据库"
      custom-class="userDig"
      center
      :show-close="true"
      :closeOnPressEscape="true"
      :close-on-click-modal="true"
      :visible.sync="editRatioCoalVisible5"
      :append-to-body="true"
      width="75%"
      height="40%"
    >
      <pl-table
        @selection-change="handleSelectionChange_5"
        id="CoalTable"
        :data="coalList_5"
        big-data-checkbox
        highlight-current-row
        :row-height="40"
        use-virtual
        border
        :header-cell-style="{
          background: 'white',
          color: '#494949',
          textAlign: 'center',
          border: '1px solid #BFBFBF',
          fontSize: '14px'
        }"
        :height="height"
        :key="Math.random()"
        :default-sort="{ prop: 'id', order: 'ascending' }"
        size="mini"
        :cell-style="{ padding: '0px', fontSize: '14px' }"
        fixedColumnsRoll
      >
        <pl-table-column type="selection" width="55" align="center" />
        <pl-table-column
          align="center"
          label="序号"
          width="80px"
          prop="id"
          fixed
        />
        <pl-table-column
          align="center"
          label="煤样名称"
          width="140px"
          prop="coal_name"
          fixed
        />
        <pl-table-column align="center" label="煤种" prop="coal_type" fixed />
        <pl-table-column
          align="center"
          label="存储量(吨)"
          width="90px"
          prop="store_number"
          key="4"
        />
        <pl-table-column
          align="center"
          label="价格(吨)"
          key="5"
          prop="coal_price"
          fixed
        />
        <pl-table-column
          align="center"
          label="水分(Mad)"
          width="110px"
          prop="coal_mad"
        />
        <pl-table-column
          align="center"
          label="灰分(Ad)"
          width="120px"
          prop="coal_ad"
        />
        <pl-table-column
          align="center"
          label="挥发分(Vdaf)"
          width="110px"
          prop="coal_vdaf"
        />
        <pl-table-column
          align="center"
          label="全硫(St,d)"
          width="110px"
          prop="coal_std"
        />
        <pl-table-column align="center" label="G" width="110px" prop="G" />
        <pl-table-column align="center" label="X" width="110px" prop="X" />
        <pl-table-column align="center" label="Y" width="110px" prop="Y" />
        <pl-table-column
          align="center"
          label="CRI"
          width="110px"
          prop="coke_CRI"
        />
        <pl-table-column
          align="center"
          label="CSR"
          width="110px"
          prop="coke_CSR"
        />
        <pl-table-column
          align="center"
          label="M10"
          width="110px"
          prop="coke_M10"
        />
        <pl-table-column
          align="center"
          label="M25"
          width="110px"
          prop="coke_M25"
        />
      </pl-table>
      <p class="qiCoalattention">{{ jiaoCoalattention }}</p>
      <el-button class="Blendingbutton_3" type="primary" @click="sendBlendingData_5">
        确认选择
      </el-button>
      <div class="heightblank"></div>
    </el-dialog>

    <!-- 瘦煤数据库弹窗 -->
    <el-dialog
      :lock-scroll="true"
      class="abow_dialog6"
      top="7vh"
      title="瘦煤数据库"
      custom-class="userDig"
      center
      :show-close="true"
      :closeOnPressEscape="true"
      :close-on-click-modal="true"
      :visible.sync="editRatioCoalVisible6"
      :append-to-body="true"
      width="75%"
      height="40%"
    >
      <pl-table
        @selection-change="handleSelectionChange_6"
        id="CoalTable"
        :data="coalList_6"
        big-data-checkbox
        highlight-current-row
        :row-height="40"
        use-virtual
        border
        :header-cell-style="{
          background: 'white',
          color: '#494949',
          textAlign: 'center',
          border: '1px solid #BFBFBF',
          fontSize: '14px'
        }"
        :height="height"
        :key="Math.random()"
        :default-sort="{ prop: 'id', order: 'ascending' }"
        size="mini"
        :cell-style="{ padding: '0px', fontSize: '14px' }"
        fixedColumnsRoll
      >
        <pl-table-column type="selection" width="55" align="center" />
        <pl-table-column
          align="center"
          label="序号"
          width="80px"
          prop="id"
          fixed
        />
        <pl-table-column
          align="center"
          label="煤样名称"
          width="140px"
          prop="coal_name"
          fixed
        />
        <pl-table-column align="center" label="煤种" prop="coal_type" fixed />
        <pl-table-column
          align="center"
          label="存储量(吨)"
          width="90px"
          prop="store_number"
          key="4"
        />
        <pl-table-column
          align="center"
          label="价格(吨)"
          key="5"
          prop="coal_price"
          fixed
        />
        <pl-table-column
          align="center"
          label="水分(Mad)"
          width="110px"
          prop="coal_mad"
        />
        <pl-table-column
          align="center"
          label="灰分(Ad)"
          width="120px"
          prop="coal_ad"
        />
        <pl-table-column
          align="center"
          label="挥发分(Vdaf)"
          width="110px"
          prop="coal_vdaf"
        />
        <pl-table-column
          align="center"
          label="全硫(St,d)"
          width="110px"
          prop="coal_std"
        />
        <pl-table-column align="center" label="G" width="110px" prop="G" />
        <pl-table-column align="center" label="X" width="110px" prop="X" />
        <pl-table-column align="center" label="Y" width="110px" prop="Y" />
        <pl-table-column
          align="center"
          label="CRI"
          width="110px"
          prop="coke_CRI"
        />
        <pl-table-column
          align="center"
          label="CSR"
          width="110px"
          prop="coke_CSR"
        />
        <pl-table-column
          align="center"
          label="M10"
          width="110px"
          prop="coke_M10"
        />
        <pl-table-column
          align="center"
          label="M25"
          width="110px"
          prop="coke_M25"
        />
      </pl-table>
      <p class="qiCoalattention">{{ souCoalattention }}</p>
      <el-button class="Blendingbutton_3" type="primary" @click="sendBlendingData_6">
        确认选择
      </el-button>
      <div class="heightblank"></div>
    </el-dialog>

    <!-- 配煤辅助决策(人工智能算法) - 综合选择后的弹窗 -->
    <el-dialog
      :lock-scroll="true"
      class="abow_dialog"
      top="7vh"
      title="配煤辅助决策(人工智能算法)"
      custom-class="userDig"
      center
      :show-close="false"
      :close-on-press-escape="false"
      :close-on-click-modal="false"
      :visible.sync="editCoalDetailVisible"
      :append-to-body="true"
      width="75%"
      height="40%"
    >
      <el-form :model="modifyParametersForm_total">
        <el-row
          v-for="(item, index) in modifyParametersForm_total.params"
          :key="item.key"
        >
          <el-col :span="6">
            <el-form-item :label="`煤样名称：`">
              <span style="font-weight:bold">{{ item.paramName }}</span>
            </el-form-item>
          </el-col>
          <el-col :span="6">
            <el-form-item :label="`煤种类型：`">
              <span style="font-weight:bold">{{ item.paramType }}</span>
            </el-form-item>
          </el-col>
          <el-col :span="5">
            <el-form-item :label="`价格：`">
              <span style="font-weight:bold">{{ item.paramPrice }}</span>
            </el-form-item>
          </el-col>
          <el-col :span="6">
            配煤比：
            <el-input
              style="font-weight:bold; width:70px"
              v-model="coalRatio[index]"
            />
            %
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="5">总配煤比：{{ totalRatio }} %</el-col>
        </el-row>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button class="Blendingbutton_2" type="primary" @click="predictBlendCoal">
          混合煤性质预测
        </el-button>
        <el-button class="Blendingbutton_2" type="primary" @click="predictBestRatio">
          最优配煤比预测
        </el-button>
        <el-button class="Blendingbutton_2" type="primary" @click="cancelDialog">
          取消
        </el-button>
      </span>
    </el-dialog>

    <!-- 混合煤性质预测结果弹窗 -->
    <el-dialog
      :lock-scroll="true"
      class="abow_dialog"
      top="7vh"
      title="混合煤性质预测结果"
      custom-class="userDig"
      center
      :show-close="true"
      :close-on-press-escape="true"
      :close-on-click-modal="true"
      :visible.sync="editBlendCoalVisible"
      :append-to-body="true"
      width="75%"
      height="40%"
    >
      <pl-table
        :data-changes-scroll-top="false"
        ref="CoalTable"
        big-data-checkbox
        highlight-current-row
        :row-height="33"
        :data="blendCoalProperty"
        use-virtual
        border
        :header-cell-style="{
          background: 'white',
          color: '#494949',
          textAlign: 'center',
          border: '1px solid #BFBFBF',
          fontSize: '14px'
        }"
        :key="Math.random()"
        :default-sort="{ prop: 'id', order: 'ascending' }"
        size="mini"
        :cell-style="{ padding: '0px', fontSize: '14px' }"
        fixedColumnsRoll
      >
        <pl-table-column align="center" label="混合煤性质" key="21">
          <pl-table-column align="center" label="水分" prop="blendCoal_mad" />
          <pl-table-column align="center" label="灰分" prop="blendCoal_ad" />
          <pl-table-column align="center" label="挥发分" prop="blendCoal_vdaf" />
          <pl-table-column align="center" label="粘结指数G" prop="blendCoal_G" />
          <pl-table-column align="center" label="X" prop="blendCoal_X" />
          <pl-table-column align="center" label="Y" prop="blendCoal_Y" />
        </pl-table-column>
      </pl-table>
      <span slot="footer" class="dialog-footer">
        <el-button class="Blendingbutton_2" type="primary">
          上传至数据库
        </el-button>
        <el-button
          class="Blendingbutton_2"
          type="primary"
          @click="editBlendCoalVisible = false"
        >
          取消
        </el-button>
      </span>
    </el-dialog>

    <!-- 最优配煤比预测弹窗 -->
    <el-dialog
      :lock-scroll="true"
      class="abow_dialog"
      top="7vh"
      title="最优配煤比预测"
      custom-class="userDig"
      center
      :show-close="true"
      :close-on-press-escape="true"
      :close-on-click-modal="true"
      :visible.sync="editRatioCoalVisible"
      :append-to-body="true"
      width="75%"
      height="40%"
    >
      <el-form>
        <!-- 优化目标：成本价格 -->
        <el-row>
          <el-col :span="24">
            <el-form-item label="优化目标" style="font-weight:bold;">
              <span style="font-weight:normal">成本价格</span>
            </el-form-item>
          </el-col>
        </el-row>

        <!-- 限制条件 -->
        <el-row>
          <el-col :span="24">
            <span style="font-weight:bold">限制条件</span>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="10">
            <!-- CRI 范围 -->
            目标CRI范围：
            最小值
            <el-input style="width:60px" v-model="paraRange[0]" />
            ~~
            最大值
            <el-input style="width:60px" v-model="paraRange[1]" />
          </el-col>
          <el-col :span="10">
            <!-- CSR 范围 -->
            目标CSR范围：
            最小值
            <el-input style="width:60px" v-model="paraRange[2]" />
            ~~
            最大值
            <el-input style="width:60px" v-model="paraRange[3]" />
          </el-col>
        </el-row>
        <p style="margin: 10px 0;"></p>
        <el-row>
          <el-col :span="10">
            <!-- M10 范围 -->
            目标M10范围：
            最小值
            <el-input style="width:60px" v-model="paraRange[4]" />
            ~~
            最大值
            <el-input style="width:60px" v-model="paraRange[5]" />
          </el-col>
          <el-col :span="10">
            <!-- M25 范围 -->
            目标M25范围：
            最小值
            <el-input style="width:60px" v-model="paraRange[6]" />
            ~~
            最大值
            <el-input style="width:60px" v-model="paraRange[7]" />
          </el-col>
        </el-row>

        <!-- 预测结果 -->
        <el-row>
          <el-col :span="24">
            <p style="font-weight:bold">预测结果</p>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="24">
            <span>最优成本价格：{{ returnPrice }} 元</span>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="24">
            <span>最优配煤比：{{ returnRatio }}</span>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="24" style="font-size:80%;">
            <span>*最优配煤比预测采用的算法包含焦炭质量预测算法与遗传算法，结果仅供参考</span>
          </el-col>
        </el-row>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button class="Blendingbutton_2" type="primary" @click="predictRatio">
          开始预测
        </el-button>
        <el-button class="Blendingbutton_2" type="primary" @click="editRatioCoalVisible = false">
          取消
        </el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import * as echarts from 'echarts/core'
import { GaugeChart } from 'echarts/charts'
import { TooltipComponent } from 'echarts/components'
import { CanvasRenderer } from 'echarts/renderers'
echarts.use([GaugeChart, TooltipComponent, CanvasRenderer])

export default {
  name: 'CurrentGauge',
  props: {
    value: { type: Number, default: 0 }
  },
  watch: {
    value (v) {
      this.renderChart(v)
    }
  },
  data () {
    return {
      // ECharts 实例
      chart1: null,
      chart2: null,
      chart3: null,
      chart4: null,
      chart5: null,
      chart6: null,
      /* —— 顶部导航 —— */
      activePage: 'echart',
      /* —— 仪表&进度相关 —— */
      pv: 35,
      sv: 35,
      current: 42.7,
      loadPercent: 0, // 初始装料进度 0%
      mixPercent: 0,
      mass: 12.5,
      volume: 9.3,
      conveyorTimer: null,
      blenderTimer: null,
      conveyorRunning: false,
      blenderRunning: false,
      bunkerPercents: [60, 45, 30, 80, 55], // 料仓示例

      /* —— 计时器句柄 —— */
      timerPV: null,
      timerLoad: null,
      chart: null,
      gettime: '',

      /* ① 6 类煤样列表（后端拉回来的原始数据） */
      coalList: [],
      coalList_2: [],
      coalList_3: [],
      coalList_4: [],
      coalList_5: [],
      coalList_6: [],

      /* ② 6 组多选表格的当前选中行 */
      multipleSelectionData: [],
      multipleSelectionData_2: [],
      multipleSelectionData_3: [],
      multipleSelectionData_4: [],
      multipleSelectionData_5: [],
      multipleSelectionData_6: [],

      modifyParametersForm: { params: [] },
      modifyParametersForm_2: { params: [] },
      modifyParametersForm_3: { params: [] },
      modifyParametersForm_4: { params: [] },
      modifyParametersForm_5: { params: [] },
      modifyParametersForm_6: { params: [] },
      modifyParametersForm_total: { params: [] },

      /* ③ 6 个弹框显隐（Element-UI 的 el-dialog） */
      editRatioCoalVisible1: false,
      editRatioCoalVisible2: false,
      editRatioCoalVisible3: false,
      editRatioCoalVisible4: false,
      editRatioCoalVisible5: false,
      editRatioCoalVisible6: false,
      editCoalDetailVisible: false, // “配煤决策”大弹窗
      editBlendCoalVisible: false, // “混合煤性质预测”
      editRatioCoalVisible: false, // “最优配煤比”
      /* —— 其它提示文字 —— */
      qiCoalattention: '',
      feiCoalattention: '',
      qifeiCoalattention: '',
      jiao13Coalattention: '',
      jiaoCoalattention: '',
      souCoalattention: '',

      /* —— 配煤预测相关 —— */
      coalRatio: [], // 输入比例
      totalRatio: 0,
      blendCoalProperty: [],
      preparedTotalResult: [],
      preparedDataforRatio: [],
      returnRatio: '',
      returnPrice: '',
      newRatio: [],
      returnTotalRatio: 0,
      max: 0,
      paraRange: [],
      /* —— 表格高度示例 —— */
      height: 600
    }
  },
  /* ————— 生命周期 ————— */
  created () {
    // 初始拉数据
    this.getCoalList()
    this.getCoalList_2()
    this.getCoalList_3()
    this.getCoalList_4()
    this.getCoalList_5()
    this.getCoalList_6()
  },
  mounted () {
    // 确保 ref 已挂载
    this.$nextTick(() => {
      this.initCharts()
      this.chart = echarts.init(this.$refs.chart)
      this.chart1 = echarts.init(this.$refs.chart1)
      this.chart2 = echarts.init(this.$refs.chart2)
      this.chart3 = echarts.init(this.$refs.chart3)
      this.chart4 = echarts.init(this.$refs.chart4)
      this.chart5 = echarts.init(this.$refs.chart5)
      this.chart6 = echarts.init(this.$refs.chart6)
      this.renderChart(this.pv)
    })
    /* —— 仪表盘初始化 —— */
    this.chart = echarts.init(this.$refs.chart)
    this.renderChart(this.pv)

    // 电流模拟
    this.timerPV = setInterval(() => {
      // 这里只示例随机，真实项目请替换为接口返回值
      this.pv = (30 + Math.random() * 10).toFixed(2)
      this.sv = (30 + Math.random() * 10).toFixed(2)
      this.current = (40 + Math.random() * 20).toFixed(2)
    }, 1000)

    /* —— ② 拉取煤样列表（示例用假数据；你可以改成真正的 this.$http.get） —— */
    this.getCoalList()
    this.getCoalList_2()
    this.getCoalList_3()
    this.getCoalList_4()
    this.getCoalList_5()
    this.getCoalList_6()

    /* —— 当前时间 —— */
    this.currentTime()

    window.addEventListener('resize', this.chart.resize)
  },
  beforeUnmount () {
    window.removeEventListener('resize', this.onWindowResize)

    // 释放 ECharts 实例
    if (this.chart1) this.chart1.dispose()
    if (this.chart2) this.chart2.dispose()
    if (this.chart3) this.chart3.dispose()
    if (this.chart4) this.chart4.dispose()
    if (this.chart5) this.chart5.dispose()
    if (this.chart6) this.chart6.dispose()

    this.chart.dispose()

    window.removeEventListener('resize', this.chart.resize)
    clearInterval(this.timerPV)
    this.stopConveyor()
    this.stopBlender()
    if (this.chart) this.chart.dispose()
  },
  methods: {
    initCharts() {
      this.chart1 = echarts.init(this.$refs.chart1)
      this.chart1.setOption(this.getRingOption(0, '#ff6666', '气煤'))

      this.chart2 = echarts.init(this.$refs.chart2)
      this.chart2.setOption(this.getRingOption(0, '#ffcc00', '肥煤'))

      this.chart3 = echarts.init(this.$refs.chart3)
      this.chart3.setOption(this.getRingOption(0, '#66ff66', '气肥煤'))

      this.chart4 = echarts.init(this.$refs.chart4)
      this.chart4.setOption(this.getRingOption(0, '#ff6666', '1/3焦煤'))

      this.chart5 = echarts.init(this.$refs.chart5)
      this.chart5.setOption(this.getRingOption(0, '#ffcc00', '焦煤'))

      this.chart6 = echarts.init(this.$refs.chart6)
      this.chart6.setOption(this.getRingOption(0, '#66ff66', '瘦煤'))
    },
    getRingOption(value, color, title) {
      const remain = 100 - value
      return {
        backgroundColor: 'transparent',
        series: [
          {
            name: title,
            type: 'pie',
            center: ['50%', '50%'],
            radius: ['50%', '60%'],
            label: { show: false },
            labelLine: { show: false },
            data: [
              { value, itemStyle: { color } },
              { value: remain, itemStyle: { color: '#555555' } }
            ]
          }
        ],
        graphic: [
          {
            type: 'text',
            left: '45%',
            top: '45%',
            style: {
              text: `${value}%`,
              fill: color,
              font: 'bold 18px sans-serif',
              textAlign: 'center'
            }
          },
          {
            type: 'text',
            left: '10%',
            top: '10%',
            style: {
              text: title,
              fill: color,
              font: '16px sans-serif',
              textAlign: 'left'
            }
          }
        ]
      }
    },
    onWindowResize() {
      const container = this.$refs.container
      if (!container) return
      this.camera.aspect = container.clientWidth / container.clientHeight
      this.camera.updateProjectionMatrix()
      this.renderer.setSize(container.clientWidth, container.clientHeight)

      if (this.chart1) this.chart1.resize()
      if (this.chart2) this.chart2.resize()
      if (this.chart3) this.chart3.resize()
      if (this.chart4) this.chart4.resize()
      if (this.chart5) this.chart5.resize()
      if (this.chart6) this.chart6.resize()
    },
    /* ===================== 一、拉数据 ===================== */
    async getCoalList() {
      // 示例： this.$http.get('getQiCoal') ...
      // 下面用伪代码或示例结构
      // 根据实际接口返回的数据结构修改
      try {
        const ret = await this.$http.get('getQiCoal')
        this.coalList = ret.data.msg
        this.coalList.reverse()
      } catch (error) {
        console.error(error)
      }
    },
    async getCoalList_2() {
      try {
        const ret = await this.$http.get('getFeiCoal')
        this.coalList_2 = ret.data.msg
        this.coalList_2.reverse()
      } catch (error) {
        console.error(error)
      }
    },
    async getCoalList_3() {
      try {
        const ret = await this.$http.get('getQiFeiCoal')
        this.coalList_3 = ret.data.msg
        this.coalList_3.reverse()
      } catch (error) {
        console.error(error)
      }
    },
    async getCoalList_4() {
      try {
        const ret = await this.$http.get('get31JiaoCoal')
        this.coalList_4 = ret.data.msg
        this.coalList_4.reverse()
      } catch (error) {
        console.error(error)
      }
    },
    async getCoalList_5() {
      try {
        const ret = await this.$http.get('getJiaoCoal')
        this.coalList_5 = ret.data.msg
        this.coalList_5.reverse()
      } catch (error) {
        console.error(error)
      }
    },
    async getCoalList_6() {
      try {
        const ret = await this.$http.get('getShouCoal')
        this.coalList_6 = ret.data.msg
        this.coalList_6.reverse()
      } catch (error) {
        console.error(error)
      }
    },

    // pl-table 多选
    handleSelectionChange(val) {
      this.multipleSelectionData = val
    },
    handleSelectionChange_2(val) {
      this.multipleSelectionData_2 = val
    },
    handleSelectionChange_3(val) {
      this.multipleSelectionData_3 = val
    },
    handleSelectionChange_4(val) {
      this.multipleSelectionData_4 = val
    },
    handleSelectionChange_5(val) {
      this.multipleSelectionData_5 = val
    },
    handleSelectionChange_6(val) {
      this.multipleSelectionData_6 = val
    },

    // 选择/清空气煤
    selectQicoal() {
      this.editRatioCoalVisible1 = true
      this.qiCoalattention = ''
      let k = 0
      for (let i = 0; i < this.coalList.length; i++) {
        if (this.coalList[i].store_number < 50) {
          k += 1
          this.qiCoalattention += this.coalList[i].coal_name + ','
        }
      }
      if (k !== 0) {
        this.qiCoalattention += '煤样存储量不足，注意及时补充！'
      }
    },
    deleteQicoal() {
      this.multipleSelectionData = []
      this.modifyParametersForm = { params: [] }
    },

    // 选择/清空肥煤
    selectFeicoal() {
      this.editRatioCoalVisible2 = true
      this.feiCoalattention = ''
      let k = 0
      for (let i = 0; i < this.coalList_2.length; i++) {
        if (this.coalList_2[i].store_number < 50) {
          k += 1
          this.feiCoalattention += this.coalList_2[i].coal_name + ','
        }
      }
      if (k !== 0) {
        this.feiCoalattention += '煤样存储量不足，注意及时补充！'
      }
    },
    deleteFeicoal() {
      this.multipleSelectionData_2 = []
      this.modifyParametersForm_2 = { params: [] }
    },

    // 选择/清空气肥煤
    selectQiFeicoal() {
      this.editRatioCoalVisible3 = true
      this.qifeiCoalattention = ''
      let k = 0
      for (let i = 0; i < this.coalList_3.length; i++) {
        if (this.coalList_3[i].store_number < 50) {
          k += 1
          this.qifeiCoalattention += this.coalList_3[i].coal_name + ','
        }
      }
      if (k !== 0) {
        this.qifeiCoalattention += '煤样存储量不足，注意及时补充！'
      }
    },
    deleteQiFeicoal() {
      this.multipleSelectionData_3 = []
      this.modifyParametersForm_3 = { params: [] }
    },

    // 选择/清空1/3焦煤
    select13jiaocoal() {
      this.editRatioCoalVisible4 = true
      this.jiao13Coalattention = ''
      let k = 0
      for (let i = 0; i < this.coalList_4.length; i++) {
        if (
          this.coalList_4[i].store_number < 50 &&
          this.coalList_4[i].store_number > 0
        ) {
          k += 1
          this.jiao13Coalattention += this.coalList_4[i].coal_name + ','
        }
      }
      if (k !== 0) {
        this.jiao13Coalattention += '煤样存储量不足，注意及时补充！'
      }
    },
    delete13jiaocoal() {
      this.multipleSelectionData_4 = []
      this.modifyParametersForm_4 = { params: [] }
    },

    // 选择/清空焦煤
    selectjiaocoal() {
      this.editRatioCoalVisible5 = true
      this.jiaoCoalattention = ''
      let k = 0
      for (let i = 0; i < this.coalList_5.length; i++) {
        if (
          this.coalList_5[i].store_number < 50 &&
          this.coalList_5[i].store_number > 0
        ) {
          k += 1
          this.jiaoCoalattention += this.coalList_5[i].coal_name + ','
        }
      }
      if (k !== 0) {
        this.jiaoCoalattention += '煤样存储量不足，注意及时补充！'
      }
    },
    deletetjiaocoal() {
      this.multipleSelectionData_5 = []
      this.modifyParametersForm_5 = { params: [] }
    },

    // 选择/清空瘦煤
    selectshoucoal() {
      this.editRatioCoalVisible6 = true
      this.souCoalattention = ''
      let k = 0
      for (let i = 0; i < this.coalList_6.length; i++) {
        if (
          this.coalList_6[i].store_number < 50 &&
          this.coalList_6[i].store_number > 0
        ) {
          k += 1
          this.souCoalattention += this.coalList_6[i].coal_name + ','
        }
      }
      if (k !== 0) {
        this.souCoalattention += '煤样存储量不足，注意及时补充！'
      }
    },
    deletetshoucoal() {
      this.multipleSelectionData_6 = []
      this.modifyParametersForm_6 = { params: [] }
    },
    // 确认选择 => 将多选的煤保存到对应 form 中
    sendBlendingData() {
      this.modifyParametersForm = { params: [] }
      for (let i = 0; i < this.multipleSelectionData.length; i++) {
        this.modifyParametersForm.params.push({
          paramName: this.multipleSelectionData[i].coal_name,
          paramType: this.multipleSelectionData[i].coal_type,
          paramPrice: this.multipleSelectionData[i].coal_price
        })
      }
      this.editRatioCoalVisible1 = false
    },
    sendBlendingData_2() {
      this.modifyParametersForm_2 = { params: [] }
      for (let i = 0; i < this.multipleSelectionData_2.length; i++) {
        this.modifyParametersForm_2.params.push({
          paramName: this.multipleSelectionData_2[i].coal_name,
          paramType: this.multipleSelectionData_2[i].coal_type,
          paramPrice: this.multipleSelectionData_2[i].coal_price
        })
      }
      this.editRatioCoalVisible2 = false
    },
    sendBlendingData_3() {
      this.modifyParametersForm_3 = { params: [] }
      for (let i = 0; i < this.multipleSelectionData_3.length; i++) {
        this.modifyParametersForm_3.params.push({
          paramName: this.multipleSelectionData_3[i].coal_name,
          paramType: this.multipleSelectionData_3[i].coal_type,
          paramPrice: this.multipleSelectionData_3[i].coal_price
        })
      }
      this.editRatioCoalVisible3 = false
    },
    sendBlendingData_4() {
      this.modifyParametersForm_4 = { params: [] }
      for (let i = 0; i < this.multipleSelectionData_4.length; i++) {
        this.modifyParametersForm_4.params.push({
          paramName: this.multipleSelectionData_4[i].coal_name,
          paramType: this.multipleSelectionData_4[i].coal_type,
          paramPrice: this.multipleSelectionData_4[i].coal_price
        })
      }
      this.editRatioCoalVisible4 = false
    },
    sendBlendingData_5() {
      this.modifyParametersForm_5 = { params: [] }
      for (let i = 0; i < this.multipleSelectionData_5.length; i++) {
        this.modifyParametersForm_5.params.push({
          paramName: this.multipleSelectionData_5[i].coal_name,
          paramType: this.multipleSelectionData_5[i].coal_type,
          paramPrice: this.multipleSelectionData_5[i].coal_price
        })
      }
      this.editRatioCoalVisible5 = false
    },
    sendBlendingData_6() {
      this.modifyParametersForm_6 = { params: [] }
      for (let i = 0; i < this.multipleSelectionData_6.length; i++) {
        this.modifyParametersForm_6.params.push({
          paramName: this.multipleSelectionData_6[i].coal_name,
          paramType: this.multipleSelectionData_6[i].coal_type,
          paramPrice: this.multipleSelectionData_6[i].coal_price
        })
      }
      this.editRatioCoalVisible6 = false
    },

    // “配煤决策”按钮 => 打开对话框，收集所有煤种
    MakingDecision() {
      this.modifyParametersForm_total = { params: [] }
      // 将 6 类煤的多选结果合并
      for (let i = 0; i < this.multipleSelectionData.length; i++) {
        this.modifyParametersForm_total.params.push({
          paramName: this.multipleSelectionData[i].coal_name,
          paramType: this.multipleSelectionData[i].coal_type,
          paramPrice: this.multipleSelectionData[i].coal_price
        })
      }
      for (let i = 0; i < this.multipleSelectionData_2.length; i++) {
        this.modifyParametersForm_total.params.push({
          paramName: this.multipleSelectionData_2[i].coal_name,
          paramType: this.multipleSelectionData_2[i].coal_type,
          paramPrice: this.multipleSelectionData_2[i].coal_price
        })
      }
      for (let i = 0; i < this.multipleSelectionData_3.length; i++) {
        this.modifyParametersForm_total.params.push({
          paramName: this.multipleSelectionData_3[i].coal_name,
          paramType: this.multipleSelectionData_3[i].coal_type,
          paramPrice: this.multipleSelectionData_3[i].coal_price
        })
      }
      for (let i = 0; i < this.multipleSelectionData_4.length; i++) {
        this.modifyParametersForm_total.params.push({
          paramName: this.multipleSelectionData_4[i].coal_name,
          paramType: this.multipleSelectionData_4[i].coal_type,
          paramPrice: this.multipleSelectionData_4[i].coal_price
        })
      }
      for (let i = 0; i < this.multipleSelectionData_5.length; i++) {
        this.modifyParametersForm_total.params.push({
          paramName: this.multipleSelectionData_5[i].coal_name,
          paramType: this.multipleSelectionData_5[i].coal_type,
          paramPrice: this.multipleSelectionData_5[i].coal_price
        })
      }
      for (let i = 0; i < this.multipleSelectionData_6.length; i++) {
        this.modifyParametersForm_total.params.push({
          paramName: this.multipleSelectionData_6[i].coal_name,
          paramType: this.multipleSelectionData_6[i].coal_type,
          paramPrice: this.multipleSelectionData_6[i].coal_price
        })
      }
      // 打开配煤决策对话框
      this.editCoalDetailVisible = true
    },
    cancelDialog() {
      this.editCoalDetailVisible = false
      this.coalRatio = []
      this.totalRatio = 0
    },

    // 混合煤性质预测
    async predictBlendCoal() {
      this.totalRatio = 0
      if (this.coalRatio.length === 0) {
        this.$confirm('配煤比例总和须为100%', '提示', {
          confirmButtonText: '确定',
          type: 'warning',
          showCancelButton: false
        })
        return
      }
      // 计算用户输入的总配比
      for (let j = 0; j < this.coalRatio.length; j++) {
        this.totalRatio += Number(this.coalRatio[j])
      }
      if (this.totalRatio !== 100) {
        this.$confirm('配煤比例总和须为100%', '提示', {
          confirmButtonText: '确定',
          type: 'warning',
          showCancelButton: false
        })
        return
      }
      // 真正请求后端预测
      this.editBlendCoalVisible = true
      // 准备数据
      for (let i = 0; i < this.multipleSelectionData.length; i++) {
        this.preparedTotalResult.push({
          id: this.multipleSelectionData[i].id,
          coalRatio: this.coalRatio[i],
          coal_mad: this.multipleSelectionData[i].coal_mad,
          coal_ad: this.multipleSelectionData[i].coal_ad,
          coal_vdaf: this.multipleSelectionData[i].coal_vdaf,
          coal_std: this.multipleSelectionData[i].coal_std,
          G: this.multipleSelectionData[i].G,
          X: this.multipleSelectionData[i].X,
          Y: this.multipleSelectionData[i].Y
        })
      }
      // 依次把多选2~6里的也 push 进 preparedTotalResult，记得注意索引位置
      // 下方仅示例做法，需根据实际情况再行校正
      let offset = this.multipleSelectionData.length
      for (let i = 0; i < this.multipleSelectionData_2.length; i++) {
        this.preparedTotalResult.push({
          id: this.multipleSelectionData_2[i].id,
          coalRatio: this.coalRatio[offset + i],
          coal_mad: this.multipleSelectionData_2[i].coal_mad,
          coal_ad: this.multipleSelectionData_2[i].coal_ad,
          coal_vdaf: this.multipleSelectionData_2[i].coal_vdaf,
          coal_std: this.multipleSelectionData_2[i].coal_std,
          G: this.multipleSelectionData_2[i].G,
          X: this.multipleSelectionData_2[i].X,
          Y: this.multipleSelectionData_2[i].Y
        })
      }
      offset += this.multipleSelectionData_2.length
      for (let i = 0; i < this.multipleSelectionData_3.length; i++) {
        this.preparedTotalResult.push({
          id: this.multipleSelectionData_3[i].id,
          coalRatio: this.coalRatio[offset + i],
          coal_mad: this.multipleSelectionData_3[i].coal_mad,
          coal_ad: this.multipleSelectionData_3[i].coal_ad,
          coal_vdaf: this.multipleSelectionData_3[i].coal_vdaf,
          coal_std: this.multipleSelectionData_3[i].coal_std,
          G: this.multipleSelectionData_3[i].G,
          X: this.multipleSelectionData_3[i].X,
          Y: this.multipleSelectionData_3[i].Y
        })
      }
      offset += this.multipleSelectionData_3.length
      // 依次下去 ...
      // 这里示例省略，合并完后：
      // 发请求
      try {
        const res = await this.$http.post('predictBlendCoalQuality', this.preparedTotalResult)
        // 后端返回混合煤性质
        this.blendCoalProperty = res.data
      } catch (error) {
        console.error(error)
      }
      // 清空
      this.preparedTotalResult = []
    },

    // 最优配煤比预测
    predictBestRatio() {
      this.editRatioCoalVisible = true
    },

    // 在最优配煤比对话框中点击“开始预测”
    /* async predictRatio() {
      // 准备数据
      for (let i = 0; i < this.multipleSelectionData.length; i++) {
        this.preparedDataforRatio.push({
          coal_price: this.multipleSelectionData[i].coal_price,
          coke_CSR: this.multipleSelectionData[i].coke_CSR,
          coke_CRI: this.multipleSelectionData[i].coke_CRI,
          coke_M10: this.multipleSelectionData[i].coke_M10,
          coke_M25: this.multipleSelectionData[i].coke_M25
        })
      }
      // 类似地把 multipleSelectionData_2 ~ _6 也 push 进去
      // ...
      // 把用户输入的 paraRange 也放进去
      this.preparedDataforRatio.push(this.paraRange)

      try {
        const res = await this.$http.post('predictBestRatio', this.preparedDataforRatio)
        if (res.data[0] === 'NoPrice') {
          this.$confirm('选择的煤样中缺少价格参数', '提示', {
            confirmButtonText: '确定',
            type: 'warning',
            showCancelButton: false
          })
        } else if (res.data[0] === 'Error') {
          this.$confirm('未能从设定范围空间中寻找到最优配煤比，请重新设置或扩大参数范围', '提示', {
            confirmButtonText: '确定',
            type: 'warning',
            showCancelButton: false
          })
        } else {
          this.returnPrice = res.data['1'][0][0].toFixed(2)
          this.returnRatio = ''
          this.newRatio = []
          // 同时修正比例之和为100
          this.returnTotalRatio = 0
          this.max = res.data['0'][0][0]
          const arr = res.data['0'][0]
          for (let i = 0; i < arr.length; i++) {
            this.returnTotalRatio += arr[i] * 100
          }
          // 找到最大值下标，把多余或不足分配到此
          let idxMax = 0
          let valMax = arr[0]
          for (let i = 1; i < arr.length; i++) {
            if (arr[i] > valMax) {
              valMax = arr[i]
              idxMax = i
            }
          }
          if (this.returnTotalRatio < 100) {
            arr[idxMax] += (100 - this.returnTotalRatio) / 100
          } else if (this.returnTotalRatio > 100) {
            arr[idxMax] -= (this.returnTotalRatio - 100) / 100
          }
          // 生成最终显示
          for (let i = 0; i < arr.length; i++) {
            this.returnRatio += (arr[i] * 100).toFixed(2) + '%\xa0\xa0\xa0\xa0'
            this.newRatio.push((arr[i] * 100).toFixed(2))
          }
          // 覆盖到 coalRatio
          this.coalRatio = this.newRatio
        }
      } catch (error) {
        console.error(error)
      } finally {
        this.preparedDataforRatio = []
      }
    } */
    async predictRatio() {
      const arr = [0.41, 0.45, 0.14] // 比例
      this.returnPrice = 843.27 // 假装返回的价格
      this.returnRatio = '' // 用来拼接显示的文本
      this.newRatio = []

      let total = 0
      for (let i = 0; i < arr.length; i++) {
        total += arr[i] * 100
      }
      if (total === 100) {
        for (let i = 0; i < arr.length; i++) {
          // 把数值拼接成百分比字符串
          this.returnRatio += (arr[i] * 100).toFixed(2) + '%\xa0\xa0\xa0\xa0'
          this.newRatio.push((arr[i] * 100).toFixed(2))
        }
        // 覆盖到 coalRatio
        this.coalRatio = this.newRatio
        // 接下来，更新 3 个环形图：
        this.chart1.setOption(this.getRingOption(Number(this.newRatio[0]), '#ff6666', '兴义'))
        this.chart2.setOption(this.getRingOption(Number(this.newRatio[1]), '#ffcc00', '霍州'))
        this.chart3.setOption(this.getRingOption(Number(this.newRatio[2]), '#66ff66', '陆良'))
      }

      // 清空请求参数
      this.preparedDataforRatio = []
    },
    startConveyor () {
      if (this.conveyorTimer) return
      this.conveyorRunning = true
      this.conveyorTimer = setInterval(() => {
        if (this.loadPercent >= 100) {
          this.stopConveyor(); return
        }
        this.loadPercent = Math.min(this.loadPercent + 5, 100)
      }, 1000)
    },
    stopConveyor () {
      clearInterval(this.conveyorTimer)
      this.conveyorTimer = null
      this.conveyorRunning = false
    },

    startBlender () {
      if (this.blenderTimer) return
      this.blenderRunning = true
      this.blenderTimer = setInterval(() => {
        if (this.mixPercent >= 100) { this.stopBlender(); return }
        this.mixPercent = Math.min(this.mixPercent + 5, 100)
      }, 1000)
    },
    stopBlender () {
      clearInterval(this.blenderTimer)
      this.blenderTimer = null
      this.blenderRunning = false
    },

    openSettings () {
      this.$message.info('打开设置面板')
    },
    renderChart (val) {
      this.chart.setOption({
        tooltip: { formatter: '{a}<br/>{c} A' },
        series: [{
          name: 'Electric current',
          type: 'gauge',
          min: 0,
          max: 100,
          pointer: { width: 4, length: '70%' },
          detail: {
            offsetCenter: [0, '75%'],
            formatter (v) {
              const style = v < 70 ? 'blue' : v < 90 ? 'orange' : 'red'
              return `{title|当前电流}\n{${style}|${v} A}`
            },
            rich: {
              title: { fontSize: 14, color: '#cccccc', lineHeight: 20 },
              blue: { fontSize: 24, fontFamily: 'Digital7', fontWeight: 'bold', lineHeight: 30, color: '#00cfff' },
              orange: { fontSize: 24, fontFamily: 'Digital7', fontWeight: 'bold', lineHeight: 30, color: '#ffa500' },
              red: { fontSize: 24, fontFamily: 'Digital7', fontWeight: 'bold', lineHeight: 30, color: '#c00000' }
            }
          },
          data: [{ value: val }]
        }]
      })
    },
    currentTime () {
      setInterval(() => {
        const now = new Date()
        const yy = now.getFullYear()
        const mm = now.getMonth() + 1
        const dd = now.getDate()
        const hh = now.getHours()
        const mf = now.getMinutes() < 10 ? '0' + now.getMinutes() : now.getMinutes()
        const ss = now.getSeconds() < 10 ? '0' + now.getSeconds() : now.getSeconds()
        this.gettime = `${yy} / ${mm} / ${dd}   ${hh} : ${mf} : ${ss}`
      }, 500)
    },
    returnHome () { window.sessionStorage.clear(); this.$router.push('/login') },
    switchEchartPage () { this.activePage = 'echart'; this.$router.push('/EchartPage') },
    switchMixingRatioPrediction () { this.activePage = 'mixing'; this.$router.push('/MixingPrediction') },
    switchCokeDigitalTwin () { this.activePage = 'coke'; this.$router.push('/cokeDigitalTwin') },
    switchQuenching () { this.activePage = 'quenching'; this.$router.push('/quenching') },
    switchPush () { this.activePage = 'push'; this.$router.push('/push') },
    switchCool () { this.activePage = 'cool'; this.$router.push('/cool') },
    emergencyStop () { this.$message.error('紧急停止已触发！') }
  },

  beforeDestroy () {
    clearInterval(this.timerPV)
    this.chart.dispose()
    window.removeEventListener('resize', this.chart.resize)
    this.stopConveyor()
    this.stopBlender()
  }
}
</script>

<style scoped>
/* ===== 顶部栏与按钮 ===== */
.header-bar {
  min-height: 200px;
  padding: 24px 0 34px;
  background: url('~@/assets/top_1.jpg') center/cover no-repeat;
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
}

/* 其余 header、按钮等样式保持不变 —— 从原文件粘贴 ↓↓↓ */
.userguide {
  position: absolute;
  top: 14px;
  left: 2.5%;
  font-size: 1.2rem;
  color: #ffd700;
  font-weight: 600;
  text-decoration: none;
}
.userguide:hover {
  color: #fff176;
  text-decoration: underline;
}
.exitbuttion {
  position: absolute;
  top: 12px;
  right: 2.5%;
  background: transparent;
  color: #ffd700 !important;
  font-weight: 600;
  border: none;
  font-size: 1.2rem;
}
.exitbuttion:hover {
  color: #fff176 !important;
  text-decoration: underline;
}
/* 标题 + 工具行 */
.header-title-time {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1.4rem;
}
.title {
  font-size: 3.6rem;
  font-weight: 900;
  color: #ffffff;
  letter-spacing: 5px;
  text-shadow: 0 0 10px #00ffff, 0 0 18px #007bff;
  text-align: center;
}
.toolbar-line {
  display: flex;
  align-items: center;
  gap: 24rem;
  flex-wrap: wrap;
}
.info-line {
  display: flex;
  align-items: center;
  gap: 1.6rem;
}
.lab_name,
.currenttime {
  font-size: 1.6rem;
  font-weight: 600;
}
.lab_name {
  color: #b8ecff;
}
.currenttime {
  color: #00e0ff;
}
.button-group {
  display: flex;
  gap: 64px;
  flex-wrap: wrap;
}
.selection {
  padding: 20px 24px !important;
  border-radius: 10px !important;
  font-size: 1.6rem !important;
  font-weight: 700 !important;
  background: linear-gradient(145deg, #0c2333, #00334d) !important;
  color: #ffffff !important;
  border: 2px solid #00eaff !important;
  box-shadow: 0 0 14px rgba(0, 255, 255, 0.6);
  transition: all 0.3s ease;
  min-width: 160px;
  text-align: center;
}
.selection:hover {
  background: linear-gradient(145deg, #095573, #006c8e) !important;
  transform: scale(1.05);
  box-shadow: 0 0 16px rgba(0, 255, 255, 0.8);
}
.selection.active {
  background: linear-gradient(145deg, #00475f, #007c9f) !important;
  border: 3px solid #00ffff !important;
  box-shadow: 0 0 22px #00ffff !important;
  color: #ffffff !important;
}

/* ===== 主体区 ===== */
.main-area {
  /* 关键：相对定位，让子元素（视频）绝对布局，仅覆盖主体 */
  position: relative;
  min-height: calc(100vh - 200px); /* 减去 header 高度 */
  padding: 20px;
  box-sizing: border-box;
  overflow: hidden; /* 防止溢出滚动条 */
  background-color: transparent; /* 顶层不再需要背景色 */
}
/* 视频仅铺满主体 */
.background-video {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  z-index: -1;
}

/* 主体内容的布局保持原样 */
.content-space {
  display: flex;
  justify-content: space-evenly;
  gap: 120px;
  margin-top: 100px;
}
.column-group {
  display: flex;
  flex-direction: column;
  gap: 40px;
}
.column-spacer {
  width: 40px;
}
.content-box {
  width: 300px;
  height: 180px;
  background: rgba(0, 255, 255, 0.05);
  border: 1px solid #00eaff;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 255, 255, 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #00eaff;
  font-size: 1.4rem;
}
/* 整体外框：左右两列并排 */
.charts-wrapper {
  position: absolute;
  top: 2%;
  left: 20px;            /* 与右侧同样边距 */
  right: 20px;
  height: 95%;
  display: flex;
  justify-content: space-between; /* 左列靠左，右列靠右 */
  /* 中央自然留空，无需 gap（或保留 20px 亦可） */
}

.charts-wrapper h1 {
  margin: 4px 0;
  font-weight: bold;
  color: white; /* 设置字体颜色为白色 */
  text-align: center; /* 居中 */
}

.charts-column {
  flex: 0 0 30%;     /* 固定 1/3 宽，不再伸缩 */
  max-width: 30%;

  display: flex;
  flex-direction: column;
  gap: 20px;
  overflow-y: auto;

  background: rgba(0, 0, 0, 0.3);
  border-radius: 10px;
  padding: 10px;
  box-shadow: 0 0 15px rgba(0, 255, 255, 0.5),
              0 0 30px rgba(0, 255, 255, 0.3);
}

/* 让同列中的两张卡片平分高度（≈各占 50%） */
.chart-container {
  flex: 1;
  width: 100%;
  height: 100%;
  padding: 14px 18px;

  /* 渐变替换原来的纯黑色背景 */
  background: linear-gradient(to right, #001f3f 0%, #001848 100%);

  border-radius: 8px;
  position: relative;
  box-sizing: border-box;
  box-shadow:
    inset 0 0 8px rgba(0, 255, 255, 0.15),
    0 0 12px rgba(0, 255, 255, 0.25);
}

/* 整体文本框样式 */
.info-block {
  padding: 20px;
  background: linear-gradient(45deg, rgba(0, 255, 255, 0.2), rgba(0, 204, 255, 0.3)); /* 渐变背景 */
  border-radius: 10px;
  box-shadow: 0 0 20px rgba(0, 255, 255, 0.5), 0 0 40px rgba(0, 255, 255, 0.2);
  transition: all 0.3s ease;
}

/* 信息行 */
.info-block p {
  color: #fff; /* 白色字体 */
  font-family: 'Orbitron', sans-serif; /* 使用科技感的字体 */
  font-size: 18px;
  margin: 15px 0;
  text-shadow: 0 0 8px rgba(0, 255, 255, 0.6), 0 0 16px rgba(0, 255, 255, 0.4); /* 发光效果 */
  letter-spacing: 0.5px; /* 增加字间距 */
}

/* 强调文本 (例如状态) */
.info-block span {
  font-weight: bold;
  font-size: 20px;
  color: #00ffcc; /* 亮绿色或者科技蓝 */
  text-shadow: 0 0 10px rgba(0, 255, 255, 1), 0 0 20px rgba(0, 255, 255, 1);
  animation: glow 1.5s infinite alternate;
}

/* 鼠标悬停时的效果 */
.info-block:hover {
  transform: scale(1.05);
  box-shadow: 0 0 40px rgba(0, 255, 255, 0.7), 0 0 60px rgba(0, 255, 255, 0.3);
  background: linear-gradient(45deg, rgba(0, 255, 255, 0.5), rgba(0, 204, 255, 0.5)); /* 增强渐变效果 */
}

/* 增加小的动感效果 */
@keyframes glow {
  0% { text-shadow: 0 0 10px rgba(0, 255, 255, 1), 0 0 20px rgba(0, 255, 255, 1); }
  50% { text-shadow: 0 0 20px rgba(0, 255, 255, 1), 0 0 40px rgba(0, 255, 255, 1); }
  100% { text-shadow: 0 0 10px rgba(0, 255, 255, 1), 0 0 20px rgba(0, 255, 255, 1); }
}
.value-box{
  min-width:70px;
  padding:4px 8px;
  background:rgba(0,255,255,.08);
  border:1px solid #00eaff;
  border-radius:4px;
  font-family:'Orbitron',sans-serif;
  font-size:18px;
  text-align:right;
  color:#00ffcc;
  box-shadow:inset 0 0 6px rgba(0,255,255,.4);
}

/* 急停按钮行只需按钮发光，文字继承原样 */
.stop-row{ gap:14px; }

.stop-btn{
  width:46px;
  height:46px;
  border-radius:50%;
  background:#c20000;
  border:3px solid #770000;
  box-shadow:0 0 12px rgba(255,0,0,.8);
  cursor:pointer;
  transition:transform .15s;
}
.stop-btn:hover{
  transform:scale(1.12);
  box-shadow:0 0 20px rgba(255,60,60,.9);
}
.progress-row{
  display:flex;
  align-items:center;
  gap:10px;
  margin:15px 0;

  font-family:'Orbitron',sans-serif;
  font-size:18px;
  color:#fff;
  text-shadow:0 0 8px rgba(0,255,255,.6),
               0 0 16px rgba(0,255,255,.4);
}
/* 进度条外壳：黑底表示“待下载” */
.progress-wrap{
  position:relative;
  flex:1;
  height:16px;
  border:1px solid #00eaff;
  border-radius:8px;
  background:#111;
  overflow:hidden;
  box-shadow:inset 0 0 6px rgba(0,255,255,.4);
}

/* 蓝色填充：已完成部分 */
.progress-fill{
  height:100%;
  background:linear-gradient(90deg,#00cfff 0%,#007bff 100%);
  transition:width .5s ease;
  box-shadow:
    0 0 8px   rgba(0,255,255,.8),
    0 0 14px  rgba(0,255,255,.6),
    0 0 24px  rgba(0,255,255,.4);
}

/* 右端百分比数字 */
.progress-digit{
  position:absolute;
  right:10px;
  top:50%;
  transform:translateY(-50%) scale(.8);
  font-size:18px;
  font-family:'Orbitron',sans-serif;
  color:#00eaff;
  animation:glowPulse 1.8s ease-in-out infinite;
  pointer-events:none;
}

/* 放大动画：0.8 → 1.15 → 1 */
@keyframes pop{
  0%   { transform:translateY(-50%) scale(.8); }
  60%  { transform:translateY(-50%) scale(1.15); }
  100% { transform:translateY(-50%) scale(1); }
}

/* 传送带状态*/
/* 带边框的状态行 */
.status-row{
  display:flex;
  align-items:center;
  gap:14px;
  flex-wrap:wrap;
  margin-bottom:14px;
  font-family:'Orbitron',sans-serif;
  font-size:18px;
  color:#fff;
  text-shadow:0 0 8px rgba(0,255,255,.6),
              0 0 16px rgba(0,255,255,.4);
}

/* 外框、字体与之前一致，这里仅列颜色和发光修改 */

/* ——— 圆点 —— */
.status-dot{
  width:22px;height:22px;border-radius:50%;
  border:2px solid #000;
}

/* 运行：亮绿 + 发光 */
.status-dot.run{
  background:#18c63d;
  box-shadow:0 0 10px #18c63d;
}

/* 停止：亮红，无发光 */
.status-dot.stop{
  background:#c00000;
}

/* ——— 图例 —— */
.legend-row{
  display:flex;
  align-items:center;
  gap:12px;
  margin:10px 0;
  font-size:18px;
  color:#dfe4ea;
}

/* 基础灰点 */
.legend-dot{
  display:inline-block;
  width:18px;height:18px;border-radius:50%;
  border:1px solid #000;
  margin:0 6px;
  background:#333;           /* 默认熄灭 */
}
/* 发光状态 */
.legend-dot.run.active  { background:#18c63d; box-shadow:0 0 8px #18c63d; }
.legend-dot.stop.active { background:#c00000; box-shadow:0 0 8px #ff4444; }

/* 方形按钮容器，固定表盘内部右下角 */
.btn-group{
  position: absolute;
  bottom: 14px;            /* 与底边距离 */
  right: 18px;             /* 与右边距离 */
  display: flex;
  gap: 16px;               /* 两按钮间距 */
}

/* 通用方形按钮基础 */
.square-btn{
  width: 96px;
  height: 44px;
  border-radius: 6px;
  font-size: 18px;
  font-weight: 600;
  color: #fff;
  border: none;
  cursor: pointer;
  transition: transform .15s, box-shadow .15s;
}

.settings-btn{
  background: linear-gradient(145deg, #e0e0e0, #b4b4b4); /* 亮灰渐变 */
  color: #333;
  box-shadow: 0 0 10px rgba(200,200,200,.8);
}
.settings-btn:hover{
  transform: scale(1.06);
  box-shadow: 0 0 16px rgba(220,220,220,1);
}

/* 绿色“运行”——确认 */
.run-btn{
  background: linear-gradient(145deg, #18c63d, #0e8e2b);
  box-shadow: 0 0 10px rgba(24,198,61,.7);
}
.run-btn:hover{
  transform: scale(1.06);
  box-shadow: 0 0 16px rgba(24,198,61,.9);
}

/* 红色“急停”——取消 */
.stop-btn{
  background: linear-gradient(145deg, #c00000, #8a0000);
  box-shadow: 0 0 10px rgba(255,60,60,.8);
}
.stop-btn:hover{
  transform: scale(1.06);
  box-shadow: 0 0 16px rgba(255,60,60,1);
}
.legend-dot{
  display:inline-block;
  width:18px;height:18px;
  border-radius:50%;
  border:1px solid #000;
  margin:0 6px;
  background:#333;          /* 默认熄灭为深灰 */
}

/* 运行 / 停止 亮起颜色 */
.legend-dot.run.active { background:#18c63d; box-shadow:0 0 8px #18c63d; }
.legend-dot.stop.active{ background:#c00000; box-shadow:0 0 8px #ff4444; }
/* 数码管字体 */
@font-face{
  font-family:'Digital7';
  src:url("https://unpkg.com/digital-7@0.0.1/digital-7.woff2") format("woff2");
}

/* 表盘外框 */
.meter-box{
  width:100%;                 /* 覆盖原固定180px */
  height: 100%;
  padding:14px 18px;
  background:#000;
  border-radius:8px;
  box-shadow:
      inset 0 0 8px rgba(0,255,255,.15),
      0 0 12px rgba(0,255,255,.25);
  box-sizing:border-box;
  position: relative;
}

/* 行排版 */
.row{
  display:flex;
  align-items:flex-end;
  gap:8px;
  margin:6px 0;
}

/* 标签 / 单位 */
.label{
  font-size:14px;
  color:#ffa500;
  font-family:'Orbitron',sans-serif;
}
.unit{
  font-size:16px;
  color:#bbb;
}

/* 数字通用 */
.digit{
  font-family:'Digital7',monospace;
  letter-spacing:3px;
  line-height:1;
}

/* SV/PV = 白黄发光 */
.digit.v{
  font-family:'Digital7',monospace;
  font-size:30px;
  color:#fff;
  text-shadow:
      0 0 6px rgba(255,255,255,.9),
      0 0 12px rgba(255,255,170,.8);
}

/* 当前电流的数字样式，可参考 PV / SV 再来一个 */
.digit.cur{
  font-family:'Digital7',monospace;
  font-size:30px;
  color:#00cfff;
  text-shadow:0 0 6px rgba(0,255,255,.9),
              0 0 12px rgba(0,170,255,.8);
}
/* 左侧数字列 */
.metrics{
  display:flex;
  flex-direction:column;
  gap:6px;
  flex:1;                /* 占满剩余宽度 */
}

/* 一行排列的数码管容器 */
.meter-inline{
  display:flex;
  align-items:flex-end;   /* 与旧 .row 保持对齐方式 */
  gap:24px;               /* 数码管间距 */
}
/* —— 仅装料进度条专用 —— */
.charge-bar{
  /* 让外框本身也微微发光 */
  box-shadow:
    0 0 6px  rgba(0,255,255,.6),
    0 0 14px rgba(0,255,255,.4);
  /* 再深一点的底色对比 */
  background:#000;
}

/* 内层填充条：霓虹渐变＋流动动画 */
.charge-bar .progress-fill{
  background-size:200% 100%;
  /* 深 → 浅 → 深， 这样滑动时反差够大 */
  background-image:linear-gradient(
      90deg,
      #ff7b00 0%,
      #ffb700 20%,
      #ffc100 40%,
      #ffeb80 60%,   /* 最亮 */
      #ffb700 80%,
      #ff7b00 100%
  );
  animation: chargeFlow 2.5s linear infinite;
  box-shadow:
    0 0 10px rgba(255,180,0,.9),
    0 0 20px rgba(255,130,0,.7),
    0 0 35px rgba(255,80 ,0,.5);
}
/* 数字颜色同步 */
.charge-bar .progress-digit{
  color:#ffc100;
  animation: glowPulse 1.6s ease-in-out infinite;
}

/* —— 动画关键帧 —— */
@keyframes chargeFlow{
  0%   { background-position:0 0;   }
  100% { background-position:-200% 0;}
}
@keyframes glowPulse{
  0%,100%{ text-shadow:0 0 8px #00ffff, 0 0 18px #00ffff;}
  50%    { text-shadow:0 0 18px #00ffff,0 0 28px #00ffff;}
}
.echart {
  width:100%;
  height:180px;
  background-color: transparent;
  border-radius: 8px;
  box-shadow: inset 0 0 10px rgba(255, 255, 255, 0.2),
    0 0 10px rgba(0, 255, 255, 0.2);
  box-sizing: border-box;
}
.ring-row{
  display:flex;
  justify-content:space-around;   /* 三个平均分布，可改 space-between / center */
  align-items:center;
  gap:20px;                       /* 环形图之间的间隙，可自行调 */
  margin-top:10px;                /* 与标题留一点距离 */
}
.fixed-button-size {
  width: 80px;  /* 固定宽度 */
  height: 30px;  /* 固定高度 */
  text-align: center;  /* 确保文字居中 */
}
</style>
