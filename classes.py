import csv


class Ingredient:
    def __init__(self, name, kcal, proteins, carbs, fats):
        """
        Class containing ingredients used to create a meal.

        :param name: name of the ingredient
        :param kcal: calories per 100g [kcal]
        :param proteins: proteins per 100g [g]
        :param carbs: hydrocarbons per 100g [g]
        :param fats: fats per 100g [g]
        """
        self.name = name
        self.kcal_per_100g = float(kcal)
        self.proteins_per_100g = float(proteins)
        self.carbs_per_100g = float(carbs)
        self.fats_per_100g = float(fats)

    def __str__(self):
        return("{}: \t{}kcal/100g, \tproteins - {}g, \tcarbs - {}g, \tfats - {}g".format(self.name, self.kcal_per_100g,
               self.proteins_per_100g, self.carbs_per_100g, self.fats_per_100g))


class Meal:
    def __init__(self, all_ingredients_list, meal_csv, csv_delimiter):
        """
        On initialization create list of ingredients in a meal

        :param all_ingredients_list: [Ingredient, Ingredient...]
        """
        self.ingredients = []
        with open(meal_csv, newline='') as csvfile:
            i = 1
            meal_file = csv.reader(csvfile, delimiter=csv_delimiter)
            for row in meal_file:
                if i == 1 or i == 3:
                    i = i+1
                elif i == 2:
                    self.meal_id = row[1]
                    i = i+1
                else:
                    for ingredient in all_ingredients_list:
                        if ingredient.name == row[0]:
                            self.ingredients.append({'ingredient': ingredient,
                                                     'quantity': float(row[1])})
                            break

    def __str__(self):
        ingredient_string = self.meal_id + "\n"
        for ingredient in self.ingredients:
            ingredient_string = ingredient_string + ('{} - {}g\n'.format(ingredient['ingredient'].name,
                                                                         ingredient['quantity']))
        return ingredient_string

    def return_kcal(self):
        """Function returns sum of kcal for given list of ingredients"""
        kcal = 0
        for item in self.ingredients:
            kcal = kcal + item['ingredient'].kcal_per_100g * item['quantity']/100
        return kcal


class ShoppingList:
    shopping_list = []

    def add_to_list(self, ingredient: Ingredient, quantity: float):
        for item in self.shopping_list:
            if ingredient.name == item['ingredient'].name:
                item['quantity'] = item['quantity']+quantity
                return
        self.shopping_list.append({'ingredient': ingredient,
                                   'quantity': quantity})

    def add_all_ingredients_to_list(self, meal: Meal):
        for item in meal.ingredients:
            self.add_to_list(item['ingredient'], item['quantity'])

    def __str__(self):
        shopping_list_string = 'LISTA ZAKUPOW\n-------------\n'
        for line in self.shopping_list:
            shopping_list_string = shopping_list_string + ('{} - {}g\n'.format(line['ingredient'].name,
                                                                               line['quantity']))
        return shopping_list_string
