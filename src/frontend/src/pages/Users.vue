<template>
  <q-table class="sm:tw-m-16 tw-m-2" v-model:pagination="pagination" :rows-per-page-options="[]" :loading="loading" :rows="users" :columns="columns" @request="onRequest">
    <template v-slot:body="props">
      <q-tr :props="props" :class="{ 'tw-bg-red-50': props.row.disabled_at, 'tw-bg-green-50': props.row.id == me.id }">
        <q-td key="avatar" :props="props">
          <q-avatar class="tw-rounded" :class="{ 'tw-bg-gray-400': !props.row.has_avatar }" square>
            <img v-if="props.row.has_avatar" :src="`${apiBaseURL}/v1/user/${props.row.id}/avatar?${+new Date(props.row.updated_at)}`" alt="avatar" />
            <template v-else>{{ props.row.firstname[0] }}{{ props.row.lastname[0] }}</template>
          </q-avatar>
        </q-td>
        <q-td key="firstname" :props="props">{{ props.row.firstname }} </q-td>
        <q-td key="lastname" :props="props">{{ props.row.lastname }} </q-td>
        <q-td key="email" :props="props">
          <a :href="`mailto:${props.row.email}`">{{ props.row.email }}</a>
        </q-td>
        <q-td key="phoneNumber" :props="props">
          <a :href="`tel:${props.row.phone_number}`">{{ props.row.phone_number }}</a>
        </q-td>
        <q-td key="age" :props="props">
          {{ props.row.age }} an{{ props.row.age > 1 ? "s" : "" }}
          <q-tooltip class="tw-text-sm">Né le {{ new Date(props.row.birthday).toLocaleString() }} </q-tooltip>
        </q-td>

        <q-td key="createdAt" :props="props">
          {{ new Date(props.row.created_at).toLocaleDateString() }}
          <q-tooltip class="tw-text-sm"> {{ new Date(props.row.created_at).toLocaleString() }} </q-tooltip>
        </q-td>
        <q-td key="type" :props="props">
          <template v-if="props.row.type === 'user'"><q-chip class="tw-bg-gray-300" square>Utilisateur</q-chip></template>
          <template v-else-if="props.row.type === 'moderator'"><q-chip class="tw-bg-blue-200" square>Moderateur</q-chip></template>
          <template v-else-if="props.row.type === 'admin'"><q-chip class="tw-bg-green-200" square>Admin</q-chip></template>
        </q-td>
        <q-td key="action">
          <div v-if="props.row.id != me.id">
            <q-btn v-if="props.row.disabled_at === null" @click="banUser(props.row)" class="tw-bg-red-400">Désactiver</q-btn>
            <q-btn v-else @click="unbanUser(props.row)" class="tw-bg-green-400">Réactiver</q-btn>
          </div>
        </q-td>
      </q-tr>
    </template>
  </q-table>
</template>

<script>
import { defineComponent, ref, computed } from "vue";
import { useStore } from "vuex";
import { useRouter } from "vue-router";
import { useQuasar, date } from "quasar";
import { api, apiBaseURL } from "boot/axios";

export default defineComponent({
  name: "Users",
  async setup() {
    const router = useRouter();
    const store = useStore();
    const me = computed(() => store.getters["auth/me"]);

    const $q = useQuasar();

    const loading = ref(true);
    const users = ref([]);
    const pagination = ref({
      page: 1,
      rowsPerPage: 2,
      rowsNumber: 0,
    });

    const columns = [
      { name: "avatar", align: "left" },
      { name: "firstname", label: "Prénom", align: "left" },
      { name: "lastname", label: "Nom", align: "left" },
      { name: "email", label: "email", align: "left" },
      { name: "phoneNumber", label: "Téléphone", align: "left" },
      { name: "age", label: "Âge", align: "left" },
      { name: "createdAt", label: "Créé le", align: "left" },
      { name: "type", label: "Type", align: "left" },
      { name: "action", label: "Action", align: "left" },
    ];

    const fetchUsers = async (page = 1) => {
      loading.value = true;
      try {
        const data = await api.$get("/v1/user", { params: { page } });
        const now = new Date();
        users.value = data.users.map((user) => {
          user.age = date.getDateDiff(now, new Date(user.birthday), "years");
          return user;
        });
        pagination.value.page = data.meta.page;
        pagination.value.rowsPerPage = data.meta.per_page;
        pagination.value.rowsNumber = data.meta.total;
      } catch (error) {
        if ([401, 403].includes(error.response?.status)) {
          await router.push("/");
        } else {
          console.error(error);
        }
      } finally {
        loading.value = false;
      }
    };

    const onRequest = (props) => {
      fetchUsers(props.pagination.page);
    };

    const banUser = (user) => {
      $q.dialog({
        message: `Êtes-vous sûr de vouloir désactiver ${user.firstname} ${user.lastname} ?`,
        cancel: true,
      }).onOk(async () => {
        try {
          await api.$post(`/v1/user/${user.id}/ban`);
          $q.notify({ position: "top", message: "Utilisateur désactivé", type: "positive" });
          await fetchUsers(pagination.value.page)
        } catch (error) {
          $q.notify({ position: "top", message: "Erreur", type: "negative" });
        }
      });
    };

    const unbanUser = (user) => {
      $q.dialog({
        message: `Êtes-vous sûr de vouloir réactiver ${user.firstname} ${user.lastname} ?`,
        cancel: true,
      }).onOk(async () => {
        try {
          await api.$post(`/v1/user/${user.id}/unban`);
          $q.notify({ position: "top", message: "Utilisateur réactivé", type: "positive" });
          await fetchUsers(pagination.value.page)
        } catch (error) {
          $q.notify({ position: "top", message: "Erreur", type: "negative" });
        }
      });
    };

    await fetchUsers();

    return {
      me,
      apiBaseURL,
      loading,
      users,
      pagination,
      columns,
      onRequest,
      banUser,
      unbanUser,
    };
  },
});
</script>
