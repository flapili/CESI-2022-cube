<template>
  <!-- <q-page>
    <div class="tw-flex tw-justify-center">
      <q-form ref="refForm" class="tw-flex tw-flex-col md:tw-w-1/3 tw-py-16 tw-gap-2">
        <q-input filled square bg-color="white" v-model="form.title" label="Titre" :rules="[(val) => !!val || 'Titre manquant']" />
        <q-select
          filled
          square
          bg-color="white"
          v-model="form.type"
          :options="[
            'communication',
            'culture',
            'personal_development',
            'emotional_intelligence',
            'hobbie',
            'professional_world',
            'parenting',
            'quality_of_life',
            'search_of_meaning',
            'physical_health',
            'spirituality',
            'emotional_life',
          ]"
          label="Catégorie"
        />
        <q-btn class="tw-bg-primary tw-text-white tw-rounded-none tw-shadow-sm tw-shadow-black" @click="publish" :disable="disabledPublish">Publier</q-btn>
      </q-form>
    </div>
  </q-page> -->
  <q-page>
    <div>À venir</div>
  </q-page>
</template>

<script>
import { defineComponent, ref, computed, reactive } from "vue";
export default defineComponent({
  async setup() {
    const refForm = ref(null);
    const form = reactive({
      title: "",
      type: "communication",
    });

    const disabledPublish = computed(() => !form.title);
    const publish = async () => {};
    return {
      refForm,
      form,
      publish,
      disabledPublish,
    };
  },
});
</script>
