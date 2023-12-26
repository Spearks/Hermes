<script setup>
import { RouterLink, RouterView } from 'vue-router'
import Navbar from './components/Navbar.vue';
import Footer from './components/Footer.vue';
</script>

<template>
  <header>
    <Navbar/>
  </header>
  
  <RouterView class="h-max"/>

  <Footer/>
</template>
