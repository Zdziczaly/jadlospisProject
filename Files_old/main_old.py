from Files_old.functions_old import createIngredientsList
from Files_old.classes_old import Meal, ShoppingList


def main_function():
    full_ingredients_list = createIngredientsList('Skladniki.csv', ';')
    meal_x = Meal(full_ingredients_list, '2BFST_1.csv', ';')
    meal_y = Meal(full_ingredients_list, '2BFST_2.csv', ';')
    for item in full_ingredients_list:
        print(item)
    print(meal_x)
    print("Kalorie: " + str(meal_x.return_kcal()) + " kcal")
    shopping_list = ShoppingList()
    shopping_list.add_all_ingredients_to_list(meal_x)
    print(shopping_list)
    shopping_list.add_all_ingredients_to_list(meal_y)
    print(shopping_list)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main_function()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
