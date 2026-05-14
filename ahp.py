from nicegui import ui
from methods_functions import ahp_method, save_answers_to_csv

ui.add_css('assets/style.css')

"""
criteria = [
    "Rodzaj bólu",
    "Intensywność bólu",
    "Ogólna elastyczność ciała",
    "Sprawność fizyczna",
    "Menstruacja",
    "Ciąża",
    "Nadciśnienie",
    "Doświadczenie w jodze",
    "Samopoczucie psychiczne"
]
"""

criteria = [
    "Rodzaj bólu",
    "Intensywność bólu",
    "Ogólna elastyczność ciała",
]

# pair generation
pairs = [(i, j) for i in range(len(criteria)) for j in range (i+1, len(criteria))]
state = {'index': 0, 'value': 2}
answers = {}

def current_pair():
    i, j = pairs[state['index']]
    return criteria[i], criteria[j]

def set_ui_from_state():
    x, y = current_pair()
    label_x.set_text(x)
    label_y.set_text(y)
    step_label.set_text(f'Pytanie {state["index"] + 1}/{len(pairs)}')
    value_badge.set_text(str(state['value']))
    if state['value'] == 1:
        direction.value = 'Równa ważność'
        slider.disable()
    else:
        slider.enable()

    slider.value = state['value']
    value_badge.set_text(str(state['value']))

def in_slider_change(e):
    state['value'] = int(e.value)
    value_badge.set_text(str(state['value']))


def go_prev():
    if state['index'] > 0:
        state['index'] -= 1

        i, j = pairs[state['index']]
        saved_value = answers.get((i, j))

        if saved_value is not None:

            if saved_value == 1:
                direction.value = 'Równa ważność'
                state['value'] = 1

            elif saved_value < 1:
                direction.value = 'Prawe kryterium'
                state['value'] = int(1 / saved_value)

            else:
                direction.value = 'Lewe kryterium'
                state['value'] = int(saved_value)

        else:
            direction.value = 'Lewe kryterium'
            state['value'] = 2

        set_ui_from_state()
def go_next():
    i, j = pairs[state['index']]

    if direction.value == 'Lewe kryterium':
        value = state['value']
    elif direction.value == 'Prawe kryterium':
        value = 1 / state['value']
    else:
        value = 1

    answers[(i, j)] = value

    if state['index'] < len(pairs) - 1:
        state['index'] += 1

        direction.value = 'Lewe kryterium'
        state['value'] = 2

        slider.enable()


        set_ui_from_state()
    else:
        questionnaire_screen.set_visibility(False)
        finish_screen.set_visibility(True)

def submit_answers():

    weights, cr = ahp_method(answers)

    save_answers_to_csv(
        answers,
        criteria,
        weights,
        cr
    )

    ui.notify('Odpowiedzi zostały zapisane 🎉')

def start_questionnaire():

    start_screen.set_visibility(False)
    questionnaire_screen.set_visibility(True)

    set_ui_from_state()


# === equal importance ===
def on_direction_change(e):
    if e.value == 'Równa ważność':
        state['value'] = 1
        slider.value = 1
        slider.disable()
        value_badge.set_text('1')
    else:
        slider.enable()

def in_slider_change(e):
    if direction.value != 'Równa ważność':
        state['value'] = int(e.value)
        value_badge.set_text(str(state['value']))

# ======= UI ======

with ui.column().classes('items-center justify-center w-full h-screen') as start_screen:

    with ui.card().classes('main-card'):

        ui.label('Badanie AHP').classes('title')

        ui.label(
            'Celem badania jest określenie ważności kryteriów diagnostycznych.'
        ).classes('introduction')

        ui.button(
            'ROZPOCZNIJ BADANIE',
            on_click=start_questionnaire
        ).props('unelevated no-caps').classes('button next')

with ui.column() as questionnaire_screen:
    with ui.card().classes('main-card'):
        ui.label('Co jest ważniejsze?').classes('title')
        step_label = ui.label().classes('step')

        with ui.row().classes('criteria-row'):
            label_x = ui.label("x").classes('criterion-box')
            label_y = ui.label('Y').classes('criterion-box')

            direction = ui.radio(
                ['Lewe kryterium', 'Równa ważność', 'Prawe kryterium'],
                value='Lewe kryterium',
                on_change = on_direction_change
            ).classes('direction-radio')

        ui.label('Wskaż, które kryterium jest ważniejsze, a następnie określ siłę przewagi').classes('introduction')
        value_badge = ui.label('25').classes('slider-value')

        slider = ui.slider(min=2, max=9, value=2, step=1).classes('custom-slider')
        slider.on_value_change(in_slider_change)
        with ui.row().classes('slider-labels'):
            ui.label('2')
            ui.label('3')
            ui.label('4')
            ui.label('5')
            ui.label('6')
            ui.label('7')
            ui.label('8')
            ui.label('9')


        with ui.row().classes('button-row'):
            #!!!! tutaj wymuszamy kolor biały, bo ma niebieski po jakiś dziwnych klasach - sorry
            ui.button('WSTECZ', on_click=go_prev).props('flat unelevated no-caps').classes('button back').style('color: white !important')
            ui.button('DALEJ', on_click=go_next).props('flat unelevated no-caps').classes('button next').style('color: white !important')

        with ui.card().classes('saaty-table'):
            ui.label('opis skali:')
            with ui.element('div').classes('saaty-row'):
                ui.label('1').classes('saaty-number')
                ui.label('równa ważność').classes('saaty-desc')

            with ui.element('div').classes('saaty-row'):
                ui.label('3').classes('saaty-number')
                ui.label('umiarkowana przewaga').classes('saaty-desc')

            with ui.element('div').classes('saaty-row'):
                ui.label('5').classes('saaty-number')
                ui.label('silna przewaga').classes('saaty-desc')

            with ui.element('div').classes('saaty-row'):
                ui.label('7').classes('saaty-number')
                ui.label('bardzo silna przewaga').classes('saaty-desc')

            with ui.element('div').classes('saaty-row'):
                ui.label('9').classes('saaty-number')
                ui.label('ekstremalna przewaga').classes('saaty-desc')

questionnaire_screen.set_visibility(False)

with ui.column() as finish_screen:

    with ui.card().classes('main-card'):

        ui.label('Dziękujemy za wypełnienie ankiety 🎉').classes('title')

        submit_button = ui.button(
            'ZAPISZ I WYŚLIJ',
            on_click=submit_answers
        ).props('unelevated no-caps').classes('button next')


finish_screen.set_visibility(False)

ui.run()

