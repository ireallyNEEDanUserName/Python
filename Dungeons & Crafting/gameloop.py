import pygame, sys
import definicoes, start, player, map_loader, menu


#escrever uma direcao a ser tomada quando apertar as teclas de move,
#e quando soltar a tecla definir a direcao como nenhuma, rodar o grafico
#de move em uma funcao separada que e chamada usando a direcao atual como
#parametro

def gameplay():
    gameplay = True
    direcao = ''

    while gameplay:
        x = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            definicoes.direcao = event.type
                
            if event.type == pygame.KEYDOWN:
                definicoes.direcao = pygame.key.name(event.key)
                direcao = event.key


        #se clicar no botao de menu e save
        try:
            if definicoes.menu_rect[1].collidepoint(x):
                map_loader.load_menu(definicoes.cinza)
            elif definicoes.menu_rect[2].collidepoint(x):
                map_loader.load_menu(definicoes.white, definicoes.cinza)
            else:
                map_loader.load_menu()

            #entrou no menu
            if event.type == pygame.MOUSEBUTTONDOWN:
                if definicoes.menu_rect[1].collidepoint(x):
                    menu.menu_button()
                    
                if definicoes.menu_rect[2].collidepoint(x):
                    start.save()
                
        except:
            print "erro ao encontrar o menu"

        if definicoes.direcao in definicoes.keyPossiveis and direcao != "":
            direcao = andar(direcao)
            definicoes.direcao_anterior = definicoes.direcao
        
        definicoes.espaco_loop += 1   
        pygame.display.update()
                    
        #frames p/s
        definicoes.clock.tick(definicoes.FPS)


def andar(direcao):
    direcao = player.mov_player(direcao)
    map_loader.draw_map_call(direcao)
    return direcao
    
