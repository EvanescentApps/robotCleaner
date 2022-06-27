# Evan Cocain et Dayan Aboudou, CSI1 & BIOST1

import time
import turtle as t
from battery_manager import *


# TODO : idées d'optimisation
# TODO : Prioriser les déchets loin de la station

def is_trash(pos_x, pos_y, trash_list):
    """
    Cette fonction permet de savoir si un déchet se trouve en x, y
    :param pos_x : Int, abscisse à vérifier
    :param pos_y : Int, ordonnée à vérifier
    :param trash_list : List, liste des déchets encore présents
    :return : Boolean, si les coordonnées pointent vers un déchet ou non
    """
    for trash in trash_list:
        trash_x, trash_y = trash["ui_obj"].position()
        if (trash_x, trash_y) == (pos_x, pos_y):
            return True
    return False


def grab_trash(trash_x, trash_y, grid_data):
    """
    Cette fonction se 
    :param trash_x : Int, L'abscisse du déchet à supprimer
    :param trash_y : Int, L'ordonnée du déchet à supprimer
    :param grid_data : Dictionnaire regroupant les caractéristiques du bot, des déchets et de la map
    :return : Turtle, L'objet Turtle du déchet supprimé
    """
    for i in range(len(grid_data["trash"])):
        if grid_data["trash"][i]["x_pos"] == trash_x and grid_data["trash"][i]["y_pos"] == trash_y:
            trash_obj = grid_data["trash"][i]["ui_obj"]
            del grid_data["trash"][i]

            return trash_obj

    return None


def update_bot_position(x, y, grid_data):
    """
    Met à jour la position du bot en se déplaçant axe par axe
    :param x: Int, Abscisse
    :param y: Int, Ordonnée
    :param grid_data : Dictionnaire regroupant les caractéristiques du bot, des déchets et de la map
    :return: Tuple, Distance par axe (effective) parcourue par le robot
    """
    m = grid_data["map"]

    if is_coord_valid(x, y, m["x_max"], m['y_max'], m['x_min'], m['y_min']):
        bot = grid_data['bot']['ui_obj']
        cur_x, cur_y = bot.position()

        # 1 move up, 2 move down
        bot.goto(x, cur_y)
        bot.goto(x, y)

        grid_data['bot']['ui_obj'] = bot
        return abs(x - cur_x), abs(y - cur_y)
    else:
        print("Coordonnée non valide", x, y)
        return None, None


def spread_trash(grid_data):
    proba_appearance = randint(1, 4)

    if proba_appearance == 1:
        print("Nouveaux déchets")

        random_position = choice([True, False])

        create_random_trash(grid_data, randint(1, 7), True, False)
        skins = next(walk("lil_trash"), (None, None, []))[2]
        ui_display_trashes(grid_data, skins, t)
        # create_random_trash() localisé autour du bot et update only new trashes


def search_for_nearest_trashes(bot_x, bot_y, trash_list, max_range):
    """
    Cherche le déchet le plus proche du robot en comparant les distances absolues
    :param bot_x: Int, abscisse du bot
    :param bot_y: Int, ordonnée du bot
    :param trash_list: List, Liste des déchets encore présents
    :param max_range: Int, Distance maximale à laquelle le robot peut aller
    :return: Liste de Tuples d'Int, Coordonnées de position des déchets les plus proches distants du même rayon du robot
    """
    nearest_trash_list = []

    if trash_list:
        nearest_trash_list.append(trash_list[0]["ui_obj"])

        for trash in trash_list:
            trash_x, trash_y = trash["ui_obj"].position()
            dist_trash_to_bot = distance_manhattan(bot_x, bot_y, trash_x, trash_y)

            nearest_x, nearest_y = nearest_trash_list[0].position()
            dist_prev_trash_to_bot = distance_manhattan(bot_x, bot_y, nearest_x, nearest_y)

            if dist_trash_to_bot < dist_prev_trash_to_bot:
                nearest_trash_list.clear()
                nearest_trash_list.append(trash["ui_obj"])
            elif dist_trash_to_bot == dist_prev_trash_to_bot:
                nearest_trash_list.append(trash["ui_obj"])

        nearest_x, nearest_y = nearest_trash_list[0].position()
        if abs(bot_x) - abs(nearest_x) > max_range or abs(bot_y) - abs(nearest_y) > max_range:
            print("----> Trashes are out of range !")
            return []
        else:
            return nearest_trash_list
    else:
        print("La liste est vide")
        return []


# Crée des déchets à des positions aléatoires en début de programme
def create_random_trash(grid_data, amount, near_position=False, around_bot=False):
    """
    Crée des déchets à une position aléatoire et les ajoute à la liste
    :param grid_data: Dictionnaire regroupant les caractéristiques du bot, des déchets et de la map
    :param amount: Int, Nombre de déchets à générer
    :return: Aucun
    """
    trashs = grid_data["trash"]

    m= grid_data['map']

    if grid_data['bot']['ui_obj'] is not None:
        bot_x, bot_y = grid_data['bot']['ui_obj'].position()
    else:
        bot_x, bot_y = grid_data['bot']['x_pos'], grid_data['bot']['y_pos']

    for i in range(amount):

        if near_position:

            if around_bot:
                initial_pos_x = bot_x
                initial_pos_y = bot_y
            else:
                initial_pos_x = randint(-5, 5)*40
                initial_pos_y = randint(-5, 5)*40

                dr_doof = t.Turtle()
                dr_doof.shape("dr_doof.gif")
                dr_doof.goto(initial_pos_x, initial_pos_y)

            x = initial_pos_x + randint(-1, 1) * 40
            y = initial_pos_y + randint(-1, 1) * 40
            while not is_coord_valid(x, y, m["x_max"], m['y_max'], m['x_min'], m['y_min']):
                x = initial_pos_x + randint(-1, 1) * 40
                y = initial_pos_y + randint(-1, 1) * 40
        else:
            x = randint(-5, 5) * 40
            y = randint(-5, 5) * 40

        trashs.append({'x_pos': x, 'y_pos': y, 'ui_obj': None})
        # print("Generated x,y :", x, y)

    grid_data["trash"] = trashs


def calcul_charging_time(capacity_milli, voltage):
    """
    Cette fonction renvoie le temps de chargement en secondes à partir de la formule t (h) = capacity (Ah) / voltage (V)
    :param capacity_milli: Int, capacité en mAh
    :param voltage: Int, Tension en V
    :return: Int, Temps de charge en s
    """

    capacity = capacity_milli / 1000
    time_in_hours = capacity / voltage
    time_in_seconds = time_in_hours * 3600
    return time_in_seconds


def recharge(grid_data, text_turtle, turtle):
    """
    Dirige le robot vers la station de chargement
    :param turtle: Turtle, Instance existante de la lib Turtle pour créer de nouveaux objets (Texte, Turtle, etc)
    :param grid_data: Dictionnaire regroupant les caractéristiques du bot, des déchets et de la map
    :param text_turtle: Turtle, Objet Turtle chargé de dessiner le texte
    :return: Aucun
    """

    update_bot_position(grid_data["station"]["x_pos"], grid_data["station"]["y_pos"], grid_data)
    print("Chargement en cours")
    max_charge = grid_data["bot"]["max_battery_capacity"]

    current_charge = grid_data["bot"]["current_battery_capacity"]

    while current_charge < max_charge:
        time.sleep(0.01)

        # Charge de 200 mAh par seconde
        current_charge = current_charge + 200
        if current_charge > max_charge:
            current_charge = max_charge

        print("Chargé à " + str(ratio_to_percent(current_charge, max_charge)) + "%")
        ui_update_battery_level(ratio_to_percent(current_charge, max_charge), text_turtle, turtle)

    time.sleep(0.7)
    grid_data["bot"]["current_battery_capacity"] = max_charge

    # ANCIEN ALGORITHME ne tenant pas compte de la charge initiale (considérée nulle)
    # for i in range(50):
    #     time.sleep(0.01)
    #     print("Chargé à " + str(i * 2 + 2) + "%")
    #     ui_update_text(text_turtle, "Chargé à " + str(i * 2 + 2) + "%")
    #
    # print("Reprise du nettoyage")

    # grid_data["bot"]["battery_capacity"] = 100

    # start_cleaning(grid_data)


def start_cleaning(grid_data, text_turtle, turtle, rounds_turtle):
    """
    Fonction qui démarre le nettoyage et veille au bon état de marche du robot
    :param turtle: Turtle, Instance existante de la lib Turtle pour créer de nouveaux objets (Texte, Turtle, etc)
    :param grid_data: Dictionnaire regroupant les caractéristiques du bot, des déchets et de la map
    :param text_turtle: Turtle, Objet Turtle chargé de dessiner le texte
    :return: Aucun
    """
    tired_bot_round = randint(70, 100) # Easter egg, quand le robot devient fatigué

    very_angry_bot_round = randint(50, 70) # Easter egg, quand le robot devient furieux

    rounds = 0
    while grid_data["trash"]:
        # Battery drop for each round with distance

        current_battery_capacity = grid_data["bot"]["current_battery_capacity"]

        bot_x, bot_y = grid_data["bot"]["ui_obj"].position()

        nearest_trashes_position_list = search_for_nearest_trashes(bot_x, bot_y, grid_data["trash"],
                                                                   grid_data["map"]["max_range_by_axis"])
        x, y = choice(nearest_trashes_position_list).position()

        if rounds == tired_bot_round:
            print("J'en ai plein les roues de vos saletés :/")

        if rounds == very_angry_bot_round:
            print("\n\nJe suis très en colère, vous ne respectez vraiment rien vous les humains :(\n\n")
            for i in range(12):
                t.bgcolor("red")
                time.sleep(0.01)
                t.bgcolor("white")
                time.sleep(0.01)

            turtle.simpledialog.askstring("Pas content :(","Je suis très en colère, vous ne respectez vraiment rien vous les humains :(")

        # print(bot_x, x, bot_y, y)

        if x is not None and y is not None:
            distance = distance_axis(bot_x, x, bot_y, y)

            distance_trash_to_station = distance_axis(x, grid_data["station"]["x_pos"], y,
                                                      grid_data["station"]["y_pos"])

            if is_enough_battery(distance, distance_trash_to_station, current_battery_capacity):
                # rounds < grid_data["map"]["max_rounds"] supprimé, car peu intéressant dans le cas présent
                dist = update_bot_position(x, y, grid_data)
                trash_got = grab_trash(x, y, grid_data)
                trash_got.hideturtle()
                spread_trash(grid_data)
                rounds = rounds + 1

                ui_update_round_text(rounds_turtle, rounds)

                # print("Distance ", dist)
                battery_drop(grid_data, dist, text_turtle, turtle)

            else:
                print("Retour à la station nécessaire (Batterie insuffisante : " + str(
                    current_battery_capacity) + "mAh, nécessaire " + str(
                    int(calculate_battery_drop(distance) + calculate_battery_drop(distance_trash_to_station))),
                      "mAh)")

                recharge(grid_data, text_turtle, turtle)

    print("Nettoyage terminé")
    ui_update_text(text_turtle, "Nettoyage terminé", style=('Arial', 18), position=(0, 220))
    recharge(grid_data, text_turtle, turtle)

def load_grid_data(conf_file_path=None):
    """
    Charge les données de la grille (BIENTÔT)
    :param conf_file_path: String, Fichier JSON regroupant les différentes caractéristiques
    :return: Dictionnaire grid_data regroupant les caractéristiques du bot, des déchets et de la map
    """
    if conf_file_path is None:
        return {'bot': {'x_pos': 20, 'y_pos': 20, 'ui_obj': None, 'max_battery_capacity': 5000,
                        'current_battery_capacity': None},  # Capacité de batterie en mAh
                'map': {
                    'max_range_by_axis': 200,  # 80
                    'max_rounds': 50,
                    'x_min': -200,
                    'y_min': -200,
                    'x_max': 200,
                    'y_max': 200},
                'trash': [  # Liste remplie par des Trashes aléatoires
                    # {'x_pos': 80, 'y_pos': 100, 'ui_obj': None},
                    # {'x_pos': 200, 'y_pos': 20, 'ui_obj': None}
                ],
                'station': {'x_pos': -190, 'y_pos': -190, 'voltage': 12}
                }
    else:
        # LATER
        print("File loading not supported for the moment")


def main():
    """
    Fonction principale, appelle les fonctions chargées de l'UI, charge les skins et démarre le processus de nettoyage
    :return : Aucun
    """

    wn = t.Screen()
    text_turtle = t.Turtle()
    rounds_turtle = t.Turtle()

    grid_data = load_grid_data()

    skins = ui_load_skins(wn)

    nb_dechets = t.simpledialog.askstring("Bonjour !", "Combien de déchets dois-je ramasser maintenant ?")  # noqa

    if nb_dechets is None or not nb_dechets.isdigit() or nb_dechets.lower().startswith('n') or not 1 <= int(
            nb_dechets) <= 300:
        print("Le nombre de déchets doit être entre 1 et 300")
        wn.clear()
        wn.bye()
    else:
        print("Génération de ", nb_dechets, " déchets")

        wn.tracer(False)

        create_random_trash(grid_data, int(nb_dechets))
        ui_screen_setup(grid_data, wn, t)
        ui_display_trashes(grid_data, skins, t)

        ui_update_text(text_turtle, "The Robot Trash Cleaner", style=('Helvetica', 26))
        ui_display_charging_station(grid_data, t)

        ui_init_bot(grid_data, t)

        wn.update()
        wn.tracer(True)
        time.sleep(1)
        draw_battery_picto(60, t)

        # On suppose le robot chargé au démarrage

        max_capacity = grid_data["bot"]["max_battery_capacity"]

        # Avertissement inutile ici donc ignoré par # noqa
        grid_data["bot"]["current_battery_capacity"] = max_capacity  # noqa

        start_cleaning(grid_data, text_turtle, t, rounds_turtle)

        wn.exitonclick()


# TODO : Eviter obstacles
# TODO : au début, perso qui jette des déchets
# TODO : perso méchant qui apparait et qui salit tout
# TODO : reservoir
# TODO : poubelles et réservoirs différents Tri séléctif
# TODO : les déchets attrapés se dirigent vers la poubelle où ils disparaissent
# TODO : texte de dialogue du robot lors d'actions précises (chargé, déchargé)
# TODO : barre de score comptabilisant le nombre de déchets jetés

main()
