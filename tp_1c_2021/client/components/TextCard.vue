<template>
  <div class="text_card">
    <b-card
      :footer="text.text_analysis.sentiment"
      :footer-bg-variant="border_variant"
      :footer-border-variant="border_variant"
      :header="text.text_retrieve_properties.timestamp | moment"
      :title="text.text_retrieve_properties.topic"
      align="center"
      footer-tag="footer"
    >
      <b-card-sub-title>id: {{ text.text_retrieve_properties.id }}</b-card-sub-title>
      <strong>Original text</strong>
      <b-card-text>{{ text.text_analysis.original_text }}</b-card-text>
      <strong>Processed text</strong>
      <b-card-text>{{ text.text_analysis.processed_text }}</b-card-text>
      <b-container class="bv-example-row">
        <b-row>
          <b-col>
            <div>
              <strong>Top 5 principales palabras</strong>
              <div v-for="(_, word) in text.text_analysis.frequency">
                <div>{{ word }}</div>
              </div>
            </div>
          </b-col>
          <b-col>
            <div>
              <strong>N.E.R</strong>
              <div v-for="(ner, word) in text.text_analysis.ner">
                <div>{{ word }}: {{ ner }}</div>
              </div>
            </div>
          </b-col>
        </b-row>
      </b-container>
      <b-button :href="text.text_retrieve_properties.link" variant="outline-primary">
        {{ text.text_retrieve_properties.source }}
      </b-button>
    </b-card>
  </div>
</template>

<script>
import moment from 'moment-timezone'
import shared from '../shared'

export default {
  name: "TextCard",
  props: ['text'],
  data() {
    return {
      border_variant: shared.get_sentiment_border_variant(this.text.text_analysis.sentiment)
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
.text_card {
  padding: 20px;
}
</style>
