<template>
  <div id="sentiment-price-deck">
    <b-container class="bv-example-row">
      <div class="d-none d-lg-block">
        <b-row class="text-center">
          <b-col cols="5">
            <strong>60 minutos previos</strong>
            <div class="id-text">id: {{ response[1].id }}</div>
            <div class="id-text">{{ response[1].timestamp | moment }}</div>
          </b-col>
          <b-col cols="2">
            <strong>Variación</strong>
          </b-col>
          <b-col cols="5">
            <strong>60 minutos posteriores</strong>
            <div class="id-text">id: {{ response[0].id }}</div>
            <div class="id-text">{{ response[0].timestamp | moment }}</div>
          </b-col>
        </b-row>
      </div>
      <template v-for="view in paired_view(response)">
        <b-row class="text-center">
          <b-col lg="5">
            <sentiment-price-card :sentiment_price="view[0]"/>
          </b-col>
          <b-col class="justify-content-center align-self-center" lg="2">
            <b-icon :icon="view[1]" style="width: 120px; height: 120px;"></b-icon>
          </b-col>
          <b-col lg="5">
            <sentiment-price-card :sentiment_price="view[2]"/>
          </b-col>
        </b-row>
      </template>
    </b-container>
  </div>
</template>

<script>
import moment from "moment-timezone";

export default {
  name: "sentimentPriceComparison",
  auth: false,
  async asyncData({$axios}) {
    const response = await $axios.$get('/sentimentPrice/snapshot/?last=2')
    return {response: response}
  },
  methods: {
    paired_view(response) {
      let my_view = []
      let icon_name = "arrow_up"
      for (const sentiment_price of response[1].sentiment_prices) {
        let sentiment_pair = response[0].sentiment_prices.find(function (element) {
          return element.symbol === sentiment_price.symbol;
        })
        if (sentiment_pair != null) {
          if (sentiment_pair.price > sentiment_price.price) {
            icon_name = "arrow-up-right"
          } else if (sentiment_pair.price === sentiment_price.price) {
            icon_name = "arrow-right"
          } else {
            icon_name = "arrow-down-right"
          }
          my_view.push([sentiment_price, icon_name, sentiment_pair])
        }
      }
      return my_view
    }
  },
  filters: {
    moment: function (date) {
      let formatted_date = moment.utc(date).tz(moment.tz.guess())
      formatted_date.locale('es')
      return formatted_date.format('LLL')
    }
  }
}
</script>

<style scoped>
.id-text {
  color: #6c757d;
  font-weight: 400;
}
</style>
