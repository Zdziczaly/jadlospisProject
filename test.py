import re
import logging


logging.getLogger().setLevel(logging.INFO)

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
        elif re.fullmatch(r'\d\d.09.\d{4}', date) or re.fullmatch(r'\d\d.10.\d{4}', date):
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
            self.ingredients_list.append([ingredient[0], round(float(ingredient[1]) * multiplier)])
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
                logging.info("LOG: Przepis {name} juz wystepuje na liscie przepisow".format(name=dish.name))
                return
        self.recipes.append(dish)
        logging.info("LOG: Dodano przepis - {name} ({date})".format(name=dish.name, date=dish.date))

    def __str__(self):
        x = ""
        for recipe in self.recipes:
            x += recipe.name + '\n'
        return x


class MealPlan:
    def __init__(self, path_to_menu):
        with open(path_to_menu) as file:
            menu_content = file.read()
        self.menu_table_str = re.split(r'[\t\n]', menu_content)
        self.menu_table_obj = []
        logging.info("LOG: Jadlospis zaimportowany w formie tekstowej - dodano {count} przepisow.".format(
            count=len(self.menu_table_str)))

    def __str__(self):
        return str(self.menu_table_str)

    def create_menu_with_objects(self, cookbook: CookBook):
        for entry in self.menu_table_str:
            for recipe in cookbook.recipes:
                if recipe.name == entry:
                    self.menu_table_obj.append(recipe)
                    break
        logging.info("LOG: Jadlospis stworzony w formie obiektowej - dodano {count} przepisow".format(
            count=len(self.menu_table_obj)))
        if len(self.menu_table_str) - len(self.menu_table_obj) > 0:
            logging.info(
                "LOG: {count} przepisow nie moglo zostac zaimportowanych - sprawdz poprawnosc nazw w pliku jadlospisu".format(
                    count=len(self.menu_table_str) - len(self.menu_table_obj)))

    def return_shopping_list(self):
        shopping_list_temp = []
        shopping_list = []
        # create list by adding together content of all ingredients lists of all Dish objects
        for entry in self.menu_table_obj:
            shopping_list_temp.extend(entry.ingredients_list)
        # TODO: make it so that the list contains only unique entries, and identical ingredients are summed
        for entry in shopping_list_temp:
            entry_added_flag = False
            if len(shopping_list) == 0:
                shopping_list.append(entry)
            else:
                # check if shopping list contains the ingredient, and if it does - add the weight and go to the next entry
                for position in shopping_list:
                    if entry[0] == position[0]:
                        position[1] += entry[
                            1]  # TODO: TO GOWNO NIE DZIALA POPRAWNIE przez PASS-BY-REFERENCE! Możesz sprawdzić zwracajac shopping_list_temp
                        entry_added_flag = True
                        break
                # if the shopping list does not contain the ingredient, add it to the list
                if not entry_added_flag:
                    shopping_list.append(entry)
        return shopping_list


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

    all_ingredients = []
    book_of_recipes = CookBook()
    for entry in dish_list:
        # print(entry)
        book_of_recipes.add_new_recipe(entry)
        all_ingredients.extend(entry.ingredient_types())  # TODO: this should use CookBook
    print("Długość listy przepisów: {cookbooklen}".format(cookbooklen=len(book_of_recipes.recipes)))
    print(set(all_ingredients))

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
