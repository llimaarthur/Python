import flet as ft

# Solitaire com Flet - Prova de conceito (Steps 1 a 3)
# Step 1: arrastar o cartão com GestureDetector dentro de um Stack
# Step 2: soltar o cartão no slot ou devolvê-lo à posição original
# Step 3: segundo cartão + trazer o cartão arrastado para o topo da pilha
# Os cartões agora usam as mesmas cores dos slots (vermelho, azul, roxo).

# [NOVO] Cole aqui os links diretos das imagens (terminam em .jpg, .png, .webp...)
# Enquanto o link não for preenchido, o cartão continua só com a cor.
IMG_CARD1 = "https://upload.wikimedia.org/wikipedia/pt/b/b4/Corinthians_simbolo.png?utm_source=pt.wikipedia.org&utm_campaign=index&utm_content=original"
IMG_CARD2 = "https://thumb.wikimedia.org/wikipedia/commons/thumb/1/10/Palmeiras_logo.svg/3840px-Palmeiras_logo.svg.png?utm_source=pt.wikipedia.org&utm_campaign=index&utm_content=thumbnail"
IMG_CARD3 = "https://thumb.wikimedia.org/wikipedia/commons/thumb/6/6f/Brasao_do_Sao_Paulo_Futebol_Clube.svg/500px-Brasao_do_Sao_Paulo_Futebol_Clube.svg.png?utm_source=pt.wikipedia.org&utm_campaign=index&utm_content=thumbnail"

# [NOVO] Tamanho do cartão e margem interna entre a borda e a imagem
# (aumente CARD_PADDING para a imagem ficar menor dentro do cartão)
CARD_WIDTH = 90
CARD_HEIGHT = 130
CARD_PADDING = 8

# [NOVO] Distância vertical entre cartões de uma pilha em leque
CARD_OFFSET = 20


# [NOVO] Cria a imagem do cartão; devolve None se o link ainda não foi preenchido
def card_image(src):
    if src.startswith("http"):
        # [AJUSTADO] a imagem cabe inteira dentro do cartão (sem cortar),
        # com o tamanho do cartão menos a margem (padding) de cada lado
        return ft.Image(
            src=src,
            width=CARD_WIDTH - 2 * CARD_PADDING,
            height=CARD_HEIGHT - 2 * CARD_PADDING,
            fit=ft.BoxFit.CONTAIN,
        )
    return None


class Solitaire:
    """Guarda a posição inicial do cartão para o 'bounce back'."""

    def __init__(self):
        self.start_top = 0
        self.start_left = 0
        # [NOVO] cartões que estão sendo arrastados juntos
        self.draggable_pile = []
        # [NOVO] pilha de cada slot e slot de cada cartão (chaves = id do controle)
        self.piles = {}
        self.card_slot = {}


def main(page: ft.Page):
    solitaire = Solitaire()

    # [NOVO] devolve a lista (pilha) de cartões de um slot
    def get_pile(slot):
        return solitaire.piles.setdefault(id(slot), [])

    # [NOVO] posição de um cartão dentro de uma pilha (comparando por identidade)
    def index_in(pile, card):
        for i, c in enumerate(pile):
            if c is card:
                return i
        return -1

    # [NOVO] cartão clicado + todos os cartões abaixo dele na pilha
    def get_draggable_pile(card):
        slot = solitaire.card_slot.get(id(card))
        if slot is None:
            # ainda não está em nenhum slot (distribuição inicial)
            return [card]
        pile = get_pile(slot)
        return pile[index_in(pile, card):]

    def move_on_top(card, controls):
        """Move o cartão arrastado para o topo da lista de controles."""
        controls.remove(card)
        controls.append(card)
        page.update()

    def bounce_back(game, card):
        """Devolve o cartão (e a pilha arrastada) à posição original."""
        # [ALTERADO] agora devolve a pilha inteira ao seu slot, com o leque
        for c in solitaire.draggable_pile:
            slot = solitaire.card_slot[id(c)]
            c.top = slot.top + index_in(get_pile(slot), c) * CARD_OFFSET
            c.left = slot.left
        page.update()

    def place(card, slot):
        """Coloca o cartão (e a pilha arrastada) no slot."""
        # [ALTERADO] coloca a pilha inteira, com deslocamento em leque
        for c in solitaire.draggable_pile:
            # remove o cartão do slot original, se existir
            old_slot = solitaire.card_slot.get(id(c))
            if old_slot is not None:
                old_pile = get_pile(old_slot)
                old_pile[:] = [x for x in old_pile if x is not c]

            # posição depende do tamanho da pilha do novo slot
            pile = get_pile(slot)
            c.top = slot.top + len(pile) * CARD_OFFSET
            c.left = slot.left

            # muda o slot do cartão e adiciona à pilha do novo slot
            solitaire.card_slot[id(c)] = slot
            pile.append(c)
        page.update()

    def start_drag(e: ft.DragStartEvent):
        # [NOVO] descobre quais cartões serão arrastados juntos
        solitaire.draggable_pile = get_draggable_pile(e.control)
        # [ALTERADO] traz a pilha toda para o topo
        for c in solitaire.draggable_pile:
            move_on_top(c, controls)
        solitaire.start_top = e.control.top
        solitaire.start_left = e.control.left
        e.control.update()

    def drag(e: ft.DragUpdateEvent):
        # [ALTERADO] move a pilha toda, mantendo o deslocamento entre os cartões
        new_top = max(0, e.control.top + e.local_delta.y)
        new_left = max(0, e.control.left + e.local_delta.x)
        for i, c in enumerate(solitaire.draggable_pile):
            c.top = new_top + i * CARD_OFFSET
            c.left = new_left
        page.update()

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
        border=ft.Border.all(3, ft.Colors.BLACK),
    )

    slot2 = ft.Container(
        width=90,
        height=130,
        left=400,
        top=200,
        border=ft.Border.all(3, ft.Colors.BLACK),
    )

    slot3 = ft.Container(
        width=90,
        height=130,
        left=0,
        top=0,
        border=ft.Border.all(3, ft.Colors.BLACK),
    )

    slots = [slot1, slot2, slot3]

    # Cartão 1 (vermelho, igual ao slot1)
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
            bgcolor=ft.Colors.PURPLE,
            border_radius=ft.BorderRadius.all(6),
            padding=CARD_PADDING,  # [AJUSTADO]
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS,  # [NOVO]
            content=card_image(IMG_CARD1),  # [NOVO]
        ),
    )

    # Cartão 2 (azul, igual ao slot2)
    card2 = ft.GestureDetector(
        mouse_cursor=ft.MouseCursor.MOVE,
        drag_interval=5,
        on_pan_start=start_drag,
        on_pan_update=drag,
        on_pan_end=drop,
        left=0,
        top=50,
        content=ft.Container(
            width=90,
            height=130,
            bgcolor=ft.Colors.GREEN,
            border_radius=ft.BorderRadius.all(6),
            padding=CARD_PADDING,  # [AJUSTADO]
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS,  # [NOVO]
            content=card_image(IMG_CARD2),  # [NOVO]
        ),
    )

    # Cartão 3 (roxo, igual ao slot3)
    card3 = ft.GestureDetector(
        mouse_cursor=ft.MouseCursor.MOVE,
        drag_interval=5,
        on_pan_start=start_drag,
        on_pan_update=drag,
        on_pan_end=drop,
        left=0,
        top=100,
        content=ft.Container(
            width=90,
            height=130,
            bgcolor=ft.Colors.BLUE,
            border_radius=ft.BorderRadius.all(6),
            padding=CARD_PADDING,  # [AJUSTADO]
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS,  # [NOVO]
            content=card_image(IMG_CARD3),  # [NOVO]
        ),
    )

    controls = slots + [card1, card2, card3]

    page.add(ft.Stack(controls=controls, width=800, height=400))

    # [NOVO] distribui os cartões no slot3 (o slot em left=0, top=0), em leque
    for card in (card1, card2, card3):
        solitaire.draggable_pile = [card]
        place(card, slot3)


ft.run(main)