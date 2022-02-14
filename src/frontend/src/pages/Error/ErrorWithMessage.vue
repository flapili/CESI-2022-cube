<template>
  <div class="tw-h-screen tw-w-screen tw-flex tw-flex-col tw-items-center tw-justify-center tw-bg-blue-400">
    <div class="tw-text-white tw-text-2xl tw-px-16">{{ message }}</div>
    <q-btn icon="home" to="/" class="tw-bg-white tw-text-blue-500 tw-mt-4 tw-text-xl">Accueil</q-btn>
  </div>
</template>

<script>
import { defineComponent } from "vue";
import { useRoute } from "vue-router";

export default defineComponent({
  name: "ErrorWithMessage",
  async setup() {
    const route = useRoute();
    const message = route.query.message;
    return {
      message,
    };
  },
});
</script>
