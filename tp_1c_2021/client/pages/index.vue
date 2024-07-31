<template>
  <div class="container container-mobile">
    <div>
      <SubjectLogo/>
      <h1 class="title">
        TP3 K3051
      </h1>
      <div class="subtitle">Detección de emociones y recuperación de la información</div>
      <p v-if="status === 'UP'">🟢 {{ status }} - {{ message }}</p>
      <p v-else-if="status">🟡 Error de servicio - {{ message }}</p>
      <p v-else>🔴 Servicio no disponible</p>
      <div class="links">
        <a
          href="https://github.com/alanzhag/nlp-utn-frba/tree/main/tp_1c_2021"
          target="_blank"
          rel="noopener noreferrer"
          class="button--green"
        >
          Documentacion
        </a>
        <a
          href="/api"
          rel="noopener noreferrer"
          class="button--grey"
        >
          API
        </a>
      </div>
    </div>
  </div>
</template>

<script lang="js">  //TODO: Migrate to TS.
//export default Vue.extend({})

export default {
  auth: false,

  async asyncData({$axios}) {
    try {
      const response = await $axios.$get('/status')
      return {message: response.message, status: response.status}
    } catch (error) {
      if (!error.response) {
        return null
      }
      return {message: error.message, status: error.response.code}
    }
  }
}
</script>

<style>
.container {
  margin: 0 auto;
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  text-align: center;
}

.title {
  font-family:
    'Quicksand',
    'Source Sans Pro',
    -apple-system,
    BlinkMacSystemFont,
    'Segoe UI',
    Roboto,
    'Helvetica Neue',
    Arial,
    sans-serif;
  display: block;
  font-weight: 300;
  font-size: 100px;
  color: #35495e;
  letter-spacing: 1px;
}

.subtitle {
  font-weight: 300;
  font-size: 42px;
  color: #526488;
  word-spacing: 5px;
  padding-bottom: 15px;
}

.links {
  padding-top: 15px;
}

.logo {
  display: flex;
  align-items: center
}

.subject {
  color: green;
}


</style>
