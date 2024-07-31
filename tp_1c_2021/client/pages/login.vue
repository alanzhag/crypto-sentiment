<template>
  <section class="section">
    <b-alert v-if="$auth.$state.redirect" show>
      Tenes que iniciar sesión antes de acceder a
      <strong>{{ $auth.$state.redirect }}</strong>
    </b-alert>
  </section>
</template>
