from os import walk
from random import *


def draw_battery_picto(battery_level, t):
    """

    :param battery_level: Int,
    :param t: Turtle, Instance existante de la lib Turtle pour créer de nouveaux objets (Texte, Turtle, etc)
    :return: Aucun
    """
    color = "green"
    if battery_level > 85:
        bars = 4
    elif battery_level > 70:
        bars = 3
    elif battery_level > 50:
        bars = 2
    elif battery_level > 30:
        bars = 1
    else:
        bars = 1
        color = "red"
        # RED !!!

    t.tracer(False)
    m_drawer = t.Turtle()
    m_drawer.up()
    m_drawer.pensize(2)
    m_drawer.hideturtle()

    m_drawer.setpos(-240, 250)
    m_drawer.begin_fill()
    m_drawer.pencolor("black")
    m_drawer.fillcolor("#e8e8e8")
    m_drawer.down()

    for i in range(2):
        m_drawer.forward(64)
        m_drawer.right(90)
        m_drawer.forward(27)
        m_drawer.right(90)
    m_drawer.end_fill()

    m_drawer.pencolor(color)
    m_drawer.fillcolor(color)

    m_drawer.up()
    m_drawer.pensize(1)
    m_drawer.left(90)
    m_drawer.backward(3)
    m_drawer.right(90)
    m_drawer.forward(3)
    m_drawer.down()

    for k in range(bars):
        for i in range(2):
            m_drawer.down()
            m_drawer.begin_fill()
            m_drawer.forward(12)
            m_drawer.right(90)
            m_drawer.forward(20)
            m_drawer.right(90)
            m_drawer.end_fill()
            m_drawer.up()

        m_drawer.forward(15)

    t.update()
    t.tracer(True)


def ui_screen_setup(grid_data, wn, t):
    """
    Cette fonction définit la fenêtre, met en place la grille et affiche le titre
    :param t: Turtle, Instance existante de la lib Turtle pour créer de nouveaux objets (Texte, Turtle, etc)
    :param grid_data: Dictionnaire regroupant les caractéristiques du bot, des déchets et de la map
    :param wn: Screen turtle, permet de modifier l'affichage
    :return: Aucun
    """

    m_map = grid_data["map"]

    width = abs(m_map["x_min"]) + m_map["x_max"]
    height = abs(m_map["y_min"]) + m_map["y_max"]

    margin = 70

    wn.bgcolor("white")
    wn.setup(width + margin * 2, height + margin * 2)

    # t.speed(5) #fastest
    t.color("black")
    t.mode(mode="world")
    t.title("The Robot Trash Cleaner")  # Title
    t.hideturtle()




def ui_update_text(turtle_text, text, color='black', style=('Helvetica', 30), position=(0, 225)):
    """
    Met à jour le texte affiché en haut de la page
    :param turtle_text: Turtle, Objet Turtle chargé de l'affichage du texte
    :param text: String, Texte à afficher
    :param color: Couleur du texte à afficher
    :param style: Tuple<String, Int, String>Style du texte (police et taille)
    :param position: Tuple<Int>, Position x,y
    :return: Aucun
    """
    turtle_text.hideturtle()
    turtle_text.up()
    turtle_text.setpos(position)

    turtle_text.pencolor(color)
    turtle_text.down()
    turtle_text.clear()
    turtle_text.write(text, align='center', font=style)


def ui_update_round_text(round_turtle, rounds):
    round_turtle.hideturtle()
    round_turtle.up()
    round_turtle.setpos((130, -260))

    round_turtle.pencolor("black")
    round_turtle.down()
    round_turtle.clear()
    round_turtle.write("Déchets ramassés : " + str(rounds), align='center', font=("Helvetica", 16))

def ui_load_skins(wn):
    """
    Récupère tous les noms de skins présents dans le dossier lil_trash et les ajoute à la liste
    :param wn: Turtle, objet dans lequel on charge les skins
    :return: List<String>, Liste contenant le nom du fichier pour chaque skin
    """
    skins = next(walk("lil_trash"), (None, None, []))[2]  # [] if no file

    # Pour chaque fichier skin (fichier GIF) on charge la Shape dans Turtle
    for skin in skins:
        wn.addshape("lil_trash\\" + skin)

    wn.addshape("bot.gif")

    wn.addshape("dr_doof.gif")

    wn.addshape("scooby_final.gif")

    wn.addshape("charging_station.gif")
    return skins


def ui_update_battery_level(battery_level, text_turtle, turtle):
    """

    :param battery_level:
    :param text_turtle:
    :param turtle: Turtle, Instance existante de la lib Turtle pour créer de nouveaux objets (Texte, Turtle, etc)
    :return:
    """
    draw_battery_picto(battery_level, turtle)

    ui_update_text(text_turtle, "Batterie : " + str(battery_level) + "%", style=('Helvetica', 18), position=(0, 230))


# Fonction ui_init_text() remplacée par ui_update_text

def ui_init_bot(grid_data, t):
    """
    Cette fonction définit la forme, la position, et la couleur du robot et le place dans 'ui_obj'
    :param t: Turtle, Instance existante de la lib Turtle pour créer de nouveaux objets (Texte, Turtle, etc)
    :param grid_data: Dictionnaire regroupant les caractéristiques du bot, des déchets et de la map
    :return: Aucun
    """
    m_bot = t.Turtle()
    m_bot.up()
    m_bot.color('green')
    m_bot.shape("bot.gif")
    # m_bot.speed(5)
    m_bot.setpos(grid_data["bot"]["x_pos"], grid_data["bot"]["y_pos"])
    m_bot.down()
    grid_data["bot"]["ui_obj"] = m_bot


def ui_display_trashes(grid_data, skins, t):
    """
    Cette fonction affiche les déchets et définit leurs attributs
    :param t: Turtle, Instance existante de la lib Turtle pour créer de nouveaux objets (Texte, Turtle, etc)
    :param grid_data: Dictionnaire regroupant les caractéristiques du bot, des déchets et de la map
    :param skins: Les différentes apparences possibles pour les déchets (choisies aléatoirement
    :return: Aucun
    """

    for i in range(len(grid_data["trash"])):

        # t.register_shape('example.gif')

        # setting the image as cursor
        # img_turtle.shape('example.gif')

        trash = grid_data["trash"][i]

        if trash["ui_obj"] is None:
            skin = choice(skins)
            t.tracer(False)
            m_trash = t.Turtle()
            m_trash.hideturtle()

            m_trash.color('blue')
            m_trash.shape("lil_trash\\" + skin)
            m_trash.speed("fastest")
            t.tracer(True)
            m_trash.up()
            m_trash.setpos(trash["x_pos"], trash["y_pos"])
            # m_trash.tilt(randint(-90, 90)) # CANNOT ROTATE CUSTOM SHAPE IN TURTLE NATIVELY..
            m_trash.showturtle()
            m_trash.down()

            grid_data["trash"][i]["ui_obj"] = m_trash


def ui_display_charging_station(grid_data, t):
    """
    Cette fonction affiche la station de chargement et définit ses attributs
    :param t: Turtle, Instance existante de la lib Turtle pour créer de nouveaux objets (Texte, Turtle, etc)
    :param grid_data: Dictionnaire regroupant les caractéristiques du bot, des déchets et de la map
    :return: Aucun
    """
    charger = grid_data['station']
    m_charger = t.Turtle()
    m_charger.color('blue')
    m_charger.shape("charging_station.gif")
    m_charger.speed("fastest")
    m_charger.up()
    m_charger.setpos(charger['x_pos'], charger['y_pos'])
    m_charger.down()
