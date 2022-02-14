<template>
  <q-layout view="lHh Lpr lFf">
    <q-header>
      <q-toolbar elevated>
        <div class="tw-hidden sm:tw-flex">
          <div class="tw-flex tw-justify-center tw-w-full sm:tw-w-auto tw-h-full sm:tw-justify-start tw-py-2">
            <img src="~assets/logo.png" alt="logo" class="tw-h-20 tw-my-1" />
          </div>
          <q-tabs class="tw-w-full" active-class="tw-bg-secondary tw-text-black">
            <q-route-tab v-for="(item, index) in menu" :key="index" :icon="item.icon" :to="item.to" :aria-label="item.label" :label="item.label" :disable="$route.path === item.to" />
          </q-tabs>
        </div>
        <div class="sm:tw-hidden tw-flex tw-justify-center tw-w-full">
          <img src="~assets/logo.png" alt="logo" class="tw-h-12 tw-my-2" />
        </div>
        <q-btn flat class="tw-absolute tw-right-3 tw-p-1">
          <q-avatar v-if="me" class="tw-rounded tw-h-12 tw-w-12" :class="{ 'tw-bg-gray-300': !me.has_avatar }" square>
            <img v-if="me.has_avatar" :src="`${apiBaseURL}/v1/user/me/avatar`" alt="avatar" />
            <template v-else>{{ me.firstname[0].toUpperCase() }}{{ me.lastname[0].toUpperCase() }}</template>
          </q-avatar>

          <q-avatar v-else class="tw-rounded tw-h-12 tw-w-12 tw-bg-gray-300" square>
            <q-icon name="fas fa-user-alt" />
          </q-avatar>

          <q-menu :offset="[-20, 0]" class="tw-shadow-sm tw-shadow-black tw-rounded-none">
            <q-list>
              <q-separator />
              <q-item v-if="me" clickable v-close-popup class="hover:tw-bg-gray-100">
                <q-item-section>
                  <q-item-label>
                    <q-icon name="fas fa-user" class="tw-mr-2 tw-text-2xl" />
                    <span>Mon profil</span>
                  </q-item-label>
                </q-item-section>
              </q-item>
              <q-separator />
              <q-item clickable v-close-popup class="hover:tw-bg-gray-100">
                <q-item-section>
                  <q-item-label>
                    <q-icon name="help" class="tw-inline tw-mr-2 tw-text-2xl" />
                    Aide
                  </q-item-label>
                </q-item-section>
              </q-item>
              <q-separator />
              <q-item v-if="me" clickable v-close-popup @click="logOut" class="hover:tw-bg-gray-100">
                <q-item-section>
                  <q-item-label class="tw-flex tw-justify-center tw-items-center">
                    <q-icon name="logout" class="tw-inline tw-mr-2 tw-text-2xl" />
                    Déconnexion
                  </q-item-label>
                </q-item-section>
              </q-item>
              <q-item v-else clickable v-close-popup @click="router.push('/login')">
                <q-item-section>
                  <q-item-label class="tw-flex tw-justify-center tw-items-center">
                    <q-icon name="login" class="tw-inline tw-mr-2 tw-text-2xl" />
                    Connexion
                  </q-item-label>
                </q-item-section>
              </q-item>
            </q-list>
          </q-menu>
        </q-btn>
      </q-toolbar>
    </q-header>
    <q-page-container class="tw-bg-secondary">
      <router-view />
    </q-page-container>
    <q-footer elevated class="sm:tw-hidden tw-flex">
      <q-tabs class="tw-w-full">
        <q-route-tab v-for="(item, index) in menu" :key="index" :icon="item.icon" :to="item.to" :aria-label="item.label" :disable="$route.path === item.to" />
      </q-tabs>
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

    const me = computed(() => store.getters["auth/me"]);

    const loginDialog = ref(false);
    const email = ref("");
    const password = ref("");
    const showPassword = ref(false);
    const disabledLogin = computed(() => !email.value || !isValidEmail(email.value) || !password.value);
    const login = async () => {
      isLogin.value = true;
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
      } finally {
        isLogin.value = false;
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

    const logOut = async () => {
      await api.$post("/v1/user/logout");
      router.go();
    };

    const menu = computed(() => {
      const menu = [
        { label: "Accueil", icon: "home", to: "/" },
        { label: "Recherche", icon: "search", to: "/search" },
        { label: "Publier", icon: "add_circle", to: "/publish" },
        { label: "Tendances", icon: "trending_up", to: "/trends" },
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
      router,
      route,
      me,
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
      logOut,
      menu,
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
