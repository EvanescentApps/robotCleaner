from helper import *
from ui import *


def is_enough_battery(distance_next_trash, distance_trash_charger, current_battery_capacity):
    """
    Vérifie si l'état de la batterie permet de continuer le nettoyage
    sans se retrouver bloqué incapable de rejoindre la station de chargement
    :param distance_next_trash : Int, distance bot-prochain déchet
    :param distance_trash_charger : Int, distance prochain déchet-station de charge
    :param current_battery_capacity : Int, Capacité actuelle de la batterie en mAh
    :return : Boolean, si la batterie peut encore rejoindre le chargeur ou non à l'issue du nettoyage
    """
    # print(distance_next_trash, distance_trash_charger, current_battery_capacity)
    estimated_drop = calculate_battery_drop(distance_next_trash) + calculate_battery_drop(distance_trash_charger)

    return current_battery_capacity - estimated_drop > 0


def battery_drop(grid_data, distance, text_turtle, t):
    """
    Diminue la charge restante de la batterie en fonction de la distance parcourue et met à jour les données du robot
    :param t : Turtle, Instance existante de la lib Turtle pour créer de nouveaux objets (Texte, Turtle, etc)
    :param grid_data : Dictionnaire regroupant les caractéristiques du bot, des déchets et de la map
    :param distance : Tuple, La distance parcourue par le robot en (x, y)
    :param text_turtle: Objet Turtle chargé de dessiner le texte
    :return : Aucun
    """
    max_capacity = grid_data["bot"]["max_battery_capacity"]
    initial_capacity = grid_data["bot"]["current_battery_capacity"]
    capacity_drop = calculate_battery_drop(distance)
    updated_capacity = initial_capacity - capacity_drop
    percentage = ratio_to_percent(updated_capacity, max_capacity)

    print("Batterie:", str(percentage), "%, Perte:", capacity_drop, "mAh")
    grid_data["bot"]["current_battery_capacity"] = updated_capacity

    ui_update_battery_level(percentage, text_turtle, t)


def calculate_battery_drop(distance):
    """
    Calcule la valeur de la perte de capacité de batterie en mAh en fonction de la distance
    (+2 à chaque déchet + k * distance effective)
    :param distance : Int, La distance parcourue par le robot en (x, y) Tuple
    :return: Int, perte de capacité de batterie en mAh
    """

    # print("dist", distance) Vérification de la distance (bug quand on générait des déchets sur les bords)

    distance_totale = distance[0] + distance[1]
    # print("Total distance :", distance_totale)
    return 20 + distance_totale
