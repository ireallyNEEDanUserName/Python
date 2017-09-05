import pygame
import definicoes, start, map_loader, player


def opt_acao(iten_acao, acao):

    if acao == "usar":
        if iten_acao == "pocao" and definicoes.inventario[iten_acao] > 0:

            pocaoAcao = definicoes.stats[iten_acao]
            
            if definicoes.playerDict["TVida"] < definicoes.playerDict["Vida"]:
                definicoes.playerDict["TVida"] += pocaoAcao["acao"]
                definicoes.inventario[iten_acao] -= 1
                
                if definicoes.playerDict["TVida"] > definicoes.playerDict["Vida"]:
                    definicoes.playerDict["TVida"] = definicoes.playerDict["Vida"]

            definicoes.texto = + str(pocaoAcao["acao"]) + " hp Recuperado!!"
            map_loader.load_menu(definicoes.cinza)
            
            if definicoes.inventario[iten_acao] == 0:
                del definicoes.inventario[iten_acao]

        elif iten_acao == "pedra" and definicoes.inventario[iten_acao] > 0:
            if definicoes.inventario[iten_acao] >= 5:
                
                if definicoes.inventario.has_key('bloco'):
                    definicoes.inventario["bloco"] += 1
                else:
                    definicoes.inventario["bloco"] = 1
                    
                definicoes.inventario[iten_acao] -= 5
                xp = definicoes.stats["bloco"]
                definicoes.playerDict[(iten_acao + "XP")] += xp["xp"]
                upou = player.atualiza_lvl(iten_acao)

                if upou == True:
                    definicoes.texto = " Level Up!! " + str(definicoes.playerDict[(iten_acao+"LV")])
                else:
                    definicoes.texto = "Bloco criado com sucesso!"
                map_loader.load_menu(definicoes.cinza)
            
            if definicoes.inventario[iten_acao] == 0:
                del definicoes.inventario[iten_acao]

        elif iten_acao == "madeira" and definicoes.inventario[iten_acao] > 0:
            if definicoes.inventario[iten_acao] >= 3:

                if definicoes.inventario.has_key('graveto'):
                    definicoes.inventario["graveto"] += 1
                else:
                    definicoes.inventario["graveto"] = 1

                definicoes.inventario[iten_acao] -= 3
                
                xp = definicoes.stats["graveto"]
                definicoes.playerDict[(iten_acao + "XP")] += xp["xp"]
                upou = player.atualiza_lvl(iten_acao)

                if upou == True:
                    definicoes.texto = " Level Up!! " + str(definicoes.playerDict[(iten_acao+"LV")])
                else:
                    definicoes.texto = "Graveto criado com sucesso!"
                map_loader.load_menu(definicoes.cinza)
            
            if definicoes.inventario[iten_acao] == 0:
                del definicoes.inventario[iten_acao]
                

    if acao == "drop":
        if definicoes.inventario[iten_acao] > 0:
            definicoes.inventario[iten_acao] -= 1
            if definicoes.inventario[iten_acao] == 0:
                del definicoes.inventario[iten_acao]
            
            
