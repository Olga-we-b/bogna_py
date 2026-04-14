from nicegui import ui
import numpy as np

ui.add_css('assets/style.css')


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
        state['value'] = answers.get(pairs[state['index']], 2)
        set_ui_from_state()

def go_next():
    answers[pairs[state['index']]] = state['value']
    if state['index'] < len(pairs) - 1:
        state['index'] += 1
        state['value'] = answers.get(pairs[state['index']], 2)
        set_ui_from_state()
    else:
        ui.notify('Koniec pytań 🎉')


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

with ui.card().classes('main-card'):
    ui.label('Co jest ważniejsze?').classes('title')
    step_label = ui.label().classes('step')

    with ui.row().classes('criteria-row'):
        label_x = ui.label("x").classes('criterion-box')
        label_y = ui.label('Y').classes('criterion-box')

        direction = ui.radio(
            ['Lewe kryterium ważniejsze', 'Równa ważność', 'Prawe kryterium ważniejsze'],
            value='Lewe kryterium ważniejsze',
            on_change = on_direction_change
        ).classes('direction-radio')

    ui.label('Wskaż, które kryterium jest ważniejsze, a następnie określ siłę przewagi').classes('introduction')
    value_badge = ui.label('25').classes('slider-value')

    slider = ui.slider(min=2, max=9, value=2, step=1).classes('custom-slider')
    def update_badge(e):
        value_badge.set_text(e.value)
    slider.on_value_change(update_badge)
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


set_ui_from_state()

ui.run()


