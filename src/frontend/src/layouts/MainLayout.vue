<template>
  <q-dialog v-model="loginDialog" class="tw-rounded-sm">
    <q-card class="sm:tw-w-2/3">
      <q-card-section class="tw-bg-primary tw-text-center tw-font-bold tw-text-2xl tw-text-white"> Connexion </q-card-section>
      <q-card-section>
        <q-form class="tw-flex tw-flex-col">
          <q-input outlined v-model="email" @keyup.enter="!disabledLogin && login()" label="Adresse email" type="email" />
          <q-input outlined class="tw-mt-2" v-model="password" @keyup.enter="!disabledLogin && login()" label="Mot de passe" :type="showPassword ? 'text' : 'password'">
            <template v-slot:append>
              <q-icon :name="showPassword ? 'visibility' : 'visibility_off'" class="cursor-pointer" @click="showPassword = !showPassword" />
            </template>
          </q-input>
          <q-btn class="tw-mt-2 tw-bg-blue-400" @click="login" :disable="disabledLogin">Connexion</q-btn>
        </q-form>
        <div class="tw-flex tw-flex-col">
          <button class="tw-mt-2 tw-text-blue-400 tw-text-center" @click="registerDialog = true">
            Inscription
            <q-dialog v-model="registerDialog" class="tw-rounded-sm">
              <q-card class="sm:tw-w-1/2">
                <q-card-section class="tw-bg-primary tw-text-center tw-font-bold tw-text-2xl tw-text-white"> Inscription </q-card-section>
                <q-card-section>
                  <q-form ref="refRegisterForm" class="tw-flex tw-flex-col">
                    <q-input outlined v-model="registerForm.firstname" label="Prénom" :rules="[(val) => !!val || 'Prénom manquant']" />
                    <q-input outlined class="tw-mt-2" v-model="registerForm.lastname" label="Nom" :rules="[(val) => !!val || 'Nom manquant']" />
                    <q-input
                      outlined
                      class="tw-mt-2"
                      v-model="registerForm.phoneNumber"
                      label="Numéro de téléphone"
                      type="tel"
                      :rules="[(val) => !!val || 'Téléphone manquant', (val) => isValidPhoneNumber(val) || 'Téléphone invalide']"
                    />
                    <q-input
                      outlined
                      class="tw-mt-2"
                      v-model="registerForm.email"
                      :rules="[(val) => !!val || 'Email manquant', (val) => isValidEmail(val) || 'Email invalide']"
                      label="Adresse email"
                      type="email"
                    />
                    <q-input
                      outlined
                      class="tw-mt-2"
                      v-model="registerForm.password"
                      :rules="[(val) => val.length >= 8 || 'Mot de passe trop court']"
                      label="Mot de passe"
                      :type="showPassword ? 'text' : 'password'"
                    >
                      <template v-slot:append>
                        <q-icon :name="showPassword ? 'visibility' : 'visibility_off'" class="cursor-pointer" @click="showPassword = !showPassword" />
                      </template>
                    </q-input>
                    <q-input outlined class="tw-mt-2" v-model="registerForm.birthday" :rules="[(val) => !!val || 'Date invalide']" label="Date de naissance" type="date" />
                    <q-btn-group spread class="tw-mt-2">
                      <q-btn class="tw-bg-yellow-400" @click="resetRegisterForm">Réinitialiser</q-btn>
                      <q-btn class="tw-bg-blue-400" @click="register" :disable="disabledRegister">Inscription</q-btn>
                    </q-btn-group>
                  </q-form>
                </q-card-section>
              </q-card>
            </q-dialog>
          </button>
          <button class="tw-mt-2 tw-text-blue-400 tw-text-center" @click="openForgotPasswordDialog">Mot de passe oublié ?</button>
        </div>
      </q-card-section>
    </q-card>
  </q-dialog>

  <q-dialog v-model="profileDialog" class="tw-rounded-sm">
    <q-card class="sm:tw-w-2/3">
      <q-card-section class="tw-bg-primary tw-text-center tw-font-bold tw-text-2xl tw-text-white"> Mon profil </q-card-section>
      <q-card-section class="tw-flex sm:tw-flex-row tw-flex-col">
        <div class="tw-flex tw-flex-col tw-items-center">
          <q-file v-model="profileAvatarFile" class="tw-hidden" ref="profileAvatarUploadRef" accept="image/png, image/jpeg" />
          <q-avatar class="tw-h-16 tw-w-16 tw-cursor-pointer tw-rounded" :class="{ 'tw-bg-gray-400': !me.has_avatar }" @click="openProfileAvatarUpload" square>
            <img v-if="profileAvatarData" :src="profileAvatarData" alt="photo de profil" />
            <img v-else-if="me.has_avatar" :src="`${apiBaseURL}/v1/user/me/avatar`" alt="photo de profil" />
            <template v-else>{{ me.firstname[0] }}{{ me.lastname[0] }}</template>
          </q-avatar>
          <q-btn class="tw-mt-4" :disable="!profileAvatarData" :loading="uploadNewAvatarLoading" @click="uploadNewAvatar">Sauvegarder</q-btn>
        </div>
        <q-separator vertical class="tw-mx-4 tw-hidden sm:tw-block" />
        <q-separator class="tw-my-4 sm:tw-hidden tw-block" />
        <div class="tw-w-full">
          <div>
            {{ me.firstname }} {{ me.lastname }} <q-chip v-if="me.type !== 'user'" square class="tw-bg-blue-400 tw-text-white"> {{ me.type }} </q-chip>
          </div>
          <div>Rejoint le : {{ new Date(me.created_at).toLocaleDateString() }}</div>

          <div class="tw-break-all">email: {{ me.email }}</div>
          <q-btn class="tw-mt-4" @click="resetPassword(me.email)">Changer de mot de passe</q-btn>
        </div>
      </q-card-section>
    </q-card>
  </q-dialog>

  <q-dialog v-model="searchDialog" class="tw-rounded-sm">
    <q-card class="sm:tw-w-2/3">
      <q-card-section class="tw-bg-primary tw-text-center tw-font-bold tw-text-2xl tw-text-white"> Rechercher </q-card-section>
      <q-card-section class="tw-flex tw-flex-col">
        <q-input v-model="search.query" :debounce="1000" label="Rechercher" />
        <div v-if="search.searching" class="tw-flex tw-justify-center">
          <q-spinner-cube class="tw-text-8xl tw-text-blue-600" />
        </div>
        <q-scroll-area v-else-if="search.result.users.length + search.result.posts.length" class="tw-h-64">
          <q-card v-for="user in search.result.users" :key="user.me" class="tw-flex tw-bg-gray-100 tw-m-4">
            <q-card-section>
              <q-avatar class="tw-rounded tw-h-24 tw-w-24" :class="{ 'tw-bg-gray-400': !user.has_avatar }" square>
                <img v-if="user.has_avatar" :src="`${apiBaseURL}/v1/user/${user.id}/avatar`" alt="avatar" />
                <template v-else>{{ user.firstname[0] }}{{ user.lastname[0] }}</template>
              </q-avatar>
            </q-card-section>
            <q-card-section>
              <div>
                {{ user.firstname }} {{ user.lastname }} <q-chip v-if="user.type !== 'user'" square class="tw-bg-blue-400 tw-text-white"> {{ user.type }} </q-chip>
              </div>
              <div>Rejoint le : {{ new Date(user.created_at).toLocaleDateString() }}</div>
            </q-card-section>
          </q-card>
          <q-separator />
        </q-scroll-area>
        <div v-else-if="search.query.length">Aucun résultat</div>
      </q-card-section>
    </q-card>
  </q-dialog>

  <q-layout view="lHh Lpr lFf">
    <q-header elevated reveal>
      <q-toolbar>
        <div class="tw-flex tw-justify-center tw-w-full sm:tw-w-auto tw-h-full sm:tw-justify-start tw-py-2">
          <img src="~assets/logo-re.png" alt="logo" class="tw-h-12 tw-w-12" />
        </div>
        <div class="tw-hidden sm:tw-block tw-ml-4">
          <q-btn-group class="tw-rounded-lg">
            <template v-for="(item, n) in menu" :key="n">
              <q-separator v-if="n > 0" vertical />
              <q-btn class="tw-bg-blue-400 tw-px-4 tw-py-2" :icon="item.icon" :to="item.to" :aria-label="item.label" :disable="route.path === item.to">{{ item.label }}</q-btn>
            </template>
            <q-separator vertical />
            <q-btn class="tw-bg-blue-400 tw-px-4 tw-py-2" @click="searchDialog = true" icon="search" aria-label="Recherche">Recherche</q-btn>
          </q-btn-group>
        </div>

        <q-btn v-if="me" flat round dense aria-label="profile" class="tw-absolute tw-right-4">
          <q-avatar class="tw-rounded" :class="{ 'tw-bg-gray-400': !me.has_avatar }" square>
            <img v-if="me.has_avatar" :src="`${apiBaseURL}/v1/user/me/avatar?${+new Date(me.updated_at)}`" alt="avatar" />
            <template v-else>{{ me.firstname[0] }}{{ me.lastname[0] }}</template>
          </q-avatar>
          <q-menu>
            <q-list>
              <q-item clickable v-close-popup @click="profileDialog = true">
                <q-item-section>
                  <q-item-label>Profil</q-item-label>
                </q-item-section>
              </q-item>

              <q-item clickable v-close-popup>
                <q-item-section>
                  <q-item-label>TODO</q-item-label>
                </q-item-section>
              </q-item>
              <q-separator />
              <q-item clickable v-close-popup>
                <q-item-section>
                  <q-item-label @click="logout">Déconnexion</q-item-label>
                </q-item-section>
              </q-item>
            </q-list>
          </q-menu>
        </q-btn>
        <q-btn v-else @click="loginDialog = true" flat dense icon="login" aria-label="Menu" class="tw-absolute tw-right-4">
          <span class="tw-hidden sm:tw-block">Connexion</span>
        </q-btn>
      </q-toolbar>
    </q-header>

    <q-page-container>
      <router-view />
    </q-page-container>

    <q-footer elevated class="sm:tw-hidden">
      <q-btn-group spread>
        <template v-for="(item, n) in menu" :key="n">
          <q-separator v-if="n" vertical />
          <q-btn :icon="item.icon" :to="item.to" :aria-label="item.label" :disable="route.path === item.to" :class="{ 'tw-text-blue-800': route.path === item.to }" />
        </template>
        <q-separator vertical />
        <q-btn @click="searchDialog = true" icon="search" aria-label="Recherche" />
      </q-btn-group>
    </q-footer>
  </q-layout>
</template>

<script>
import { defineComponent, ref, computed, reactive, watch } from "vue";
import { useRouter, useRoute } from "vue-router";
import { useStore } from "vuex";
import { useQuasar, date } from "quasar";

import { apiBaseURL, api } from "boot/axios";

export default defineComponent({
  name: "MainLayout",
  async setup() {
    const isValidEmail = (val) => {
      const re = /^(?=[a-zA-Z0-9@._%+-]{6,254}$)[a-zA-Z0-9._%+-]{1,64}@(?:[a-zA-Z0-9-]{1,63}\.){1,8}[a-zA-Z]{2,63}$/;
      return re.test(val);
    };

    const isValidPhoneNumber = (val) => {
      const re = /^(?:(?:\+|00)33[\s.-]{0,3}(?:\(0\)[\s.-]{0,3})?|0)[1-9](?:(?:[\s.-]?\d{2}){4}|\d{2}(?:[\s.-]?\d{3}){2})$/;
      return re.test(val);
    };

    const store = useStore();
    const $q = useQuasar();
    const router = useRouter();
    const route = useRoute();

    const loginDialog = ref(false);
    const email = ref("");
    const password = ref("");
    const showPassword = ref(false);
    const disabledLogin = computed(() => !email.value || !isValidEmail(email.value) || !password.value);

    const login = async () => {
      try {

        await api.$post("/v1/user/login", { email: email.value, password: password.value });
        const me = await api.$get("/v1/user/me");
        store.commit("auth/setMe", me);
        loginDialog.value = false;
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
      }
    };

    const refRegisterForm = ref();
    const registerDialog = ref(false);
    const registerForm = reactive({
      firstname: "",
      lastname: "",
      email: "",
      password: "",
      phoneNumber: "",
      birthday: null,
    });
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

    const register = async () => {
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
        resetRegisterForm();
        registerDialog.value = false;
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

    const logout = async () => {
      await api.$post("/v1/user/logout");
      router.go();
    };

    const me = computed(() => store.getters["auth/me"]);

    const menu = computed(() => {
      const menu = [
        { label: "Accueil", icon: "home", to: "/" },
        { label: "todo", icon: "home", to: "/" },
      ];
      if (["moderator", "admin"].includes(me.value?.type)) {
        menu.push({ label: "Utilisateurs", icon: "fas fa-user", to: "/users" });
      }
      return menu;
    });
    const profileDialog = ref(false);
    const profileAvatarFile = ref(null);
    const profileAvatarData = ref(null);
    watch(profileAvatarFile, () => {
      if (profileAvatarFile.value === null) {
        return;
      }
      const reader = new FileReader();
      reader.onload = (e) => {
        profileAvatarData.value = e.target.result;
      };
      reader.readAsDataURL(profileAvatarFile.value);
    });
    const profileAvatarUploadRef = ref(null);
    const openProfileAvatarUpload = () => {
      profileAvatarUploadRef.value.pickFiles();
    };
    const uploadNewAvatarLoading = ref(false);
    const uploadNewAvatar = async () => {
      uploadNewAvatarLoading.value = true;
      const formdata = new FormData();
      formdata.append("avatar", profileAvatarFile.value);
      try {
        await api.$post("/v1/user/me/avatar", formdata, { headers: { "Content-Type": "multipart/form-data" } });
        $q.notify({ position: "top", message: "Photo de profil changé", type: "positive" });
        const me = await api.$get("/v1/user/me");
        store.commit("auth/setMe", me);
        profileAvatarFile.value = null;
      } catch (error) {
        if (error.response?.status === 400) {
          $q.notify({ position: "top", message: "Photo non pris en charge (mauvaise extension)", type: "negative" });
        } else if (error.response?.status === 413) {
          $q.notify({ position: "top", message: "Photo non pris en charge (trop volumineuse)", type: "negative" });
        }
        console.error(error);
      } finally {
        uploadNewAvatarLoading.value = false;
      }
    };

    const resetPassword = async (email) => {
      try {
        await api.$post("/v1/reset_password/send_mail", { email });
        $q.notify({
          position: "top",
          message: "Un email vient de vous être envoyé",
          type: "positive",
        });
      } catch (error) {
        throw error;
      }
    };

    function openForgotPasswordDialog() {
      $q.dialog({
        message: "Quel est votre mail ?",
        prompt: { model: "", isValid: isValidEmail },
        cancel: true,
        persistent: true,
      }).onOk(async (email) => {
        await resetPassword(email);
      });
    }

    const searchDialog = ref(false);
    const search = reactive({
      searching: false,
      query: "",
      result: {
        users: [],
        posts: [],
      },
    });

    watch(
      () => search.query,
      async (query_search) => {
        if (query_search.length === 0) {
          search.result.users = [];
        } else {
          search.searching = true;
          try {
            const { users } = await api.$get("/v1/user/search", { params: { query_search } });
            search.result.users = users;
          } catch (error) {
            search.result.users = [];
            console.error(error);
          } finally {
            search.searching = false;
          }
        }
      },
      { deep: true }
    );

    return {
      route,
      isValidEmail,
      isValidPhoneNumber,
      apiBaseURL,
      loginDialog,
      email,
      password,
      showPassword,
      disabledLogin,
      refRegisterForm,
      resetRegisterForm,
      registerDialog,
      registerForm,
      disabledRegister,
      register,
      login,
      logout,
      menu,
      me,
      profileDialog,
      profileAvatarFile,
      profileAvatarData,
      profileAvatarUploadRef,
      openProfileAvatarUpload,
      uploadNewAvatar,
      uploadNewAvatarLoading,
      resetPassword,
      openForgotPasswordDialog,
      searchDialog,
      search,
    };
  },
});
</script>
