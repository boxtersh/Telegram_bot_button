# Домашние задания по Telegram‑ботам №1
# Вариант 4 — RecipeSuggest (рецепты по продуктам)
import token_file as tk
import asyncio
import aiogram
from aiogram import filters, F, types
from aiogram.filters import Command, CommandObject


def token():
    return tk.token


bot = aiogram.Bot(token=token())
dp = aiogram.Dispatcher()


@dp.message(filters.Command('start'))
async def start(message: types.Message):
    user_name = message.from_user.username
    if user_name is None:
        user_name = 'таинственный "Незнакомец"'
    keyboard = [
        [types.InlineKeyboardButton(text="Да", callback_data="yes"),
         types.InlineKeyboardButton(text="Нет", callback_data="no")]
    ]

    await message.reply(f'Приветствую Вас {user_name} 👋 в чате рецептов легкого завтрака 🍲 🍝.\n\n'
                        f'Я помогу вам подобрать простой рецепт из списка 📑 ингредиентов которые есть у любого '
                        f'человека - в холодильнике или на кухне.\n\n'
                        f'Для начала введите команду в формате:\n/find (ингредиенты через пробел)\n'
                        f'пример:\n/find яйцо сыр томат\n\n'
                        f'/help - Помощь по командам. Выводит список доступных команд с описанием\n\n'
                        f'Приступим, Да / Нет?',
                        reply_markup=types.InlineKeyboardMarkup(inline_keyboard=keyboard))


@dp.message(filters.Command('product'))
async def start(message: types.Message):
    await message.reply(f'Ингредиенты 🍆🧄🥔🍅 из которых помогу составить рецепт:\n'
                        f'{ingredients_str()}\n\n')


@dp.message(filters.Command('help'))
async def start(message: types.Message):
    await message.reply(f'Список моих доступных команд:\n'
                        f'/start - приветствие, с описанием чат бота;\n'
                        f'/help - список доступных команд;\n'
                        f'/product - перечень продуктов из которых могу предложить рецепт;\n'
                        f'/find - поиск рецепта по указанным ингредиентам\nнапример:\n/find яйцо хлеб\n'
                        f'/popular - наборы популярных ингредиентов, с последующим выводом рецептов;\n'
                        f'/quick - выбор отображения "Быстрый рецепт" или "Подробный"')


@dp.callback_query(lambda butt: butt.data in ['yes', 'no'])
async def process_callback(callback_query: types.CallbackQuery):
    await callback_query.answer()

    if callback_query.data == 'yes':
        await callback_query.message.answer(f'Отлично! Давайте продолжим.\n\n'
                                            f'Ожидаю от вас команду 👇')
    elif callback_query.data == 'no':
        await callback_query.message.answer(f'Жаль😟\nВозможно позже вы воспользуетесь моими услугами😉\n'
                                            f'Всего наилучшего!👋')


@dp.message(filters.Command('find'))
async def start(message: types.Message, command: filters.CommandObject):
    reply_text = None
    if command.args is None:
        reply_text = (f'Вы ввели команду без ингредиентов❗\nВ данном случае невозможно создать рецепт,'
                            f' но вам, я так и быть помогу.\nМожно попробовать приготовить классический завтрак\n'
                            f'вот несколько рецептов:\n\n'
                            f'{food_recipes()[1]}\n\nХорошего дня☺️')

    elif len(validity(command.args)) == len(command.args.split()):
        reply_text = (f'Таких ингредиентов: {', '.join(validity(command.args))} - нет в моём списке❗\n'
                      f'Извините, я не смогу вам помочь 😟')

    elif validity(command.args):
        res = coincidence(command.args)
        reply_text = (
            f'Таких ингредиентов: {', '.join(validity(command.args))} - нет в моём списке❗ Но я могу составить рецепт из:\n'
            f'{', '.join(res)}\nвот ваш рецепт:\n'
            f'{'\n'.join(food_recipes()[key] for key in res)}')

    elif not validity(command.args):
        reply_text = (f'Все указанное вами есть в моём списке!\n'
                      f'вот ваш рецепт:\n'
                      f'{'\n'.join(food_recipes()[key] for key in command.args.split())}')

    await message.reply(reply_text)


@dp.message(filters.Command('popular'))
async def pay_for_delivery(message: types.Message):
    keyboard = [
        [types.KeyboardButton(text='хлеб бекон яйцо')],
        [types.KeyboardButton(text='творог сметана хлеб сыр')],
        [types.KeyboardButton(text='бекон яйцо томаты огурцы зелень')],
        [types.KeyboardButton(text='бекон картофель лук томаты огурцы хлеб')]
    ]

    await message.reply(
        "Выберете рецепт из стандартного набора",
        reply_markup=types.ReplyKeyboardMarkup(
            keyboard=keyboard,
            resize_keyboard=True,
        )
    )


def list_commands():
    dict_commands = {'хлеб бекон яйцо': 50, 'творог сметана хлеб сыр': 51, 'бекон яйцо томаты огурцы зелень': 52,
                     'бекон картофель лук томаты огурцы хлеб': 53}
    return dict_commands


@dp.message(F.text.in_(list_commands().keys()))
async def pay_for_delivery_with_card(message: types.Message):
    text = message.text
    if text in list_commands().keys():
        id_recipes = list_commands()[text]
        recipes = food_recipes()[id_recipes]
        comment = None
        if message.text == 'хлеб бекон яйцо':
            comment = 'Хороший выбор👍'
        elif message.text == 'творог сметана хлеб сыр':
            comment = 'Лёгкий завтрак🍨'
        elif message.text == 'бекон яйцо томаты огурцы зелень':
            comment = 'Прекрасный выбор🍳'
        elif message.text == 'бекон картофель лук томаты огурцы хлеб':
            comment = 'Сытный завтрак🍝'
        await message.reply(
            f'{comment}\nваш рецепт:\n{recipes}\n\nХорошего дня☺️',
            reply_markup=types.ReplyKeyboardRemove())
    else:
        await message.reply(f'Неверная команда')


@dp.message(F.text)
async def pay_for_delivery_with_card(message: types.Message):
    await message.reply(f'Вы ввели команду:\n__*{message.text}*__\nданная команда мне не известна⁉️ 🤔\n\n'
                        f'попробуйте ещё раз ✍️, у вас обязательно получится 👇', parse_mode="MarkdownV2")


def ingredients_dict():
    dict_ingredients = {0: 'хлеб', 1: 'картофель', 2: 'чеснок', 3: 'морковь', 4: 'бекон', 5: 'лук',
                        6: 'томаты', 7: 'огурцы', 8: 'зелень', 9: 'творог',
                        10: 'яйцо', 11: 'сыр', 12: 'сметана', 13: 'молоко'}
    return dict_ingredients


def ingredients_str():
    str_ingredients = '\n'.join(f'- {ingredients_dict()[key]};' for key in ingredients_dict())
    return str_ingredients


def validity(attribute):
    get_dict = set(ingredients_dict().values())
    result = set(attribute.split()) - get_dict
    return result


def coincidence(attribute):
    result = set(attribute.split()) & set(ingredients_dict().values())
    return result


# 5️⃣ 6️⃣
def food_recipes():
    dict_food_recipes = {
        1: '1️⃣ Омлет с сыром, бутерброд с кофе или чаем;\n'
           '2️⃣ Жареные помидоры с яйцом и беконом, кекс с кусочком сыра и какао\n'
           '3️⃣ Творог с сахаром, сметаной и изюмом, кофе или чай с печеньем\n'
           '4️⃣ Коктейль из овсяного молока, банана, творога, сырого яйца, с щепоткой ванили, меда или варенья по вкусу\n',
        'хлеб': '1️⃣ Жареные хлебцы в масле;\n'
                '2️⃣ Хлеб жареный в яйцах;\n'
                '3️⃣ Бутерброд с беконом и зеленью.\n',
        'яйцо':'1️⃣ Яичница с зеленью и соусом;\n'
               '2️⃣ Яйцо пашот с майонезом и зеленью;\n'
               '3️⃣ Яйцо вареное с беконом и хлебом.\n',
        50: '1️⃣ Жареные тосты из хлеба с беконом, варёное яйцо, чай или кофе',
        51: '1️⃣ Творог со сметаной и сахаром, хлеб с сыром, чай или кофе',
        52: '1️⃣ Жареные яйца с беконом и томатами, салат с огурцами и зеленью, чай или кофе',
        53: '1️⃣ Жареный картофель с луком и беконом, салат с огурцами, томатами и луком, чай или кофе'

    }
    return dict_food_recipes


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
