from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram import Bot
import xlwings as xw

import keyboards as kb
from states import *

router = Router()

@router.message(Command('start'))
async def start(message: Message, state: FSMContext):
    await message.answer('Добро пожаловать', reply_markup=kb.main)
    try:
        await state.clear()
    except:
        print('erorr 3')


@router.message(Command('cancel'))
async def cancel(message: Message, state: FSMContext):
    try:
        await state.clear()
    except:
        print('error 2')
    await message.answer('Действие отменено', reply_markup=kb.main)


""" 

Первоначальная сделка

"""

@router.message(F.text == 'Первоначальная сделка')
async def initial_deal(message: Message, state: FSMContext):
    await state.set_state(Initial.type_of_cur)
    await message.answer('Выберите тип валюты.', reply_markup=kb.types_of_currencies)


@router.message(Initial.type_of_cur)
async def initial_type_cur(message: Message, state: FSMContext):
    await state.set_state(Initial.currency)
    await message.answer('Выберите валюту.', reply_markup=kb.get_currencies(message.text))


@router.message(Initial.currency)
async def initial_cur(message: Message, state: FSMContext):
    await state.update_data(currency=message.text)
    await state.set_state(Initial.open_price)
    await message.answer('Введите цену.', reply_markup=ReplyKeyboardRemove())


@router.message(Initial.open_price)
async def initial_open_price(message: Message, state: FSMContext):
    await state.update_data(open_price=message.text)
    await state.set_state(Initial.stop_loss)
    await message.answer('Введите стоп-лосс.')


@router.message(Initial.stop_loss)
async def initial_stop_loss(message: Message, state: FSMContext):
    await state.update_data(stop_loss=message.text)
    message = await message.answer('Производятся вычисления...', reply_markup=kb.main)
    data = await state.get_data()

    wb = xw.Book("rabota.xlsx")

    sheet = wb.sheets[data['currency']]

    list_of_words = ['B', 'C', 'D', 'E', 'F']

    for word in list_of_words:
        sheet[f'{word}3'].value = 0
        sheet[f'{word}4'].value = 0
    sheet['B3'].value = float(data['open_price'])
    sheet['B4'].value = float(data['stop_loss'])
    await message.answer(f'{data["currency"]} |{"Левередж"} {int(sheet["B17"].value)}, |{"Обьём Сделки"} {format(sheet["B2"].value, ".7f")} |{"Стоимость сделки в $"} {format(sheet["B5"].value, ".7f")} |{"Прибыль"} {format(sheet["B11"].value, ".7f")}')

    wb.save('rabota.xlsx')
    await state.clear()


""" 

Плюсовая сделка

"""
@router.message(F.text == 'Плюсовая')
async def Masthav_type_of_cur(message: Message, state: FSMContext):
    await state.set_state(Masthav.type_of_cur)
    await message.answer('Выберите тип валюты.', reply_markup=kb.types_of_currencies)


@router.message(Masthav.type_of_cur)
async def masthav_type_cur(message: Message, state: FSMContext):
    await state.set_state(Masthav.currency)
    await message.answer('Выберите валюту.', reply_markup=kb.get_currencies(message.text))



@router.message(Masthav.currency)
async def masthav_currency(message: Message, state: FSMContext):
    await state.update_data(currency=message.text)
    await state.set_state(Masthav.plus)
    message = await message.answer('Производятся вычисления...', reply_markup=ReplyKeyboardRemove())
    data = await state.get_data()

    wb = xw.Book("rabota.xlsx")

    sheet = wb.sheets[data['currency']]
    #Тут отображаются все сделки которые записаны на листе

    if sheet['B4'].value == 0 and sheet['B3'].value == 0:
        await message.answer(f'{"Ошибка, на этом листе не записано ещё ни одной сделки"}', reply_markup=kb.main)
        await state.clear()

    elif sheet['C4'].value == 0 and sheet['C3'].value == 0:

        await message.answer(f'1 {data["currency"]} |{"Левередж"} {int(sheet["B17"].value)} |{"Обьём Сделки"} {format(sheet["B2"].value, ".7f")} |{"Стоимость Сделки в $"} {format(sheet["B5"].value, ".7f")} |{"Прибыль"} {format(sheet["B11"].value, ".7f")} |{"Убыток"} {format(sheet["B8"].value, ".7f")}',
                             reply_markup=kb.plus_kb)

    elif sheet['D4'].value == 0 and sheet['D3'].value == 0:

        await message.answer(f'1 {data["currency"]} |{"Левередж"} {int(sheet["B17"].value)} |{"Обьём Сделки"} {format(sheet["B2"].value, ".7f")} |{"Стоимость Сделки в $"} {format(sheet["B5"].value, ".7f")} |{"Прибыль"} {format(sheet["B11"].value, ".7f")}\n'
                             f'2 {data["currency"]} |{"Левередж"} {int(sheet["B17"].value)} |{"Обьём Сделки"} {format(sheet["C2"].value, ".7f")} |{"Стоимость Сделки в $"} {format(sheet["C5"].value, ".7f")} |{"Прибыль"} {format(sheet["C11"].value, ".7f")} |{"Суммарный Убыток"} {format(sheet["D10"].value, ".7f")}',
                             reply_markup=kb.plus_kb)

    elif sheet['E4'].value == 0 and sheet['E3'].value == 0:

        await message.answer(f'1 {data["currency"]} |{"Левередж"} {int(sheet["B17"].value)} |{"Обьём Сделки"} {format(sheet["B2"].value, ".7f")} |{"Стоимость Сделки в $"} {format(sheet["B5"].value, ".7f")} |{"Прибыль"} {format(sheet["B11"].value, ".7f")}\n'
                             f'2 {data["currency"]} |{"Левередж"} {int(sheet["B17"].value)} |{"Обьём Сделки"} {format(sheet["C2"].value, ".7f")} |{"Стоимость Сделки в $"} {format(sheet["C5"].value, ".7f")} |{"Прибыль"} {format(sheet["C11"].value, ".7f")}\n'
                             f'3 {data["currency"]} |{"Левередж"} {int(sheet["B17"].value)} |{"Обьём Сделки"} {format(sheet["D2"].value, ".7f")} |{"Стоимость Сделки в $"} {format(sheet["D5"].value, ".7f")} |{"Прибыль"} {format(sheet["D11"].value, ".7f")} |{"Суммарный Убыток"} {format(sheet["E10"].value, ".7f")}',
                             reply_markup=kb.plus_kb)

    elif sheet['F4'].value == 0 and sheet['F3'].value == 0:

        await message.answer(f'1 {data["currency"]} |{"Левередж"} {int(sheet["B17"].value)} |{"Обьём Сделки"} {format(sheet["B2"].value, ".7f")} |{"Стоимость Сделки в $"} {format(sheet["B5"].value, ".7f")} |{"Прибыль"} {format(sheet["B11"].value, ".7f")}\n'
                             f'2 {data["currency"]} |{"Левередж"} {int(sheet["B17"].value)} |{"Обьём Сделки"} {format(sheet["C2"].value, ".7f")} |{"Стоимость Сделки в $"} {format(sheet["C5"].value, ".7f")} |{"Прибыль"} {format(sheet["C11"].value, ".7f")}\n'
                             f'3 {data["currency"]} |{"Левередж"} {int(sheet["B17"].value)} |{"Обьём Сделки"} {format(sheet["D2"].value, ".7f")} |{"Стоимость Сделки в $"} {format(sheet["D5"].value, ".7f")} |{"Прибыль"} {format(sheet["D11"].value, ".7f")}\n'
                             f'4 {data["currency"]} |{"Левередж"} {int(sheet["B17"].value)} |{"Обьём Сделки"} {format(sheet["E2"].value, ".7f")} |{"Стоимость Сделки в $"} {format(sheet["E5"].value, ".7f")} |{"Прибыль"} {format(sheet["E11"].value, ".7f")} |{"Суммарный Убыток"} {format(sheet["F10"].value, ".7f")}',
                             reply_markup=kb.plus_kb)
    else:

        await message.answer(f'1 {data["currency"]} |{"Левередж"} {int(sheet["B17"].value)} |{"Обьём Сделки"} {format(sheet["B2"].value, ".7f")} |{"Стоимость Сделки в $"} {format(sheet["B5"].value, ".7f")} |{"Прибыль"} {format(sheet["B11"].value, ".7f")}\n'
                             f'2 {data["currency"]} |{"Левередж"} {int(sheet["B17"].value)} |{"Обьём Сделки"} {format(sheet["C2"].value, ".7f")} |{"Стоимость Сделки в $"} {format(sheet["C5"].value, ".7f")} |{"Прибыль"} {format(sheet["C11"].value, ".7f")}\n'
                             f'3 {data["currency"]} |{"Левередж"} {int(sheet["B17"].value)} |{"Обьём Сделки"} {format(sheet["D2"].value, ".7f")} |{"Стоимость Сделки в $"} {format(sheet["D5"].value, ".7f")} |{"Прибыль"} {format(sheet["D11"].value, ".7f")}\n'
                             f'4 {data["currency"]} |{"Левередж"} {int(sheet["B17"].value)} |{"Обьём Сделки"} {format(sheet["E2"].value, ".7f")} |{"Стоимость Сделки в $"} {format(sheet["E5"].value, ".7f")} |{"Прибыль"} {format(sheet["E11"].value, ".7f")}\n'
                             f'5 {data["currency"]} |{"Левередж"} {int(sheet["B17"].value)} |{"Обьём Сделки"} {format(sheet["F2"].value, ".7f")} |{"Стоимость Сделки в $"} {format(sheet["F5"].value, ".7f")} |{"Прибыль"} {format(sheet["F11"].value, ".7f")} |{"Суммарный Убыток"} {format(sheet["F8"].value, ".7f")}',
                             reply_markup=kb.plus_kb)


@router.message(Masthav.plus, F.text == '+')
async def initial_cur(message: Message, state: FSMContext):
    await state.set_state(Masthav.minus)
    await message.answer('Введите плюс', reply_markup=kb.cancel_reply)


@router.message(Masthav.minus)
async def initial_cur(message: Message, state: FSMContext):
    await state.set_state(Masthav.ravno)
    await state.update_data(plus=message.text)
    await message.answer(f'Вы уверены что плюс {message.text} больше минуса', reply_markup=kb.types_of_vibor)


@router.message(Masthav.plus, F.text == 'Назад')
async def initial_cur(message: Message, state: FSMContext):
    await message.answer('ok', reply_markup=kb.main)
    await state.clear()

@router.message(Masthav.ravno, F.text == 'Нет')
async def initial_cur(message: Message, state: FSMContext):
    data = await state.get_data()
    wb = xw.Book("rabota.xlsx")

    sheet = wb.sheets[data['currency']]
    list_of_words = ['B', 'C', 'D', 'E', 'F']

    for word in list_of_words:
        sheet[f'{word}3'].value = 0
        sheet[f'{word}4'].value = 0

    await message.answer('ok', reply_markup=kb.main)
    await state.clear()


@router.message(Masthav.ravno, F.text == 'Да')
async def initial_cur(message: Message, state: FSMContext):
    list_of_words = ['B', 'C', 'D', 'E', 'F']
    wb = xw.Book("rabota.xlsx")
    data = await state.get_data()
    sheet = wb.sheets[data['currency']]
    result_message = ''
    for word in list_of_words:
        if sheet[f'{word}3'].value == 0 or sheet[f'{word}4'].value == 0:
            continue
        else:
            if sheet[f'{word}8'].value is not None and sheet[f'{word}11'].value is not None:
                if float(sheet[f'{word}8'].value) > float(sheet[f'{word}11'].value):
                    income = f"Убыток {format(sheet[f'{word}10'].value, '.7f')}"
                else:
                    income = f"Доход {format(sheet[f'{word}11'].value, '.7f')}"

                result_message += f'{data["currency"]} |{"Объём Сделки"} {format(sheet[f"{word}2"].value, ".7f")} ' \
                                  f'|{"Цена Открытия"} {format(sheet[f"{word}3"].value, ".7f")} | {income}\n'

    await message.answer(result_message)



    wb.save('rabota.xlsx')
    wb.close()
    await state.clear()


""" 

Минусовая сделка

"""
@router.message(F.text == 'Минусовая')
async def initial_deal(message: Message, state: FSMContext):
    await state.set_state(Minus.type_of_cur)
    await message.answer('Выберите тип валюты.', reply_markup=kb.types_of_currencies)


@router.message(Minus.type_of_cur)
async def initial_type_cur(message: Message, state: FSMContext):
    await state.set_state(Minus.currency)
    await message.answer('Выберите валюту.', reply_markup=kb.get_currencies(message.text))


@router.message(Minus.currency)
async def initial_cur(message: Message, state: FSMContext):
    await state.update_data(currency=message.text)
    await state.set_state(Minus.open_price)
    await message.answer('Введите цену.', reply_markup=ReplyKeyboardRemove())


@router.message(Minus.open_price)
async def initial_open_price(message: Message, state: FSMContext):
    await state.update_data(open_price=message.text)
    await state.set_state(Minus.stop_loss)
    await message.answer('Введите стоп-лосс.')


@router.message(Minus.stop_loss)
async def initial_stop_loss(message: Message, state: FSMContext):
    await state.update_data(stop_loss=message.text)
    message = await message.answer('Производятся вычисления...', reply_markup=kb.main)
    data = await state.get_data()

    wb = xw.Book("rabota.xlsx")

    sheet = wb.sheets[data['currency']]
    #Тут отображаются все сделки которые записаны на листе

    if sheet['B4'].value == 0 and sheet['B3'].value == 0:
        await message.answer(f'{"Ошибка, на этом листе не записано ещё ни одной сделки"}')

    elif sheet['C4'].value == 0 and sheet['C3'].value == 0:
        sheet['C3'].value = float(data['open_price'])
        sheet['C4'].value = float(data['stop_loss'])
        plus = sheet['B2'].value
        minus = sheet['C2'].value
        sume_value = float(plus) + float(minus)
        await message.answer(f'1 {data["currency"]} | {int(sheet["B17"].value)} |{"Обьём Сделки"} {format(sheet["B2"].value, ".4f")} |{"Стоимость сделки в $"} {format(sheet["B5"].value, ".4f")} |{"Прибыль 2x стопа"} {format(sheet["B11"].value, ".7f")} |{"Убыток в $"} {format(sheet["B8"].value, ".7f")} \n '
                             f'2 {data["currency"]} | {int(sheet["B17"].value)} |{"Обьём Сделки"} {format(sheet["C2"].value, ".4f")} |{"Cтоимость сделки в $"} {format(sheet["C5"].value, ".4f")} |{"Прибыль 2x стопа"} {format(sheet["C11"].value, ".7f")} |{"Убыток в $"} {format(sheet["C8"].value, ".7f")} \n '
                             f'{"Суммарный обьём"} {format(sume_value, ".4f")} {"Суммарный убыток всех сделок"} {format(sheet["D10"].value, ".4f")}  ')

    elif sheet['D4'].value == 0 and sheet['D3'].value == 0:
        sheet['D3'].value = float(data['open_price'])
        sheet['D4'].value = float(data['stop_loss'])
        plus = sheet['B2'].value
        minus = sheet['C2'].value
        damage = sheet['D2'].value
        sume_value = float(plus) + float(minus) + float(damage)
        await message.answer(f'1 {data["currency"]} | {int(sheet["B17"].value)} |{"Обьём Сделки"} {format(sheet["B2"].value, ".7f")} |{"Стоимость сделки в $"} {format(sheet["B5"].value, ".7f")} |{"Прибыль 2x стопа"} {format(sheet["B11"].value, ".7f")} |{"Убыток в $"} {format(sheet["B8"].value, ".7f")}\n '
                             f'2 {data["currency"]} | {int(sheet["B17"].value)} |{"Обьём Сделки"} {format(sheet["C2"].value, ".7f")} |{"Стоимость сделки в $"} {format(sheet["C5"].value, ".7f")} |{"Прибыль 2x стопа"} {format(sheet["C11"].value, ".7f")} |{"Убыток в $"} {format(sheet["C8"].value, ".7f")}\n '
                             f'3 {data["currency"]} | {int(sheet["B17"].value)} |{"Обьём Сделки"} {format(sheet["D2"].value, ".7f")} |{"Стоимость сделки в $"} {format(sheet["D5"].value, ".7f")} |{"Прибыль 2x стопа"} {format(sheet["D11"].value, ".7f")} |{"Убыток в $"} {format(sheet["D8"].value, ".7f")}\n'
                             f'{"Суммарный обьём"} {format(sume_value, ".4f")} {"Суммарный убыток всех сделок"} {format(sheet["E10"].value, ".7f")}  ')

    elif sheet['E4'].value == 0 and sheet['E3'].value == 0:
        sheet['E3'].value = float(data['open_price'])
        sheet['E4'].value = float(data['stop_loss'])
        plus = sheet['B2'].value
        minus = sheet['C2'].value
        damage = sheet['D2'].value
        equipment = sheet['E2'].value
        sume_value = float(plus) + float(minus) + float(damage) +float(equipment)
        await message.answer(f'1 {data["currency"]} | {int(sheet["B17"].value)} |{"Обьём Сделки"} {format(sheet["B2"].value, ".7f")} |{"Стоимость сделки в $"} {format(sheet["B5"].value, ".7f")} |{"Прибыль 2x стопа"} {format(sheet["B11"].value, ".7f")} |{"Убыток в $"} {format(sheet["B8"].value, ".7f")}\n'
                             f'4 {data["currency"]} | {int(sheet["B17"].value)} |{"Обьём Сделки"} {format(sheet["E2"].value, ".7f")} |{"Стоимость сделки в $"} {format(sheet["E5"].value, ".7f")} |{"Прибыль 2x стопа"} {format(sheet["E11"].value, ".7f")} |{"Убыток в $"} {format(sheet["E8"].value, ".7f")}\n'
                             f'{"Суммарный обьём"} {format(sume_value, ".4f")} {"Суммарный убыток всех сделок"} {format(sheet["F10"].value, ".7f")}' )

    elif sheet['F4'].value == 0 and sheet['F3'].value == 0:
        sheet['F3'].value = float(data['open_price'])
        sheet['F4'].value = float(data['stop_loss'])
        plus = sheet['B2'].value
        minus = sheet['C2'].value
        damage = sheet['D2'].value
        equipment = sheet['E2'].value
        fatality = sheet['F2'].value
        one_kill = sheet['F8'].value
        last_kill = sheet['F10'].value
        rampage = float(one_kill) + float(last_kill)
        sume_value = float(plus) + float(minus) + float(damage) + float(equipment) + float(fatality)
        await message.answer(f'1 {data["currency"]} | {int(sheet["B17"].value)} |{"Обьём Сделки"} {format(sheet["B2"].value, ".7f")} |{"Стоимость сделки в $"} {format(sheet["B5"].value, ".7f")} |{"Прибыль 2x стопа"} {format(sheet["B11"].value, ".7f")} | {"Убыток в $"} {format(sheet["B8"].value, ".7f")}\n' 
                             f'4 {data["currency"]} | {int(sheet["B17"].value)} |{"Обьём Сделки"} {format(sheet["E2"].value, ".7f")} |{"Стоимость сделки в $"} {format(sheet["E5"].value, ".7f")} |{"Прибыль 2x стопа"} {format(sheet["E11"].value, ".7f")} | {"Убыток в $"} {format(sheet["E8"].value, ".7f")}\n'
                             f'5 {data["currency"]} | {int(sheet["B17"].value)} |{"Обьём Сделки"} {format(sheet["F2"].value, ".7f")} |{"Стоимость сделки в $"} {format(sheet["F5"].value, ".7f")} |{"Прибыль 2x стопа"} {format(sheet["F11"].value, ".7f")} | {"Убыток в $"} {format(sheet["F8"].value, ".7f")}\n'
                             f'{"Суммарный обьём"} {format(sume_value, ".4f")} {"Суммарный убыток всех сделок"} {format(rampage, ".7f")}')


"""
    if ws['B3'].value == 0:
        ws['B3'] = data['open_price']
        ws['B4'] = data['stop_loss']
        
        leverage = ws['B17'].value
        open_quantity = ws['B18'].value
        price = ws['B19'].value
        orders = ((ws['B19'].value * (abs(float(ws['B4'].value)) - abs(float(ws['B3'].value))) / ws['B20'].value) + (ws['B16'].value / ws['B20'].value * ws['B19'].value) / 2)
    elif ws['C3'] == 0:
        ws['C3'] = data['open_price']
        ws['C4'] = data['stop_loss']
        
        leverage = ws['B17'].value
        open_quantity = ws['B18'].value
        price = ws['B19'].value
        orders = ws['C11'].formula"""
