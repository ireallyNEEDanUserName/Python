import pygame

pygame.init()

#definicoes

clock = pygame.time.Clock()
FPS = 45

#cores
white            = (255, 255, 255)
branco_ostra     = (234, 230, 202)
cinza            = (185, 185, 185)
cinza_claro      = (200, 200, 200)
cinza_escuro     = (100, 100, 100)
black            = (  0,   0,   0)
vermelho         = (155,   0,   0)
vermelho_claro   = (175,  20,  20)
verde            = (  0, 155,   0)
verde_claro      = ( 20, 175,  20)
azul             = (  0,   0, 155)
azul_claro       = ( 20,  20, 175)
amarelo          = (155, 155,   0)
amarelo_claro    = (175, 175,  20)
amarelo_ocre     = (174, 160,  75)
amarelo_luminoso = (255, 255,   0)
marron           = (138,  86,  57)
marron_claro     = (185, 122,  87)

#surface
width = 640
height = 480
screen = pygame.display.set_mode((width, height))
scr_rect = screen.get_rect()
scr_rect.height = height - 32
pygame.display.set_caption('Dungeons & Crafting')

altTela = height / 32
largTela = width / 32
ini_tela = 1

limite_larg = 0
limite_alt = 0

moveTela = 0

#outros
font = pygame.font.Font(None, 25)
menu = 0
map_load_var = 0

#jogador
movePlayer = 2
keyPossiveis = ["left", "right", "up", "down", "space"]
direcao = ''
direcao_anterior = ''
contadorFrame = 0

chanceDeCombate = 5

#variaveis
nome = ''
playerDict = {"level": 0,
              "exp": 0,
              "expTotal": 0,
              "expProxLV": 0,
              "pedraLV": 0,
              "pedraXP": 0,
              "pedraXpProx": 0,
              "pedraTotalXP": 0,
              "madeiraLV": 0,
              "madeiraXP": 0,
              "madeiraXpProx": 0,
              "madeiraTotalXP": 0,
              "moedas": 0,
              "PosX": 305,
              "PosY": 333,
              "LALT": 0,
              "LARG": 0,
              "Vida": 10,
              "TVida": 10,
              "Ataque": 5,
              "Defesa": 1,
              "Ganhou": 0
              }

inventario = {}


#imagem do jogador
loop_andar = 0

player = pygame.image.load("gameloop\\eusprite.png").convert_alpha()
player1 = pygame.image.load("gameloop\\eusprite1.png").convert_alpha()
player2 = pygame.image.load("gameloop\\eusprite2.png").convert_alpha()

playerC = pygame.image.load("gameloop\\euspriteC.png").convert_alpha()
playerC1 = pygame.image.load("gameloop\\euspriteC1.png").convert_alpha()
playerC2 = pygame.image.load("gameloop\\euspriteC2.png").convert_alpha()

playerD = pygame.image.load("gameloop\\euspriteD.png").convert_alpha()
playerD1 = pygame.image.load("gameloop\\euspriteD1.png").convert_alpha()
playerD2 = pygame.image.load("gameloop\\euspriteD2.png").convert_alpha()

playerE = pygame.image.load("gameloop\\euspriteE.png").convert_alpha()
playerE1 = pygame.image.load("gameloop\\euspriteE1.png").convert_alpha()
playerE2 = pygame.image.load("gameloop\\euspriteE2.png").convert_alpha()

player_rect = player.get_rect(centerx = playerDict["PosX"], centery = playerDict["PosY"])

#monstros
corvo = pygame.image.load("gameloop\\corvo.png").convert_alpha()
corvo_rect = corvo.get_rect()

monsterLife = 50
monsterATK = 5


#imagem
back = pygame.image.load("tiles\\tile1.jpg").convert_alpha()

#spries soltos 32x32

valoresSpritesLayer1 = 0
valoresSpritesLayer2 = 0

spritesList = {}
colisao = {}
interagir = {}
locais = {}


#definicoes dos itens
lojaBuy = ["madeira", "pedra", "pocao", "gravetos", "graveto"]

sprites = {}
stats = {}
itensDef = {}

defIten = {}


#Rect do mapa
all_rects = []

data_backLayer0_manipulavel = []
data_backLayer1_manipulavel = []
mudancas = {}

data_alt = 0
data_comp = 0

#Definicoes menu
menu_rect = []

#localizacao do menu quando aberto.
OpenMenu_rect = screen.get_rect()
OpenMenu_rect.height = height - 128
OpenMenu_rect.width = width - 128
OpenMenu_rect.centerx = width / 2
OpenMenu_rect.centery = (height - 64) / 2

checkIter = False
texto = ''
espaco_loop = 0

