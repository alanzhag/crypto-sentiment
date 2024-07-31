export default {

  // Disable server-side rendering: https://go.nuxtjs.dev/ssr-mode
  ssr: false,

  // Global page headers: https://go.nuxtjs.dev/config-head
  head: {
    title: 'TP3 PLN K351',
    htmlAttrs: {
      lang: 'en'
    },
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      { hid: 'description', name: 'description', content: '' }
    ],
    link: [
      { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' }
    ]
  },

  // Global CSS: https://go.nuxtjs.dev/config-css
  css: [
  ],

  // Plugins to run before rendering page: https://go.nuxtjs.dev/config-plugins
  plugins: [
    '~/plugins/axios'
  ],

  // Auto import components: https://go.nuxtjs.dev/config-components
  components: true,

  // Modules for dev and build (recommended): https://go.nuxtjs.dev/config-modules
  buildModules: [
    // https://go.nuxtjs.dev/typescript
    '@nuxt/typescript-build',
  ],

  // Modules: https://go.nuxtjs.dev/config-modules
  modules: [
    // https://go.nuxtjs.dev/bootstrap
    'bootstrap-vue/nuxt',
    '@nuxtjs/axios',
    '@nuxtjs/auth-next',
    'nuxt-izitoast',
    'moment',
    'moment-timezone'
  ],

  izitoast: {
    position: 'center',
    transitionIn: 'bounceInLeft',
    transitionOut: 'fadeOutRight',
    transitionInMobile: 'fadeInUp',
    transitionOutMobile: 'fadeOutDown',
  },

  // Axios config
  axios: {
    proxy: true,
    prefix: (process.env.BACKEND_URL || 'https://127.0.0.1:5000') + '/api'
  },

  // Proxy config
  proxy: {
    '/api': {
      target: process.env.NUXT_PROXY_HOST || 'http://localhost:5000',
      secure: !!process.env.SECURE
    },
    '/swaggerui': {
      target: process.env.NUXT_PROXY_HOST || 'http://localhost:5000',
      secure: !!process.env.SECURE
    },
    '/auth': {
      target: process.env.NUXT_PROXY_HOST || 'http://localhost:5000',
      secure: !!process.env.SECURE
    },
  },

  // Auth
  auth: {
    strategies: {
      google: {
        clientId: process.env.GOOGLE_CLIENT_ID,
        codeChallengeMethod: '',
        responseType: 'code',
        endpoints: {
          token: process.env.BACKEND_URL + '/api/auth/token'
        }
      },
    }
  },

  // Router
  router: {
    middleware: ["auth"],
  },

  // Build Configuration: https://go.nuxtjs.dev/config-build
  build: {},

  // BootstrapVue config
  bootstrapVue: {
    icons: true
  }
}
