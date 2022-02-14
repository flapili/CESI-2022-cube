<template>
  <div class="tw-h-screen tw-w-screen tw-flex tw-flex-col tw-items-center tw-justify-center tw-bg-blue-400">
    <q-card>
      <q-card-section v-if="errorMessage" class="tw-text-center tw-font-bold tw-text-2xl"> {{ errorMessage }}</q-card-section>
      <q-card-section v-else class="tw-text-center tw-font-bold tw-text-2xl"> Bienvenue {{ firstname }}</q-card-section>
    </q-card>
    <q-btn icon="home" to="/" class="tw-bg-white tw-text-blue-500 tw-mt-4 tw-text-xl">Accueil</q-btn>
  </div>
</template>

<script>
import { defineComponent, ref } from "vue";
import { useRoute } from "vue-router";

import { api } from "boot/axios";

export default defineComponent({
  name: "PageIndex",
  async setup() {
    const route = useRoute();
    const token = route.query.token;
    const firstname = ref("");

    const errorMessage = ref("");

    try {
      const data = await api.$post("/v1/user/register", { token });
      firstname.value = data.firstname;
    } catch (error) {
      if (!error.response) {
        errorMessage.value = "Service indisponible, veuillez réessayer plus tard";
      } else if (error.response.status === 409) {
        errorMessage.value = "Email déjà utilisé";
      } else if (error.response.status === 410) {
        errorMessage.value = "Lien expiré";
      } else if (error.response.status === 400) {
        errorMessage.value = "Lien invalide";
      }
    }

    return {
      firstname,
      errorMessage,
    };
  },
});
</script>
