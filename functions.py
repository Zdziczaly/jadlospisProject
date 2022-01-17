from classes import Ingredient, Meal, ShoppingList
import csv


def createIngredientsList(csv_filename, csv_delimiter):
    """
    This function is responsible for creating a list of Ingredients objects from a given csv file.

    :param csv_filename: 'Skladniki.csv'
    :param csv_delimiter: ';'
    :return: list of Ingredient items
    """
    ingredients_list = []
    with open(csv_filename, newline='') as csvfile:
        ingredientsCsv = csv.reader(csvfile, delimiter=csv_delimiter)
        for row in ingredientsCsv:
            if row[0] == "Skladnik":
                continue
            ingredients_list.append(Ingredient(row[0], int(row[1]), int(row[2]), int(row[3]), int(row[4])))
    return (ingredients_list)
