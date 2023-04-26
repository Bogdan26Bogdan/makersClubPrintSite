<template>
    <hr>
  <p>Above this line is index.html</p>
  <img alt="Vue logo" src="./assets/logo.png">
  <p>This area is the App.vue - below this line is vueRouter for the components</p>
  <hr>
  <router-view /> <!--this is where the vue component get displayed-->
</template>

<script>


export default {
  name: 'App',
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
