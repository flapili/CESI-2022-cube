<template>
  <suspense>
    <router-view />
  </suspense>
</template>
<script>
import { defineComponent } from "vue";

export default defineComponent({
  name: "App",
});
</script>
