<template>
  <b-navbar fixed="top" toggleable="lg" type="light" variant="light">
    <b-navbar-brand class="d-none d-md-block" href="/">
      <img alt="UtnLogo" class="d-inline-block align-center utn-logo" height="40px"
           src="../static/logo-only-utn-frba.png" width="40px"/>
      Procesamiento del Lenguaje Natural
    </b-navbar-brand>

    <b-navbar-brand class="d-md-none" href="/">
      <img alt="UtnLogo" class="d-inline-block align-center utn-logo" height="40px"
           src="../static/logo-only-utn-frba.png" width="40px"/>
      P.L.N
    </b-navbar-brand>
    <template>
      <b-navbar-toggle target="nav-collapse">
        <template #default="{ expanded }">
          <b-icon v-if="expanded" icon="chevron-bar-up"></b-icon>
          <b-icon v-else icon="chevron-bar-down"></b-icon>
        </template>
      </b-navbar-toggle>
      <b-collapse id="nav-collapse" is-nav>
        <b-navbar-nav>
          <b-nav-item href="/informationRetrieval">Recuperación de la información</b-nav-item>
          <b-nav-item href="/sentimentPriceComparison">Comparación sentimiento-precio</b-nav-item>
          <b-nav-item href="/api">Api Doc</b-nav-item>
        </b-navbar-nav>
        <b-navbar-nav class="ml-auto">
          <template v-if="$auth.loggedIn">
            <b-nav-item-dropdown right>
              <template #button-content>
                <b-avatar :src="$auth.user.picture" variant="primary"></b-avatar>
              </template>
              <b-dropdown-item href="/profile">Mi perfil</b-dropdown-item>
              <b-dropdown-item v-on:click="$auth.logout()">Cerrar sesión</b-dropdown-item>
            </b-nav-item-dropdown>
          </template>
          <template v-else>
            <b-button v-on:click="loginUser">
              <b-icon icon="google"></b-icon>
              Iniciar sesión
            </b-button>
          </template>
        </b-navbar-nav>
      </b-collapse>
    </template>
  </b-navbar>
</template>

<script>
export default {
  methods: {
    async loginUser() {
      await this.$auth.loginWith('google')
    }
  }
}
</script>

<style scoped>
.utn-logo {
  margin-bottom: 6px;
}
</style>
