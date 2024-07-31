export default function ({$axios, $izitoast}) {
  $axios.onRequest(config => {
    console.log('Making request to ' + config.baseURL + config.url)
  })

  $axios.onResponse(response => {
    console.log('Response obtained: ' + JSON.stringify(response.data))
  })

  $axios.onError(error => {
    console.log('Error response: ' + JSON.stringify(error))
    /*
     $izitoast.error({
      'title': "Oops!",
      'message': error.message
    })
    */
  })
}
