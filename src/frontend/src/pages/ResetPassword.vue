<template>
  <div class="tw-h-screen tw-w-screen tw-flex tw-flex-col tw-items-center tw-justify-center tw-bg-blue-400">
    <q-card v-if="tokenIsValid">
      <q-card-section class="tw-text-center tw-font-bold tw-text-2xl"> Réinitialiser votre mot de passe </q-card-section>
      <q-card-section class="tw-flex tw-flex-col">
        <q-form ref="refRegisterForm" class="tw-flex tw-flex-col">
          <q-input outlined class="tw-mt-2" v-model="password" :rules="[(val) => val.length >= 8 || 'Mot de passe trop court']" label="Mot de passe" :type="showPassword ? 'text' : 'password'">
            <template v-slot:append>
              <q-icon :name="showPassword ? 'visibility' : 'visibility_off'" class="cursor-pointer" @click="showPassword = !showPassword" />
            </template>
          </q-input>
          <q-input outlined class="tw-mt-2" v-model="password2" :rules="[(val) => val == password || 'Les mots de passe ne correspondent pas']" label="Mot de passe" type="password" />
        </q-form>
        <q-btn class="tw-mt-2 tw-bg-blue-400" @click="resetPassword" :disabled="disabledButton">Réinitialiser</q-btn>
      </q-card-section>
    </q-card>
    <template v-else>
      <q-card>
        <q-card-section class="tw-font-bold tw-text-2xl"> Lien invalide </q-card-section>
      </q-card>
      <q-btn icon="home" to="/" class="tw-bg-white tw-text-blue-500 tw-mt-4 tw-text-xl">Accueil</q-btn>
    </template>
  </div>
</template>

<script>
import { defineComponent, ref, computed } from "vue";
import { useRoute } from "vue-router";
import { useQuasar } from "quasar";

import { api } from "boot/axios";

export default defineComponent({
  name: "PageIndex",
  async setup() {
    const route = useRoute();
    const token = route.query.token;

    const $q = useQuasar();

    const tokenIsValid = ref(true);

    try {
      await api.$get("/v1/reset_password/verify_token", { params: { token } });
    } catch (error) {
      tokenIsValid.value = false;
    }

    const password = ref("");
    const password2 = ref("");
    const showPassword = ref(false);
    const disabledButton = computed(() => password.value.length < 8 || password.value != password2.value);

    const resetPassword = async () => {
      await api.$post("/v1/reset_password", { token, password: password.value });
      $q.notify({ position: "top", message: "Mot de passe changé", type: "positive" });
    };
    return {
      tokenIsValid,
      resetPassword,
      password,
      password2,
      showPassword,
      disabledButton,
    };
  },
});
</script>
