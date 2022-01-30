from functions import *
from classes import CookBook, MealPlan
import logging


def main():
    # scrap files to prepare full dish list
    dish_list = prepare_dish_list()

    # create set of unique recipes
    book_of_recipes = CookBook()
    for entry in dish_list:
        book_of_recipes.add_new_recipe(entry)

    # Logging information:
    logging.info("Długość listy przepisów: {cookbooklen}".format(cookbooklen=len(book_of_recipes.recipes)))
    logging.info("liczba skladnikow: {}".format(len(book_of_recipes.ingredient_types())))
    logging.info(book_of_recipes.ingredient_types())

    # save all recipes to files
    for item in book_of_recipes.recipes:
        save_dish_to_file(item)

    # test wczytywania jadlospisu
    meal_plan = MealPlan("test_meal_plan.txt")
    # print(meal_plan)
    meal_plan.create_menu_with_objects(book_of_recipes)
    print(show_shopping_list(meal_plan.return_shopping_list()))  # test listy zakupów

    # lista wszystkich sniadan
    # for entry in dish_list:
    #     print(entry.name)
    # print(len(dish_list))
    # print(book_of_recipes)
    # print(len(book_of_recipes.recipes))


if __name__ == "__main__":
    main()
