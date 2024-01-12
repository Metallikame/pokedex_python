from django.core.cache import cache
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import requests


# test branch
def get_pokemon_list():
    # Essayer de récupérer les données depuis le cache
    pokemon_list = cache.get('pokemon_list')

    if pokemon_list is None:
        # Si les données ne sont pas en cache, les récupérer depuis l'API
        url = 'https://pokeapi.co/api/v2/pokemon/?limit=151'
        response = requests.get(url)
        result = response.json()

        pokemons = []  # Liste pour stocker tous les Pokémon
        # Récupérer la liste des résultats à partir de la clé 'results'
        pokemon_results = result.get('results', [])

        for pokemon in pokemon_results:
            pokemon_url = pokemon['url']
            pokemon_response = requests.get(pokemon_url)
            pokemon_data = pokemon_response.json()

            pokemon_details = {
                'id': pokemon_data['id'],
                'name': pokemon_data['name'],
                'image': pokemon_data['sprites']['front_default'],
                'hp': pokemon_data['stats'][0]['base_stat'],
                'attaque': pokemon_data['stats'][1]['base_stat'],
                'defense': pokemon_data['stats'][2]['base_stat'],
                'type': pokemon_data['types'][0]['type']['name'],
                'specialAttack': pokemon_data['stats'][3]['base_stat'],
                'specialDefense': pokemon_data['stats'][4]['base_stat'],
                'speed': pokemon_data['stats'][5]['base_stat'],
                'front_gif': pokemon_data['sprites']["other"]['showdown']['front_default'],
                'back_gif': pokemon_data['sprites']["other"]['showdown']['back_default'],
            }

            pokemons.append(pokemon_details)

        # Mettre en cache les données pour la prochaine requête
        cache.set('pokemon_list', pokemons, timeout=3600)  # Cache pendant 1 heure (en secondes)
        pokemon_list = pokemons

    return pokemon_list


def pokemons(request):
    # Utiliser la fonction pour récupérer la liste des Pokémon
    pokemons = get_pokemon_list()

    team_pokemons = request.session.get('team_pokemons', [])

    # Gérer la recherche
    query = request.GET.get('pokemon-filter')
    if query:
        pokemons = [pokemon for pokemon in pokemons if query.lower().strip() in pokemon['name'].lower()]
        if not pokemons:
            return render(request, 'pokedex.html',
                          {'pokemons': pokemons, 'message': f"Désolé le Pokémon '{query}' n'existe pas"})

    pokemon_id = request.POST.get('pokemon_id')
    pokemon_id_suppression = request.POST.get('pokemon_id_suppression')

    message = ""

    # Récupérer les valeurs des pokemon_id_x depuis la session
    pokemon_id_1 = request.session.get('pokemon_id_1', 0)
    pokemon_id_2 = request.session.get('pokemon_id_2', 0)
    pokemon_id_3 = request.session.get('pokemon_id_3', 0)
    pokemon_id_4 = request.session.get('pokemon_id_4', 0)
    pokemon_id_5 = request.session.get('pokemon_id_5', 0)
    pokemon_id_6 = request.session.get('pokemon_id_6', 0)

    # Si pokemon_id existe, attribuer les valeurs pokemon_id_x si elles sont égales à 0
    if pokemon_id:
        if pokemon_id_1 == 0:
            pokemon_id_1 = int(pokemon_id)
        elif pokemon_id_2 == 0:
            pokemon_id_2 = int(pokemon_id)
        elif pokemon_id_3 == 0:
            pokemon_id_3 = int(pokemon_id)
        elif pokemon_id_4 == 0:
            pokemon_id_4 = int(pokemon_id)
        elif pokemon_id_5 == 0:
            pokemon_id_5 = int(pokemon_id)
        elif pokemon_id_6 == 0:
            pokemon_id_6 = int(pokemon_id)
        else:
            message = "Vous ne pouvez pas mettre plus de 6 pokemons dans votre équipe"

    # Gérer la suppression du pokemon_id_suppression de l'équipe
    if pokemon_id_suppression:
        if int(pokemon_id_suppression) == 1:
            pokemon_id_1 = 0
        elif int(pokemon_id_suppression) == 2:
            pokemon_id_2 = 0
        elif int(pokemon_id_suppression) == 3:
            pokemon_id_3 = 0
        elif int(pokemon_id_suppression) == 4:
            pokemon_id_4 = 0
        elif int(pokemon_id_suppression) == 5:
            pokemon_id_5 = 0
        elif int(pokemon_id_suppression) == 6:
            pokemon_id_6 = 0

    # Enregistrer les valeurs mises à jour dans la session
    request.session['pokemon_id_1'] = pokemon_id_1
    request.session['pokemon_id_2'] = pokemon_id_2
    request.session['pokemon_id_3'] = pokemon_id_3
    request.session['pokemon_id_4'] = pokemon_id_4
    request.session['pokemon_id_5'] = pokemon_id_5
    request.session['pokemon_id_6'] = pokemon_id_6

    # Logique pour supprimer une équipe
    delete_team_number = request.POST.get('delete_team_number')
    if delete_team_number:
        team_number_to_delete = int(delete_team_number)
        if f'equipe_{team_number_to_delete}' in request.session:
            del request.session[f'equipe_{team_number_to_delete}']

            # Réorganiser les numéros d'équipe restants
            equipe_count = request.session.get('equipe_count', 1)
            for i in range(team_number_to_delete + 1, equipe_count):
                current_equipe = request.session.get(f'equipe_{i}')
                if current_equipe:
                    del request.session[f'equipe_{i}']
                    request.session[f'equipe_{i - 1}'] = current_equipe

            # Mettre à jour le nombre total d'équipes après réorganisation
            request.session['equipe_count'] = equipe_count - 1

    # Logique pour sauvegarder l'équipe
    save_team = request.POST.get('save_team')
    if save_team:
        # Récupérer le numéro de l'équipe à partir de la session
        equipe_count = request.session.get('equipe_count', 1)

        # Créer une liste pour sauvegarder les Pokemon ID de l'équipe actuelle
        equipe = [
            pokemon_id_1, pokemon_id_2, pokemon_id_3,
            pokemon_id_4, pokemon_id_5, pokemon_id_6
        ]

        # Stocker cette équipe dans la session en utilisant le numéro de l'équipe comme clé
        request.session[f'equipe_{equipe_count}'] = equipe

        # Incrémenter le compteur pour l'équipe suivante
        request.session['equipe_count'] = equipe_count + 1

    # Récupérer toutes les équipes enregistrées dans la session
    equipe_count = request.session.get('equipe_count', 1)
    equipes = []
    for i in range(1, equipe_count):
        equipe = request.session.get(f'equipe_{i}', [])
        equipes.append(equipe)

    context = {
        'pokemons': pokemons,
        'team_pokemons': team_pokemons,
        'message': message,
        'pokemon_id': pokemon_id,
        'pokemon_id_1': pokemon_id_1,
        'pokemon_id_2': pokemon_id_2,
        'pokemon_id_3': pokemon_id_3,
        'pokemon_id_4': pokemon_id_4,
        'pokemon_id_5': pokemon_id_5,
        'pokemon_id_6': pokemon_id_6,
        'equipe_count': request.session.get('equipe_count', 1),
        'equipes': equipes,
    }

    return render(request, 'pokedex.html', context)


def pokemon_details(request, pokemon_id):
    # Utiliser la fonction pour récupérer la liste des Pokémon
    pokemons = get_pokemon_list()

    # Trouver le Pokémon par son ID
    selected_pokemon = next((pokemon for pokemon in pokemons if pokemon['id'] == pokemon_id), None)

    if selected_pokemon is None:
        return HttpResponse("Pokémon non trouvé", status=404)

    current_index = pokemons.index(selected_pokemon)

    previous_index = (current_index - 1) % len(pokemons)

    # Calculer l'index du Pokémon suivant
    next_index = (current_index + 1) % len(pokemons)

    context = {
        'selected_pokemon': selected_pokemon,
        'previous_pokemon': pokemons[previous_index],
        'next_pokemon': pokemons[next_index],
    }

    return render(request, 'pokemon_details.html', context)


def loading(request):
    return render(request, 'loading.html')
