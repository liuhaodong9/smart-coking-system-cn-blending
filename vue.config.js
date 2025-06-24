module.exports = {
  publicPath: '/smart-coking-system-cn-blending/',
  devServer: {
    open: true,
    port: 8888
  },
  chainWebpack: (config) => {
    config.module
      .rule('glb') // 创建一个新的规则
      .test(/\.(glb|gltf)$/) // 匹配 .glb 和 .gltf 文件
      .use('file-loader') // 使用 file-loader
      .loader('file-loader')
      .options({
        outputPath: 'models', // 输出到 models 文件夹
        name: '[name].[hash].[ext]' // 文件名格式
      });
    // 输出 Webpack 配置以便调试
    console.log(config.toConfig());
  }
};
