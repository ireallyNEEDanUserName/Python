# -*- coding: cp1252 -*-
import pygame, sys, definicoes, map_loader, player, json

new_game = pygame.image.load("new game.jpg").convert_alpha()
intro2 = pygame.image.load("2.jpg").convert_alpha()
basic = pygame.image.load("basic.jpg").convert_alpha()

def menu_call():
    definicoes.screen.blit(intro2,(0,0))
    pygame.display.update()

def new():
    definicoes.screen.blit(new_game,(0,0))
    pygame.display.update()

    return_menu = multi_box(500, 400, 100, 25, definicoes.vermelho_claro, "sim",
              "Menu", definicoes.white)
    
    z = ''
    definicoes.nome = ''
    sair = False
    loop_texto = 0

    while loop_texto == 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            movimento = pygame.mouse.get_pos()

            if event.type == pygame.MOUSEMOTION:

                if return_menu.collidepoint(movimento):
                    multi_box(500, 400, 100, 25, definicoes.vermelho, "sim",
                              "Menu", definicoes.white)
                else:
                    multi_box(500, 400, 100, 25, definicoes.vermelho_claro, "sim",
                              "Menu", definicoes.white)
                    
            if event.type == pygame.MOUSEBUTTONDOWN:

                if return_menu.collidepoint(movimento):
                    definicoes.menu = 0
                    loop_texto += 1
                    menu_call()
                    
                    
            if event.type == pygame.KEYDOWN:
                
                z = pygame.key.name(event.key)
                
                if len(definicoes.nome) >= 8 or z == "return":
                    sair = True
                    loop_texto += 1
                    save(True)
                    map_loader.load_tela()
                    map_loader.load_menu()
                    player.player_load()
                    
                if z == "backspace":
                    z1 = definicoes.nome[:-1]
                    definicoes.nome = z1
                    multi_box(260, 200, 80, 30, definicoes.white, "sim",
                              definicoes.nome, definicoes.black)
                    
                if z == "error":
                    multi_box(260, 200, 80, 30, definicoes.white, "sim",
                              "não aceito", definicoes.black)
            
                if not sair and z != "backspace" and z != "error":
                    definicoes.nome += z
                    multi_box(260, 200, 80, 30, definicoes.white, "sim",
                              definicoes.nome, definicoes.black)

def verf_exist():

    filecatalogo = open("catalogo.txt", "r")
    flcread = filecatalogo.readline(12)
    while flcread != '':
        flcread = flcread[:-1]
        #se ja existe chamar função new game novamente.
        if flcread == definicoes.nome:
            definicoes.screen.blit(basic, (0,0))
            pygame.display.update()
            return 1
        flcread = filecatalogo.readline(12)
    filecatalogo.close()

    return 0
    

def save(new_game = False):

    verf = 1
    nome = "jogos\\" + str(definicoes.nome) + ".txt"

    #verificar se o nome ja existe.
    if new_game:
        verf = verf_exist()
        
    if verf == 0 or new_game == False:
        #salvar o jogador se não existe
        
        fileplayer = open(nome, "w") 
        fileplayer.close()
        
        definicoes.playerDict["inventario"] = definicoes.inventario
        json.dump(definicoes.playerDict, open(nome, 'w'))

        definicoes.texto = "JOGO SALVO!!"
        
        #salvar o nome no catalogo para chamar no load.
        if new_game:
            filecatalogo = open("catalogo.txt", "a")
            filecatalogo.write(definicoes.nome + "\n")
            filecatalogo.close()
        
    elif verf == 1:
        new()

    
def load():
    selected = False
    loop_load = 0

    filecatalogo = open("catalogo.txt", "r")
    filecatread = filecatalogo.readline(15)        

    load_select = multi_box(185, 231, 100, 25, definicoes.vermelho_claro, "sim",
                            filecatread[:-1], definicoes.white)

    return_menu = multi_box(500, 400, 100, 25, definicoes.vermelho_claro, "sim",
                                  "Menu", definicoes.white)
    
    while not selected:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            movimento = pygame.mouse.get_pos()
                        
            if event.type == pygame.MOUSEMOTION:
                if return_menu.collidepoint(movimento):
                    multi_box(500, 400, 100, 25, definicoes.vermelho, "sim", "Menu", definicoes.white)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if return_menu.collidepoint(movimento):
                    definicoes.menu = 0
                    selected = True
                    menu_call()

            if event.type == pygame.KEYDOWN:
                
                if event.key == pygame.K_UP:
                    
                    filecatalogo.close()
                    filecatalogo = open("catalogo.txt", "r")
                    if loop_load == 0:
                        filecatread = filecatalogo.readline(15)

                    else:
                        for i in range(loop_load):
                            filecatread = filecatalogo.readline(15)
                            i += 1
                            
                    multi_box(185, 231, 100, 25, definicoes.vermelho_claro, "sim",
              filecatread[:-1], definicoes.white)
                    loop_load -= 1
        
                else:
                    filecatread = filecatalogo.readline(15)
                    multi_box(185, 231, 100, 25, definicoes.vermelho_claro, "sim",
                              filecatread[:-1], definicoes.white)
                    loop_load += 1

            movimento = pygame.mouse.get_pos()
            numeros = ['0','1','2','3','4','5','6','7','8','9']

            if event.type == pygame.MOUSEBUTTONDOWN:

                if load_select.collidepoint(movimento):

                    nameLoad = "jogos\\" + filecatread[:-1] + ".txt"
                    definicoes.nome = filecatread[:-1]                    
                    
                    Dict = json.load(open(nameLoad))

                    for keys in definicoes.playerDict:
                        if keys not in Dict:
                            Dict[keys] = definicoes.playerDict[keys]

                    definicoes.playerDict = Dict
                    
                    definicoes.inventario = definicoes.playerDict["inventario"]
                    
                    selected = True
                    map_loader.load_tela(definicoes.playerDict["LARG"], definicoes.playerDict["LALT"])
                    map_loader.load_menu()
                    player.player_load_first()         
                
    filecatalogo.close()
            
            
def input_text(msg, x, y, color, manual = "no"):

    text = definicoes.font.render(msg, 1, color)
    if manual == "no":
        textPos = text.get_rect(left = x, top = y)
        definicoes.screen.blit(text, textPos)
        pygame.display.update(textPos)

    else:
        textPos = text.get_rect(centerx = x, centery = y)
        definicoes.screen.blit(text, textPos)
        pygame.display.update(textPos)

    
def multi_box(esquerda, cima, largura, altura, color, msgOpt = "no", msg = "", color_text = definicoes.black):
    
    rectangle = pygame.draw.rect(definicoes.screen, color,
                                 (esquerda, cima, largura, altura))
    pygame.display.update(rectangle)

    if msgOpt == "no":
        return rectangle
    else:
        x1 = (esquerda+(largura/2))
        y1 = (cima+(altura/2))
        input_text(msg, x1, y1, color_text, manual = "sim")

    return rectangle
    

        
    
