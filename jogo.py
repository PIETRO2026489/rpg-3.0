import pygame
import random
import json
import os
import math

# ============================================================
# REINO DE ELEMENTARIA
# ============================================================

pygame.init()

WIDTH, HEIGHT = 1100, 700
FPS = 60
SAVE_FILE = "elementaria_save.json"

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Reino de Elementaria")
clock = pygame.time.Clock()

# ============================================================
# CORES
# ============================================================

WHITE = (245, 245, 245)
BLACK = (15, 15, 20)
GRAY = (80, 80, 90)
DARK_GRAY = (35, 35, 45)

GREEN = (60, 190, 80)
RED = (210, 55, 55)
BLUE = (50, 130, 220)
YELLOW = (240, 210, 50)
ORANGE = (240, 120, 30)
PURPLE = (145, 70, 190)
CYAN = (50, 210, 220)
BROWN = (130, 85, 45)
ICE = (150, 225, 245)

DARK_GREEN = (35, 100, 45)
LIGHT_GREEN = (120, 220, 120)
STONE = (105, 105, 115)
DARK_STONE = (60, 60, 70)

FONT = pygame.font.SysFont("arial", 20)
SMALL = pygame.font.SysFont("arial", 16)
BIG = pygame.font.SysFont("arial", 32, bold=True)
TITLE = pygame.font.SysFont("arial", 48, bold=True)

# ============================================================
# ELEMENTOS
# ============================================================

ELEMENTS = {
    "Fogo": {
        "icon": "FOGO",
        "color": ORANGE,
        "weak": ["Água"],
        "strong": ["Planta"],
        "attacks": [
            ("Brasa", 20, 25, 10, 15),
            ("Bola de Fogo", 30, 40, 15, 25),
            ("Explosão de Fogo", 45, 55, 30, 45),
        ],
    },
    "Água": {
        "icon": "AGUA",
        "color": BLUE,
        "weak": ["Elétrico"],
        "strong": ["Fogo"],
        "attacks": [
            ("Jato d'Água", 20, 25, 10, 15),
            ("Surfar", 30, 40, 15, 25),
            ("Hidro Bomba", 45, 55, 30, 45),
        ],
    },
    "Elétrico": {
        "icon": "ELETRICO",
        "color": YELLOW,
        "weak": ["Planta"],
        "strong": ["Água"],
        "attacks": [
            ("Faísca", 20, 25, 10, 15),
            ("Raio", 30, 40, 15, 25),
            ("Trovoada", 45, 55, 30, 45),
        ],
    },
    "Planta": {
        "icon": "PLANTA",
        "color": GREEN,
        "weak": ["Fogo"],
        "strong": ["Elétrico"],
        "attacks": [
            ("Chicote de Vinha", 20, 25, 10, 15),
            ("Folha Navalha", 30, 40, 15, 25),
            ("Bomba de Sementes", 45, 55, 30, 45),
        ],
    },
    "Sombrio": {
        "icon": "SOMBRA",
        "color": PURPLE,
        "weak": [],
        "strong": ["Fogo", "Água", "Elétrico", "Planta"],
        "attacks": [
            ("Sombra", 18, 24, 10, 15),
            ("Trevas", 30, 40, 15, 25),
            ("Abismo", 45, 60, 30, 45),
        ],
    },
    "Terra": {
        "icon": "TERRA",
        "color": BROWN,
        "weak": ["Voador"],
        "strong": ["Veneno"],
        "attacks": [
            ("Pedrada", 20, 25, 10, 15),
            ("Tremor", 30, 40, 15, 25),
            ("Terremoto", 45, 55, 30, 45),
        ],
    },
    "Voador": {
        "icon": "VOADOR",
        "color": CYAN,
        "weak": ["Gelo"],
        "strong": ["Terra"],
        "attacks": [
            ("Rajada", 20, 25, 10, 15),
            ("Corte de Ar", 30, 40, 15, 25),
            ("Tempestade", 45, 55, 30, 45),
        ],
    },
    "Gelo": {
        "icon": "GELO",
        "color": ICE,
        "weak": ["Fogo"],
        "strong": ["Voador"],
        "attacks": [
            ("Estilhaço", 20, 25, 10, 15),
            ("Lança de Gelo", 30, 40, 15, 25),
            ("Nevasca", 45, 55, 30, 45),
        ],
    },
    "Fantasma": {
        "icon": "FANTASMA",
        "color": PURPLE,
        "weak": ["Veneno"],
        "strong": ["Água", "Fogo", "Planta", "Elétrico"],
        "attacks": [
            ("Susto", 20, 25, 10, 15),
            ("Alma Sombria", 30, 40, 15, 25),
            ("Possessão", 45, 55, 30, 45),
        ],
    },
    "Veneno": {
        "icon": "VENENO",
        "color": GREEN,
        "weak": ["Terra"],
        "strong": ["Fantasma"],
        "attacks": [
            ("Veneno", 20, 25, 10, 15),
            ("Ácido", 30, 40, 15, 25),
            ("Explosão Tóxica", 45, 55, 30, 45),
        ],
    },
}

# ============================================================
# ILHAS
# ============================================================

ISLANDS = [
    ("Ilha Inicial", "Planta", (75, 160, 80), "A ilha onde a aventura começa."),
    ("Ilha Vulcânica", "Fogo", (190, 65, 35), "Vulcões e rios de lava."),
    ("Ilha Aquática", "Água", (40, 130, 200), "Uma ilha cercada por mares."),
    ("Ilha Eletrônica", "Elétrico", (100, 100, 150), "Fábricas e máquinas elétricas."),
    ("Ilha Sombria", "Sombrio", (55, 45, 70), "Construções abandonadas."),
    ("Ilha de Terra", "Terra", (145, 105, 65), "Montanhas e terrenos rochosos."),
    ("Ilha Voadora", "Voador", (150, 205, 235), "Ilhas flutuantes."),
    ("Ilha de Gelo", "Gelo", (165, 220, 240), "Uma região congelada."),
    ("Ilha Fantasmagórica", "Fantasma", (90, 70, 110), "Prédios habitados por fantasmas."),
    ("Ilha Venenosa", "Veneno", (90, 145, 65), "Uma ilha cheia de perigos."),
]

LEVEL_RANGES = [
    (1, 2), (2, 4), (3, 5), (4, 7), (5, 8),
    (6, 10), (8, 10), (9, 10), (10, 10), (10, 10)
]

MONSTER_NAMES = {
    "Planta": ["Floragron", "Vinhante", "Sementouro"],
    "Fogo": ["Braseiro", "Lavagor", "Ignifera"],
    "Água": ["Aquanix", "Maréon", "Peixor"],
    "Elétrico": ["Voltix", "Choquim", "Eletrodrone"],
    "Sombrio": ["Sombruxo", "Trevor", "Noctus"],
    "Terra": ["Pedrano", "Terragor", "Montor"],
    "Voador": ["Aviãoz", "Penas", "Ventor"],
    "Gelo": ["Gelix", "Cristalor", "Glacius"],
    "Fantasma": ["Fantomin", "Assustor", "Espectro"],
    "Veneno": ["Serpentox", "Tóxix", "Peçonha"],
}

SHOP_ITEMS = {
    "Armadura de Ferro": 250,
    "Armadura de Escamas": 350,
    "Cajado Arcano": 150,
    "Espada de Ferro": 200,
    "Escudo Elemental": 300,
}

owned_items = []

# ============================================================
# JOGADOR
# ============================================================

class Player:

    def __init__(self):
        self.x = 550
        self.y = 350

        self.level = 1
        self.level_xp = 0

        self.element = None
        self.element_level = 1
        self.element_xp = 0

        self.max_hp = 100
        self.hp = 100

        self.max_mana = 100
        self.mana = 100

        self.coins = 100

        self.armor = None
        self.staff = False
        self.sword = False
        self.shield = False

        self.scrolls = []

        self.monsters_defeated = 0
        self.different_monsters = set()

        self.missions = {
            "first_monster": False,
            "five_monsters": False,
            "final_boss": False,
        }

        self.unlocked_islands = 1
        self.dungeons_completed = []

    def elemental_bonus(self):
        return max(0, self.element_level - 1) * 5

    def defense(self):
        if self.armor == "Armadura de Ferro":
            return 10
        if self.armor == "Armadura de Escamas":
            return 25
        return 0

    def physical_damage(self):
        return 30 if self.sword else 10

    def gain_xp(self, amount):
        self.level_xp += amount

        # ====================================================
        # NÍVEL MÁXIMO = 10
        # ====================================================

        while self.level < 10 and self.level_xp >= 100:
            self.level_xp -= 100
            self.level += 1

            self.max_hp += 20
            self.max_mana += 20

            self.hp = self.max_hp
            self.mana = self.max_mana

            show_message(
                f"Você subiu para o nível {self.level}!"
            )

        # Nunca permite passar do nível 10.
        if self.level >= 10:
            self.level = 10
            self.level_xp = min(self.level_xp, 99)

    def gain_element_xp(self, amount):
        self.element_xp += amount

        while self.element_level < 5 and self.element_xp >= 100:
            self.element_xp -= 100
            self.element_level += 1

            show_message(
                f"Seu elemento chegou ao nível {self.element_level}!"
            )

    def heal(self):
        self.hp = self.max_hp
        self.mana = self.max_mana


# ============================================================
# MONSTRO
# ============================================================

class Monster:

    def __init__(self, element, level):
        self.element = element
        self.level = max(1, min(10, level))

        self.name = random.choice(
            MONSTER_NAMES[element]
        )

        self.max_hp = 55 + self.level * 24
        self.hp = self.max_hp

        self.max_mana = 40 + self.level * 10
        self.mana = self.max_mana

        self.speed = 1.0 + self.level * 0.07

        self.x = 0
        self.y = 0

    def damage(self):
        return random.randint(
            6 + self.level * 2,
            11 + self.level * 3
        )


# ============================================================
# DRAGÃO
# ============================================================

class Dragon:

    def __init__(self):
        self.name = "Dragão Guardião de Elementaria"
        self.element = "Sombrio"
        self.max_hp = 1200
        self.hp = self.max_hp
        self.level = 20

    def damage(self):
        return random.randint(30, 50)


dragon = Dragon()

# ============================================================
# ESTADO DO JOGO
# ============================================================

player = Player()

game_state = "menu"
current_island = 0
current_monster = None

monsters_on_map = []

battle_log = []
battle_turn = True

message = ""
message_timer = 0

dungeon_active = False
dungeon_monsters_left = 0
dungeon_total_defeated = 0

# ============================================================
# UTILIDADES
# ============================================================

def text(surface, value, x, y, color=WHITE, font=FONT):
    surface.blit(
        font.render(str(value), True, color),
        (int(x), int(y))
    )


def center_text(surface, value, y, color=WHITE, font=FONT):
    obj = font.render(str(value), True, color)

    surface.blit(
        obj,
        ((WIDTH - obj.get_width()) // 2, y)
    )


def show_message(msg, seconds=3):
    global message, message_timer

    message = msg
    message_timer = seconds * FPS


def draw_bar(x, y, width, height, value, maximum, color):
    pygame.draw.rect(
        screen,
        DARK_GRAY,
        (x, y, width, height)
    )

    if maximum > 0:
        current = int(
            width * max(0, value) / maximum
        )

        pygame.draw.rect(
            screen,
            color,
            (x, y, current, height)
        )

    pygame.draw.rect(
        screen,
        WHITE,
        (x, y, width, height),
        2
    )


# ============================================================
# SALVAR
# ============================================================

def save_game():

    data = {
        "x": player.x,
        "y": player.y,

        "level": min(player.level, 10),
        "level_xp": player.level_xp,

        "element": player.element,
        "element_level": player.element_level,
        "element_xp": player.element_xp,

        "max_hp": player.max_hp,
        "hp": player.hp,

        "max_mana": player.max_mana,
        "mana": player.mana,

        "coins": player.coins,

        "armor": player.armor,
        "staff": player.staff,
        "sword": player.sword,
        "shield": player.shield,

        "scrolls": player.scrolls,

        "monsters_defeated": player.monsters_defeated,
        "different_monsters": list(
            player.different_monsters
        ),

        "missions": player.missions,

        "unlocked_islands": player.unlocked_islands,
        "dungeons_completed": player.dungeons_completed,

        "current_island": current_island,
        "owned_items": owned_items,
    }

    try:
        with open(
            SAVE_FILE,
            "w",
            encoding="utf-8"
        ) as file:
            json.dump(
                data,
                file,
                ensure_ascii=False,
                indent=4
            )

        show_message("Jogo salvo!")

    except Exception as error:
        print(error)
        show_message("Erro ao salvar o jogo.")


# ============================================================
# CARREGAR
# ============================================================

def load_game():

    global current_island

    if not os.path.exists(SAVE_FILE):
        show_message("Nenhum jogo salvo.")
        return False

    try:
        with open(
            SAVE_FILE,
            "r",
            encoding="utf-8"
        ) as file:
            data = json.load(file)

        player.x = data.get("x", 550)
        player.y = data.get("y", 350)

        # ====================================================
        # CORREÇÃO DE SAVE ANTIGO
        # NUNCA PASSA DO NÍVEL 10
        # ====================================================

        player.level = min(
            10,
            data.get("level", 1)
        )

        player.level_xp = data.get(
            "level_xp",
            0
        )

        if player.level >= 10:
            player.level_xp = min(
                player.level_xp,
                99
            )

        player.element = data.get(
            "element"
        )

        player.element_level = data.get(
            "element_level",
            1
        )

        player.element_xp = data.get(
            "element_xp",
            0
        )

        player.max_hp = data.get(
            "max_hp",
            100
        )

        player.hp = min(
            data.get("hp", player.max_hp),
            player.max_hp
        )

        player.max_mana = data.get(
            "max_mana",
            100
        )

        player.mana = min(
            data.get("mana", player.max_mana),
            player.max_mana
        )

        player.coins = data.get(
            "coins",
            100
        )

        player.armor = data.get("armor")
        player.staff = data.get("staff", False)
        player.sword = data.get("sword", False)
        player.shield = data.get("shield", False)

        player.scrolls = data.get(
            "scrolls",
            []
        )

        player.monsters_defeated = data.get(
            "monsters_defeated",
            0
        )

        player.different_monsters = set(
            data.get(
                "different_monsters",
                []
            )
        )

        player.missions = data.get(
            "missions",
            player.missions
        )

        player.unlocked_islands = min(
            len(ISLANDS),
            data.get(
                "unlocked_islands",
                1
            )
        )

        player.dungeons_completed = data.get(
            "dungeons_completed",
            []
        )

        current_island = min(
            len(ISLANDS) - 1,
            data.get(
                "current_island",
                0
            )
        )

        owned_items.clear()

        owned_items.extend(
            data.get(
                "owned_items",
                []
            )
        )

        show_message("Jogo carregado!")

        return True

    except Exception as error:

        print(
            "Erro ao carregar:",
            error
        )

        show_message(
            "Erro ao carregar o jogo."
        )

        return False


# ============================================================
# ELEMENTO
# ============================================================

def draw_element_selection():

    screen.fill(BLACK)

    center_text(
        screen,
        "ESCOLHA SEU ELEMENTO",
        50,
        WHITE,
        TITLE
    )

    center_text(
        screen,
        "1 - Fogo     2 - Água     3 - Elétrico     4 - Planta",
        120
    )

    elements = [
        "Fogo",
        "Água",
        "Elétrico",
        "Planta"
    ]

    for i, element in enumerate(elements):

        x = 100 + i * 250

        pygame.draw.rect(
            screen,
            ELEMENTS[element]["color"],
            (x, 220, 200, 250),
            border_radius=20
        )

        center = x + 100

        icon = FONT.render(
            ELEMENTS[element]["icon"],
            True,
            WHITE
        )

        screen.blit(
            icon,
            (
                center - icon.get_width() // 2,
                260
            )
        )

        obj = BIG.render(
            element,
            True,
            WHITE
        )

        screen.blit(
            obj,
            (
                center - obj.get_width() // 2,
                320
            )
        )

        text(
            screen,
            "Ataque 1 - Nv. 1",
            x + 25,
            380,
            WHITE,
            SMALL
        )

        text(
            screen,
            "Ataque 2 - Nv. 2",
            x + 25,
            410,
            WHITE,
            SMALL
        )

        text(
            screen,
            "Ataque 3 - Nv. 4",
            x + 25,
            440,
            WHITE,
            SMALL
        )


# ============================================================
# MENU
# ============================================================

def draw_menu():

    screen.fill(
        (20, 25, 40)
    )

    center_text(
        screen,
        "REINO DE ELEMENTARIA",
        100,
        YELLOW,
        TITLE
    )

    center_text(
        screen,
        "RPG de aventura elemental",
        165
    )

    buttons = [
        ("1 - NOVO JOGO", 270),
        ("2 - CARREGAR JOGO", 340),
        ("3 - SAIR", 410),
    ]

    for label, y in buttons:

        pygame.draw.rect(
            screen,
            (50, 70, 100),
            (400, y, 300, 55),
            border_radius=10
        )

        center_text(
            screen,
            label,
            y + 15
        )


# ============================================================
# ÁRVORES / PEDRAS
# ============================================================

def draw_tree(x, y, size=1):

    pygame.draw.rect(
        screen,
        BROWN,
        (
            x - int(7 * size),
            y,
            int(14 * size),
            int(40 * size)
        )
    )

    pygame.draw.circle(
        screen,
        DARK_GREEN,
        (x, y),
        int(28 * size)
    )

    pygame.draw.circle(
        screen,
        GREEN,
        (
            x - int(12 * size),
            y - int(10 * size)
        ),
        int(20 * size)
    )

    pygame.draw.circle(
        screen,
        LIGHT_GREEN,
        (
            x + int(12 * size),
            y - int(7 * size)
        ),
        int(18 * size)
    )


def draw_rock(x, y, size=1):

    pygame.draw.ellipse(
        screen,
        STONE,
        (
            x - int(25 * size),
            y - int(15 * size),
            int(50 * size),
            int(30 * size)
        )
    )


# ============================================================
# MAPA
# ============================================================

def draw_island():

    island_name, element, island_color, description = ISLANDS[
        current_island
    ]

    screen.fill(
        (30, 130, 190)
    )

    pygame.draw.rect(
        screen,
        island_color,
        (50, 50, WIDTH - 100, HEIGHT - 100),
        border_radius=35
    )

    # Cenário básico
    for x, y, size in [
        (150, 150, 1),
        (900, 150, 1),
        (250, 520, 0.8),
        (900, 520, 0.8),
    ]:
        draw_tree(x, y, size)

    for x, y in [
        (350, 500),
        (850, 300),
        (300, 350)
    ]:
        draw_rock(x, y)

    # ========================================================
    # LOJA
    # ========================================================

    if current_island == 0:

        pygame.draw.rect(
            screen,
            (220, 180, 140),
            (450, 120, 100, 80)
        )

        pygame.draw.polygon(
            screen,
            RED,
            [
                (440, 120),
                (500, 70),
                (560, 120)
            ]
        )

        pygame.draw.rect(
            screen,
            BROWN,
            (485, 160, 30, 40)
        )

        # CORRIGIDO:
        # O texto agora fica junto da loja.
        text(
            screen,
            "LOJA",
            475,
            205,
            BLACK,
            SMALL
        )

        # Médico
        pygame.draw.rect(
            screen,
            WHITE,
            (120, 400, 100, 90)
        )

        pygame.draw.rect(
            screen,
            RED,
            (160, 420, 20, 50)
        )

        pygame.draw.rect(
            screen,
            RED,
            (145, 435, 50, 20)
        )

        text(
            screen,
            "MÉDICO",
            125,
            470,
            BLACK,
            SMALL
        )

        pygame.draw.circle(
            screen,
            BLUE,
            (650, 300),
            50
        )

        pygame.draw.circle(
            screen,
            CYAN,
            (650, 300),
            35
        )

    # Jogador
    pygame.draw.circle(
        screen,
        ELEMENTS[player.element]["color"],
        (
            int(player.x),
            int(player.y)
        ),
        18
    )

    pygame.draw.circle(
        screen,
        WHITE,
        (
            int(player.x),
            int(player.y)
        ),
        18,
        2
    )

    text(
        screen,
        "MAGO",
        player.x - 25,
        player.y - 42,
        WHITE,
        SMALL
    )

    draw_hud()

    for monster in monsters_on_map:
        draw_monster(monster)

    draw_world_help()


# ============================================================
# HUD
# ============================================================

def draw_hud():

    pygame.draw.rect(
        screen,
        (20, 20, 30),
        (0, 0, WIDTH, 80)
    )

    text(
        screen,
        f"Lv {player.level}/10",
        20,
        10
    )

    text(
        screen,
        f"Elemento: {player.element}",
        20,
        38,
        ELEMENTS[player.element]["color"]
    )

    draw_bar(
        220,
        10,
        200,
        22,
        player.hp,
        player.max_hp,
        RED
    )

    draw_bar(
        220,
        42,
        200,
        22,
        player.mana,
        player.max_mana,
        BLUE
    )

    text(
        screen,
        f"{player.hp}/{player.max_hp}",
        430,
        10,
        WHITE,
        SMALL
    )

    text(
        screen,
        f"{player.mana}/{player.max_mana}",
        430,
        42,
        WHITE,
        SMALL
    )

    text(
        screen,
        f"Moedas: {player.coins}",
        520,
        20,
        YELLOW
    )

    text(
        screen,
        f"Elemento Lv.{player.element_level}",
        650,
        20
    )

    text(
        screen,
        f"Ilha: {ISLANDS[current_island][0]}",
        830,
        20,
        WHITE,
        SMALL
    )


# ============================================================
# MONSTROS
# ============================================================

def get_monster_level():

    minimum, maximum = LEVEL_RANGES[
        current_island
    ]

    return random.randint(
        minimum,
        maximum
    )


def spawn_monsters():

    global monsters_on_map

    monsters_on_map = []

    element = ISLANDS[
        current_island
    ][1]

    for _ in range(
        random.randint(3, 5)
    ):

        monster = Monster(
            element,
            get_monster_level()
        )

        while True:

            monster.x = random.randint(
                120,
                950
            )

            monster.y = random.randint(
                120,
                570
            )

            distance = math.hypot(
                monster.x - player.x,
                monster.y - player.y
            )

            if distance > 130:
                break

        monsters_on_map.append(
            monster
        )


def draw_monster(monster):

    color = ELEMENTS[
        monster.element
    ]["color"]

    pygame.draw.circle(
        screen,
        color,
        (
            int(monster.x),
            int(monster.y)
        ),
        23
    )

    pygame.draw.circle(
        screen,
        BLACK,
        (
            int(monster.x - 8),
            int(monster.y - 5)
        ),
        4
    )

    pygame.draw.circle(
        screen,
        BLACK,
        (
            int(monster.x + 8),
            int(monster.y - 5)
        ),
        4
    )

    text(
        screen,
        f"{monster.name} Lv.{monster.level}",
        monster.x - 55,
        monster.y - 48,
        WHITE,
        SMALL
    )


def move_monsters():

    for monster in monsters_on_map:

        dx = player.x - monster.x
        dy = player.y - monster.y

        distance = math.hypot(
            dx,
            dy
        )

        if distance > 45:

            monster.x += (
                dx / max(distance, 1)
            ) * monster.speed

            monster.y += (
                dy / max(distance, 1)
            ) * monster.speed

        elif distance < 45:

            start_battle(monster)
            return


# ============================================================
# BATALHA
# ============================================================

def start_battle(monster):

    global current_monster
    global game_state
    global battle_turn

    current_monster = monster
    battle_turn = True

    game_state = "battle"

    battle_log.clear()

    battle_log.append(
        f"{monster.name} apareceu!"
    )


def draw_battle():

    screen.fill(
        (25, 25, 40)
    )

    center_text(
        screen,
        "BATALHA",
        20,
        YELLOW,
        TITLE
    )

    # Jogador
    pygame.draw.circle(
        screen,
        ELEMENTS[player.element]["color"],
        (230, 230),
        70
    )

    text(
        screen,
        "MAGO",
        200,
        320,
        WHITE,
        BIG
    )

    draw_bar(
        130,
        365,
        220,
        25,
        player.hp,
        player.max_hp,
        RED
    )

    draw_bar(
        130,
        400,
        220,
        25,
        player.mana,
        player.max_mana,
        BLUE
    )

    # Inimigo
    color = ELEMENTS[
        current_monster.element
    ]["color"]

    pygame.draw.circle(
        screen,
        color,
        (850, 230),
        80
    )

    text(
        screen,
        current_monster.name,
        760,
        330,
        WHITE,
        BIG
    )

    text(
        screen,
        f"Lv. {current_monster.level}",
        760,
        370
    )

    text(
        screen,
        f"Elemento: {current_monster.element}",
        760,
        395,
        color
    )

    draw_bar(
        730,
        430,
        240,
        25,
        current_monster.hp,
        current_monster.max_hp,
        RED
    )

    pygame.draw.rect(
        screen,
        DARK_GRAY,
        (80, 500, 940, 70)
    )

    for i, log in enumerate(
        battle_log[-3:]
    ):

        text(
            screen,
            log,
            100,
            510 + i * 20,
            WHITE,
            SMALL
        )

    actions = [
        ("1 - Elemental 1", 100),
        ("2 - Elemental 2", 330),
        ("3 - Elemental 3", 560),
        ("4 - Punho/Espada", 790),
    ]

    for label, x in actions:

        pygame.draw.rect(
            screen,
            (55, 65, 90),
            (x, 600, 200, 45),
            border_radius=8
        )

        text(
            screen,
            label,
            x + 10,
            612,
            WHITE,
            SMALL
        )

    text(
        screen,
        "H - Poção de vida | P - Poção de mana | ESC - Sair",
        350,
        660,
        WHITE,
        SMALL
    )


def elemental_multiplier(attacker, defender):

    if defender in ELEMENTS[attacker]["weak"]:
        return 0.65

    if defender in ELEMENTS[attacker]["strong"]:
        return 1.5

    return 1.0


def player_attack(index):

    global battle_turn

    if not battle_turn or current_monster is None:
        return

    if index == 3:

        damage = player.physical_damage()

        current_monster.hp -= damage

        battle_log.append(
            f"Você causou {damage} de dano físico!"
        )

        end_player_turn()
        return

    required = {
        0: 1,
        1: 2,
        2: 4
    }[index]

    if player.element_level < required:

        battle_log.append(
            f"Precisa do nível elemental {required}."
        )

        return

    attack = ELEMENTS[
        player.element
    ]["attacks"][index]

    name, min_d, max_d, min_m, max_m = attack

    cost = random.randint(
        min_m,
        max_m
    )

    if player.mana < cost:

        battle_log.append(
            "Mana insuficiente!"
        )

        return

    player.mana -= cost

    damage = random.randint(
        min_d,
        max_d
    )

    damage += player.elemental_bonus()

    if player.staff:
        damage += 15

    damage = int(
        damage *
        elemental_multiplier(
            player.element,
            current_monster.element
        )
    )

    current_monster.hp -= damage

    battle_log.append(
        f"{name}: {damage} dano! (-{cost} mana)"
    )

    end_player_turn()


def end_player_turn():

    global battle_turn

    if current_monster is None:
        return

    if current_monster.hp <= 0:
        win_battle()
        return

    player.mana = min(
        player.max_mana,
        player.mana + random.randint(10, 25)
    )

    battle_turn = False

    enemy_attack()

    battle_turn = True


def enemy_attack():

    if current_monster is None:
        return

    if current_monster.hp <= 0:
        return

    damage = current_monster.damage()

    if player.shield and random.random() < 0.30:

        battle_log.append(
            "Você desviou do ataque!"
        )

        return

    damage = int(
        damage *
        (1 - player.defense() / 100)
    )

    damage = max(
        1,
        damage
    )

    player.hp -= damage

    battle_log.append(
        f"{current_monster.name} causou {damage} de dano!"
    )

    if player.hp <= 0:
        player.hp = 0
        game_over()


# ============================================================
# RECOMPENSAS
# ============================================================

def monster_coin_reward(level):

    if level <= 2:
        return random.randint(8, 18)

    if level <= 5:
        return random.randint(12, 25)

    if level <= 8:
        return random.randint(18, 32)

    return random.randint(25, 40)


def monster_xp_reward(level):

    return random.randint(
        15 + level * 3,
        25 + level * 4
    )


def win_battle():

    global current_monster
    global game_state
    global dungeon_monsters_left
    global dungeon_active

    monster = current_monster

    if monster is None:
        return

    coins = monster_coin_reward(
        monster.level
    )

    xp = monster_xp_reward(
        monster.level
    )

    element_xp = random.randint(
        8,
        20
    )

    player.coins += coins
    player.gain_xp(xp)
    player.gain_element_xp(element_xp)

    player.monsters_defeated += 1

    player.different_monsters.add(
        monster.name
    )

    if not player.missions["first_monster"]:

        player.missions["first_monster"] = True
        player.coins += 25
        player.gain_xp(15)

    if (
        len(player.different_monsters) >= 5
        and not player.missions["five_monsters"]
    ):

        player.missions["five_monsters"] = True
        player.coins += 50
        player.gain_xp(30)

    # ========================================================
    # MASMORRA
    # ========================================================

    if dungeon_active:

        dungeon_monsters_left -= 1

        current_monster = None

        if dungeon_monsters_left > 0:

            game_state = "dungeon"

            show_message(
                f"Monstro derrotado! "
                f"Faltam {dungeon_monsters_left}.",
                3
            )

        else:

            element = ISLANDS[
                current_island
            ][1]

            reward_coins = random.randint(
                35,
                50
            )

            reward_xp = random.randint(
                40,
                55
            )

            player.coins += reward_coins
            player.gain_xp(reward_xp)

            if element not in player.scrolls:
                player.scrolls.append(element)

            if current_island + 2 > player.unlocked_islands:

                player.unlocked_islands = min(
                    len(ISLANDS),
                    current_island + 2
                )

            if current_island not in player.dungeons_completed:

                player.dungeons_completed.append(
                    current_island
                )

            dungeon_active = False
            dungeon_monsters_left = 0
            current_monster = None

            game_state = "world"

            show_message(
                f"MASMORRA CONCLUÍDA! "
                f"Pergaminho de {element} recebido! "
                f"+{reward_coins} moedas!",
                5
            )

        return

    # ========================================================
    # BATALHA NORMAL
    # ========================================================

    if monster in monsters_on_map:
        monsters_on_map.remove(monster)

    current_monster = None
    game_state = "world"

    show_message(
        f"Vitória! +{coins} moedas, "
        f"+{xp} XP e +{element_xp} XP elemental."
    )


# ============================================================
# POÇÕES
# ============================================================

def use_health_potion():

    if player.coins < 15:

        battle_log.append(
            "Moedas insuficientes."
        )

        return

    player.coins -= 15

    amount = random.randint(
        20,
        35
    )

    player.hp = min(
        player.max_hp,
        player.hp + amount
    )

    battle_log.append(
        f"Poção recuperou {amount} de vida."
    )

    end_player_turn()


def use_mana_potion():

    if player.coins < 20:

        battle_log.append(
            "Moedas insuficientes."
        )

        return

    player.coins -= 20

    amount = random.randint(
        20,
        35
    )

    player.mana = min(
        player.max_mana,
        player.mana + amount
    )

    battle_log.append(
        f"Poção recuperou {amount} de mana."
    )

    end_player_turn()


# ============================================================
# MASMORRA
# ============================================================

def enter_dungeon():

    global dungeon_active
    global dungeon_monsters_left
    global game_state

    if current_island in player.dungeons_completed:

        show_message(
            "Esta masmorra já foi concluída!"
        )

        return

    dungeon_active = True
    dungeon_monsters_left = 3

    game_state = "dungeon"

    show_message(
        "Você entrou na masmorra! Derrote 3 monstros.",
        4
    )


def draw_dungeon():

    screen.fill(
        (35, 30, 42)
    )

    center_text(
        screen,
        "MASMORRA",
        20,
        YELLOW,
        TITLE
    )

    center_text(
        screen,
        ISLANDS[current_island][0],
        80
    )

    center_text(
        screen,
        "VOCÊ ESTÁ PRESO!",
        140,
        RED,
        BIG
    )

    center_text(
        screen,
        "Derrote os 3 monstros para sair.",
        190
    )

    pygame.draw.rect(
        screen,
        (50, 45, 60),
        (300, 240, 500, 100),
        border_radius=12
    )

    center_text(
        screen,
        f"MONSTROS RESTANTES: {dungeon_monsters_left}",
        275,
        YELLOW
    )

    if dungeon_monsters_left > 0:

        center_text(
            screen,
            "ENTER - Enfrentar próximo monstro",
            430,
            GREEN,
            BIG
        )

    center_text(
        screen,
        "ESC - BLOQUEADO",
        520,
        RED
    )


def start_dungeon_battle():

    element = ISLANDS[
        current_island
    ][1]

    monster = Monster(
        element,
        get_monster_level()
    )

    start_battle(monster)


# ============================================================
# LOJA
# ============================================================

def draw_shop():

    screen.fill(
        (35, 35, 45)
    )

    center_text(
        screen,
        "LOJA",
        30,
        YELLOW,
        TITLE
    )

    y = 110

    for i, (item, price) in enumerate(
        SHOP_ITEMS.items()
    ):

        pygame.draw.rect(
            screen,
            (60, 70, 90),
            (120, y, 600, 55),
            border_radius=8
        )

        text(
            screen,
            f"{i + 1}. {item}",
            140,
            y + 16
        )

        text(
            screen,
            f"{price} moedas",
            560,
            y + 16,
            YELLOW
        )

        y += 65

    text(
        screen,
        "H - Poção de Regeneração: 15 moedas",
        120,
        y + 20
    )

    text(
        screen,
        "M - Poção de Mana: 20 moedas",
        120,
        y + 50
    )

    text(
        screen,
        "ESC - Sair",
        120,
        y + 100
    )

    text(
        screen,
        f"Suas moedas: {player.coins}",
        800,
        120,
        YELLOW
    )


def buy_item(index):

    items = list(
        SHOP_ITEMS.items()
    )

    if index < 0 or index >= len(items):
        return

    item, price = items[index]

    if item in owned_items:

        show_message(
            "Você já possui esse item."
        )

        return

    if player.coins < price:

        show_message(
            "Moedas insuficientes."
        )

        return

    player.coins -= price
    owned_items.append(item)

    if item.startswith("Armadura"):
        player.armor = item

    elif item == "Cajado Arcano":
        player.staff = True

    elif item == "Espada de Ferro":
        player.sword = True

    elif item == "Escudo Elemental":
        player.shield = True

    show_message(
        f"{item} comprado!"
    )


# ============================================================
# INVENTÁRIO
# ============================================================

def draw_inventory():

    screen.fill(
        (25, 30, 40)
    )

    center_text(
        screen,
        "INVENTÁRIO",
        30,
        YELLOW,
        TITLE
    )

    text(
        screen,
        f"Elemento: {player.element}",
        100,
        120
    )

    text(
        screen,
        f"Nível: {player.level}/10",
        100,
        155
    )

    text(
        screen,
        f"XP: {player.level_xp}/100",
        100,
        190
    )

    text(
        screen,
        f"Moedas: {player.coins}",
        100,
        225,
        YELLOW
    )

    text(
        screen,
        "Equipamentos:",
        100,
        280,
        YELLOW
    )

    if owned_items:

        for i, item in enumerate(
            owned_items
        ):

            text(
                screen,
                f"- {item}",
                120,
                315 + i * 30
            )

    else:

        text(
            screen,
            "Nenhum",
            120,
            315
        )

    text(
        screen,
        "Pergaminhos:",
        500,
        280,
        YELLOW
    )

    if player.scrolls:

        for i, scroll in enumerate(
            player.scrolls
        ):

            text(
                screen,
                f"- Pergaminho de {scroll}",
                520,
                315 + i * 30
            )

    else:

        text(
            screen,
            "Nenhum",
            520,
            315
        )

    text(
        screen,
        f"Monstros derrotados: {player.monsters_defeated}",
        500,
        500
    )

    text(
        screen,
        "ESC - Voltar",
        100,
        620
    )


# ============================================================
# MAPA DAS ILHAS
# ============================================================

def draw_island_menu():

    screen.fill(
        (20, 25, 35)
    )

    center_text(
        screen,
        "MAPA DE ELEMENTARIA",
        25,
        YELLOW,
        BIG
    )

    for i, island in enumerate(ISLANDS):

        row = i // 2
        col = i % 2

        x = 100 + col * 480
        y = 100 + row * 105

        unlocked = i < player.unlocked_islands

        color = (
            island[2]
            if unlocked
            else GRAY
        )

        pygame.draw.rect(
            screen,
            color,
            (x, y, 400, 80),
            border_radius=10
        )

        text(
            screen,
            f"{i + 1}. {island[0]}",
            x + 20,
            y + 15
        )

        text(
            screen,
            island[3],
            x + 20,
            y + 45,
            WHITE,
            SMALL
        )

        if not unlocked:

            text(
                screen,
                "BLOQUEADA",
                x + 285,
                y + 30,
                RED,
                SMALL
            )

    text(
        screen,
        "1-9 = Ilhas | 0 = Ilha 10 | ESC = Voltar",
        360,
        650,
        WHITE,
        SMALL
    )


def travel_to(index):

    global current_island
    global game_state

    if index < 0 or index >= len(ISLANDS):
        return

    if index >= player.unlocked_islands:

        show_message(
            "Essa ilha está bloqueada!"
        )

        return

    current_island = index

    player.x = 550
    player.y = 350

    spawn_monsters()

    game_state = "world"


# ============================================================
# PORTÃO DO DRAGÃO
# ============================================================

def all_dungeons_completed():

    return len(
        player.dungeons_completed
    ) >= len(ISLANDS)


def draw_boss_gate():

    screen.fill(
        (15, 10, 20)
    )

    center_text(
        screen,
        "PORTÃO DO DRAGÃO",
        50,
        RED,
        TITLE
    )

    center_text(
        screen,
        "O Guardião de Elementaria aguarda você.",
        120
    )

    if all_dungeons_completed():

        center_text(
            screen,
            "Todas as masmorras foram derrotadas!",
            220,
            GREEN
        )

        center_text(
            screen,
            "Entre pagando 150 moedas.",
            270,
            YELLOW
        )

        center_text(
            screen,
            "ENTER - Entrar",
            360
        )

    else:

        center_text(
            screen,
            "Você precisa derrotar todas as 10 masmorras.",
            220,
            RED
        )

        center_text(
            screen,
            f"Masmorras: {len(player.dungeons_completed)}/10",
            270
        )

    center_text(
        screen,
        "ESC - Voltar",
        500
    )


def enter_boss():

    global game_state

    if not all_dungeons_completed():

        show_message(
            "Derrote todas as 10 masmorras primeiro!"
        )

        return

    if player.coins < 150:

        show_message(
            "Você precisa de 150 moedas."
        )

        return

    player.coins -= 150

    dragon.hp = dragon.max_hp
    game_state = "boss"


# ============================================================
# BATALHA DO DRAGÃO
# ============================================================

def draw_boss():

    screen.fill(
        (18, 10, 25)
    )

    center_text(
        screen,
        "BATALHA FINAL",
        25,
        RED,
        TITLE
    )

    pygame.draw.circle(
        screen,
        (130, 30, 160),
        (800, 250),
        120
    )

    text(
        screen,
        "DRAGÃO",
        730,
        200,
        WHITE,
        TITLE
    )

    text(
        screen,
        dragon.name,
        650,
        390,
        WHITE,
        BIG
    )

    draw_bar(
        650,
        440,
        300,
        30,
        dragon.hp,
        dragon.max_hp,
        RED
    )

    text(
        screen,
        f"HP: {dragon.hp}/{dragon.max_hp}",
        720,
        480
    )

    pygame.draw.circle(
        screen,
        ELEMENTS[player.element]["color"],
        (250, 250),
        75
    )

    text(
        screen,
        "MAGO",
        210,
        350,
        WHITE,
        BIG
    )

    draw_bar(
        130,
        400,
        250,
        25,
        player.hp,
        player.max_hp,
        RED
    )

    draw_bar(
        130,
        435,
        250,
        25,
        player.mana,
        player.max_mana,
        BLUE
    )

    text(
        screen,
        "1 - Ataque elemental",
        150,
        540
    )

    text(
        screen,
        "2 - Ataque forte",
        150,
        580
    )

    text(
        screen,
        "3 - Ataque supremo",
        150,
        620
    )

    text(
        screen,
        "4 - Espada/Punho",
        550,
        540
    )

    text(
        screen,
        "P - Poção de mana",
        550,
        580
    )

    text(
        screen,
        "H - Poção de vida",
        550,
        620
    )


def boss_attack():

    damage = dragon.damage()

    if player.shield and random.random() < 0.30:

        show_message(
            "O Escudo Elemental desviou o ataque!"
        )

        return

    damage = int(
        damage *
        (1 - player.defense() / 100)
    )

    damage = max(
        1,
        damage
    )

    player.hp -= damage

    if player.hp <= 0:

        player.hp = 0

        game_over()


def boss_player_attack(index):

    global game_state

    if index == 3:

        damage = player.physical_damage()

    else:

        required = {
            0: 1,
            1: 2,
            2: 4
        }[index]

        if player.element_level < required:

            show_message(
                f"Você precisa do nível elemental {required}."
            )

            return

        name, min_d, max_d, min_m, max_m = ELEMENTS[
            player.element
        ]["attacks"][index]

        cost = random.randint(
            min_m,
            max_m
        )

        if player.mana < cost:

            show_message(
                "Mana insuficiente!"
            )

            return

        player.mana -= cost

        damage = random.randint(
            min_d,
            max_d
        )

        damage += player.elemental_bonus()

        if player.staff:
            damage += 15

        if player.element == "Água":
            damage = int(damage * 1.7)
        else:
            damage = int(damage * 0.65)

    dragon.hp -= damage

    player.mana = min(
        player.max_mana,
        player.mana + random.randint(10, 25)
    )

    if dragon.hp <= 0:

        dragon.hp = 0

        player.missions[
            "final_boss"
        ] = True

        # ====================================================
        # CORREÇÃO PRINCIPAL:
        # AO MATAR O DRAGÃO VAI PARA A TELA DE VITÓRIA
        # ====================================================

        game_state = "victory"

        return

    boss_attack()


# ============================================================
# POÇÕES DO CHEFE
# ============================================================

def use_boss_health_potion():

    if player.coins < 15:

        show_message(
            "Moedas insuficientes."
        )

        return

    player.coins -= 15

    amount = random.randint(
        20,
        35
    )

    player.hp = min(
        player.max_hp,
        player.hp + amount
    )

    show_message(
        f"Poção recuperou {amount} de vida."
    )

    boss_attack()


def use_boss_mana_potion():

    if player.coins < 20:

        show_message(
            "Moedas insuficientes."
        )

        return

    player.coins -= 20

    amount = random.randint(
        20,
        35
    )

    player.mana = min(
        player.max_mana,
        player.mana + amount
    )

    show_message(
        f"Poção recuperou {amount} de mana."
    )

    boss_attack()


# ============================================================
# VITÓRIA
# ============================================================

def draw_victory():

    # Tela verde escura
    screen.fill(
        (10, 40, 25)
    )

    # Título
    center_text(
        screen,
        "VITÓRIA!",
        90,
        YELLOW,
        TITLE
    )

    center_text(
        screen,
        "Você derrotou o Dragão Guardião de Elementaria!",
        190,
        WHITE,
        BIG
    )

    center_text(
        screen,
        "O Reino de Elementaria foi salvo!",
        270,
        GREEN,
        BIG
    )

    # ========================================================
    # TEXTO PEDIDO
    # ========================================================

    center_text(
        screen,
        "OBRIGADO POR JOGAR!",
        380,
        YELLOW,
        TITLE
    )

    center_text(
        screen,
        "Sua aventura chegou ao fim.",
        450,
        WHITE
    )

    center_text(
        screen,
        "ESC - Voltar ao menu",
        550,
        WHITE
    )


# ============================================================
# GAME OVER
# ============================================================

def game_over():

    global game_state
    global dungeon_active
    global current_monster

    dungeon_active = False
    current_monster = None

    game_state = "game_over"


def draw_game_over():

    screen.fill(
        (35, 10, 15)
    )

    center_text(
        screen,
        "VOCÊ FOI DERROTADO",
        180,
        RED,
        TITLE
    )

    center_text(
        screen,
        "A aventura chegou ao fim.",
        260
    )

    center_text(
        screen,
        "ENTER - Voltar ao menu",
        400
    )


# ============================================================
# INTERAÇÃO
# ============================================================

def interact_world():

    if current_island != 0:
        return None

    # ========================================================
    # LOJA
    # ========================================================

    if (
        430 < player.x < 570
        and
        60 < player.y < 230
    ):

        return "shop"

    # ========================================================
    # MÉDICO
    # ========================================================

    if (
        100 < player.x < 250
        and
        360 < player.y < 520
    ):

        player.heal()

        show_message(
            "Médico recuperou toda sua vida e mana!"
        )

    return None


def draw_world_help():

    pygame.draw.rect(
        screen,
        (20, 20, 30),
        (
            10,
            HEIGHT - 70,
            WIDTH - 20,
            55
        )
    )

    text(
        screen,
        "WASD/SETAS: andar | M: mapa | I: inventário | E: interagir | F: masmorra | B: portão | F5: salvar",
        25,
        HEIGHT - 52,
        WHITE,
        SMALL
    )


# ============================================================
# CONTROLES
# ============================================================

def handle_world_key(key):

    global game_state

    if key == pygame.K_m:
        game_state = "islands"

    elif key == pygame.K_i:
        game_state = "inventory"

    elif key == pygame.K_e:

        result = interact_world()

        if result == "shop":
            game_state = "shop"

    elif key == pygame.K_f:
        enter_dungeon()

    elif key == pygame.K_b:
        game_state = "boss_gate"

    elif key == pygame.K_F5:
        save_game()


def handle_battle_key(key):

    if key == pygame.K_1:
        player_attack(0)

    elif key == pygame.K_2:
        player_attack(1)

    elif key == pygame.K_3:
        player_attack(2)

    elif key == pygame.K_4:
        player_attack(3)

    elif key == pygame.K_h:
        use_health_potion()

    elif key == pygame.K_p:
        use_mana_potion()

    elif key == pygame.K_ESCAPE:

        if dungeon_active:

            battle_log.append(
                "Você está preso na masmorra!"
            )

        else:

            global game_state
            game_state = "world"


# ============================================================
# NOVO JOGO
# ============================================================

def new_game():

    global player
    global current_island
    global current_monster
    global monsters_on_map
    global dungeon_active

    player = Player()

    current_island = 0
    current_monster = None

    monsters_on_map = []

    dungeon_active = False

    owned_items.clear()


# ============================================================
# LOOP PRINCIPAL
# ============================================================

running = True

while running:

    clock.tick(FPS)

    # ========================================================
    # EVENTOS
    # ========================================================

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
            continue

        if event.type != pygame.KEYDOWN:
            continue

        # ====================================================
        # MENU
        # ====================================================

        if game_state == "menu":

            if event.key == pygame.K_1:

                new_game()
                game_state = "choose_element"

            elif event.key == pygame.K_2:

                if load_game():
                    spawn_monsters()
                    game_state = "world"

            elif event.key == pygame.K_3:
                running = False

            elif event.key == pygame.K_ESCAPE:
                running = False

        # ====================================================
        # ELEMENTO
        # ====================================================

        elif game_state == "choose_element":

            choices = {
                pygame.K_1: "Fogo",
                pygame.K_2: "Água",
                pygame.K_3: "Elétrico",
                pygame.K_4: "Planta",
            }

            if event.key in choices:

                player.element = choices[
                    event.key
                ]

                game_state = "world"

                spawn_monsters()

        # ====================================================
        # MUNDO
        # ====================================================

        elif game_state == "world":

            handle_world_key(
                event.key
            )

        # ====================================================
        # BATALHA
        # ====================================================

        elif game_state == "battle":

            handle_battle_key(
                event.key
            )

        # ====================================================
        # MASMORRA
        # ====================================================

        elif game_state == "dungeon":

            if event.key == pygame.K_RETURN:

                if dungeon_active:
                    start_dungeon_battle()

            elif event.key == pygame.K_ESCAPE:

                show_message(
                    "Você está preso na masmorra!"
                )

            elif event.key == pygame.K_m:

                show_message(
                    "O mapa está bloqueado."
                )

            elif event.key == pygame.K_i:

                show_message(
                    "O inventário está bloqueado."
                )

            elif event.key == pygame.K_b:

                show_message(
                    "O portão está bloqueado."
                )

        # ====================================================
        # LOJA
        # ====================================================

        elif game_state == "shop":

            if event.key in (
                pygame.K_1,
                pygame.K_2,
                pygame.K_3,
                pygame.K_4,
                pygame.K_5
            ):

                buy_item(
                    int(event.unicode) - 1
                )

            elif event.key == pygame.K_h:

                if player.coins >= 15:

                    player.coins -= 15

                    amount = random.randint(
                        20,
                        35
                    )

                    player.hp = min(
                        player.max_hp,
                        player.hp + amount
                    )

                    show_message(
                        f"Poção recuperou {amount} de vida."
                    )

                else:

                    show_message(
                        "Moedas insuficientes."
                    )

            elif event.key == pygame.K_m:

                if player.coins >= 20:

                    player.coins -= 20

                    amount = random.randint(
                        20,
                        35
                    )

                    player.mana = min(
                        player.max_mana,
                        player.mana + amount
                    )

                    show_message(
                        f"Poção recuperou {amount} de mana."
                    )

                else:

                    show_message(
                        "Moedas insuficientes."
                    )

            elif event.key == pygame.K_ESCAPE:

                game_state = "world"

        # ====================================================
        # INVENTÁRIO
        # ====================================================

        elif game_state == "inventory":

            if event.key == pygame.K_ESCAPE:
                game_state = "world"

        # ====================================================
        # MAPA
        # ====================================================

        elif game_state == "islands":

            if event.key == pygame.K_ESCAPE:

                game_state = "world"

            elif event.key in (
                pygame.K_1,
                pygame.K_2,
                pygame.K_3,
                pygame.K_4,
                pygame.K_5,
                pygame.K_6,
                pygame.K_7,
                pygame.K_8,
                pygame.K_9,
                pygame.K_0
            ):

                number = int(
                    event.unicode
                )

                if number == 0:
                    number = 10

                travel_to(
                    number - 1
                )

        # ====================================================
        # PORTÃO
        # ====================================================

        elif game_state == "boss_gate":

            if event.key == pygame.K_RETURN:
                enter_boss()

            elif event.key == pygame.K_ESCAPE:
                game_state = "world"

        # ====================================================
        # CHEFE
        # ====================================================

        elif game_state == "boss":

            if event.key == pygame.K_1:
                boss_player_attack(0)

            elif event.key == pygame.K_2:
                boss_player_attack(1)

            elif event.key == pygame.K_3:
                boss_player_attack(2)

            elif event.key == pygame.K_4:
                boss_player_attack(3)

            elif event.key == pygame.K_p:
                use_boss_mana_potion()

            elif event.key == pygame.K_h:
                use_boss_health_potion()

        # ====================================================
        # GAME OVER
        # ====================================================

        elif game_state == "game_over":

            if event.key == pygame.K_RETURN:

                game_state = "menu"

        # ====================================================
        # VITÓRIA
        # ====================================================

        elif game_state == "victory":

            if event.key == pygame.K_ESCAPE:

                game_state = "menu"

    # ========================================================
    # MOVIMENTO DO MUNDO
    # ========================================================

    if game_state == "world":

        keys = pygame.key.get_pressed()

        speed = 4

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            player.y -= speed

        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            player.y += speed

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            player.x -= speed

        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            player.x += speed

        player.x = max(
            70,
            min(WIDTH - 70, player.x)
        )

        player.y = max(
            90,
            min(HEIGHT - 90, player.y)
        )

        move_monsters()

    # ========================================================
    # MENSAGEM
    # ========================================================

    if message_timer > 0:

        message_timer -= 1

    # ========================================================
    # DESENHO
    # ========================================================

    if game_state == "menu":

        draw_menu()

    elif game_state == "choose_element":

        draw_element_selection()

    elif game_state == "world":

        draw_island()

    elif game_state == "battle":

        draw_battle()

    elif game_state == "dungeon":

        draw_dungeon()

    elif game_state == "shop":

        draw_shop()

    elif game_state == "inventory":

        draw_inventory()

    elif game_state == "islands":

        draw_island_menu()

    elif game_state == "boss_gate":

        draw_boss_gate()

    elif game_state == "boss":

        draw_boss()

    elif game_state == "game_over":

        draw_game_over()

    # ========================================================
    # TELA DE VITÓRIA
    # ========================================================

    elif game_state == "victory":

        draw_victory()

    # ========================================================
    # MENSAGEM NA TELA
    # ========================================================

    if message_timer > 0 and game_state not in (
        "menu",
        "choose_element",
        "victory"
    ):

        pygame.draw.rect(
            screen,
            (20, 20, 30),
            (250, 85, 600, 45),
            border_radius=8
        )

        center_text(
            screen,
            message,
            97,
            YELLOW,
            SMALL
        )

    pygame.display.flip()


pygame.quit()
