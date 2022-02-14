<template>
  <q-page class="tw-flex tw-flex-col tw-bg-secondary">
    <q-tabs v-model="tab" no-caps class="tw-text-white tw-bg-primary">
      <q-tab name="logIn" label="Connexion" />
      <q-tab name="signIn" label="Inscription" />
    </q-tabs>
    <div class="tw-grow tw-flex tw-justify-center tw-items-center">
      <q-form v-if="tab === 'signIn'" ref="refRegisterForm" class="tw-flex tw-flex-col md:tw-w-1/3 tw-py-16 tw-gap-2">
        <q-input filled square bg-color="white" v-model="registerForm.firstname" label="Prénom" :rules="[(val) => !!val || 'Prénom manquant']" />
        <q-input filled square bg-color="white" v-model="registerForm.lastname" label="Nom" :rules="[(val) => !!val || 'Nom manquant']" />
        <q-input
          filled
          square
          bg-color="white"
          v-model="registerForm.phoneNumber"
          label="Numéro de téléphone"
          type="tel"
          :rules="[(val) => !!val || 'Téléphone manquant', (val) => isValidPhoneNumber(val) || 'Téléphone invalide']"
        >
          <template v-slot:prepend>
            <q-icon name="fas fa-mobile-alt" />
          </template>
        </q-input>
        <q-input
          filled
          square
          bg-color="white"
          v-model="registerForm.email"
          :rules="[(val) => !!val || 'Email manquant', (val) => isValidEmail(val) || 'Email invalide']"
          label="Adresse email"
          type="email"
        >
          <template v-slot:prepend> <q-icon name="fas fa-at" /></template>
        </q-input>
        <q-input
          filled
          square
          bg-color="white"
          v-model="registerForm.password"
          :rules="[(val) => val.length >= 8 || 'Mot de passe trop court']"
          label="Mot de passe"
          :type="showPassword ? 'text' : 'password'"
        >
          <template v-slot:prepend>
            <q-icon name="fas fa-lock" />
          </template>
          <template v-slot:append>
            <q-icon :name="showPassword ? 'visibility' : 'visibility_off'" class="cursor-pointer" @click="showPassword = !showPassword" />
          </template>
        </q-input>
        <q-input filled square stack-label bg-color="white" v-model="registerForm.birthday" :rules="[(val) => !!val || 'Date invalide']" label="Date de naissance" type="date">
          <template v-slot:prepend>
            <q-icon name="far fa-calendar" />
          </template>
        </q-input>
        <q-btn class="tw-bg-black tw-text-white tw-rounded-none tw-shadow-sm tw-shadow-black tw-mb-2" @click="resetRegisterForm">Réinitialiser</q-btn>
        <q-btn class="tw-bg-primary tw-text-white tw-rounded-none tw-shadow-sm tw-shadow-black" @click="signIn" :disable="disabledRegister">S'inscrire</q-btn>
      </q-form>
      <q-form v-if="tab === 'logIn'" class="tw-flex tw-flex-col md:tw-w-1/3 tw-py-16 tw-py-16 tw-gap-4">
        <q-input filled square bg-color="white" v-model="email" @keyup.enter="!disabledLogin && logIn()" label="Adresse email" type="email">
          <template v-slot:prepend>
            <q-icon name="fas fa-at" />
          </template>
        </q-input>
        <q-input filled square bg-color="white" class="tw-mt-2" v-model="password" @keyup.enter="!disabledLogin && logIn()" label="Mot de passe" :type="showPassword ? 'text' : 'password'">
          <template v-slot:prepend> <q-icon name="fas fa-lock" /></template>
          <template v-slot:append>
            <q-icon :name="showPassword ? 'visibility' : 'visibility_off'" class="cursor-pointer" @click="showPassword = !showPassword" />
          </template>
        </q-input>
        <q-btn class="tw-bg-primary tw-text-white tw-rounded-none" @click="logIn" :disable="disabledLogin" :loading="isLogin"> Connexion </q-btn>
      </q-form>
    </div>
  </q-page>
</template>

<script>
import { defineComponent, ref, reactive, computed } from "vue";
import { useStore } from "vuex";
import { useRouter } from "vue-router";
import { useQuasar, date } from "quasar";

import { api } from "boot/axios";

export default defineComponent({
  name: "PageInscriptionOrLogin",
  async setup() {
    const $q = useQuasar();
    const store = useStore();
    const router = useRouter();
    const tab = ref("logIn");

    const isValidEmail = (val) => {
      const re = /^(?=[a-zA-Z0-9@._%+-]{6,254}$)[a-zA-Z0-9._%+-]{1,64}@(?:[a-zA-Z0-9-]{1,63}\.){1,8}[a-zA-Z]{2,63}$/;
      return re.test(val);
    };

    const isValidPhoneNumber = (val) => {
      const re = /^(?:(?:\+|00)33[\s.-]{0,3}(?:\(0\)[\s.-]{0,3})?|0)[1-9](?:(?:[\s.-]?\d{2}){4}|\d{2}(?:[\s.-]?\d{3}){2})$/;
      return re.test(val);
    };

    const refRegisterForm = ref(null);
    const registerForm = reactive({
      firstname: "",
      lastname: "",
      email: "",
      password: "",
      phoneNumber: "",
      birthday: null,
    });
    const showPassword = ref(false);

    const resetRegisterForm = () => {
      registerForm.firstname = "";
      registerForm.lastname = "";
      registerForm.email = "";
      registerForm.password = "";
      registerForm.phoneNumber = "";
      registerForm.birthday = null;
      refRegisterForm.value.reset();
    };
    const disabledRegister = computed(
      () =>
        !registerForm.firstname ||
        !registerForm.lastname ||
        !registerForm.email ||
        !isValidEmail(registerForm.email) ||
        !registerForm.password ||
        registerForm.password.length < 8 ||
        !registerForm.phoneNumber ||
        !registerForm.birthday
    );

    const signIn = async () => {
      try {
        await api.$post("/v1/user", {
          firstname: registerForm.firstname,
          lastname: registerForm.lastname,
          email: registerForm.email,
          password: registerForm.password,
          phone_number: registerForm.phoneNumber,
          birthday: date.extractDate(registerForm.birthday, "YYYY-MM-DD"),
        });
        $q.notify({ position: "top", message: "Un email de confirmation vous a été envoyé", type: "positive" });
        await router.push("/");
      } catch (error) {
        if (!error.response) {
          $q.notify({ position: "top", message: "Vérifiez votre connexion internet", type: "negative" });
        } else if (error.response.status === 422) {
          $q.notify({ position: "top", message: "Vérifiez le formulaire", type: "warning" });
        } else if (error.response.status === 409) {
          $q.notify({ position: "top", message: "Email Déjà utilisé !", type: "warning" });
        } else {
          $q.notify({ position: "top", message: "Erreur inconnue !", type: "negative" });
          console.error(error);
        }
      }
    };

    const email = ref(null);
    const password = ref(null);
    const disabledLogin = computed(() => !email.value || !isValidEmail(email.value) || !password.value);
    const isLogin = ref(false);

    const logIn = async () => {
      isLogin.value = true;
      try {
        await api.$post("/v1/user/login", { email: email.value, password: password.value });
        const me = await api.$get("/v1/user/me");
        store.commit("auth/setMe", me);
        await router.push("/");
      } catch (error) {
        if (!error.response) {
          $q.notify({ position: "top", message: "Impossible de se connecter. Vérifiez votre connexion internet", type: "negative" });
          throw error;
        } else if (error.response.status == 401) {
          $q.notify({ position: "top", message: "Impossible de se connecter. Vérifiez vos indentifiants", type: "warning" });
        } else if (error.response.status === 403) {
          $q.notify({ position: "top", message: "Compte banni", type: "negative" });
        } else {
          $q.notify({ position: "top", message: "Erreur inconnue", type: "nagative" });
          console.error(error);
        }
      } finally {
        isLogin.value = false;
      }
    };

    return {
      tab,
      refRegisterForm,
      registerForm,
      resetRegisterForm,
      disabledRegister,
      isValidEmail,
      isValidPhoneNumber,
      showPassword,
      signIn,
      isLogin,
      logIn,
      email,
      password,
      disabledLogin,
    };
  },
});
</script>
