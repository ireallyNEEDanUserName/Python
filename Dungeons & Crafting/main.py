import sys, pygame
#modulos escritos por mim.
import start, definicoes, player, map_loader, menu, gameloop, spritesLoad

#intro screen
intro = pygame.image.load("1.jpg")
definicoes.screen.blit(intro,(0,0))
pygame.display.update()

#load nos sprites e definicoes dos itens
spritesLoad.Load()

while True:
    x = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            
        # lidar com mouse
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if definicoes.menu == 0:
                start.menu_call()
                definicoes.menu += 1

            #new game and continue
            if definicoes.menu == 1:
                if 385 > x[0] > 215 and 435 > x[1] > 370:
                    definicoes.menu += 1
                    #new game
                    if x[1] >= 370 and x[1] <= 400:
                        start.new()
                                    
                    #continue
                    else:
                        basic = pygame.image.load("basic.jpg").convert_alpha()
                        definicoes.screen.blit(basic, (0,0))
                        pygame.display.update()
                        start.load()
                        definicoes.menu += 1

    
    #inicio do jogo
    if definicoes.menu >= 2:
    
        gameloop.gameplay()



    
        

