<template>
    <fwb-navbar solid>
      <template #logo>
        <fwb-navbar-logo alt="Hermes logo" image-url="/images/logo.svg" link="#">
          Hermes
        </fwb-navbar-logo>
      </template>
      <template #default="{isShowMenu}">
        <fwb-navbar-collapse :is-show-menu="isShowMenu">
          <fwb-navbar-link link="/">
            <RouterLink to="/">Home</RouterLink>
          </fwb-navbar-link>
          <fwb-navbar-link link="/about">
            <RouterLink to="/about">About</RouterLink>
          </fwb-navbar-link>
          <fwb-navbar-link link="#">
            Pricing
          </fwb-navbar-link>
          <fwb-navbar-link link="#">
            Contact
          </fwb-navbar-link>
        </fwb-navbar-collapse>
      </template>
    </fwb-navbar>
</template>
  
<script setup>
import {
    FwbNavbar,
    FwbNavbarCollapse,
    FwbNavbarLink,
    FwbNavbarLogo,
} from 'flowbite-vue'
import { RouterLink, RouterView } from 'vue-router'
</script>