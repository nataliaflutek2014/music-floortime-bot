import logging
from dataclasses import dataclass

from aiogram import Dispatcher, F
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

@dataclass
class Brand:
    title: str
    tagline: str
    about: str
    tone: str
    colors: dict
    links: dict

brand = Brand(
    title="Музыкальный Флортайм — Наталья Каменева",
    tagline="DIRFloortime® • Музыкальная терапия • Интермодальная терапия экспрессивными искусствами",
    about=(
        "Я — Наталья Каменева: эксперт-преподаватель DIRFloortime®, музыкальный терапевт, "
        "мультиинструменталист. С 2014 года провела 4500+ индивидуальных и семейных сессий. "
        "Помогаю детям, подросткам и взрослым с РАС развивать коммуникацию, эмоциональную регуляцию "
        "и радость взаимодействия через игру, музыку и творчество. Работаю с семьями и специалистами — "
        "индивидуально, в группах, онлайн и офлайн."
    ),
    tone="Тёплый, уважительный, поддерживающий. Профессионально и без медицинских обещаний.",
    colors={"olive":"#7a8b56", "beige":"#f2ebdd", "peach":"#f7b77c"},
    links={
        "Сайт": "https://musicfloortime.tilda.ws",
        "Курс «Слух, музыка и речь»": "https://musicfloortime.tilda.ws/sluhkurs",
        "Телеграм-канал": "https://t.me/musicfloortime"
    }
)

DISCLAIMER = (
    "⚠️ <b>Важно:</b> бот не ставит диагнозы и не заменяет очную диагностику, медицинскую или психотерапевтическую помощь. "
    "Материалы носят образовательный характер."
)

def main_menu_kb() -> InlineKeyboardMarkup:
    rows = [
        [
            InlineKeyboardButton(text="👋 О Наталье и подходе", callback_data="about"),
            InlineKeyboardButton(text="🎵 Почему музыка работает", callback_data="music_why")
        ],
        [
            InlineKeyboardButton(text="🧩 Что такое DIRFloortime®", callback_data="dirf"),
            InlineKeyboardButton(text="📚 Материалы для родителей", callback_data="parents_materials"),
        ],
        [
            InlineKeyboardButton(text="📝 Мини-чеклист стресса", callback_data="stress_check"),
            InlineKeyboardButton(text="🗓 Заявка на консультацию", callback_data="intake_start")
        ],
        [
            InlineKeyboardButton(text="🎓 Курсы и обучение", callback_data="courses"),
            InlineKeyboardButton(text="❓ Частые вопросы", callback_data="faq")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=rows)

def back_menu_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="⬅️ В меню", callback_data="menu")]])

class Intake(StatesGroup):
    parent_name = State()
    child_age = State()
    goals = State()
    contact = State()

def register_handlers(dp: Dispatcher, ADMIN_CHAT_ID: str | None = None):
    @dp.message(CommandStart())
    async def start(m: Message):
        text = (
            f"<b>{brand.title}</b>
{brand.tagline}

"
            f"{DISCLAIMER}

"
            "Я помогу вам сориентироваться: расскажу о подходе, дам практические материалы, "
            "и — при желании — соберу краткую заявку на консультацию.

"
            "Выберите раздел ниже:"
        )
        await m.answer(text, reply_markup=main_menu_kb())

    @dp.message(Command("menu"))
    async def menu_cmd(m: Message):
        await m.answer("Главное меню:", reply_markup=main_menu_kb())

    @dp.callback_query(F.data == "menu")
    async def menu_cb(c: CallbackQuery):
        await c.message.edit_text("Главное меню:", reply_markup=main_menu_kb())
        await c.answer()

    @dp.callback_query(F.data == "about")
    async def about_cb(c: CallbackQuery):
        text = (
            f"<b>О специалисте</b>

{brand.about}

"
            "Мой подход:
"
            "• Индивидуальность ребёнка — в центре: следуем за интересом, усиливаем инициативу.
"
            "• Эмоциональная регуляция и связь — основа развития мышления и речи.
"
            "• Музыка и импровизация — мягкий путь к контакту, ритму и совместному вниманию.
"
            "• Партнёрство с родителями: учимся превращать повседневность в терапевтические моменты.
"
        )
        await c.message.edit_text(text, reply_markup=back_menu_kb())
        await c.answer()

    @dp.callback_query(F.data == "music_why")
    async def music_why_cb(c: CallbackQuery):
        text = (
            "<b>Почему музыкальная терапия помогает при аутизме?</b>

"
            "• Ритм упорядочивает: помогает телу и нервной системе находить устойчивость.
"
            "• Звук — дорога к совместному вниманию: проще «встретиться» в мелодии, чем в словах.
"
            "• Импровизация развивает инициативу и гибкость — через игру и удовольствие.
"
            "• Музыка поддерживает регуляцию: дышим, двигаемся, «качаем» темп и динамику.

"
            "Практика дома (3 идеи на каждый день):
"
            "1) «Музыкальный диалог»: повторяйте ритм ребёнка (ладони/стол), затем предложите микро-изменение.
"
            "2) «Звуковая пауза»: 30–60 секунд совместного дыхания + тихий длинный звук (на «м-м-м»).
"
            "3) «Песенка-ритуал»: короткая мелодия для переходов (сборы, умывание, сон).
"
        )
        await c.message.edit_text(text, reply_markup=back_menu_kb())
        await c.answer()

    @dp.callback_query(F.data == "dirf")
    async def dir_cb(c: CallbackQuery):
        text = (
            "<b>DIRFloortime® — кратко</b>

"
            "• D (Developmental): фокус на функционально-эмоциональных стадях развития.
"
            "• I (Individual): чувствуем сенсорный профиль, темп и интересы ребёнка.
"
            "• R (Relationship): отношения — двигатель развития.

"
            "Как это выглядит:
"
            "— Входим в игру ребёнка, откликаемся на его инициативу, мягко расширяем.
"
            "— Настраиваемся на ритм/сенсорику (движение, звук, осязание) и даём посильные вызовы.
"
            "— Поддерживаем совместное внимание, чередование, причинность и зарождение символической игры.
"
        )
        await c.message.edit_text(text, reply_markup=back_menu_kb())
        await c.answer()

    @dp.callback_query(F.data == "parents_materials")
    async def materials_cb(c: CallbackQuery):
        links = "
".join([f"• <a href='{url}'>{name}</a>" for name, url in brand.links.items()])
        text = (
            "<b>Материалы для родителей</b>

"
            "Подборка для спокойного старта:
"
            "• «Стимминг: уважать и поддерживать» — что это и как сделать безопасным.
"
            "• «Переходы без слёз» — мини-гайд по ритуалам и музыкальным подсказкам.
"
            "• «10 идей музыкальных игр дома» — от ритмических диалогов до песен-процедур.

"
            f"{links}

"
            "Если нужна индивидуальная рекомендация — оставьте заявку в разделе «Заявка на консультацию»."
        )
        await c.message.edit_text(text, reply_markup=back_menu_kb())
        await c.answer()

    @dp.callback_query(F.data == "stress_check")
    async def stress_check_cb(c: CallbackQuery):
        text = (
            "<b>Мини-чеклист стресса родителя (самооценка)</b>

"
            "Отметьте про себя: 
"
            "1) Я сплю не менее 6–7 часов чаще всего.
"
            "2) У меня есть 10–15 минут тишины ежедневно.
"
            "3) Я имею 1–2 «быстрых» способа восстановиться (дыхание/музыка/движение).
"
            "4) У нас есть 2–3 предсказуемых ритуала в семье.

"
            "Если «нет» больше чем на 2 пункта — это сигнал бережно понизить требования к себе, "
            "упростить день и добавить короткие практики восстановления. 

"
            "Микро-практика: 2 минуты «дыхание + звук» — 4 медленных вдоха носом, на выдохе тихий звук «м-м-м». "
            "Делайте вместе с ребёнком — это заразительно и успокаивает."
        )
        await c.message.edit_text(text, reply_markup=back_menu_kb())
        await c.answer()

    @dp.callback_query(F.data == "courses")
    async def courses_cb(c: CallbackQuery):
        text = (
            "<b>Обучение и программы</b>

"
            "• «Слух, музыка и речь» — курс для родителей и специалистов: как звук и ритм помогают "
            "регуляции, вниманию и коммуникации.
"
            "• Индивидуальное сопровождение семьи: разбор видео, домашние стратегии, музыкальные ритуалы.
"
            "• Супервизии для специалистов: кейсы, разбор сессий, планирование.

"
            "Подробнее и запись — по кнопкам в разделе «Материалы для родителей» или оставьте заявку в боте."
        )
        await c.message.edit_text(text, reply_markup=back_menu_kb())
        await c.answer()

    @dp.callback_query(F.data == "faq")
    async def faq_cb(c: CallbackQuery):
        text = (
            "<b>Частые вопросы</b>

"
            "• <b>Это заменит занятия с логопедом/психологом?</b>
"
            "Нет. Это поддерживающий подход, который помогает ребёнку быть устойчивее и включённее в работу.

"
            "• <b>Можно ли заниматься только музыкой?</b>
"
            "Музыка — мощный вход в контакт и регуляцию, но мы соединяем её с игрой, движением, рутиной семьи.

"
            "• <b>Работаете ли вы онлайн?</b>
"
            "Да. Форматы — консультации, разбор видео, сопровождение родителей и супервизии.

"
            "⚠️ <b>Важно:</b> бот не ставит диагнозы и не заменяет очную диагностику, медицинскую или психотерапевтическую помощь. "
            "Материалы носят образовательный характер."
        )
        await c.message.edit_text(text, reply_markup=back_menu_kb())
        await c.answer()

    @dp.callback_query(F.data == "intake_start")
    async def intake_start_cb(c: CallbackQuery, state: FSMContext):
        await state.set_state(Intake.parent_name)
        await c.message.edit_text(
            "<b>Заявка на консультацию</b>

Как к вам обращаться? (Имя и, если хотите, фамилия)",
            reply_markup=back_menu_kb()
        )
        await c.answer()

    @dp.message(Intake.parent_name)
    async def intake_parent_name(m: Message, state: FSMContext):
        await state.update_data(parent_name=m.text.strip())
        await state.set_state(Intake.child_age)
        await m.answer("Возраст ребёнка (например: 3 года 4 месяца):")

    @dp.message(Intake.child_age)
    async def intake_child_age(m: Message, state: FSMContext):
        await state.update_data(child_age=m.text.strip())
        await state.set_state(Intake.goals)
        await m.answer("Коротко опишите ваш запрос/цели (например: «частые истерики», «сложно с речью», «затруднены переходы»):")

    @dp.message(Intake.goals)
    async def intake_goals(m: Message, state: FSMContext):
        await state.update_data(goals=m.text.strip())
        await state.set_state(Intake.contact)
        await m.answer("Как с вами связаться? (Телеграм @ник или e-mail):")

    @dp.message(Intake.contact)
    async def intake_contact(m: Message, state: FSMContext):
        await state.update_data(contact=m.text.strip())
        data = await state.get_data()
        await state.clear()

        summary = (
            "<b>Заявка получена!</b>

"
            f"Имя: {data.get('parent_name')}
"
            f"Возраст ребёнка: {data.get('child_age')}
"
            f"Цели/запрос: {data.get('goals')}
"
            f"Контакт: {data.get('contact')}

"
            "Спасибо! Я свяжусь с вами, чтобы согласовать формат и время."
        )
        await m.answer(summary, reply_markup=main_menu_kb())

        if ADMIN_CHAT_ID:
            try:
                await m.bot.send_message(int(ADMIN_CHAT_ID), f"🆕 Новая заявка:
{summary}")
            except Exception as e:
                logging.warning(f"Не удалось отправить уведомление админу: {e}")

    @dp.message()
    async def fallback(m: Message):
        await m.answer(
            "Я слышу ваш запрос. Чтобы было быстрее, попробуйте меню ниже — или напишите, что вам нужно:",
            reply_markup=main_menu_kb()
        )
