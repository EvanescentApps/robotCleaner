# Module regroupant les fonctions utiles et indépendantes

def distance_manhattan(x1, y1, x2, y2):
    """
    Détermine la distance de Manhattan entre deux éléments
    :param x1 : Abscisse de l'élément 1
    :param y1 : Ordonnée de l'élément 1
    :param x2 : Abscisse de l'élément 2
    :param y2 : Ordonnée de l'élément 2
    :return : Un entier, distance de Manhattan entre les deux éléments
    """
    return abs(x1 - x2) + abs(y1 - y2)


def distance_axis(x1, y1, x2, y2):
    """
        Détermine la distance effective parcourue par le robot entre deux éléments (axe par axe)
        :param x1 : Abscisse de l'élément 1
        :param y1 : Ordonnée de l'élément 1
        :param x2 : Abscisse de l'élément 2
        :param y2 : Ordonnée de l'élément 2
        :return : Un entier, distance parcourue entre les deux éléments
        """
    return abs(x1 - x2), abs(y1 - y2)


def is_coord_valid(x, y, x_max, y_max, x_min, y_min):
    """
    Vérifie si la coordonnée est située dans la grille
    :param x : abscisse
    :param y : ordonnée
    :param x_max : limite haute de l'abscisse
    :param y_max : limite haute de l'ordonnée
    :param x_min : limite basse de l'abscisse
    :param y_min : limite basse de l'ordonnée
    :return : Boolean, si la coordonnée est valide ou non
    """
    if x_min <= x <= x_max and y_min <= y <= y_max:
        return True
    else:
        return False


def ratio_to_percent(num, denom):
    """
    Cette fonction retourne un pourcentage à partir d'une fraction
    :param num : Numérateur de la fraction
    :param denom : Dénominateur de la fraction (maximum)
    :return: Int, pourcentage
    """

    return int((num / denom) * 100)
