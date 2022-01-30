from functions import splitlist
from classes import CookBook, MealPlan


def main():
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

    book_of_recipes = CookBook()
    for entry in dish_list:
        book_of_recipes.add_new_recipe(entry)
    print("Długość listy przepisów: {cookbooklen}".format(cookbooklen=len(book_of_recipes.recipes)))
    print("liczba skladnikow: {}".format(len(book_of_recipes.ingredient_types())))
    print(book_of_recipes.ingredient_types())

    # test wczytywania jadlospisu
    meal_plan = MealPlan("test_meal_plan.txt")
    print(meal_plan)
    print(len(meal_plan.menu_table_str))
    meal_plan.create_menu_with_objects(book_of_recipes)
    print(len(meal_plan.menu_table_obj))
    print(meal_plan.return_shopping_list())  # test listy zakupów

    # lista wszystkich sniadan
    # for entry in dish_list:
    #     print(entry.name)
    # print(len(dish_list))
    # print(book_of_recipes)
    # print(len(book_of_recipes.recipes))


if __name__ == "__main__":
    main()
