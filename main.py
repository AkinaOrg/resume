# Импортируем библиотеку aiogram
from aiogram import Bot, Dispatcher, executor, types

# Создаем объекты бота и диспетчера
bot = Bot(token="6349133623:AAG4wQ6iqdgYdm9jzpA6xQTOZHzPH7xWGgA")
dp = Dispatcher(bot)

# Создаем клавиатуру с кнопками для ввода чисел и операций
keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.add("1", "2",)
keyboard.add("3", "4",)
keyboard.add("5", "6",)
keyboard.add("7", "8",)
keyboard.add("9", "0",)
keyboard.add("+", "-",)
keyboard.add("*", "/",)
keyboard.add("=")

# Создаем переменные для хранения введенных чисел и операции
num1 = None
num2 = None
op = None

# Обрабатываем команду /start
@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    # Приветствуем пользователя и предлагаем ввести первое число
    await message.answer("Введите первое число, используя клавиатуру ниже.", reply_markup=keyboard)

# Обрабатываем команду /new
@dp.message_handler(commands=["new"])
async def new(message: types.Message):
    # Доступ к глобальным переменным
    global num1, num2, op

    # Сбрасываем переменные
    num1 = None
    num2 = None
    op = None

    # Предлагаем ввести первое число
    await message.answer("Введите первое число, используя клавиатуру ниже.")

# Обрабатываем текстовые сообщения
@dp.message_handler()
async def calculate(message: types.Message):
    # Доступ к глобальным переменным
    global num1, num2, op

    # Получаем текст сообщения
    text = message.text

    # Проверяем, является ли текст числом
    try:
        # Преобразуем текст в число с плавающей точкой
        num = float(text)

        # Если первое число еще не введено, сохраняем его в переменную num1
        if num1 is None:
            num1 = num
            # Отправляем сообщение с подтверждением ввода первого числа
            await message.answer(f"Первое число: {num1}\n"
                                 "Введите операцию (+, -, *, /).")

        # Если первое число уже введено, но второе еще нет, сохраняем его в переменную num2
        elif num2 is None:
            num2 = num
            # Отправляем сообщение с подтверждением ввода второго числа
            await message.answer(f"Второе число: {num2}\n"
                                 "Введите знак равно (=) для получения результата.")

        # Если оба числа уже введены, сообщаем об ошибке
        else:
            await message.answer("Вы уже ввели два числа. Введите знак равно (=) для получения результата.")

    # Если текст не является числом, проверяем, является ли он операцией или знаком равно
    except ValueError:
        # Если текст является одним из знаков операций, сохраняем его в переменную op
        if text in ["+", "-", "*", "/"]:
            # Проверяем, что первое число уже введено
            if num1 is not None:
                # Проверяем, что операция еще не введена
                if op is None:
                    op = text
                    # Отправляем сообщение с подтверждением ввода операции
                    await message.answer(f"Операция: {op}\n"
                                         "Введите второе число.")
                # Если операция уже введена, сообщаем об ошибке
                else:
                    await message.answer("Вы уже ввели операцию. Введите второе число.")
            # Если первое число еще не введено, сообщаем об ошибке
            else:
                await message.answer("Введите сначала первое число.")

        # Если текст является знаком равно, вычисляем и выводим результат
        elif text == "=":
            # Проверяем, что введены все необходимые данные
            if num1 is not None and num2 is not None and op is not None:
                # Вычисляем результат в зависимости от операции
                if op == "+":
                    result = num1 + num2
                elif op == "-":
                    result = num1 - num2
                elif op == "*":
                    result = num1 * num2
                elif op == "/":
                    # Проверяем, что знаменатель не равен нулю
                    if num2 != 0:
                        result = num1 / num2
                    else:
                        result = "Ошибка: деление на ноль"
                # Отправляем сообщение с результатом
                await message.answer(f"{num1} {op} {num2} = {result}\n"
                                     "Для начала нового вычисления введите команду /new.")
                # Сбрасываем переменные
                num1 = None
                num2 = None
                op = None
            # Если данные не введены полностью, сообщаем об ошибке
            else:
                await message.answer("Введите сначала два числа и операцию.")

        # Если текст не является ни числом, ни операцией, ни знаком равно, сообщаем об ошибке
        else:
            await message.answer("Неверный ввод. Используйте клавиатуру ниже для ввода чисел и операций.")

            # Обрабатываем команду /language
            @dp.message_handler(commands=["language"])
            async def language(message: types.Message):
                # Создаем клавиатуру с кнопками для выбора языка
                lang_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                lang_keyboard.add("Русский", "Украинский", "English")

                # Отправляем сообщение с предложением выбрать язык
                await message.answer("Выберите язык, на котором вы хотите общаться с ботом.",
                                     reply_markup=lang_keyboard)

            # Обрабатываем выбор языка
            @dp.message_handler(lambda message: message.text in ["Русский", "Украинский", "English"])
            async def set_language(message: types.Message):
                # Получаем текст сообщения
                lang = message.text

                # Устанавливаем язык бота в зависимости от выбранного языка
                if lang == "Русский":
                    bot_language = "ru"
                elif lang == "Украинский":
                    bot_language = "uk"
                elif lang == "English":
                    bot_language = "en"

                # Отправляем сообщение с подтверждением выбора языка
                await message.answer(f"Вы выбрали язык: {lang}\n"
                                     "Теперь бот будет общаться с вами на этом языке.", reply_markup=keyboard)


# Запускаем бота
executor.start_polling(dp, skip_updates=True)