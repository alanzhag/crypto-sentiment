<template>
  <div id="texts_deck">
    <template v-for="text in response">
      <text-card :text="text"/>
    </template>
  </div>
</template>

<script>
export default {
  name: "informationRetrieval",
  auth: false,
  async asyncData({$axios}) {
    const response = await $axios.$get('/texts/latests/all-sources?limit=20')
    return {response: response}
  }
}
</script>

<style scoped>
</style>
