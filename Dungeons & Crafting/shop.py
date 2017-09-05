import pygame
import player, map_loader, start, definicoes

def load():

    sair = False
    buyBol = False
    sellBol = False
    buy, sell = print_tela()
    

    while not sair:
        mouse = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN or (buyBol == True or sellBol == True):
                
                if buy.collidepoint(mouse) or buyBol == True:
                    close_Menu, sair, sellBol = buy_func()
                    buyBol = False
                    
                elif sell.collidepoint(mouse) or sellBol == True:
                    close_Menu, sair, buyBol = sell_func()
                    sellBol = False

                try:
                    if close_Menu.collidepoint(mouse):
                        sair = True
                        map_loader.load_tela(definicoes.playerDict["LARG"], definicoes.playerDict["LALT"])
                        player.player_load()
                except:
                    print "erros close inn"


        definicoes.clock.tick(5)
        pygame.display.update()



def print_tela():

    option_rect = pygame.draw.rect(definicoes.screen, definicoes.branco_ostra,
                                   (definicoes.scr_rect.centerx - 50,
                                    definicoes.scr_rect.centery - 13, 120, 26))

    buy = start.multi_box(option_rect.left + 5, option_rect.top + 3, 50, 20,
                          definicoes.vermelho, "Yes", "BUY", definicoes.white)
    sell = start.multi_box(option_rect.left + 65, option_rect.top + 3, 50, 20,
                           definicoes.vermelho, "Yes", "SELL", definicoes.white)
                    
    return buy, sell


def buy_func():
    definicoes.screen.fill(definicoes.branco_ostra, definicoes.OpenMenu_rect)
                    
    close_Menu = start.multi_box(definicoes.OpenMenu_rect.right - 20, definicoes.OpenMenu_rect.top, 20, 20,
                                 definicoes.vermelho, "Yes", "X", definicoes.white)
                    
    start.multi_box(definicoes.OpenMenu_rect.centerx - 70, definicoes.OpenMenu_rect.top + 3, 70, 40,
                    definicoes.vermelho, "Yes", "BUY", definicoes.white)
    sell = start.multi_box(definicoes.OpenMenu_rect.centerx + 5, definicoes.OpenMenu_rect.top + 3, 70, 40,
                           definicoes.vermelho, "Yes", "SELL", definicoes.white)

    line = pygame.draw.line(definicoes.screen, definicoes.vermelho,
                            (definicoes.OpenMenu_rect.left, sell.bottom + 5),
                            (definicoes.OpenMenu_rect.right, sell.bottom + 5), 5)

    qtd_dinheiro(line)
    
    linhas = 1
    itens_rect = []
    buy_exit = False
    sair = False
    sellBol = False
    
    if len(definicoes.lojaBuy) > 5:
        linhas = 2
    
    
    for x in range(0, linhas, 1):
        for y in range(0, len(definicoes.lojaBuy), 1):
            j = pygame.draw.rect(definicoes.screen, definicoes.white,
                                 (definicoes.OpenMenu_rect.centerx - (y * 32),
                                  definicoes.OpenMenu_rect.centery - (x * 32), 38, 38), 5)
            itens_rect.append(j)
            
            #poem a imagem do itens na tela
            var = definicoes.lojaBuy[y]
            rectNome = definicoes.stats[var]
            rect = rectNome["rect"]
            img = definicoes.sprites[var]
            
            varY = j.centery - (rect.height / 2)
            varX = j.centerx - (rect.width / 2)
            definicoes.screen.blit(img, (varX, varY))

    while not buy_exit:
        mouse = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        
            if event.type == pygame.MOUSEBUTTONDOWN:
                for loop in range(0, len(itens_rect), 1):
                    if itens_rect[loop].collidepoint(mouse):
                        var = definicoes.lojaBuy[loop]
                        itenStats = definicoes.itensDef[var]
                        defIten = definicoes.stats[itenStats]
                        textoIten = defIten["nome"] + " --- Valor: " + str(defIten["venda"])
                        rect_texto_iten = start.multi_box(definicoes.OpenMenu_rect.left, definicoes.OpenMenu_rect.bottom - 30,
                                                          200, 30, definicoes.branco_ostra, "Yes", textoIten, definicoes.black)
                        comprar = start.multi_box(rect_texto_iten.right + 10, definicoes.OpenMenu_rect.bottom - 30,
                                                  90, 30, definicoes.vermelho, "Yes", "Comprar", definicoes.white)
                try:
                    if comprar.collidepoint(mouse):
                        itenStats = definicoes.itensDef[var]
                        defIten = definicoes.stats[itenStats]
                        if definicoes.playerDict["moedas"] >= defIten["venda"]:
                            definicoes.playerDict["moedas"] -= defIten["venda"]
                            try:
                                definicoes.inventario[var] += 1
                            except:
                                definicoes.inventario[var] = 1
                                
                            qtd_dinheiro(line)
                except:
                    print "erro na func comprar"

                if sell.collidepoint(mouse):
                    buy_exit = True
                    sellBol = True

                elif close_Menu.collidepoint(mouse):
                        buy_exit = True
                        sair = True
                        map_loader.load_tela(definicoes.playerDict["LARG"], definicoes.playerDict["LALT"])
                        player.player_load()

        definicoes.clock.tick(5)
        pygame.display.update()
                

    return close_Menu, sair, sellBol

def sell_func():
    definicoes.screen.fill(definicoes.branco_ostra, definicoes.OpenMenu_rect)
                    
    close_Menu = start.multi_box(definicoes.OpenMenu_rect.right - 20, definicoes.OpenMenu_rect.top, 20, 20,
                                 definicoes.vermelho, "Yes", "X", definicoes.white)
                    
    buy = start.multi_box(definicoes.OpenMenu_rect.centerx - 70, definicoes.OpenMenu_rect.top + 3, 70, 40,
                          definicoes.vermelho, "Yes", "BUY", definicoes.white)
    start.multi_box(definicoes.OpenMenu_rect.centerx + 5, definicoes.OpenMenu_rect.top + 3, 70, 40,
                    definicoes.vermelho, "Yes", "SELL", definicoes.white)

    line = pygame.draw.line(definicoes.screen, definicoes.vermelho,
                            (definicoes.OpenMenu_rect.left, buy.bottom + 5),
                            (definicoes.OpenMenu_rect.right, buy.bottom + 5), 5)

    qtd_dinheiro(line)


    linhas = 0
    itens_rect = []
    
    if (len(definicoes.inventario) / 5) < 1:
        linhas = 1
    else:
        linhas = len(definicoes.inventario) / 5
    
    for x in range(0, linhas, 1):
        for y in range(0, len(definicoes.inventario), 1):
            j = pygame.draw.rect(definicoes.screen, definicoes.cinza,
                                 (definicoes.OpenMenu_rect.centerx - (y * 32),
                                  definicoes.OpenMenu_rect.centery - (x * 32), 38, 38))
            itens_rect.append(j)

    var = []
    
    #poem a imagem do itens na tela
    for keys in definicoes.inventario:
        var.append(keys)


    texto_sell(itens_rect, var)

    sair_exit = False
    sair = False
    buyBol = False

    while not sair_exit:
        mouse = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        
            if event.type == pygame.MOUSEBUTTONDOWN:
                
                
                for loop_inv in range(0, len(itens_rect), 1):
                    if itens_rect[loop_inv].collidepoint(mouse):
                        nome_iten = var[loop_inv]
                        defIten = definicoes.stats[nome_iten]
                        textoIten = defIten["nome"] + " --- Valor: " + str(defIten["compra"])
                        rect_texto_iten_inv = start.multi_box(definicoes.OpenMenu_rect.left, definicoes.OpenMenu_rect.bottom - 30,
                                                              200, 30, definicoes.branco_ostra, "Yes", textoIten, definicoes.black)
                        venda = start.multi_box(rect_texto_iten_inv.right + 10, definicoes.OpenMenu_rect.bottom - 30,
                                                90, 30, definicoes.vermelho, "Yes", "Vender", definicoes.white)

                try:
                    if venda.collidepoint(mouse):
                        statsIten = definicoes.stats[nome_iten]
                        
                        if definicoes.inventario[nome_iten] > 0:
                            definicoes.playerDict["moedas"] += statsIten["compra"]
                            definicoes.inventario[nome_iten] -= 1
                            if definicoes.inventario[nome_iten] == 0:
                                del definicoes.inventario[nome_iten]

                            texto_sell(itens_rect, var)
                            qtd_dinheiro(line)
                except:
                    print "erro vender iten"

                if buy.collidepoint(mouse):
                    sair_exit = True
                    buyBol = True

                elif close_Menu.collidepoint(mouse):
                        sair_exit = True
                        sair = True
                        map_loader.load_tela(definicoes.playerDict["LARG"], definicoes.playerDict["LALT"])
                        player.player_load()
                        

        definicoes.clock.tick(5)
        pygame.display.update()
    

    return close_Menu, sair, buyBol


#atualiza o texto nos itens na aba sell

def texto_sell(itens_rect, var):
    
    quantidade_text = []
    qtd = 0

    for keys in definicoes.inventario:
        var.append(keys)
        qtd = definicoes.inventario[keys]

        if qtd > 999 and qtd < 999999:
            qtd = definicoes.inventario[keys] / 1000
            quantidade_text.append(str(qtd) + "k")
        elif qtd > 999999:
            qtd = definicoes.inventario[keys] / 1000000
            quantidade_text.append(str(qtd) + "m")
        else:
            quantidade_text.append(str(qtd))

    for loop in range(0, len(itens_rect), 1):
        varStats = definicoes.stats[var[loop]]

        rect = varStats["rect"]
        img = definicoes.sprites[var[loop]]
        
        varY = itens_rect[loop].centery - (rect.height / 2)
        varX = itens_rect[loop].centerx - (rect.width / 2)
        definicoes.screen.blit(img, (varX, varY))

        start.input_text(quantidade_text[loop], itens_rect[loop].centerx, itens_rect[loop].centery, definicoes.white, "Yes")

    
    
def qtd_dinheiro(line):

    textoGold = "$: " + str(definicoes.playerDict["moedas"])
    gold = start.multi_box(definicoes.OpenMenu_rect.centerx - 105, line.bottom + 3, 210, 25,
                           definicoes.branco_ostra, "Yes", textoGold, definicoes.black)
    
