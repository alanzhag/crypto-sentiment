# Trabajo Práctico Nº3

## Detección de Emociones y recuperación de la información (Information Retrieval)

### Consigna

-----------
El análisis y detección de sentimientos (positivos, negativos o neutros) es uno de los campos más importantes del Procesamiento del Lenguaje Natural. Diversas técnicas y estado del arte (SOTA) son aportadas día a día por la comunidad científica, lo cuál luego lleva a la implementación de los mismos por parte de las organizaciones.  

En este Trabajo Práctico, además de aplicar análisis de sentimientos, se deberá usar accesos a información de diversas APIs (las que se nombren en este enunciado son solamente a modo de ejmplo, sin limitar de ninguna forma las que puedan ser implementadas). Además, técnicas de Recuperación de Información (Information Retrieval) deberán ser usadas para capturar y recuperar la información analizada sobre los tópicos o palabras claves (keywords) pedidas.  

En este año las keywords serán nombres de criptomonedas y su correspondiente símbolo con el cuál operan en los mercados (Ejemplo, para Bitcon será Bitcon y $BTC, o para Ethereum, $ETH, o en el screenshot adjunto se muestra la moneda TERRA LUNA y su símbolo es $LUNA, y así sucesivamente). Se deben elegir 20 criptomonedas/símbolos.  

Dado que es un proyecto que requiere de Information Retrieval, se requiere implementar una base de datos para almacenar la información analizada (queda a criterio del/a estudiante qué base de datos utilizar).  

Se debe utilizar varias fuentes de información – al menos 3 - (por ejemplo: google.com, bing.con. twitter, reddit, cointelegraph) desde dónde se tomará información de las 20 criptomonedas elegidas previamente, se guardarán sus X principales palabras (frequency), su timestamp, sus NERs (Named Entity Recognition) y su Sentimiento asociado al pedazo de información analizado. Se pueden combinar varias fuentes de información para tomar una decisión final.  

La nota máxima se alcanza si se lograra comparar el sentimiento predecido con el precio o variación de esa criptmoneda en el mercado en los últimos 30 minutos previos y 30 posteriores (conectarse con una API como coinmarketcap, coingecko u okex, por solo nombrar tres ejemplos, sería lo correcto en este caso para automatizar el proceso de captura de información pero pueden hacerlo manualmente).  


### Arquitectura

#### [Cliente](https://github.com/alanzhag/nlp-utn-frba/tree/main/tp_1c_2021/client)  

* Javascript
* Nuxt.js como framework para exponer una SPA basada en Vue.js
  * Axios para requests HTTP basados en promises
  * BootstrapVue como Framework CSS

#### [Servidor](https://github.com/alanzhag/nlp-utn-frba/tree/main/tp_1c_2021/servidor)

* Python 3.9
* SpaCy y sklearn para NLP
* newspaper3k para web scrapping
* GoogleNews, praw (reddit), tweepy (twitter) como wrappers de sus correspondientes APIs.
* Flask para exponer API Rest
* Firebase-Firestore para almacenamiento no-sql y obtención de los datos procesados
* PostgreSQL para almacenamiento sql de modelos para la gestion interna de la app.
* SqlAlchemy como ORM
* marshmallow para serialización de objetos
* Flask-HTTPAuth y google-auth-oauthlib para autenticación
* Flask-CLI + flask-command para crear el punto de entrada al job de obtención de información
* Hosting en Heroku + heroku-scheduler para correr el job de obtención de información cada 30 minutos
* Flask-Executor para mantener cola de trabajo asincrónica.