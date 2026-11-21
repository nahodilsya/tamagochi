import streamlit as st

st.set_page_config(page_title="Тамагочи", page_icon="🐱", layout="centered")

MAX_STAT = 100
TARGET_TURNS = 15


def init_game():
    st.session_state.satiety = 50
    st.session_state.fatigue = 0
    st.session_state.mood = 50
    st.session_state.turns = 0
    st.session_state.menu_mode = None  # None | "feed" | "play"
    st.session_state.game_over = False
    st.session_state.victory = False
    st.session_state.finished_by_exit = False
    st.session_state.log = [f"Игра началась! Цель: продержаться {TARGET_TURNS} дней."]


if "satiety" not in st.session_state:
    init_game()

s = st.session_state


def add_log(msg):
    s.log.append(msg)


def finish_defeat(msg):
    s.game_over = True
    s.menu_mode = None
    add_log(f"💀 {msg}")


def finish_victory():
    s.victory = True
    s.menu_mode = None
    add_log(
        f"🏆 ПОБЕДА! Продержался {TARGET_TURNS} дней! "
        f"(Сытость: {s.satiety}/{MAX_STAT}, настроение: {s.mood}/{MAX_STAT}, усталость: {s.fatigue}/{MAX_STAT})"
    )


def end_turn():
    # Фоновые списания конца хода (как в конце основного цикла)
    s.mood -= 5
    s.satiety -= 5
    s.fatigue += 5

    if s.satiety <= 25:
        s.mood -= 10
        add_log("Живот урчит, питомец раздражен от голода!")

    if s.mood >= 85:
        s.fatigue += 10
        s.satiety -= 5
        add_log("Кот на лютом кураже носится по стенам — тратит силы и сжигает калории!")

    s.turns += 1
    if s.turns >= TARGET_TURNS:
        finish_victory()


def do_feed(kind):
    s.menu_mode = None

    if kind == "a":
        s.satiety += 10
        s.mood -= 10
        add_log("Сухой корм: сытость увеличена на 10, настроение уменьшено на 10.")
        if s.satiety > MAX_STAT:
            finish_defeat("Грустные новости :( Ваш питомец подавился сухим кормом и умер")
            return
        if s.satiety == MAX_STAT:
            add_log("Вашему питомцу нездоровится")

    elif kind == "b":
        s.satiety += 30
        add_log(f"Мясной пауч: сытость увеличена на 30. Сытость: {s.satiety}")
        if s.satiety > MAX_STAT:
            finish_defeat("Нам жаль, но Вам питомец не справился в бою с мясным пунчем и погиб")
            return
        if s.satiety == MAX_STAT:
            add_log("Ваш питомец чувствует себя плохо")

    elif kind == "c":
        s.satiety += 50
        add_log(f"Элитная рыба: сытость увеличена на 50. Сытость: {s.satiety}")
        if s.satiety > MAX_STAT:
            finish_defeat("Элитная рыба показала урок Вашему питомцу")
            return
        if s.satiety == MAX_STAT:
            add_log("Элитная рыба нанесла ощутимый урон Вашему питомцу")

    if s.mood <= 0:
        s.mood = 0
        finish_defeat("Питомец вконец заскучал от этих сухарей, впал в апатию и сбежал.")
        return

    add_log(f"Текущие показатели после кормёжки — сытость: {s.satiety}, настроение: {s.mood}")
    end_turn()


def do_play(kind):
    s.menu_mode = None

    if kind == "a":
        s.satiety -= 10
        s.mood += 15
        s.fatigue += 15
        if s.mood > MAX_STAT:
            s.mood = 90
            s.satiety -= 10
            add_log("Передоз радости! Питомец на радостях снёс полку, выдохся и проголодался (-10 сытости, настроение 90)")
        if s.mood <= 0:
            finish_defeat("Депрессия от скуки заставила питомца совершить побег")
            return
        if s.fatigue >= MAX_STAT:
            finish_defeat("Ваш питомец упал без сил и умер")
            return
        if s.satiety <= 0:
            s.satiety = 0
            finish_defeat("Сытость на нуле. Похоже, ваш питомец переоценил свою выносливость и недооценил важность еды")
            return
        add_log(f"Красная точка от лазерной указки была поймана! Сытость: {s.satiety}, настроение: {s.mood}, усталость: {s.fatigue}")

    elif kind == "b":
        s.satiety -= 25
        s.mood += 30
        s.fatigue += 30
        if s.mood > MAX_STAT:
            s.mood = 90
            add_log(f"Передоз радости! Питомец так увлёкся клубком, что запутался, выдохся и проголодался (-10 сытости, настроение: {s.mood})")
        if s.mood <= 0:
            finish_defeat("Питомец так запутался в нитках, что потерял веру в жизнь и ушёл в закат")
            return
        if s.satiety <= 0:
            s.satiety = 0
            finish_defeat("Сытость на нуле. Клубок ниток победил — у питомца просто кончилось топливо")
            return
        if s.fatigue >= MAX_STAT:
            finish_defeat("Слишком долгая битва с клубком — сердце питомца не выдержало такой нагрузки")
            return
        add_log(f"Клубок ниток повержен! Вся комната в шерсти, но питомец в восторге. Сытость: {s.satiety}, настроение: {s.mood}, усталость: {s.fatigue}")

    elif kind == "c":
        s.satiety -= 45
        s.mood += 50
        s.fatigue += 50
        if s.mood > MAX_STAT:
            s.mood = 90
            add_log(f"Передоз радости! Ночной тыгыдык вышел из-под контроля — кот впечатался в шкаф, выдохся и проголодался (-10 сытости, настроение: {s.mood})")
        if s.mood <= 0:
            finish_defeat("Призраки оказались скучнее, чем ожидалось — питомец впал в апатию и сбежал")
            return
        if s.satiety <= 0:
            s.satiety = 0
            finish_defeat("Сытость на нуле. Охота на призраков сожгла последние калории, питомец пал в бою")
            return
        if s.fatigue >= MAX_STAT:
            finish_defeat("Ночной тыгыдык забрал все силы — питомец рухнул посреди комнаты и не проснулся")
            return
        add_log(f"Ночной тыгыдык удался: все призраки в квартире изгнаны! Сытость: {s.satiety}, настроение: {s.mood}, усталость: {s.fatigue}")

    end_turn()


def do_sleep():
    s.menu_mode = None

    if s.fatigue < 20:
        s.mood -= 15
        add_log("Кот выспался ещё вчера — в итоге просто провалялся и заскучал (-15 настроения).")
    else:
        s.fatigue -= 35
        if s.fatigue < 0:
            s.fatigue = 0
        add_log("Питомец сладко потянулся и немного вздремнул.")

    s.satiety -= 20

    if s.mood > 80:
        s.mood -= 10
    elif s.mood < 40 and s.satiety > 25:
        s.mood += 10

    if s.satiety <= 0:
        s.satiety = 0
        finish_defeat("Кот крепко уснул... но проголодался настолько, что так и не проснулся.")
        return

    add_log(f"После сна — сытость: {s.satiety}, настроение: {s.mood}, усталость: {s.fatigue}")
    end_turn()


# --- ИНТЕРФЕЙС ---
st.title("🐱 ТАМАГОЧИ")
display_day = min(s.turns + 1, TARGET_TURNS)
st.subheader(f"День {display_day}/{TARGET_TURNS}")

c1, c2, c3 = st.columns(3)
with c1:
    st.metric("Сытость", f"{s.satiety}/{MAX_STAT}")
    st.progress(max(0.0, min(1.0, s.satiety / MAX_STAT)))
with c2:
    st.metric("Настроение", f"{s.mood}/{MAX_STAT}")
    st.progress(max(0.0, min(1.0, s.mood / MAX_STAT)))
with c3:
    st.metric("Усталость", f"{s.fatigue}/{MAX_STAT}")
    st.progress(max(0.0, min(1.0, s.fatigue / MAX_STAT)))

if s.satiety <= 25:
    st.info("Состояние: кот на грани голодного обморока, срочно нужна еда.")
elif s.fatigue >= 75:
    st.info("Состояние: лапы уже не держат, пора укладывать спать.")
elif s.mood <= 25:
    st.info("Состояние: глубокая хандра, пора доставать лазер или устраивать тыгыдык.")
else:
    st.info("Состояние: кот в полном порядке, шерсть блестит, хвост трубой.")

st.divider()

if not s.game_over and not s.victory and not s.finished_by_exit:
    if s.menu_mode is None:
        m1, m2, m3, m4 = st.columns(4)
        if m1.button("a. Покормить", use_container_width=True):
            s.menu_mode = "feed"
            st.rerun()
        if m2.button("b. Поиграть", use_container_width=True):
            s.menu_mode = "play"
            st.rerun()
        if m3.button("c. Спать", use_container_width=True):
            do_sleep()
            st.rerun()
        if m4.button("e. Выход", use_container_width=True):
            s.finished_by_exit = True
            add_log("Спасибо за игру! Питомец будет ждать Вас!")
            st.rerun()

    elif s.menu_mode == "feed":
        st.markdown("### Чем покормить?")
        f1, f2, f3 = st.columns(3)
        if f1.button("a. Сухой корм (+25* / -10 настр.)", use_container_width=True):
            do_feed("a")
            st.rerun()
        if f2.button("b. Мясной пауч (+35*)", use_container_width=True):
            do_feed("b")
            st.rerun()
        if f3.button("c. Элитная рыба (+50*)", use_container_width=True):
            do_feed("c")
            st.rerun()
        if st.button("← Назад"):
            s.menu_mode = None
            st.rerun()

    elif s.menu_mode == "play":
        st.markdown("### Во что поиграем?")
        p1, p2, p3 = st.columns(3)
        if p1.button("a. Лазерная указка (+15/15/-10)", use_container_width=True):
            do_play("a")
            st.rerun()
        if p2.button("b. Клубок ниток (+30/30/-25)", use_container_width=True):
            do_play("b")
            st.rerun()
        if p3.button("c. Охота на призраков (+50/50/-45)", use_container_width=True):
            do_play("c")
            st.rerun()
        if st.button("← Назад"):
            s.menu_mode = None
            st.rerun()

else:
    if s.victory:
        st.success(f"=== ПОБЕДА! Продержался {TARGET_TURNS} дней! ===")
    elif s.game_over:
        st.error(s.log[-1])
    elif s.finished_by_exit:
        st.warning("Спасибо за игру! Питомец будет ждать Вас!")

    if st.button("🔄 Начать заново", use_container_width=True):
        init_game()
        st.rerun()

st.divider()
st.subheader("Журнал событий")
for item in reversed(s.log[-10:]):
    st.write(f"• {item}")