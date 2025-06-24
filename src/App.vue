<template>
  <div id="app">
    <!-- 全局背景视频，仅加载一次 -->
    <video
      class="background-video"
      autoplay
      muted
      loop
      playsinline
      preload="auto"
    >
      <source src="@/assets/blendingPlant.mp4" type="video/mp4" />
      您的浏览器不支持 HTML5 视频。
    </video>

    <!-- 路由内容 -->
    <router-view />
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
/* 这些是全局样式，不要 scoped */
html,
body,
#app {
  margin: 0;
  padding: 0;
  height: 100%;
  overflow: hidden;
}

.background-video {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  object-fit: cover; /* 或 contain 看需求 */
  z-index: -1;      /* 确保所有前景内容在视频之上 */
}
</style>
