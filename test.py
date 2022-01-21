import re


def splitlist_may(meal_list):
    """
    Returns list of meals.

    :param meal_list: string containing all of the PDF.
    :return: list of dictionaries (meal nr, date, meal name, ingredients, instruction)
    """
    dishes_list = re.split(r'\d\d:\d\d.', meal_list)
    dishes_list = dishes_list[1:]  # remove first input in the list, which is not a meal
    splitted_list = []
    for dish in dishes_list:
        meal_nr = dish.partition('\n')[0]
        date = re.findall(r'(\d\d\.\d\d\.\d\d\d\d)', dish)[0]
        meal_name = re.findall(r'\d\d\.\d\d\.\d\d\d\d\n([\S\s]+)\nWARTO', dish)
        meal_name = meal_name[0].replace('\n', ' ')
        ingredients_temp = re.findall(r'^(.+) - .+\(([0-9]+) g\)$', dish, re.MULTILINE)
        ingredients = []
        for position in ingredients_temp:
            ingredients.append([position[0], float(position[1])])
        instruction = re.findall(r'SPOSÓB PRZYGOTOWANIA:\n([\s\S]+)$', dish)
        splitted_list.append({'meal_nr': meal_nr, 'date': date, 'meal_name': meal_name,
                              'ingredients': ingredients, 'instruction': instruction})
    return splitted_list


jadlospis = """Indywidualny plan żywieniowy
(06.05.2021 - 21.05.2021)
Bartłomiej Nazarko
Bartłomiej Nazarko - Indywidualny plan żywieniowy (06.05.2021 - 21.05.2021)
www.fabrykasily.pl 1
06:30 Posiłek I
czwartek, 06.05.2021
Owsianka z bananem,
żurawiną i migdałami
WARTOŚCI
ODŻYWCZE:
Energia: 575 kcal
Białko: 22 g
Tłuszcz: 19 g
Węglowodany: 79 g
SKŁADNIKI:
Płatki owsiane - 5 łyżek (50 g)
Migdały - 2,5 łyżeczki (18 g)
Banan - 1 średnia sztuka (160 g)
Jogurt naturalny 2% - 1 szklanka (240 g)
Żurawina suszona - 1 łyżka (10 g)
SPOSÓB PRZYGOTOWANIA:
1. Płatki owsiane zalej niewielką ilością wrzątku, tuż
nad poziom płatków.
2. Odstaw na 2-5 minut do napęcznienia.
3. Dodaj jogurt, banana pokrojonego w plastry oraz
żurawinę.
4. Udekoruj owsiankę posiekanymi migdałami.
11:15 Posiłek II
czwartek, 06.05.2021
Kanapka z pastą jajeczną z
koperkiem i sok
pomidorowy
WARTOŚCI
ODŻYWCZE:
Energia: 411 kcal
Białko: 21 g
Tłuszcz: 9 g
Węglowodany: 56 g
SKŁADNIKI:
Bułka graham - 1,25 sztuki (95 g)
Jaja - 1 duże (65 g)
Koper ogrodowy - 0,25 pęczka (6 g)
Jogurt naturalny 2% - 0,5 łyżki (12 g)
Sok pomidorowy - 1 szklanka (240 g)
SPOSÓB PRZYGOTOWANIA:
1. Pokrój pieczywo i przygotuj pastę.
2. Ugotowane na twardo jajka wymieszaj z jogurtem i
posiekanym koperkiem i rozgnieć widelcem, aby
uzyskać konsystencję pasty. Dopraw do smaku.
3. Posmaruj pieczywo pastą i podawaj ze szklanką soku
pomidorowego.
15:45 Posiłek III
czwartek, 06.05.2021
Pieczone udko z kurczaka,
ziemniaki, mizeria
WARTOŚCI
ODŻYWCZE:
Energia: 821 kcal
Białko: 60 g
Tłuszcz: 39 g
Węglowodany: 49 g
SKŁADNIKI:
Udko z kurczaka bez skóry i kości - 1,75 porcji (250 g)
Ziemniaki - 4 średnie sztuki (375 g)
Ogórek - 0,75 sztuki (160 g)
Jogurt naturalny 2% - 2 łyżki (45 g)
Szczypiorek - 1,5 łyżki (8 g)
Papryka czerwona (w proszku) - 2 szczypty (1 g)
Oliwa z oliwek - 2,5 łyżki (25 g)
SPOSÓB PRZYGOTOWANIA:
1. Udko natrzyj ulubionymi przyprawami (np. czosnek
w proszku, sól, pieprz, zioła prowansalskie, papryka
słodka).
2. Ziemniaki obierz, pokrój w kostkę i ugotuj.
3. Umieść mięso w naczyniu żaroodpornym, skrop
oliwą i piecz w temperaturze 180 stopni przez około
40-50 minut (do miękkości mięsa).
4. Z ogórka, szczypiorku, jogurtu i przypraw przygotuj
mizerię.
5. Podawaj mięso z ziemniakami i mizerią.
20:30 Posiłek IV
czwartek, 06.05.2021
Kanapka z masłem
orzechowym, bananem i
dżemem
WARTOŚCI
ODŻYWCZE:
Energia: 493 kcal
Białko: 17 g
Tłuszcz: 20 g
Węglowodany: 61 g
SKŁADNIKI:
Bułka graham - 1 sztuka (80 g)
Masło orzechowe - 1,5 łyżki (30 g)
Banan - 1 mała sztuka (90 g)
Dżem wiśniowy niskosłodzony - 1,5 łyżeczki (18 g)
SPOSÓB PRZYGOTOWANIA:
1. Pokrój pieczywo i posmaruj masłem orzechowym.
2. Na pieczywie ułóż plastry banana.
3. Na koniec całość posmaruj dżemem.
Bartłomiej Nazarko - Indywidualny plan żywieniowy (06.05.2021 - 21.05.2021)
www.fabrykasily.pl 2
06:30 Posiłek I
piątek, 07.05.2021
Owsianka z bananem,
żurawiną i migdałami
WARTOŚCI
ODŻYWCZE:
Energia: 575 kcal
Białko: 22 g
Tłuszcz: 19 g
Węglowodany: 79 g
SKŁADNIKI:
Płatki owsiane - 5 łyżek (50 g)
Migdały - 2,5 łyżeczki (18 g)
Banan - 1 średnia sztuka (160 g)
Jogurt naturalny 2% - 1 szklanka (240 g)
Żurawina suszona - 1 łyżka (10 g)
SPOSÓB PRZYGOTOWANIA:
1. Płatki owsiane zalej niewielką ilością wrzątku, tuż
nad poziom płatków.
2. Odstaw na 2-5 minut do napęcznienia.
3. Dodaj jogurt, banana pokrojonego w plastry oraz
żurawinę.
4. Udekoruj owsiankę posiekanymi migdałami.
11:15 Posiłek II
piątek, 07.05.2021
Kanapka z pastą jajeczną z
koperkiem i sok
pomidorowy
WARTOŚCI
ODŻYWCZE:
Energia: 411 kcal
Białko: 21 g
Tłuszcz: 9 g
Węglowodany: 56 g
SKŁADNIKI:
Bułka graham - 1,25 sztuki (95 g)
Jaja - 1 duże (65 g)
Koper ogrodowy - 0,25 pęczka (6 g)
Jogurt naturalny 2% - 0,5 łyżki (12 g)
Sok pomidorowy - 1 szklanka (240 g)
SPOSÓB PRZYGOTOWANIA:
1. Pokrój pieczywo i przygotuj pastę.
2. Ugotowane na twardo jajka wymieszaj z jogurtem i
posiekanym koperkiem i rozgnieć widelcem, aby
uzyskać konsystencję pasty. Dopraw do smaku.
3. Posmaruj pieczywo pastą i podawaj ze szklanką soku
pomidorowego.
15:45 Posiłek III
piątek, 07.05.2021
Pieczone udko z kurczaka,
ziemniaki, mizeria
WARTOŚCI
ODŻYWCZE:
Energia: 821 kcal
Białko: 60 g
Tłuszcz: 39 g
Węglowodany: 49 g
SKŁADNIKI:
Udko z kurczaka bez skóry i kości - 1,75 porcji (250 g)
Ziemniaki - 4 średnie sztuki (375 g)
Ogórek - 0,75 sztuki (160 g)
Jogurt naturalny 2% - 2 łyżki (45 g)
Szczypiorek - 1,5 łyżki (8 g)
Papryka czerwona (w proszku) - 2 szczypty (1 g)
Oliwa z oliwek - 2,5 łyżki (25 g)
SPOSÓB PRZYGOTOWANIA:
1. Udko natrzyj ulubionymi przyprawami (np. czosnek
w proszku, sól, pieprz, zioła prowansalskie, papryka
słodka).
2. Ziemniaki obierz, pokrój w kostkę i ugotuj.
3. Umieść mięso w naczyniu żaroodpornym, skrop
oliwą i piecz w temperaturze 180 stopni przez około
40-50 minut (do miękkości mięsa).
4. Z ogórka, szczypiorku, jogurtu i przypraw przygotuj
mizerię.
5. Podawaj mięso z ziemniakami i mizerią."""
#lista = re.split(r'\d\d:\d\d.', jadlospis)

dish_list = splitlist_may(jadlospis)
ingredients_list = []
for dish in dish_list:
    for item in dish['ingredients']:
        ingredients_list.append(item[0])
print(len(ingredients_list))
print(ingredients_list)
print(list(set(ingredients_list)))
print(len(list(set(ingredients_list))))


#print(lista[1])
#x = re.split(r'SKŁADNIKI:|WARTOŚCI\nODŻYWCZE:', lista[2])
#print(x)
#print(len(x))
#x = x[1:]
#energy = float(str(re.findall(r'Energia:.(\d+).*', x[0])[0]))

# Lista skladnikow z masami skonwertowanymi na float do latwiejszej obrobki
# zwroc liste tupli ('skladnik', 'masa')
#skladniki_temp = re.findall(r'(.+) -.+\((\d+) g\)', x[1])
# konwertuj masy na float (wymaga nowej zmiennej, bo tuple sa niezmienne)
#skladniki = []
#for i in skladniki_temp:
#    skladniki.append((i[0], float(i[1])))

# DEBUG
#print(skladniki)
#print(energy*2)
#print(x[0])
#print(len(x))
