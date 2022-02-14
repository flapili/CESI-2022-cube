<template>
  <q-layout view="lHh Lpr lFf">
    <q-header elevated>
      <q-toolbar class="tw-flex tw-justify-center">
        <img src="~assets/logo.png" alt="logo" class="tw-h-32 tw-py-4 tw-cursor-pointer" @click="$router.push('/')" />
      </q-toolbar>
    </q-header>
    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>