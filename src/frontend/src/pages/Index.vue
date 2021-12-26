<template>
  <q-page>
    <div v-for="n in 1000" :key="n">test</div>
  </q-page>
</template>

<script>
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'PageIndex'
})
</script>
