# Cliente

Utilizamos una SPA basada en Nuxt.JS, Axios y BoostrapVue para consumir y presentar la API del servidor.

## Inicialización

```bash
# Instalar dependencias
$ yarn install

# Server de desarrollo con hot reload en localhost:3000
$ yarn dev

# Buildear e iniciar el servidor productivo
$ yarn build
$ yarn start

# Generar proyecto estático
$ yarn generate
```

## Idea general

Este frontend se creó con el fin de disponibilizar la info de los jobs croneados cada media hora del backend.

## Vistas

### /informationRetrieval

Muestra una lista de tarjetas donde cada una contiene:
  - El texto original
  - El texto analizado (con sanitizado, tokenizado, stemming, lemmatizacion, sin stopwords)
  - El tópico/criptomoneda
  - Un boton con el link a la fuente de información (noticia, tweet, post, etc.)
  - El top 5 principales palabras (frequency)
  - El N.E.R
  - El sentimiento asociado al texto
  - Su timestamp de creación y recupero.

### /sentimentPriceComparison

Muestra una grilla de 3 columnas donde las columnas laterales tienen una tarjeta con:
 - Nombre de la criptomoneda
 - Precio
 - Sentimiento asociado

A la izquierda se muestra el snapshot del anteultimo cron job corrido por el backend, mientras que a la derecha el último.  

Ambas columnas tienen el id del snapshot que representan y el timestamp del mismo.

La columna del centro muestra una flecha que indica si el precio subió o bajó entre snapshots.

### /api

Nos lleva al swagger del backend.

## Autenticación

Nos podemos loguear con google para obtener el bearer token que nos permitirá jugar con endpoints más avanzandos de la API.
