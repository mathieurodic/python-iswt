# Webservice Python

Pour fournir une estimation fiable de la production d’une instalation photovoltaïque, il est nécessaire de connaître l’irradiation en kWh/m²/an en un point donné en France pour ensuite déterminer la puissance en fonction de la taille du système installé.

Pour fournir cette valeur aux utilisateurs en fonction de leur position il est nécessaire de rendre cette mesure accessibbe via un webservice.

Le but de cet exercice est donc de fournir un webservice écrit avec [Flask](http://flask.pocoo.org/) et Python, qui retourne au format JSON l’irradiation annuelle à un point donné par sa latitude et sa longitude, selon la formule suivante :

```
irradiance = 2000.0 - 900.0 * (latitude – 41.0) / (51.5 – 41.0)
```

Cette méthode n’étant pas définie en dehors du cadre géographique donné le webservice retournera une erreur 403 pour :

 * les latitudes strictement inférieures à 41.00°
 * les latitudes strictement supérieures à 51.50°
 * les longitudes strictement inférieures à -5.50°
 * les longitudes strictement supérieures à 10.00°

En supposant que le webservice fonctionne localement sur le port 5000, il devra donc
renvoyer les résultats suivants pour les commandes données (en ignorant les versions
des outils) :

```
$ curl -D - 'localhost:5000'
HTTP/1.0 200 OK
Content-Type: text/html; charset=utf-8
Content-Length: 19
Server: Werkzeug/0.14.1 Python/3.6.5
Date: Sat, 02 Mar 2049 14:42:52 GMT
Simulation service
```

```
$ curl -D - 'localhost:5000/data?lat=45&lng=5'
HTTP/1.0 200 OK
Content-Type: text/html; charset=utf-8
Content-Length: 29
Server: Werkzeug/0.14.1 Python/3.6.5
Date: Sat, 02 Mar 2049 14:43:50 GMT
{"result": 1657.142857142857}
```

```
$ curl -D - 'localhost:5000/data?lat=42.13&lng=8.24'
HTTP/1.0 200 OK
Content-Type: text/html; charset=utf-8
Content-Length: 30
Server: Werkzeug/0.14.1 Python/3.6.5
Date: Sat, 02 Mar 2049 14:44:41 GMT
{"result": 1903.1428571428569}
```

```
$ curl -D - 'localhost:5000/data?lat=52.34&lng=-12.04'
HTTP/1.0 403 FORBIDDEN
Content-Type: text/html
Content-Length: 234
Server: Werkzeug/0.14.1 Python/3.6.5
Date: Sat, 02 Mar 2049 14:48:40 GMT
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
<title>403 Forbidden</title>
<h1>Forbidden</h1>
<p>You don't have the permission to access the requested resource.
It is either read-protected or not readable by the server.</p>
Javascript / HTML
```

Faire une page permettant de saisir une latitude et une longitude et d’afficher le résultat d’une requête au webservice.

La page peut être aussi simple que voulu avec simplement deux champs de texte pour saisir les coordonnées et un bouton pour envoyer la requête avec un affichage dans le corps du document.

Le webservice peut continuer à fonctionner localement sur le port 5000.

## Pour aller plus loin…

Une fois que le formulaire fonctionne, si tu veux aller plus loin, tu peux utiliser le framework de ton choix et intégrer une carte pour qu’on puisse sélectionner la position en un clic, mais ce n’est pas obligatoire ;-)

De même tu pourras déployer ton webservice sur un « Dyno » gratuit chez [Heroku](https://www.heroku.com), mais ça non plus ce n’est pas obligatoire.
