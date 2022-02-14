<template>
  <q-page>
    <div class="tw-grid tw-grid-cols-1 md:tw-grid-cols-2 lg:tw-grid-cols-3 xl:tw-grid-cols-4 tw-gap-8 md:tw-p-20 tw-p-4">
      <div v-for="entrie in posts" :key="entrie.post.id" class="tw-border tw-shadow-md tw-bg-white tw-p-4">
        <div class="tw-flex tw-text-primary">
          <q-avatar class="tw-rounded tw-h-12 tw-w-12" :class="{ 'tw-bg-gray-300': !entrie.author.has_avatar }" square>
            <img v-if="entrie.author.has_avatar" :src="`${apiBaseURL}/v1/user/${entrie.author.id}/avatar`" alt="avatar" />
            <template v-else>{{ entrie.author.firstname[0].toUpperCase() }}{{ entrie.author.lastname[0].toUpperCase() }}</template>
          </q-avatar>
          <div class="tw-grow tw-text-center">
            <div class="tw-font-bold">{{ entrie.post.title }}</div>
            <div>{{types[entrie.post.type]}}</div>
          </div>
          <div class="tw-w-12" />
        </div>
        {{ entrie.post }}
      </div>
    </div>
  </q-page>
</template>

<script>
import { defineComponent, ref } from "vue";

import { api, apiBaseURL } from "boot/axios";

const types = {
  communication: "Communication",
  culture: "Culture",
  personal_development: "Développement personnel",
  emotional_intelligence: "Intelligence émotionelle",
  professional_world: "Monde professionnel",
  parenting: "Parentalité",
  quality_of_life: "Qualité de vie",
  search_of_meaning: "Recherche de sens",
  physical_health: "Santé physique",
  spirituality: "Spiritualité",
  emotional_life: "Vie affective",
};

export default defineComponent({
  name: "PageIndex",
  async setup() {
    const posts = ref([]);
    posts.value = await api.$get("/v1/post").then((d) => d.data);
    return {
      apiBaseURL,
      posts,
      types,
    };
  },
});
</script>
