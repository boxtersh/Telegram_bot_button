# Домашние задания по Telegram‑ботам №1
# Вариант 4 — RecipeSuggest (рецепты по продуктам)
import token_file as tk
import asyncio
import aiogram
from aiogram import filters, F, types
from aiogram.filters.command import Command, CommandObject


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
    if command.args is None:
        await message.reply(f'Вы ввели команду без ингредиентов❗\nВ данном случае невозможно создать рецепт,'
                            f' но вам, я так и быть помогу.\nМожно попробовать приготовить классический завтрак:\n\n'
                            f'{food_recipes()[1]}')
        return

    option = validity(command.args)
    if len(option) == len(command.args.split()):
        await message.reply(f'Таких ингредиентов: {', '.join(option)} - нет в моём списке❗')

    elif option:
        res = coincidence(command.args)
        await message.reply(
            f'Таких ингредиентов: {', '.join(option)} - нет в моём списке❗ но я могу составить рецепт из:\n'
            f'{', '.join(res)}\nвот ваш рецепт:\n'
            f'тут я указываю рецепт для частичного совпадений')
    else:
        await message.reply(f'здесь я должен написать рецепт для полного совпадения')

    # Здесь начинается проблема: и так далее конструкция из if, elif, else для всевозможных вариантов запроса от
    # пользователя по command.args, а их ооооочень много!


@dp.message(F.text)
async def no_name_command(message: types.Message):
    await message.reply(f'Вы ввели команду:\n__*{message.text}*__\nданная команда мне не известна⁉️ 🤔\n\n'
                        f'попробуйте ещё раз 👐, у вас обязательно получится 👇', parse_mode="MarkdownV2")


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


def food_recipes():
    dict_food_recipes = {
        1: '1️⃣ Омлет с сыром, бутерброд с кофе или чаем;\n'
           '2️⃣ Жареные помидоры с яйцом и беконом, бутерброд с кофе или чаем\n'
           '3️⃣ Творог с сахаром и изюмом, кофе или чай с печеньем'
    }
    return dict_food_recipes


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())