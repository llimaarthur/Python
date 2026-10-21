import flet as ft

# Solitaire com Flet - Prova de conceito (Steps 1 a 3)
# Step 1: arrastar o cartão com GestureDetector dentro de um Stack
# Step 2: soltar o cartão no slot ou devolvê-lo à posição original
# Step 3: segundo cartão + trazer o cartão arrastado para o topo da pilha

# Cole aqui os links diretos das imagens (terminam em .png, .jpg, .svg...)
IMG_CARD1 = "COLE_O_LINK_DA_IMAGEM_1"
IMG_CARD2 = "COLE_O_LINK_DA_IMAGEM_2"
IMG_CARD3 = "COLE_O_LINK_DA_IMAGEM_3"


class Solitaire:
    """Guarda a posição inicial do cartão para o 'bounce back'."""

    def __init__(self):
        self.start_top = 0
        self.start_left = 0


def main(page: ft.Page):
    solitaire = Solitaire()

    def move_on_top(card, controls):
        """Move o cartão arrastado para o topo da lista de controles."""
        controls.remove(card)
        controls.append(card)
        page.update()

    def bounce_back(game, card):
        """Devolve o cartão à posição original."""
        card.top = game.start_top
        card.left = game.start_left
        page.update()

    def place(card, slot):
        """Coloca o cartão no slot."""
        card.top = slot.top
        card.left = slot.left
        page.update()

    def start_drag(e: ft.DragStartEvent):
        move_on_top(e.control, controls)
        solitaire.start_top = e.control.top
        solitaire.start_left = e.control.left
        e.control.update()

    def drag(e: ft.DragUpdateEvent):
        e.control.top = max(0, e.control.top + e.local_delta.y)
        e.control.left = max(0, e.control.left + e.local_delta.x)
        e.control.update()

    def drop(e: ft.DragEndEvent):
        # Testa cada slot da lista; encaixa no primeiro que estiver perto
        for slot in slots:
            if (
                abs(e.control.top - slot.top) < 50
                and abs(e.control.left - slot.left) < 50
            ):
                place(e.control, slot)
                e.control.update()
                return

        # Nenhum slot por perto: volta para a posição original
        bounce_back(solitaire, e.control)
        e.control.update()

    # Slots onde os cartões podem ser soltos
    slot1 = ft.Container(
        width=90,
        height=130,
        left=500,
        top=200,
        border=ft.Border.all(3, ft.Colors.RED),
    )

    slot2 = ft.Container(
        width=90,
        height=130,
        left=400,
        top=200,
        border=ft.Border.all(3, ft.Colors.BLUE),
    )

    slot3 = ft.Container(
        width=90,
        height=130,
        left=600,
        top=200,
        border=ft.Border.all(3, ft.Colors.PURPLE),
    )

    slots = [slot1, slot2, slot3]

    # Cartão 1 (imagem)
    card1 = ft.GestureDetector(
        mouse_cursor=ft.MouseCursor.MOVE,
        drag_interval=5,
        on_pan_start=start_drag,
        on_pan_update=drag,
        on_pan_end=drop,
        left=0,
        top=0,
        content=ft.Container(
            width=90,
            height=130,
            border_radius=ft.BorderRadius.all(6),
            content=ft.Image(src=""),
        ),
    )

    # Cartão 2 (imagem)
    card2 = ft.GestureDetector(
        mouse_cursor=ft.MouseCursor.MOVE,
        drag_interval=5,
        on_pan_start=start_drag,
        on_pan_update=drag,
        on_pan_end=drop,
        left=100,
        top=0,
        content=ft.Container(
            width=90,
            height=130,
            border_radius=ft.BorderRadius.all(6),
            content=ft.Image(src=""),
        ),
    )

    # Cartão 3 (imagem)
    card3 = ft.GestureDetector(
        mouse_cursor=ft.MouseCursor.MOVE,
        drag_interval=5,
        on_pan_start=start_drag,
        on_pan_update=drag,
        on_pan_end=drop,
        left=200,
        top=0,
        content=ft.Container(
            width=90,
            height=130,
            border_radius=ft.BorderRadius.all(6),
            content=ft.Image(src=""),
        ),
    )

    controls = slots + [card1, card2, card3]

    page.add(ft.Stack(controls=controls, width=800, height=400))


ft.run(main)