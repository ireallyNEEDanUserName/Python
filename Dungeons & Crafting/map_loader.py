import pygame
import json
import definicoes, player, start

def all_tiles_f():

    f = open("map\\tile2.json", "r")
    file_data = f.read()
    f.close()

    mapdata = json.loads(file_data)

    layers = mapdata["layers"]
    height = mapdata["height"]
    width = mapdata["width"]

    tileset = mapdata["tilesets"]
    tileId = 0
    colisao = {}
    interagir = {}
    locais = {}
    all_tiles = {}
    loop = 0
    tilecount = 0
    sprites_em_tiles = []
    loopInc = 32

    for tilesets in tileset:
        tilesurface = pygame.image.load("sprites/" + tilesets["image"]).convert_alpha()
        
        if tilesets["spacing"] == 1:
            loopInc = 33
        else:
            loopInc = 32
            
        for y in range(0, tilesets["imageheight"], loopInc):
            for x in range(0, tilesets["imagewidth"], loopInc):
                tileId += 1
                rect = pygame.Rect(x, y, 32, 32)
                tile = tilesurface.subsurface(rect)
                all_tiles[tileId] = tile
                
                
        tilecount = (tileId + 1) - tilesets["tilecount"]

        #pega a propriedade tileproperties e poem na variavel
        tileproperties = tilesets["tileproperties"]
        #faz o loop na propriedade tileproprieties
        for loop2 in range(0, len(tileproperties), 1):
            Prop = tileproperties[str(loop2)]
            #definie os valores dentro de colisao
            ValColisao = Prop["colisao"]
            if ValColisao == "True":
                colisao[tilecount + loop2] = 1
                
            try:
                #define os valores em interagir
                ValInteragir = Prop["interagir"]
                if ValInteragir == "True":
                    interagir[tilecount + loop2] = Prop["nome"]
            except:
                pass
                
            try:
                #define os valores em locais
                ValLocais = Prop["locais"]
                if ValLocais == "True":
                    locais[tilecount + loop2] = Prop["nome"]
            except:
                pass
                
        loop += 1

    x = 0
    for layer in layers:
        if x == 0:
            data = layer["data"]
        if x == 1:
            data1 = layer["data"]

        x+=1

    return data, data1, height, width, all_tiles, colisao, interagir, locais

def load_map_struct():
    
    data_layer, data_layer1, altura, comp, sprites, colisao, interagir, locais = all_tiles_f()

    definicoes.spritesList = sprites

    definicoes.colisao = colisao
    definicoes.interagir = interagir
    definicoes.locais = locais
    
    definicoes.data_backLayer0_manipulavel = data_layer
    definicoes.data_backLayer1_manipulavel = data_layer1
    
    definicoes.data_alt = altura
    definicoes.data_comp = comp

    definicoes.limite_larg = definicoes.data_comp - definicoes.largTela
    definicoes.limite_alt = altura - (definicoes.altTela - definicoes.ini_tela)

    if definicoes.limite_larg < 0:
        definicoes.limite_larg = 0
    if definicoes.limite_alt < 0:
        definicoes.limite_alt = 0

    for y in range(0, (definicoes.altTela - definicoes.ini_tela), 1):
        for x in range(0, definicoes.largTela, 1):
        
            rect = pygame.draw.rect(definicoes.screen, definicoes.black, ((x * 32), (y * 32), 32, 32))
            definicoes.all_rects.append(rect)

    #barra onde ficam os botoes.
    rect = pygame.draw.rect(definicoes.screen, definicoes.black, (0,  (definicoes.height - 32), definicoes.width, 32))
    definicoes.menu_rect.append(rect)
    #botao menu
    menu = pygame.draw.rect(definicoes.screen, definicoes.black,(5, (definicoes.height - 28), 80, 24))
    definicoes.menu_rect.append(menu)
    #botao save
    save = pygame.draw.rect(definicoes.screen, definicoes.black,(definicoes.width - 100, (definicoes.height - 28), 80, 24))
    definicoes.menu_rect.append(save)

#carrega a estrutura principal do mapa antes de tudo.
load_map_struct()


def posicoes():

    definicoes.playerDict["PosX"] = definicoes.player_rect.centerx
    definicoes.playerDict["PosY"] = definicoes.player_rect.centery

    posx = definicoes.player_rect.centerx / 32
    posy = definicoes.player_rect.centery / 32

    posdef = ((posy + definicoes.playerDict["LALT"]) * definicoes.data_comp) + (posx + definicoes.playerDict["LARG"])
    posdef_baixo = posdef + definicoes.data_comp
    posdef_cima = posdef - definicoes.data_comp
    
    scr_rect = posx + (posy * definicoes.largTela)
    scr_rect_baixo = scr_rect + definicoes.largTela
    scr_rect_cima = scr_rect - definicoes.largTela

    return posx, posy, posdef, posdef_baixo, posdef_cima, scr_rect, scr_rect_baixo, scr_rect_cima

def draw_map_call(key):

    posx, posy, posdef, posdef_baixo, posdef_cima, scr_rect, scr_rect_baixo, scr_rect_cima = posicoes()

    if ((posx >= (definicoes.largTela - 3) or posx <= 3
         or posy >= (definicoes.altTela - 3) or posy <= 3) and key != pygame.K_SPACE):
        
        if posx >= (definicoes.largTela - 3) and definicoes.playerDict["LARG"] < definicoes.limite_larg and definicoes.direcao == "right":
            if not player.check_colisao(32, 0):
                definicoes.playerDict["LARG"] += 1
            else:
                definicoes.playerDict["LARG"] += 1
            definicoes.player_rect = definicoes.player_rect.move(-30,0)
                
        elif posx <= 3 and definicoes.playerDict["LARG"] > 0 and definicoes.direcao == "left":
            if not player.check_colisao(-32, 0):
                definicoes.playerDict["LARG"] -= 1
            else:
                definicoes.playerDict["LARG"] -= 1
            definicoes.player_rect = definicoes.player_rect.move(30,0)
            
        elif posy >= (definicoes.altTela - 3) and definicoes.playerDict["LALT"] < definicoes.limite_alt and definicoes.direcao == "down":
            if not player.check_colisao(0, 32):
                definicoes.playerDict["LALT"] += 1
            else:
                definicoes.playerDict["LALT"] += 1
            definicoes.player_rect = definicoes.player_rect.move(0,-30)
                
        elif posy <= 3 and definicoes.playerDict["LALT"] > 0 and definicoes.direcao == "up":
            if not player.check_colisao(0, -32):
                definicoes.playerDict["LALT"] -= 1
            else:
                definicoes.playerDict["LALT"] -= 1
            definicoes.player_rect = definicoes.player_rect.move(0,30)

        load_tela(definicoes.playerDict["LARG"], definicoes.playerDict["LALT"])

        
    else:
        draw_map(posdef, scr_rect)
        #desenhar sprite da frente e tras do player
        if posx >= 1:
            draw_map(posdef - 1, scr_rect - 1)
        if posx <= (definicoes.largTela - 2):
            draw_map(posdef + 1, scr_rect + 1)

        #desenhar os 3 sprites de cima do player
        if posy >= 1:
            draw_map(posdef_cima, scr_rect_cima)
            if posx >= 1:
                draw_map(posdef_cima - 1, scr_rect_cima - 1)
            if posx <= (definicoes.largTela - 2):
                draw_map(posdef_cima + 1, scr_rect_cima + 1)

        #desenhar os 3 sprites de baixo do player
        if posy <= (definicoes.altTela - 2):
            draw_map(posdef_baixo, scr_rect_baixo)
            if posx <= (definicoes.largTela - 2):
                draw_map(posdef_baixo + 1, scr_rect_baixo + 1)
            if posx >= 1:
                draw_map(posdef_baixo - 1, scr_rect_baixo - 1)

            
    player.player_load()
    load_menu()
    definicoes.moveTela += 1
        
def draw_map(pos, rect_pos):

    if definicoes.data_backLayer0_manipulavel[pos] != 0:
        definicoes.screen.blit(definicoes.spritesList[definicoes.data_backLayer0_manipulavel[pos]], definicoes.all_rects[rect_pos])
       
    if definicoes.data_backLayer1_manipulavel[pos] != 0:
        definicoes.screen.blit(definicoes.spritesList[definicoes.data_backLayer1_manipulavel[pos]], definicoes.all_rects[rect_pos])
        
def load_tela(larg = 0, alt = 0):

    ini_data = 0
    rect = 0

    definicoes.screen.fill(definicoes.white, definicoes.scr_rect)
    
    for y1 in range(0, (definicoes.altTela - definicoes.ini_tela), 1):
        for x1 in range(0, definicoes.largTela, 1):

            ini_data = ((y1 + alt) * definicoes.data_comp) + (x1 + larg)

            if definicoes.data_backLayer0_manipulavel[ini_data] != 0:
                definicoes.screen.blit(definicoes.spritesList[definicoes.data_backLayer0_manipulavel[ini_data]], definicoes.all_rects[rect])
  
            if definicoes.data_backLayer1_manipulavel[ini_data] != 0:
                definicoes.screen.blit(definicoes.spritesList[definicoes.data_backLayer1_manipulavel[ini_data]], definicoes.all_rects[rect])

            rect += 1

def load_menu(menu_rect1 = definicoes.white, menu_rect2 = definicoes.white):

    definicoes.screen.fill(definicoes.branco_ostra, definicoes.menu_rect[0])
    pygame.display.update(definicoes.menu_rect[0])

    Text = start.input_text(definicoes.texto, (250), definicoes.height - 16, definicoes.black, "yes")
    definicoes.menu_rect[1] = start.multi_box(5, definicoes.height - 28, 80, 24, menu_rect1, "yes", "Char")
    definicoes.menu_rect[2] = start.multi_box(definicoes.width - 100, definicoes.height - 28, 80, 24, menu_rect2, "yes", "Save")
    
    

