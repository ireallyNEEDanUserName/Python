import pygame, random
import start, definicoes, combat, shop

def player_load_first():
     
     definicoes.player_rect.centerx = definicoes.playerDict["PosX"]
     definicoes.player_rect.centery = definicoes.playerDict["PosY"]
     definicoes.screen.blit(definicoes.player, definicoes.player_rect)

def player_load():

     framePlayer = definicoes.player
     frame = definicoes.loop_andar % 2
     
     if definicoes.direcao == "right":
          if definicoes.loop_andar > 0:
               if frame != 0:
                    framePlayer = definicoes.playerD1
               else:
                    framePlayer = definicoes.playerD2
          else:
               framePlayer = definicoes.playerD
          
     elif definicoes.direcao == "left":
          if definicoes.loop_andar > 0:
               if frame != 0:
                    framePlayer = definicoes.playerE1
               else:
                    framePlayer = definicoes.playerE2
          else:
               framePlayer = definicoes.playerE
          
     elif definicoes.direcao == "up":
          if definicoes.loop_andar > 0:
               if frame != 0:
                    framePlayer = definicoes.playerC1
               else:
                    framePlayer = definicoes.playerC2
          else:
               framePlayer = definicoes.playerC
               
     else:
          if definicoes.loop_andar > 0:
               if frame != 0:
                    framePlayer = definicoes.player1
               else:
                    framePlayer = definicoes.player2
          else:
               framePlayer = definicoes.player

          
     definicoes.screen.blit(framePlayer, definicoes.player_rect)
    
def mov_player(dir_player):

     #gerar numero random para entrar em combate
     rand = random.randrange(2500) 

     #Tratando acao
     if dir_player == pygame.K_SPACE:
          iten = 0
          #Adicionar inventario
          if definicoes.espaco_loop % 5 == 0:
               definicoes.checkIter, iten = check_interacao()
               if definicoes.checkIter == True:
                    atualiza_invt(iten)
          definicoes.direcao = definicoes.direcao_anterior

     #funcao para entrar em combate
     elif rand <= definicoes.chanceDeCombate:
          combat.callCombate()
          dir_player = ""
          return dir_player
          
                    
     #terminar de fazer a identacao
     else:
          definicoes.player_rect_last_move = definicoes.player_rect

          if dir_player == pygame.K_LEFT:
               definicoes.direcao = pygame.key.name(dir_player)
               if definicoes.player_rect.left < 0:
                    pass
               else:
                    if check_colisao(-definicoes.movePlayer,0):
                         pass
                    else:
                         if definicoes.direcao_anterior == "left":
                              definicoes.contadorFrame += 1
                              if definicoes.contadorFrame % 8 == 0:
                                   definicoes.loop_andar += 1
                                   if definicoes.loop_andar > 2:
                                        definicoes.loop_andar = 0
                         else:
                              definicoes.loop_andar = 0
                              definicoes.contadorFrame = 0
                         definicoes.player_rect = definicoes.player_rect.move(-definicoes.movePlayer,0)

          elif dir_player == pygame.K_RIGHT:
               definicoes.direcao = pygame.key.name(dir_player)
               if definicoes.player_rect.right < -definicoes.width:
                    pass
               else:
                    if check_colisao(definicoes.movePlayer,0):
                         pass
                    else:
                         if definicoes.direcao_anterior == "right":
                              definicoes.contadorFrame += 1
                              if definicoes.contadorFrame % 8 == 0:
                                   definicoes.loop_andar += 1
                                   if definicoes.loop_andar > 2:
                                        definicoes.loop_andar = 0
                         else:
                              definicoes.loop_andar = 0
                              definicoes.contadorFrame = 0
                         definicoes.player_rect = definicoes.player_rect.move(definicoes.movePlayer,0)
        
          elif dir_player == pygame.K_UP:
               definicoes.direcao = pygame.key.name(dir_player)
               if definicoes.player_rect.top < 0:
                    pass
               else:
                    if check_colisao(0,-definicoes.movePlayer):
                         pass
                    else:
                         if definicoes.direcao_anterior == "up":
                              definicoes.contadorFrame += 1
                              if definicoes.contadorFrame % 8 == 0:
                                   definicoes.loop_andar += 1
                                   if definicoes.loop_andar > 2:
                                        definicoes.loop_andar = 0
                         else:
                              definicoes.loop_andar = 0
                              definicoes.contadorFrame = 0
                         definicoes.player_rect = definicoes.player_rect.move(0, -definicoes.movePlayer)
        
          elif dir_player == pygame.K_DOWN:
               definicoes.direcao = pygame.key.name(dir_player)
               if definicoes.player_rect.bottom > (definicoes.height - 50):
                    pass
               else:
                    if check_colisao(0,definicoes.movePlayer):
                         pass
                    else:
                         if definicoes.direcao_anterior == "down":
                              definicoes.contadorFrame += 1
                              if definicoes.contadorFrame % 8 == 0:
                                   definicoes.loop_andar += 1
                                   if definicoes.loop_andar > 2:
                                        definicoes.loop_andar = 0
                         else:
                              definicoes.loop_andar = 0
                              definicoes.contadorFrame = 0
                         definicoes.player_rect = definicoes.player_rect.move(0, definicoes.movePlayer)
        
     return dir_player
     
     
def atualiza_invt(iten):
     var = ''
     #verifica qual iten foi adiquirido
     
     var = definicoes.interagir[iten]

     if var == "porta":
          return 0

     #atualiza o exp e o lvl
     definicoes.playerDict[(var + "XP")] += 5
     upou = atualiza_lvl(var)

     #adiciona o iten na variavel do inventario     
     try:
          j = definicoes.inventario[var]
     except:
          j = 0
     j += 1
     definicoes.inventario[var] = j

     #mostra o texto correspondente ao que e verdadeiro.
     if upou == True:
          definicoes.texto = " Level Up!! " + str(definicoes.playerDict[(var+"LV")])
     else:
          definicoes.texto = var + ": " + str(definicoes.inventario[var])
   

def atualiza_lvl(var):
     
     if var != "luta":
          #print definicoes.playerDict[(var+"LV")], definicoes.playerDict[(var+"XP")], definicoes.playerDict[(var+"XpProx")], definicoes.playerDict[(var+"TotalXP")]
          exp_Necessario = ((definicoes.playerDict[(var+"LV")] + 1) * (definicoes.playerDict[(var+"LV")] + 1)) * ((definicoes.playerDict[(var+"LV")] * 10) / 2)
          definicoes.playerDict[(var+"XpProx")] = exp_Necessario - definicoes.playerDict[(var+"XP")]
          if definicoes.playerDict[(var+"XpProx")] == 0:
               definicoes.playerDict[(var+"TotalXP")] += definicoes.playerDict[(var+"XP")]
               definicoes.playerDict[(var+"XP")] -= exp_Necessario
               definicoes.playerDict[(var+"LV")] += 1
               return True
               
     else:
          exp_Necessario = ((definicoes.playerDict["level"] + 1) * (definicoes.playerDict["level"] + 1)) * ((definicoes.playerDict["level"] * 10) / 2)
          definicoes.playerDict["expProxLVL"] = exp_Necessario - definicoes.playerDict["exp"]
          if definicoes.playerDict["expProxLVL"] == 0:
               definicoes.playerDict["expTotal"] += definicoes.playerDict["exp"]
               definicoes.playerDict["exp"] -= exp_Necessario
               definicoes.playerDict["level"] += 1
               definicoes.playerDict["Vida"] = definicoes.playerDict["level"] * 10
               definicoes.playerDict["TVida"] = definicoes.playerDict["Vida"]
               definicoes.playerDict["Ataque"] = definicoes.playerDict["level"] * 5
               definicoes.playerDict["Defesa"] = definicoes.playerDict["level"] * 2
               return True

        
def check_colisao(x, y):

    p_rect = definicoes.player_rect
    p_rect = p_rect.move(x, y)
    
    if x > 0:
        posx = (p_rect.centerx + 18) / 32
        posy = (p_rect.centery + 9) / 32
    elif y > 0:
        posx = (p_rect.centerx - 9) / 32
        posy = (p_rect.centery + 18) / 32
    elif x < 0:
        posx = (p_rect.centerx - 18) / 32
        posy = (p_rect.centery + 9) / 32
    elif y < 0:
        posx = (p_rect.centerx - 9) / 32
        posy = (p_rect.centery - 18) / 32

    
    posdef = ((posy + definicoes.playerDict["LALT"]) * definicoes.data_comp) + (posx + definicoes.playerDict["LARG"])

    if definicoes.data_backLayer1_manipulavel[posdef] in definicoes.colisao or definicoes.data_backLayer0_manipulavel[posdef] in definicoes.colisao:
         return True
    else:
         return False
    
def check_interacao():

     pos = 0
     locais = "nenhum"
    
     p_rect = definicoes.player_rect
     #direita
     p_rect = p_rect.move(definicoes.movePlayer, 0)
     posxD = (p_rect.centerx + 18) / 32
     posyD = (p_rect.centery + 12) / 32
     #baixo
     p_rect = p_rect.move(-definicoes.movePlayer, definicoes.movePlayer)
     posxB = (p_rect.centerx - 12) / 32
     posyB = (p_rect.centery + 18) / 32
     #esquerda
     p_rect = p_rect.move(-definicoes.movePlayer, -definicoes.movePlayer)
     posxE = (p_rect.centerx - 18) / 32
     posyE = (p_rect.centery + 12) / 32
     #cima
     p_rect = p_rect.move(definicoes.movePlayer, (definicoes.movePlayer * 2))
     posxC = (p_rect.centerx - 15) / 32
     posyC = (p_rect.centery - 25) / 32
    
     posdefD = ((posyD + definicoes.playerDict["LALT"]) * definicoes.data_comp) + (posxD + definicoes.playerDict["LARG"])
     posdefE = ((posyE + definicoes.playerDict["LALT"]) * definicoes.data_comp) + (posxE + definicoes.playerDict["LARG"])
     posdefC = ((posyC + definicoes.playerDict["LALT"]) * definicoes.data_comp) + (posxC + definicoes.playerDict["LARG"])
     posdefB = ((posyB + definicoes.playerDict["LALT"]) * definicoes.data_comp) + (posxB + definicoes.playerDict["LARG"])

     
     if definicoes.data_backLayer1_manipulavel[posdefC] in definicoes.locais:
          locais = "inn" 
     
     elif definicoes.data_backLayer1_manipulavel[posdefD] in definicoes.interagir:
          pos = posdefD
 
     elif definicoes.data_backLayer1_manipulavel[posdefE] in definicoes.interagir:
          pos = posdefE

     elif definicoes.data_backLayer1_manipulavel[posdefC] in definicoes.interagir:
          pos = posdefC

     elif definicoes.data_backLayer1_manipulavel[posdefB] in definicoes.interagir:
          pos = posdefB

     else:
          return False, 0


     if pos != 0:
          definicoes.mudancas[pos] = definicoes.data_backLayer1_manipulavel[pos]
          definicoes.data_backLayer1_manipulavel[pos] = 0

          return True, definicoes.mudancas[pos]
     
     elif locais == "inn":
          shop.load()

          return False, 0

    
