from data import MENU, resources
from time import sleep

READY = False
CASH = 0
END_MACHINE = False
QUESTION = ""
resources['money'] = 0


# функция по проверке инпута:

#  функция, проверяющая хватает ли ресурсов на изготовление кофе
def check_resources(coffee):
    global MENU, resources, READY
    local_coffee = MENU[coffee]
    not_enough = 0
    for key in local_coffee['ingredients']:
        if int(local_coffee['ingredients'][key]) > int(resources[key]):
            not_enough += 1
            print(f"В машине не хватает ингридиента: {key.capitalize()}")
    if not_enough > 0:
        READY = False
    else:
        READY = True
    return READY

# функция по вычету ресурсов
def minus_resources(coffee):
    global MENU, resources, READY
    local_coffee = MENU[coffee]['ingredients']
    for key in local_coffee:
        resources[key] -= local_coffee[key]

# функция по внесению денег
def insert_cash():
    five_hundred = int(input("Сколько бумажек по 500 ₽? "))
    one_hundred = int(input("Сколько бумажек по 100 ₽? "))
    fifty_rub = int(input("Сколько бумажек по 50 ₽? "))
    sum = five_hundred * 500 + one_hundred * 100 + fifty_rub * 50
    print(f"Было внесено {sum} ₽")
    return sum


# функция по проверке необходимых внесенных средств
def check_money(money, coffee):
    global MENU, resources
    local_price = MENU[coffee]['cost']
    if local_price > resources['money']:
        print(f"Нужно больше денег. {resources['money']}₽ возвращены")
        resources['money'] = 0
    else:
        money -= local_price
        resources['money'] -= local_price
    return money


# функция кофе машины
def coffe_machine():
    global QUESTION, resources, CASH, END_MACHINE, MENU
    #          Если ресурсов хватает, то прошу внести деньги
    #          Вносятся 50 или 100 или 500
    CASH = insert_cash()

    #          Проверка хватает ли денег
    #          Если денег не хватает - вывести сообщение "Нужно больше денег, деньги возвращены"
    #          Если денег хватает, то цена на кофе вычитается из суммы денег, а сумма добавляется в
    #          Переменную report. Сдача должна выдаваться

    if CASH < MENU[QUESTION]['cost']:
        print(f"Нужно больше денег. {CASH} ₽ возвращены")
        resources['money'] -= CASH
    else:
        print(f"Твоя сдача: {CASH-MENU[QUESTION]['cost']} ₽")
        resources['money'] += MENU[QUESTION]['cost']

        #          Сделать кофе.
        #          Если денег хватает и ресурсы на месте, тогда ресурсы вычитаются из переменной report
        #          После вычитания ресурсов,выдать сообщение "Ваш кофе, сэр!"
        minus_resources(QUESTION)
        print(f"Ваш {QUESTION} готов ☕")


# основная часть программы
print("Вас приветствует кофемашина Фугарова. Мы предлагаем три вида напитков: эспрессо, латте и капучино.")
sleep(2)

while not END_MACHINE:
    #       Ask user "What would you like?" (espresso/latte/cappuccino)
    #       a. Check the user’s input to decide what to do next.
    #       b. The prompt should show every time action has completed, e.g. once the drink is
    #       dispensed. The prompt should show again to serve the next customer.
    QUESTION = input("Чего желаете, мусье? Эспрессо, латте или капучино? "
                     "Посмотреть ресурсы: 'инфо'. Выключить девайс: 'выкл' ").lower()

    #           Turn off the Coffee Machine by entering “off” to the prompt.
    #           a. For maintainers of the coffee machine, they can use “off” as
    #           the secret word to turn off the machine. Your code should end execution when this happens.
    if QUESTION == 'выкл':
        END_MACHINE = True

    # Print report if question is report

    elif QUESTION == 'инфо':
        print("Сейчас в автомате:")
        for key in resources:
            print(f"{key.capitalize()}: {resources[key]}")

    #          Проверить количество оставшихся ресурсов
    #          когда выбираешь напиток, машина проверяет, хватает ли ресурсов
    #          Если не хватает ресурса - вывести сообщение "Не хватает ресурсов"
    elif QUESTION == 'эспрессо' or QUESTION == 'капучино' or QUESTION == 'латте':
        READY = check_resources(QUESTION)
        if READY:
            print(f"Стоимость {QUESTION}: {MENU[QUESTION]['cost']} ₽")
            coffe_machine()
    else:
        print("Такая команда отсутствует, пожалуйста, выберите из доступного")