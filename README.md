# Pokedex Django Project
Ce projet Django a été réalisé dans le cadre d'un exercice en équipe, visant à récupérer et afficher les informations des 151 premiers Pokémon à partir de l'API PokeAPI.
## Installation
1. **Cloner le dépôt puis vous déplacer dans le bon dossier:**
    ```bash
    git clone https://B3Projects@dev.azure.com/B3Projects/Pokedex_Python/_git/Pokedex_Python
    cd pokedex
    ```
2. **Appliquer les migrations :**
    ```bash
    python manage.py migrate
    ```
3. **Lancer le serveur de développement :**
    ```bash
    python manage.py runserver
    ```
    Le site sera accessible à l'adresse en cliquant sur le lien de votre terminal quand le serveur sera lancé.
## Fonctionnalités
- Affichage des 151 premiers Pokémon depuis l'API PokeAPI.
- Cliquez sur une carte pour afficher des détails sur le Pokémon sélectionné.
- Navigation facile entre les Pokémon suivants et précédents.
- Possibilité d'ajouter un Pokémon à son équipe (limite de 6 Pokémon).
- L'équipe est affichée en haut à droite du Pokédex.
- Mise en cache des Pokémon afin d'éviter les longs délais de chargement.
## Structure du Projet
-`pokedex/pokedex/`: Contient notamment le fichier **urls** pour ajouter nos path mais aussi le fichier **settings** dans lequel nous avons ajouter notre application(pokemons) dans **INSTALLED_APPS**
- `pokedex/pokemons/`: Application principale contenant les vues, modèles, et fichiers statiques.
- `templates/`: Contient les fichiers HTML pour le rendu des pages.
- `static/`: Répertoire pour les fichiers statiques contenant le CSS et les images.
- `views.py`: Contient les fonctions qui définissent le comportement de chaque page de notre application Django
## Fichier 'views.py'
Voici quelques explications sur notre fichier et ses fonctionnalités :
-**'get_pokemon_list()'** : Cette fonction récupère la liste des 151 premiers Pokémon depuis l'API PokeAPI. Elle utilise le cache Django pour stocker les données pendant une heure afin d'éviter de faire des requêtes fréquentes à l'API.
-**'pokemon_details(request, pokemon_id)'** : Cette fonction gère la page de détails d'un Pokémon spécifique. Elle utilise la fonction get_pokemon_list() pour obtenir la liste des Pokémon, trouve le Pokémon correspondant à l'ID fourni, puis rend la page HTML avec les détails du Pokémon sélectionné ainsi que les Pokémon précédent et suivant.
-**'add_to_team(request)'** : Cette fonction gère l'ajout d'un Pokémon à l'équipe. Elle récupère l'ID du Pokémon à partir de la requête POST, vérifie s'il n'est pas déjà dans l'équipe, puis l'ajoute à la session utilisateur
-**'pokemons(request)'** : Cette fonction gère la page principale du Pokédex (pokedex.html). Elle utilise la fonction get_pokemon_list() pour obtenir la liste des Pokémon et filtre les résultats en fonction d'une éventuelle recherche. Ensuite, elle rend la page HTML avec la liste des Pokémon.
## Fichier 'pokedex.html'
Voici quelques explications sur notre fichier :
-**Section d'équipe** : Cette section affiche les six premiers Pokémon de l'équipe en haut à droite de la page. Les images des Pokémon sont affichées dans des cartes Bootstrap.
-**Formulaire de recherche** : Un formulaire de recherche simple permet à l'utilisateur de rechercher un Pokémon spécifique par nom.
-**Gestion des erreurs** : Si un message d'erreur est généré (par exemple, si le Pokémon recherché n'existe pas), il est affiché dans la section d'erreur.
-**Affichage des Pokémon** : La liste des Pokémon est affichée sous forme de cartes, chaque carte contenant le nom, les points de vie (HP), l'image, l'attaque, la défense et le type du Pokémon. Un bouton est également inclus pour ajouter le Pokémon à l'équipe.
## Auteurs
- [ROUZIOUX MATTEO]
- [MA JIANCHAO]
- [COUET QUENTIN]
- [RICOUL CHARLY]