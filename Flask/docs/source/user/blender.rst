步骤 1：打开 Shader Editor
切换到 Shading 工作区
在 Blender 顶部菜单栏，点击 "Shading" 选项卡，进入 Shading 工作区。这样可以同时看到 3D 视图和 Shader Editor。
步骤 2：选择对象和材质
选择你的对象

在 3D 视图中，点击选择你要导出的模型。
确保对象有材质

在右侧属性栏中，点击 "材质" 图标（圆球图标）。
如果对象没有材质，点击 "New" 创建一个新材质。
步骤 3：连接渐变到 Principled BSDF
查看节点布局

在 Shader Editor 中，你应该能看到 Principled BSDF 节点和 Material Output 节点。
添加 ColorRamp 节点（如果还没有）

按 Shift + A，选择 Color > ColorRamp，添加一个 ColorRamp 节点，用于创建颜色渐变。
连接节点

将 ColorRamp 节点的 Color 输出（右侧的小圆点）拖动并连接到 Principled BSDF 的 Base Color 输入端。

（示意图：ColorRamp 连接到 Principled BSDF 的 Base Color）

步骤 4：确保对象有正确的 UV 映射
切换到 UV Editing 工作区

在顶部菜单栏，点击 "UV Editing"，进入 UV Editing 工作区。
进入编辑模式

在 3D 视图中，选择对象并按 Tab 键进入编辑模式。
展开 UV

按 A 键选择所有面。
按 U 键，选择 Smart UV Project 或 Unwrap，根据模型选择合适的展开方式。
调整 UV 以确保贴图能正确应用。

（示意图：Smart UV Project 操作）

步骤 5：添加 Image Texture 节点用于烘焙
回到 Shading 工作区

切换回 Shading 工作区，继续编辑材质节点。
添加 Image Texture 节点

按 Shift + A，选择 Texture > Image Texture，添加一个 Image Texture 节点。
创建新图像

在 Image Texture 节点中，点击 New 按钮。
命名为例如 "GradientBake"，设置合适的分辨率（如 1024x1024），点击 OK。
连接 Image Texture 节点

将 Image Texture 节点的 Color 输出连接到 Principled BSDF 的 Base Color 输入端，暂时替代 ColorRamp 的连接。
步骤 6：设置烘焙参数并进行烘焙
选择渲染引擎

在右侧属性栏，点击 "Render Properties"（相机图标）。
确保渲染引擎设置为 Cycles（烘焙操作更稳定）。
打开 Bake 面板

在 Render Properties 下，找到 Bake 面板。
设置 Bake 类型

Bake Type 选择 Diffuse。
取消勾选 Direct 和 Indirect，只保留 Color。
选择要烘焙的图层

确保 Image Texture 节点中的 GradientBake 图像被选中（点击高亮）。
开始烘焙

点击 Bake 按钮，Blender 会将当前材质的颜色信息烘焙到 GradientBake 图像中。

（示意图：Bake 面板设置）

步骤 7：保存烘焙的贴图
保存图像

在 Image Texture 节点中，点击 Image 菜单，选择 Save As。
选择保存路径和文件格式（如 PNG），命名为 "gradient_bake.png"，然后点击 Save As Image。

（示意图：保存烘焙图像）

步骤 8：应用烘焙的贴图到材质
加载烘焙图像

在 Shader Editor 中，确保 Image Texture 节点已经加载了刚刚保存的 "gradient_bake.png"。
连接贴图

确保 Image Texture 节点的 Color 输出连接到 Principled BSDF 的 Base Color 输入端。

（示意图：Image Texture 连接到 Principled BSDF）

步骤 9：导出为 glTF
选择对象

在 3D 视图中，选择你要导出的对象。
导出 glTF

点击顶部菜单的 File -> Export -> glTF 2.0。
设置导出选项

Format 选择 glTF Binary (.glb)（推荐，所有内容打包在一个文件中）。
勾选 Selected Objects（如果只需要导出选中的对象）。
确保 Materials 选项为 Export。
在 Images 部分选择 Embed，以确保贴图被嵌入到 glb 文件中。

（示意图：glTF 导出设置）

完成导出

选择保存路径和文件名，点击 Export glTF 2.0 按钮，完成导出。
步骤 10：验证导出结果
使用查看器打开 glb 文件

你可以使用 Windows 3D Viewer、在线 glTF Viewer 或 Babylon.js Sandbox 等工具打开导出的 glb 文件，检查材质和颜色渐变是否正确显示。
检查贴图

确认颜色渐变贴图已经正确应用，没有色彩丢失或异常。
