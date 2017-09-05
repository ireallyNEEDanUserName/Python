import sys, pygame
import definicoes, map_loader, start, player, itens_opt, spritesLoad

def imprimir_menu():
    inventario_Loop = 0
    Iten_Menu = []
    descricao_Menu = {}
    all_rects = {}

    #tela do menu
    definicoes.screen.fill(definicoes.cinza_claro, definicoes.OpenMenu_rect)

    #texto na parte superior do inventario
    descricao_tela = start.multi_box(definicoes.OpenMenu_rect.left, definicoes.OpenMenu_rect.top,
                                     definicoes.OpenMenu_rect.width, 20,
                                     definicoes.branco_ostra, "Yes", "Status / Inventario")

    #botao de fechar
    close_Menu = start.multi_box(definicoes.OpenMenu_rect.right - 20, definicoes.OpenMenu_rect.top, 20, 20,
                                 definicoes.vermelho, "Yes", "X", definicoes.white)
    
    #box geral dos status
    barra_status = start.multi_box(definicoes.OpenMenu_rect.right - 195, descricao_tela.bottom + 10,
                                   180, 75,
                                   definicoes.branco_ostra, "no")
    
    barra_status_lvl = start.multi_box(barra_status.left + 20, barra_status.top,
                                       140, 25,
                                       definicoes.branco_ostra, "Yes",
                                       ("Lv: " + str(definicoes.playerDict["level"])), definicoes.cinza_escuro)
    
    #barra de progresso de exp
    player.atualiza_lvl("pedra")
    texto_next_xp = "Exp: " + str(definicoes.playerDict["exp"])
    um_por_cento = (definicoes.playerDict["exp"] + definicoes.playerDict["expProxLVL"]) / 140.0
    barra = definicoes.playerDict["exp"] / um_por_cento

    barra_status_xp_full = start.multi_box(barra_status.left + 20, barra_status.top + 50,
                                           140, 25,
                                           definicoes.cinza, "no")
    barra_status_xp_next = start.multi_box(barra_status.left + 20, barra_status.top + 50,
                                           barra, 25,
                                           definicoes.vermelho, "no")
    texto_tela_next_xp = start.input_text(texto_next_xp, (barra_status.left + 20 + (140 / 2)),
                                          (barra_status.top + 50 + (25 / 2)), definicoes.branco_ostra, "sim")
                    

    #status do jogado ex: hp, att, def
    texto_vida = "HP: " + str(definicoes.playerDict["TVida"]) + " / " + str(definicoes.playerDict["Vida"])
    um_por_cento_vida = definicoes.playerDict["Vida"] / 100.0
    barra_vida = definicoes.playerDict["TVida"] / um_por_cento_vida

    barraVidaFull = start.multi_box(definicoes.OpenMenu_rect.left + 20, descricao_tela.bottom + 20,
                                    100, 25,
                                    definicoes.branco_ostra, "no")
    barra_status_vida = start.multi_box(definicoes.OpenMenu_rect.left + 20, descricao_tela.bottom + 20,
                                        barra_vida, 25,
                                        definicoes.vermelho, "no")
    texto_tela_vida = start.input_text(texto_vida, (barra_status_vida.left + (100 / 2)),
                                       (descricao_tela.bottom + 20 + (25 / 2)), definicoes.cinza_escuro, "sim")

    texto_att = "ATT: " + str(definicoes.playerDict["Ataque"])
    att_tela = start.input_text(texto_att, (definicoes.OpenMenu_rect.left + 20 + (100 / 2)),
                                (barra_status_vida.bottom + 12.5), definicoes.cinza_escuro, "sim")

    texto_def = "DEF: " + str(definicoes.playerDict["Defesa"])
    def_tela = start.input_text(texto_def, (definicoes.OpenMenu_rect.left + 20 + (100 / 2)),
                                (barra_status_vida.bottom + 37.5), definicoes.cinza_escuro, "sim")

    texto_ganhou = "Lutas Ganhas: " + str(definicoes.playerDict["Ganhou"])
    ganhou_tela = start.input_text(texto_ganhou, (definicoes.OpenMenu_rect.left + 20 + (100 / 2)),
                                   (barra_status_vida.bottom + 62.5), definicoes.cinza_escuro, "sim")

    #skills ##############################################################################################
    boxSkill = start.multi_box(definicoes.OpenMenu_rect.left + 10, (barra_status_vida.bottom + 80),
                               270,((definicoes.OpenMenu_rect.bottom - 20) - (barra_status_vida.bottom + 73)),
                               definicoes.branco_ostra, "no")

    SkillText = start.input_text("SKILLS", ((boxSkill.width / 2) + (definicoes.OpenMenu_rect.left + 10)),
                                 (boxSkill.top + 15), definicoes.vermelho, "sim")
                               
    #Trabalho com pedra
    textoPedra = "Pedra LV: " + str(definicoes.playerDict["pedraLV"])
    XPumPC = ((definicoes.playerDict["pedraXP"] + definicoes.playerDict["pedraXpProx"]) + 1) / 120.0
    barraXP = definicoes.playerDict["pedraXP"] / XPumPC

    barraPedraFull = start.multi_box(boxSkill.left + 10, (boxSkill.top + 30),
                                     120, 25,
                                     definicoes.cinza_claro, "no")
    barraPedraXP = start.multi_box(boxSkill.left + 10, (boxSkill.top + 30),
                                   barraXP, 25,
                                   definicoes.vermelho, "no")
    barraTextoPedra = start.input_text(textoPedra, (barraPedraXP.left + 60),
                                       (barraPedraFull.top + 12.5), definicoes.branco_ostra, "sim")

    #Trabalho com madeira
    textoMadeira = "Madeira LV: " + str(definicoes.playerDict["madeiraLV"])
    XPumPCMadeira = ((definicoes.playerDict["madeiraXP"] + definicoes.playerDict["madeiraXpProx"]) + 1) / 120.0
    MadeiraBarraXP = definicoes.playerDict["madeiraXP"] / XPumPCMadeira

    barraMadeiraFull = start.multi_box((boxSkill.left + 10), (barraPedraFull.bottom + 3),
                                       120, 25,
                                       definicoes.cinza_claro, "no")
    barraMadeiraXP = start.multi_box((boxSkill.left + 10), (barraPedraFull.bottom + 3),
                                     MadeiraBarraXP, 25,
                                     definicoes.vermelho, "no")
    barraTextoMadeira = start.input_text(textoMadeira, (barraMadeiraXP.left + 60),
                                         (barraMadeiraFull.top + 12.5), definicoes.branco_ostra, "sim")
    

    #fim box skill #######################################################################################
    
    #localizacao dos itens
    tamanho  = 42
    tamanho_BAG = 5
    for l in range(0, tamanho_BAG, 1):
        for j in range(0, tamanho_BAG, 1):
            j = pygame.draw.rect(definicoes.screen, definicoes.marron,
                                 ((definicoes.OpenMenu_rect.right - ((tamanho_BAG * tamanho) - (tamanho * j))),
                                  (definicoes.OpenMenu_rect.bottom - ((tamanho_BAG * tamanho) - (tamanho * l))), tamanho, tamanho))
            Iten_Menu.append(j)

    #imprime a quantia de dinheiro do player
    textoGold = "GOLD: " + str(definicoes.playerDict["moedas"])
    gold = start.multi_box(definicoes.OpenMenu_rect.right - 210, Iten_Menu[0].top - 27, 210, 25,
                           definicoes.branco_ostra, "Yes", textoGold, definicoes.amarelo_ocre)
    
                             
    #iten no menu se existir algum
    try:
        for keys in definicoes.inventario:
            load_menu_iten(keys, inventario_Loop, Iten_Menu)
            descricao_Menu[keys] = Iten_Menu[inventario_Loop]
            inventario_Loop += 1
            
    except:
        print "erro: sem itens no inventario ou erro na criacao dos itens no menu"

        

    all_rects = {"descricao_tela": descricao_tela,
                 "close_Menu": close_Menu,
                 "barra_status": barra_status,
                 "barra_status_lvl": barra_status_lvl,
                 "barra_status_xp_next": barra_status_xp_next,
                 "barra_status_vida": barra_status_vida,               
                 }
    
    pygame.display.update()
    return all_rects, descricao_Menu

def menu_button():

    close = False #sair do menu
    verf_ob = 0

    all_rects, descricao_Menu = imprimir_menu()
              
    #acoes enquanto o menu estiver aberto
    while not close:

        mouse_pos = pygame.mouse.get_pos()
        x = mouse_pos[0]
        y = mouse_pos[1]
        pressed = pygame.mouse.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if all_rects["close_Menu"].collidepoint(mouse_pos):
                    close = True
                    map_loader.load_tela(definicoes.playerDict["LARG"], definicoes.playerDict["LALT"])
                    player.player_load()
                    
                try:
                    if usar.collidepoint(mouse_pos):
                        itens_opt.opt_acao(qual_iten, "usar")
                        qual_iten = 0
                        all_rects, descricao_Menu = imprimir_menu()
                        
                    if drop.collidepoint(mouse_pos):
                        itens_opt.opt_acao(qual_iten, "drop")
                        qual_iten = 0
                        all_rects, descricao_Menu = imprimir_menu()
                except:
                    print "erro usar collide"
                    
                    
            #codigo para menu de opcoes botao direito
            if pressed == (0,0,1):
                
                #funcao que verifica qual iten clicado
                qual_iten = iten_press(mouse_pos, descricao_Menu) 
                if qual_iten != 0:
                    
                    #funcao que cria menu com usar e dropar
                    option_box, usar, drop = new_rect(x, y) 
                    verf_op = 1
            try:
                #funcao que apaga a box com opcoes se mouse sair de cima
                if not option_box.collidepoint(mouse_pos): 
                    if verf_op == 1:
                        
                        #funcao que chama tela de menu novamente
                        all_rects, descricao_Menu = imprimir_menu() 
                        verf_op = 0
            except:
                print "erro no mouse_option not collide"

            #funcao que imprime a descricao na parte inferior da tela, ao lado do botao menu        
            #print_descricao(mouse_pos, descricao_Menu)
                                                         
        definicoes.clock.tick(10)

def new_rect(x, y):
    
    novo = pygame.draw.rect(definicoes.screen, definicoes.branco_ostra, (x, y, 100, 50))
    usar = start.multi_box(novo.left + 10, novo.top, 80, 25, definicoes.branco_ostra, "Yes", "Usar")
    drop = start.multi_box(novo.left + 10, novo.top + 25, 80, 25, definicoes.branco_ostra, "Yes", "Drop")
    pygame.display.update()
    return novo, usar, drop

def iten_press(x11, descricao_Menu):
    
    for keys in descricao_Menu:
        if descricao_Menu[keys].collidepoint(x11):
            return keys

    return 0


def print_descricao(x11, descricao_Menu):

    texto = definicoes.texto

    for keys in descricao_Menu:
        if descricao_Menu[keys].collidepoint(x11):
            definicoes.texto = keys + ": " + str(definicoes.inventario[keys])

    if texto != definicoes.texto:
        map_loader.load_menu(definicoes.cinza)


def load_menu_iten(keys, loop, Iten_Menu):

    spriteDef = definicoes.stats[keys]

    rect = spriteDef["rect"]
    img = definicoes.sprites[keys]

    y = Iten_Menu[loop].centery - (rect.height / 2)
    x = Iten_Menu[loop].centerx - (rect.width / 2)
    definicoes.screen.blit(img, (x, y))

    quantidade = definicoes.inventario[keys]

    if quantidade > 999 and quantidade < 999999:
        quantidade = definicoes.inventario[keys] / 1000
        quantidade_text = str(quantidade) + "k"
    elif quantidade > 999999:
        quantidade = definicoes.inventario[keys] / 1000000
        quantidade_text = str(quantidade) + "m"
    else:
        quantidade_text = str(quantidade)

    start.input_text(quantidade_text, Iten_Menu[loop].centerx, Iten_Menu[loop].centery, definicoes.white, "Yes")


