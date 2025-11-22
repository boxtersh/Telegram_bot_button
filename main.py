# Вариант 4 — RecipeSuggest (рецепты по продуктам)
import token_file as tk
import asyncio
import aiogram
from aiogram import filters, F, types


def token():
    return tk.token

def ingredients_dict():
    dict_ingredients = {0: 'хлеб', 1:'картофель', 2: 'капуста', 3:'морковь', 4:'свекла', 5:'лук',
                        6:'чеснок', 7:'томаты', 8:'огурцы',9: 'зелень (укроп, петрушка)',10: 'творог',
                        11: 'яйцо', 12: 'сыр', 13: 'молоко'}
    return dict_ingredients

def ingredients_str():
    str_ingredients = '\n'.join(f'- {ingredients_dict()[key]};' for key in ingredients_dict())
    return str_ingredients

bot = aiogram.Bot(token=token())
dp = aiogram.Dispatcher()

@dp.message(filters.Command('start'))
async def start(message: types.Message, command: filters.CommandObject):
    user_name = message.from_user.username
    if user_name is None:
        user_name = 'таинственный "Незнакомец"'
    keyboard = [
        [types.InlineKeyboardButton(text="Да", callback_data="yes")],
        [types.InlineKeyboardButton(text="Нет", callback_data="no")],
    ]

    await message.reply(f'Приветствую Вас {user_name} 👋 в чате рецептов легкого завтрака 🍲 🍝.\n\n'
                        f'Я помогу вам подобрать простой рецепт из списка 📑 ингредиентов которые есть у любого человека - в холодильнике или на кухне.\n\n'
                        f'Для начала введите команду в формате "/find (ингридиенты через пробел)"\n\n'
                        f'пример: /find яйцо сыр томат\n\n'
                        f'Помощь по командам, выведет список доступных команд:  /help\n\n'
                        f'Ингридиенты из которых помогу составить рецепт 🍆🧄🥔🍅:\n'
                        f'{ingredients_str()}\n\n'
                        f'Приступим, Да / Нет?',
                        reply_markup=types.InlineKeyboardMarkup(inline_keyboard=keyboard))


# Обработчик callback-запросов
@dp.callback_query(lambda butt: butt.data in ['yes', 'no'])
async def process_callback(callback_query: types.CallbackQuery):
    # Удаляем старую клавиатуру
    await callback_query.answer()

    if callback_query.data == 'yes':
        await callback_query.message.answer("Отлично! Давайте продолжим.")
        # Здесь можно добавить логику для случая "Да"
    elif callback_query.data == 'no':
        await callback_query.message.answer("Жаль. Может быть, позже?")
        # Здесь можно добавить логику для случая "Нет"





# @dp.message(filters.Command("pay"))
# async def pay_for_delivery(message: types.Message):
#     keyboard = [
#         [types.KeyboardButton(text="Оплата за наличные")],
#         [types.KeyboardButton(text="Оплата по карте")]
#     ]
#
#     await message.reply(
#         "Как вы хотите оплатить заказ?",
#         reply_markup=types.ReplyKeyboardMarkup(
#             keyboard=keyboard,
#             resize_keyboard=True,
#         )
#     )



















async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())




