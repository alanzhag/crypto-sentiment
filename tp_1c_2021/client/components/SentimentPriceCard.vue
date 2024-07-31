<template>
  <div class="sentinment_price_card">
    <b-card
      :footer="sentiment_price.sentiment"
      :footer-bg-variant="border_variant"
      :footer-border-variant="border_variant"
      :header="sentiment_price.symbol"
      :title="price(sentiment_price.price)"
      align="center"
      footer-tag="footer"
    >
    </b-card>
  </div>
</template>

<script>
import shared from '../shared'

export default {
  name: "SentimentPriceCard",
  props: ['sentiment_price'],
  data() {
    return {
      border_variant: shared.get_sentiment_border_variant(this.sentiment_price.sentiment),
      formatter: new Intl.NumberFormat("es-AR", {style: 'currency', currency: 'USD', minimumFractionDigits: 8})
    };
  },
  methods: {
    price(some_price) {
      return this.formatter.format(some_price);
    }
  }
}
</script>

<style scoped>
.sentinment_price_card {
  padding: 20px;
}
</style>
