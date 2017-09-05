import pygame, sys, random
import map_loader, player, definicoes, start


def callCombate():

    #adicionar efeito de combate, uma tela com acoes realizadas,
    #mostrar lucros do combate e vida na tela de status do player

    endCombat = False
    definicoes.monsterLife = 50

    ataque, fugir = load_tela_combat()


    while not endCombat:
        mouse = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if fugir.collidepoint(mouse):
                    
                    endCombat = True
                    map_loader.load_tela(definicoes.playerDict["LARG"], definicoes.playerDict["LALT"])
                    player.player_load()

                if ataque.collidepoint(mouse):
                    #criar uma funcao que chama todos os rects de status e monstros para atualizar texto na tela.
                    definicoes.monsterATK = 5
                    status_batalha= ataqueFunc()

                    ataque, fugir = load_tela_combat()
                    
                    if status_batalha == "end":
                        endCombat = True
                        map_loader.load_tela(definicoes.playerDict["LARG"], definicoes.playerDict["LALT"])
                        player.player_load()
                        
                    elif status_batalha == "game over":
                        GM = pygame.image.load("GAME_OVER.png")
                        definicoes.screen.fill(definicoes.white, definicoes.scr_rect)
                        definicoes.screen.blit(GM, (0,0))
                        

        definicoes.clock.tick(5)
        pygame.display.update()
        
#criar um dicionario para status dos monstros.
def ataqueFunc():

    rand = random.randrange(5)
    definicoes.monsterATK *= rand

    definicoes.monsterLife -= definicoes.playerDict["Ataque"]

    definicoes.playerDict["TVida"] -= definicoes.monsterATK

    if definicoes.playerDict["TVida"] <= 0:

        return "game over"

    if definicoes.monsterLife <= 0:

        definicoes.playerDict["exp"] += 10
        definicoes.playerDict["moedas"] += 10
        definicoes.playerDict["Ganhou"] += 1

        definicoes.texto = "Ganhou: XP -> 5 ; MOEDAS -> 5"
        map_loader.load_menu(definicoes.cinza)
        
        player.atualiza_lvl("luta")

        return "end"

    else:
        return "continue"

    
def load_tela_combat():

    
    #tela de combate
    definicoes.screen.fill(definicoes.branco_ostra, definicoes.OpenMenu_rect)

    #barra de status
    statusBar = pygame.draw.rect(definicoes.screen, definicoes.vermelho_claro,
                                 (definicoes.OpenMenu_rect.left + 50,
                                  (definicoes.OpenMenu_rect.height / 2) - 30, 100, 25))
    statusText = "Vida: " + str(definicoes.playerDict["TVida"])

    monsterBar = pygame.draw.rect(definicoes.screen, definicoes.vermelho_claro,
                                 (definicoes.OpenMenu_rect.right - 150,
                                  (definicoes.OpenMenu_rect.height / 2) - 30, 100, 25))
    
    monsterText = "Vida: " + str(definicoes.monsterLife)

    #localizacao do player na tela
    localizacaoPlayer = pygame.draw.rect(definicoes.screen, definicoes.branco_ostra,
                                         (definicoes.OpenMenu_rect.left + 50,
                                          definicoes.OpenMenu_rect.height / 2, 100, 100))

    #localizacao do monstro na tela
    localizacaoMonstro = pygame.draw.rect(definicoes.screen, definicoes.branco_ostra,
                                          (definicoes.OpenMenu_rect.right - 150,
                                           definicoes.OpenMenu_rect.height / 2, 100, 100))
        

    #imprimir texto de status na tela    
    start.input_text(statusText, (statusBar.left + (statusBar.width / 2)), (statusBar.top + (statusBar.height / 2)), definicoes.white, "yes")
    start.input_text(monsterText, (monsterBar.right - (monsterBar.width / 2)),
                     (monsterBar.top + (monsterBar.height / 2)), definicoes.white, "yes")

    #imprimir player na tela
    x = localizacaoPlayer.centerx - (definicoes.player_rect.width / 2)
    y = localizacaoPlayer.centery - (definicoes.player_rect.height / 2)
    definicoes.screen.blit(definicoes.playerD, (x, y))

    #imprimir monstro na tela
    x = localizacaoMonstro.centerx - (definicoes.corvo_rect.width / 2)
    y = localizacaoMonstro.centery - (definicoes.corvo_rect.height / 2)
    definicoes.screen.blit(definicoes.corvo, (x, y))

    #botao de ataque e fugir
    ataque = start.multi_box(definicoes.OpenMenu_rect.left, definicoes.OpenMenu_rect.bottom - 56, 80, 25,
                            definicoes.vermelho, "Yes", "Ataque", definicoes.white)
    fugir = start.multi_box(definicoes.OpenMenu_rect.left, definicoes.OpenMenu_rect.bottom - 30, 80, 25,
                            definicoes.vermelho, "Yes", "Fugir", definicoes.white)

    return ataque, fugir
    
    
    

    
    
    
        

            
    
