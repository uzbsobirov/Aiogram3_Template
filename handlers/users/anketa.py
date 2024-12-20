from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram import types

from states.ankst import newAnketa

router = Router()


@router.message(Command("new"))
async def new_ank(message: types.Message, state: FSMContext):
    await message.answer("Iltimos, ismingizni kiriting")
    await state.set_state(newAnketa.name)


@router.message(newAnketa.name)
async def get_name(message: types.Message, state: FSMContext):
    name = message.text
    if len(name.split()) == 2:
        if not (
                "1" in name or
                "2" in name or
                "3" in name or
                "4" in name or
                "5" in name or
                "6" in name or
                "7" in name or
                "8" in name or
                "9" in name):
            await message.answer("Ismingiz qabul qilindi")
            await message.answer("Telefon raqamingizni yozing: +998951008303")
            await state.update_data(name=name)
            await state.set_state(newAnketa.phone)
        else:
            await message.answer("Ismda sonlar qatnashishi mumkin emas")
            await state.set_state(newAnketa.name)
    else:
        await message.answer("Ismingizni to'liq kirgazing")
        await state.set_state(newAnketa.name)


@router.message(newAnketa.phone)
async def get_phone(message: types.Message, state: FSMContext):
    phone = message.text
    if len(phone) == 13:
        if phone.startswith("+998"):
            await message.answer("Telefon raqamingiz qabul qilindi")
            await message.answer("Ishingizni yozing")
            await state.update_data(phone=phone)
            await state.set_state(newAnketa.job)
        else:
            await message.answer("Telefon raqam '+998' bilan boshlanishi shart")
            await state.set_state(newAnketa.phone)
    else:
        await message.answer("Telefon raqam xato")
        await state.set_state(newAnketa.phone)


@router.message(newAnketa.job)
async def get_phone(message: types.Message, state: FSMContext):
    job = message.text
    if len(job) <= 15:
            await message.answer("Ish saqlandi")
            await message.answer("Maqsadingizni yozing yozing")
            await state.update_data(job=job)
            await state.set_state(newAnketa.goal)

    else:
        await message.answer("15 harfdan kop emas")
        await state.set_state(newAnketa.job)


@router.message(newAnketa.goal)
async def get_phone(message: types.Message, state: FSMContext):
    goal = message.text
    if len(goal) <= 100:
            await message.answer("Maqsad saqlandi saqlandi")
            data = await state.get_data()
            name = data.get("name")
            phone = data.get("phone")
            job = data.get("job")
            text = f"""Ismingiz: {name}
                        Raqam: {phone}
                        Ish: {job}
                        Maqsad: {goal}"""
            await message.answer(text)
            await state.clear()

    else:
        await message.answer("100 harfdan kop emas")
        await state.set_state(newAnketa.goal)
