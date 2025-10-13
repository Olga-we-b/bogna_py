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

state = {'k': 0} #indeks aktualnego zapytania

def refresh():
    i, j = pairs[state['k']]
    question.set_text(f"Co jest ważniejsze: '{criteria[i]}' czy '{criteria[j]}'?")
    step.set_text(f'Pytanie {state["k"]+1}/{len(pairs)}')
    progress.set_value((state['k'] + 1) / len(pairs))
    btn_prev.disable() if state['k'] == 0 else btn_prev.enable()
    btn_next.disable() if state['k'] == len(pairs) - 1 else btn_next.enable()

def go_prev():
    if state['k'] > 0:
        state['k'] -= 1
        refresh()

def go_next():
    if state['k'] < len(pairs) - 1:
        state['k'] += 1
        refresh()

with ui.card().classes('card'):
    ui.label('AHP').classes('text-lg font-semibold')
    step = ui.label()
    progress = ui.linear_progress(value=0).props('rounded color=green').classes('w-full')
    question = ui.label().classes('text-base')
    with ui.row().classes('button-container'):
        btn_prev = ui.button('← Wstecz', on_click=go_prev).classes('button custom-btn').props('flat no-wrap no-caps')
        btn_next = ui.button('Dalej →', on_click=go_next).classes('button').props('flat no-wrap no-caps')

refresh()
ui.run()
