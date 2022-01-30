import re
from classes import Dish


def splitlist(meal_list):
    """
    Returns list of meals.

    :param meal_list: string containing all of the PDF.
    :return: list of Dish objects
    """
    dishes_list = re.split(r'\d\d:\d\d.', meal_list)
    dishes_list = dishes_list[1:]  # remove first input in the list, which is not a meal
    splitted_list = []
    for dish in dishes_list:
        meal_nr = dish.partition('\n')[0]
        date = re.findall(r'(\d\d\.\d\d\.\d\d\d\d)', dish)[0]
        meal_name = re.findall(r'\d\d\.\d\d\.\d\d\d\d\n([\S\s]+)\nWARTO', dish)
        # meal_name = meal_name[0].replace('\n', ' ')
        ingredients_temp = re.findall(r'^(.+) - .+\(([0-9]+) g\)$', dish, re.MULTILINE)
        instruction = re.findall(r'SPOSÓB PRZYGOTOWANIA:\n([\s\S]+)$', dish)
        splitted_list.append(Dish(meal_nr, meal_name[0], date, ingredients_temp, instruction[0]))
    return splitted_list


def show_shopping_list(shopping_list):
    shopping_list_string = "LISTA ZAKUPÓW:\n"
    for entry in shopping_list:
        shopping_list_string += "{ingredient} - {mass}g\n".format(ingredient=entry[0], mass=entry[1])
    return shopping_list_string


def save_dish_to_file(dish: Dish):
    with open("Karty dań/{meal}/{name}.txt".format(meal=dish.meal, name=dish.name), 'w', encoding='utf8') as f:
        f.write(str(dish))


def prepare_dish_list():
    with open("IPZ 06.05-21.05.txt") as f:
        jadlospis_1 = f.read()
    with open("IPZ 22.05-05.06.txt") as f:
        jadlospis_2 = f.read()
    with open("IPZ 30.09-15.10.txt") as f:
        jadlospis_3 = f.read()
    with open("IPZ 16.10-30.10.txt") as f:
        jadlospis_4 = f.read()
    dish_list = splitlist(jadlospis_1)
    dish_list.extend(splitlist(jadlospis_2))
    dish_list.extend(splitlist(jadlospis_3))
    dish_list.extend(splitlist(jadlospis_4))
    return dish_list
