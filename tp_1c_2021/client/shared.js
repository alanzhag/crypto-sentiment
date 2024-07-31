export default {
  get_sentiment_border_variant: function (sentiment) {
    if (sentiment === 'POSITIVE') {
      return "success"
    } else if (sentiment === "NEUTRAL") {
      return "secondary"
    } else {
      return "danger"
    }
  }
}
