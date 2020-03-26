<template>
  <div id="app"> 
    <!-- <TodoList/> -->
    <!-- <Login/> -->
    <Sports/>
  </div>
</template>

<script>
import HelloWorld from './components/HelloWorld'
import TodoList from './components/TodoList'
import Login from './components/Login'
import Sports from './components/Sports'

export default {
  name: 'App',
  components: {
    HelloWorld,
    TodoList,
    Login,
    Sports
  }
}
</script>

<style>

</style>
