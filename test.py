import re


class Dish:
    def __init__(self, meal, dish_name, date, ingredients, instruction):
        """
        Initializes a new dish

        :param meal: what meal is it for (accepts: Breakfast, Shake, Dinner, Supper)
        :param dish_name: name of the dish
        :param date: when was it defined in our diet in DD.MM.YYYY format
        :param ingredients: list of ingredients in [("name", "quantity"), ...] format
        :param instruction: string containing preparation instruction
        """
        # Defines what meal is it based on original meal description and a date
        # if the date is xx.05 or xx.06, then I - Breakfast, II - Shake, III - Dinner, IV - Supper
        # if the date is xx.09 or xx.10, then I - Breakfast, II - Skip, III - Dinner, IV - Shake, V - Supper
        breakfast = "Breakfast"
        shake = "Shake"
        dinner = "Dinner"
        supper = "Supper"
        multiplier = 0
        if re.fullmatch(r'\d\d.0[56].\d{4}', date):
            if re.fullmatch(r'Posiłek I', meal):
                self.meal = breakfast
                multiplier = 1.5
            elif re.fullmatch(r'Posiłek II', meal):
                self.meal = shake
                multiplier = 1.5
            elif re.fullmatch(r'Posiłek III', meal):
                self.meal = dinner
                multiplier = 1.66
            elif re.fullmatch(r'Posiłek IV', meal):
                self.meal = supper
                multiplier = 1.5
            else:
                raise Exception("Meal not recognized")
        elif re.fullmatch(r'\d\d.09.\d{4}', date) or re.fullmatch(r'\d\d.09.\d{4}', date):
            if re.fullmatch(r'Posiłek I', meal):
                self.meal = breakfast
                multiplier = 3
            elif re.fullmatch(r'Posiłek II', meal):
                self.meal = "Second Breakfast"
                multiplier = 3
            elif re.fullmatch(r'Posiłek III', meal):
                self.meal = dinner
                multiplier = 2.5
            elif re.fullmatch(r'Posiłek IV', meal):
                self.meal = shake
                multiplier = 3
            elif re.fullmatch(r'Posiłek V', meal):
                self.meal = supper
                multiplier = 3
            else:
                raise Exception("Meal not recognized")
        else:
            raise Exception("date format not recognized - unable to create dish")

        self.name = dish_name.replace('\n', ' ')
        self.date = date
        self.ingredients_list = []
        for ingredient in ingredients:
            self.ingredients_list.append([ingredient[0], float(ingredient[1]) * multiplier])
        self.preparation_instruction = instruction

    def __str__(self):
        return """{meal} - {name}
        
Składniki:
{ingred}
        
Instrukcja:
{instruction}""".format(meal=self.meal, name=self.name, ingred=self.ingredients_list,
                        instruction=self.preparation_instruction)

    def ingredient_types(self):
        """
        Returns list of unique ingredients without adding their quantities

        :return: [ingredient1_name, ingredient2_name, ...]
        """
        return [item[0] for item in self.ingredients_list]


class CookBook:
    recipes = []

    def add_new_recipe(self, dish: Dish):
        for recipe in self.recipes:
            if dish.name == recipe.name and dish.meal == recipe.meal:
                return
        self.recipes.append(dish)

    def __str__(self):
        x = ""
        for recipe in self.recipes:
            x += recipe.name + '\n'
        return x


def splitlist_may(meal_list):
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


with open("IPZ 06.05-21.05.txt") as f:
    jadlospis_1 = f.read()
# TODO: add the rest of IPZ files
dish_list = splitlist_may(jadlospis_1)
# TODO: lish_list can be extended with splitlists of other IPZs
all_ingredients = []
book_of_recipes = CookBook()
for entry in dish_list:
    # print(entry)
    book_of_recipes.add_new_recipe(entry)
    all_ingredients.extend(entry.ingredient_types())  # TODO: this should use CookBook
print(set(all_ingredients))

# lista wszystkich sniadan
for entry in dish_list:
    print(entry.name)
print(len(dish_list))
print(book_of_recipes)
print(len(book_of_recipes.recipes))