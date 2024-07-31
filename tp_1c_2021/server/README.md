# Servidor

Utilizamos una SPA basada en Nuxt.JS, Axios y BoostrapVue para consumir y presentar la API del servidor.

## Inicialización

```bash
# Instalar dependencias
$ pip install -r requirements.txt

# Levantar servidor en localhost:5000
$ flask run
```

# Idea general

Este backend contiene toda la logica que pide la consigna del tp.

Hay un job croneado cada 30 minutos en heroku que ejecuta un **/fetch** y busca en varias fuentes de informacion (reddit, twitter, google_news) los ultimos posts de la ultima media hora de cada una de las 20 criptos configuradas.

Cada texto se pasa por el analizador que se encuentra en **/textAnalysis** y se taggea con su top 5 palabras mas frecuents, su N.E.R y su sentimiento asociado.
El precio de la criptomoneda correspondiente que se puede obtener de **/cryptoPrice** también se agrega al registro.

Esta información se persiste en una base no-sql facilitada por Google Firebase.

# Fuentes de datos
```
> curl http://localhost:3000/api/textSources
{
  "sources": [
    {
      "enabled": true,
      "name": "twitter"
    },
    {
      "enabled": true,
      "name": "google_news"
    },
    {
      "enabled": true,
      "name": "reddit"
    },
    {
      "enabled": true,
      "name": "news"
    }
  ]
}
```

# Cryptos a buscar

```
> curl http://localhost:3000/api/textTopics
{
  "topics": [
    "BTC",
    "ETH",
    "BNB",
    "ADA",
    "DOGE",
    "XRP",
    "BCH",
    "MATIC",
    "XLM",
    "TRX",
    "XMR",
    "AAVE",
    "MKR",
    "MIOTA",
    "CAKE",
    "XTZ",
    "SHIB",
    "YFI",
    "SNX",
    "THETA"
  ]
}
```

# API

Se puede encontrar documentación swagger bajo el endpoint **/api**.

## Endpoints relevantes dentro de /api

### /fetch

Con este endpoint podremos ingresar una petición de búsqueda de información tal cual ofrece **/nlpTagger/run** a la cola de trabajo interna.  
Si el job se logra generar, responderá 200, un job_id y un job_status en WAITING.

Solo se puede ejecutar con token oauth y privilegio de admin.

#### /fetch/id
Se puede consultar el estado del job, siendo este WAITING, RUNNING, FINISHED o FAILURE.


### /nlpTagger/run

Este endpoint expone el servicio que consume fetch, pero no persiste información, por lo que es util para tareas exploratorias y debugging.
Se puede imaginar con el coordinador de la llamada a los demás endpoints. 
  1.  Primero hace un /informationRetrieval para obtener los textos
  2.  Luego a cada texto los pasa por /textAnalysis para agregarles la información relacionada a PLN.
  3.  El precio de /cryptoPrice también se adjunta a cada texto.
  4.  Finalmente se organizan los textos dejandolos con información de /sentimentPrice pero no se persisten.

### /sentimentPrice

Este servicio se encarga de ver los sentimientos de todos los textos y generalizar un sentimiento por cada crypro utilizando un algorimto de mayoria.
Es decir, si hay 3 noticias sobre BTC de fuentes diferentes, y 2 tienen sentimiento positivo, determinamos que para esta crypto en ese timestamp, su sentimiento es POSITIVE.

#### /sentimentPrice/compute

Sirve para debuggear el algoritmo con casos hipoteticos. En caso de empate se tira un random entre los contendientes para definir que sentimiento gana.
```
> curl -X 'POST' \
  'https://alan-zhao-nlp-utn-frba.herokuapp.com/api/sentimentPrice/compute' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "input": [
    {
      "source": "google_news",
      "symbol": "BTC",
      "price": 1,
      "sentiment": "POSITIVE"
    },
    {
      "source": "twitter",
      "symbol": "BTC",
      "price": 1,
      "sentiment": "POSITIVE"
    },
    {
      "source": "reddit",
      "symbol": "BTC",
      "price": 1,
      "sentiment": "NEGATIVE"
    }
  ]
}'

{
  "timestamp": "2021-07-07T01:10:31.336076",
  "sentiment_prices": [
    {
      "sentiment": "POSITIVE",
      "price": 1,
      "symbol": "BTC"
    }
  ]
}
```

#### /sentimentPrice/snapshot

Se trae de la base de datos los ultimos n snapshots de los jobs corridos. Esta info se utiliza para armar la vista de **/sentimentPriceComparison** en el front. 
La info del snapshot contiente el sentimiento asociado a cada cripto y su respectivo precio. Esto nos permite ir comparando las variaciones entre cada ejecución.

###

### /texts
  
Nos permite obtener los textos analizados hasta el momento.

#### /texts/latests

Nos devuelve los últimos textos persistidos.

#### /texts/latests/all-sources

Nos devuelve los ultimos textos persistidos de todas las fuentes habilitadas. Esta info se utiliza para armar la vista de **/informationRetrieval** en el front.

#### /texts/id

Nos devuelve un texto en particular.

### /textAnalysis

Este endpoint acepta un payload json con un campo text, donde se coloca el texto a analizar.

``` 
> curl -X 'POST' \
  'https://alan-zhao-nlp-utn-frba.herokuapp.com/api/textAnalysis' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "text": "25 most mentioned cryptocurrencies on Reddit - July 6th, 2021: ETH, BTC, ADA, LINK, AAVE | Source: Rising Candle"
}'

{
  "sentiment": "POSITIVE",
  "processed_text": "25 mention cryptocurrencie reddit july 6th 2021 eth btc ada link aave source rise candle",
  "original_text": "25 most mentioned cryptocurrencies on Reddit - July 6th, 2021: ETH, BTC, ADA, LINK, AAVE | Source: Rising Candle",
  "frequency": {
    "source": 0.2581988897471611,
    "rise": 0.2581988897471611,
    "reddit": 0.2581988897471611,
    "mention": 0.2581988897471611,
    "link": 0.2581988897471611
  },
  "subjectivity": 0.5,
  "timestamp": "2021-07-07T00:39:50.482293",
  "polarity": 0.5,
  "ner": {
    "25": "CARDINAL",
    "july 6th 2021 eth btc": "DATE"
  },
  "sanitized_text": "25 most mentioned cryptocurrencies on reddit - july 6th, 2021 eth, btc, ada, link, aave | source rising candle"
}
```
### /informationRetrieval

Este endpoint expone el servicio encargado del recupero de información, es decir, buscar los textos relacionados a cada criptomoneda en cada fuente de datos habilitada.

```
> curl http://localhost:3000/api/informationRetrieval
{
  "status": {
    "elapsed_time": 6.053932517010253
  },
  "results": [
    {
      "status": {
        "elapsed_time": 0.5181920090108179
      },
      "source_name": "twitter",
      "by_topics": [
        {
          "topic": "BTC",
          "texts": [
            {
              "content": "Unusual #volume spike in $CHZ-PERP\n\n- 193,951 USD worth of $CHZ traded in the last 5 mins.\n- 9 times the average volume in $CHZ - $PERP\n\n$FTX $crypto $BTC $ETH $DOGE\n\nFor latest alerts, checkout - https://t.co/rLLR03cU0l https://t.co/01B28OjCta",
              "external_id": "1412576106415198215",
              "source": "twitter",
              "metadata": {
                "time_ago": "0:00:03.182134",
                "mapping_time": 0.00028067396488040686
              },
              "id": "58aea325-13cb-47b9-bf5a-ac1bd7c2634f",
              "retrieve_time": "2021-07-07T00:56:05.182134",
              "timestamp": "2021-07-07T00:56:02",
              "link": "https://twitter.com/twitter/statuses/1412576106415198215",
              "topic": "BTC"
            }
          ],
          "status": {
            "elapsed_time": 0.19116818299517035,
            "error": false
          }
        }
      ]
    }
  ]
}
```

# Autenticación

Requiere un Bearer token de Google OAuth. Logearse en el frontend genera uno.
