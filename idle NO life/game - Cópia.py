import pygame
import json
from datetime import datetime
import time
from random import randint

###################################FUNC TEMPO######################################
def Tempo(tempo):

    tempo += tempoSoma
    
    horas = minutos = segundos = 0
    if(tempo > 60):
        minutos = tempo / 60
        if(minutos > 60):
            horas = minutos / 60
            minutos = minutos - (horas * 60)
            segundos = tempo - ((horas * 3600) + (minutos * 60))
        else:
            segundos = tempo - (minutos * 60)
            if(segundos < 0):
                segundos = 0
    else:
        segundos = tempo
        
    horario = "H: " + str(horas) + " M: " + str(minutos) + " S: " + str(segundos) + "   "
    return horario

###############MINING###########################################################

def Skills(StatusRect):

    Menu(branco)

    Mining = fonte.render("Mining", 3, (branco), (preto))
    MiningRect = Mining.get_rect()
    MiningRect = MiningRect.move(0, StatusRect.bottom + 5)

    Slaves = fonte.render("Slaves", 3, (branco), (vermelho_escuro))
    SlavesRect = Slaves.get_rect()
    SlavesRect = SlavesRect.move(0, MiningRect.bottom + 5)

    screen.blit(Mining, MiningRect)
    screen.blit(Slaves, SlavesRect)
    

    return MiningRect, SlavesRect

def MiningSCR(StatusRect):
    Menu(branco)

    textoTempoMinerar = fonte.render("Tempo para Minerar", 1, (preto))
    textoTempoMinerarRect = textoTempoMinerar.get_rect()
    textoTempoMinerarRect = textoTempoMinerarRect.move(0, StatusRect.bottom + 5)
    
    texttempoMining = fonte.render((Tempo(jogador.jogadorDict["tempoMining"] - tempoSoma)), 1, (preto))
    texttempoMiningRect = texttempoMining.get_rect()
    texttempoMiningRect = texttempoMiningRect.move(0, textoTempoMinerarRect.bottom + 3)

    screen.blit(textoTempoMinerar, textoTempoMinerarRect)
    screen.blit(texttempoMining, texttempoMiningRect)

    x = 1
    y = 0
    rectsMining = []

    while x <= len(jogador.catalogoMining):
        if jogador.jogadorDict["miningLvl"] >= int(jogador.catalogoMiningLevel[str(x)]):
            Minerio = fonte.render(jogador.catalogoMining[str(x)], 1, (branco), (preto))
            rectsMining.append(Minerio.get_rect())
        
            if y == 0:
                rectsMining[y] = rectsMining[y].move(0, texttempoMiningRect.bottom + 7)
            else:
                rectsMining[y] = rectsMining[y].move(0, rectsMining[y - 1].bottom + 2)
            
            screen.blit(Minerio, rectsMining[y])
            y += 1
        x = x + 1

    return rectsMining

def Mining(utilizador):
    
    utilizador2 = utilizador
    x = "jogador"
    
    if not utilizador == jogador.jogadorDict:
        utilizador2 = jogador.jogadorDict
        x = "slave"

    if utilizador["tempoMining"] > 0:
        utilizador["tempoMining"] -= 1

        if (utilizador["tempoMining"] == 0 or
            (utilizador["tempoMining"] % (40 + (utilizador["pedraAtual"] * 20)) == 0)):

            if jogador.catalogoMining[str(utilizador["pedraAtual"])] not in jogador.jogadorInv:
                jogador.jogadorInv[jogador.catalogoMining[str(utilizador["pedraAtual"])]] = 1 * (utilizador["miningLvl"] /
                                                                                                 utilizador["pedraAtual"])
            else:
                jogador.jogadorInv[jogador.catalogoMining[str(utilizador["pedraAtual"])]] += 1 * (utilizador["miningLvl"] /
                                                                                                  utilizador["pedraAtual"])

            if x == "jogador":
                utilizador2["miningExp"] += 10 * (utilizador["pedraAtual"] * utilizador["miningLvl"])
            elif x == "slave":
                utilizador2["miningExp"] += 10 * utilizador["pedraAtual"]
                utilizador2["slaveMasterExp"] += utilizador["pedraAtual"]
                utilizador["miningExp"] += utilizador["pedraAtual"]
                
                LevelUp(utilizador, "miningLvl", "miningExp")
                LevelUp(utilizador2, "slaveMasterLvl", "slaveMasterExp")

            LevelUp(utilizador2, "miningLvl", "miningExp")

            if utilizador["tempoMining"] == 0:
                utilizador["pedraAtual"] = 0
                

def SlavesSCR(StatusRect):
    Menu(branco)
    
    x = 0
    rectsSlavesNome = []
    rectsSlavesLvl = []
    rectsSlavesPedra = []
    rectsSlaveTempo = []

    for key in jogador.slavesDict:
        
        nomeSlave = fonte.render(str(jogador.slavesDict[key]["nome"]), 1, (branco), (vermelho_escuro))
        slaveLvl = fonte.render("Lvl: " + str(jogador.slavesDict[key]["miningLvl"]), 1, (branco), (preto))

        pedra = jogador.catalogoMining[str(jogador.slavesDict[key]["pedraAtual"])]
        slavePedra = fonte.render(pedra, 1, (branco), (preto))
        tempoSkill = fonte.render("Tempo: " + str(jogador.slavesDict[key]["tempoMining"]), 1, (branco), (preto))


        rectsSlaveTempo.append(tempoSkill.get_rect())
        rectsSlavesPedra.append(slavePedra.get_rect())    
        rectsSlavesLvl.append(slaveLvl.get_rect())
        rectsSlavesNome.append(nomeSlave.get_rect())

        
        if x == 0:
            rectsSlavesNome[x] = rectsSlavesNome[x].move(0, StatusRect.bottom + 5)
            rectsSlavesLvl[x] = rectsSlavesLvl[x].move(rectsSlavesNome[x].right + 5, StatusRect.bottom + 5)
            rectsSlavesPedra[x] = rectsSlavesPedra[x].move(rectsSlavesLvl[x].right + 5, StatusRect.bottom + 5)
            rectsSlaveTempo[x] = rectsSlaveTempo[x].move(rectsSlavesPedra[x].right + 5, StatusRect.bottom + 5)
            
        else:
            rectsSlavesNome[x] = rectsSlavesNome[x].move(0, rectsSlavesNome[x - 1].bottom + 2)
            rectsSlavesLvl[x] = rectsSlavesLvl[x].move(rectsSlavesNome[x].right + 5, rectsSlavesNome[x - 1].bottom + 2)
            rectsSlavesPedra[x] = rectsSlavesPedra[x].move(rectsSlavesLvl[x].right + 5, rectsSlavesNome[x - 1].bottom + 2)
            rectsSlaveTempo[x] = rectsSlaveTempo[x].move(rectsSlavesPedra[x].right + 5, rectsSlavesNome[x - 1].bottom + 2)
    
        screen.blit(nomeSlave, rectsSlavesNome[x])
        screen.blit(slavePedra, rectsSlavesPedra[x])
        screen.blit(tempoSkill, rectsSlaveTempo[x])
        screen.blit(slaveLvl, rectsSlavesLvl[x])

        x += 1

def Dungeon(StatusRect):
    Menu(preto)
    
    dungeonLevel = fonte.render("Ultimo Andar Alcancado: " + str(jogador.combateDict["ultimaDungeon"]), 1, (branco), (vermelho_escuro))
    dungeonLevelRect = dungeonLevel.get_rect()
    dungeonLevelRect = dungeonLevelRect.move(0, StatusRect.bottom + 5)

    dungeonLevelMaximo = fonte.render("Maior Andar Alcancado: " + str(jogador.combateDict["maiorDungeon"]), 1, (branco), (vermelho_escuro))
    dungeonLevelMaximoRect = dungeonLevelMaximo.get_rect()
    dungeonLevelMaximoRect = dungeonLevelMaximoRect.move(dungeonLevelRect.right + 5, StatusRect.bottom + 5)

    mobsMaximo = fonte.render("Total de Mobs Mortos: " + str(jogador.combateDict["mobsMortosTotal"]), 1, (branco), (vermelho_escuro))
    mobsMaximoRect = mobsMaximo.get_rect()
    mobsMaximoRect = mobsMaximoRect.move(0, dungeonLevelMaximoRect.bottom + 5)
    
    entrarDungeon = fonte.render("Entrar", 1, (branco), (vermelho_escuro))
    entrarDungeonRect = entrarDungeon.get_rect()
    entrarDungeonRect = entrarDungeonRect.move(mobsMaximoRect.right + 5, dungeonLevelMaximoRect.bottom + 5)

    ########Status Player############
    jogadorLvlRect = JogadorStats(10, entrarDungeonRect.bottom + 7)

    ######Botoes para Upar############
    botaoVida = fonte.render(" + ", 1, (branco), (vermelho))
    botaoVidaRect = botaoVida.get_rect()
    botaoVidaRect = botaoVidaRect.move(200, jogadorLvlRect.bottom + 2)

    botaoAtaque = fonte.render(" + ", 1, (branco), (vermelho))
    botaoAtaqueRect = botaoAtaque.get_rect()
    botaoAtaqueRect = botaoAtaqueRect.move(botaoVidaRect.left, botaoVidaRect.bottom + 2)

    botaoCritico = fonte.render(" + ", 1, (branco), (vermelho))
    botaoCriticoRect = botaoCritico.get_rect()
    botaoCriticoRect = botaoCriticoRect.move(botaoVidaRect.left, botaoAtaqueRect.bottom + 2)

    botaoDefesa = fonte.render(" + ", 1, (branco), (vermelho))
    botaoDefesaRect = botaoDefesa.get_rect()
    botaoDefesaRect = botaoDefesaRect.move(botaoVidaRect.left, botaoCriticoRect.bottom + 2)

    botaoChanceDefesa = fonte.render(" + ", 1, (branco), (vermelho))
    botaoChanceDefesaRect = botaoChanceDefesa.get_rect()
    botaoChanceDefesaRect = botaoChanceDefesaRect.move(botaoVidaRect.left, botaoDefesaRect.bottom + 2)

    if jogador.combateDict["pontos"] > 0:

        screen.blit(botaoVida, botaoVidaRect)
        screen.blit(botaoAtaque, botaoAtaqueRect)
        screen.blit(botaoDefesa, botaoDefesaRect)
        screen.blit(botaoChanceDefesa, botaoChanceDefesaRect)
        screen.blit(botaoCritico, botaoCriticoRect)
        
    screen.blit(dungeonLevel, dungeonLevelRect)
    screen.blit(entrarDungeon, entrarDungeonRect)
    screen.blit(dungeonLevelMaximo, dungeonLevelMaximoRect)
    screen.blit(mobsMaximo, mobsMaximoRect)

    return entrarDungeonRect, botaoVidaRect, botaoAtaqueRect, botaoDefesaRect, botaoChanceDefesaRect, botaoCriticoRect

def JogadorStats(x, y):

    jogadorText = fonte.render(str(jogador.jogadorDict["nome"]), 1, (branco), (preto))
    jogadorTextRect = jogadorText.get_rect()
    jogadorTextRect = jogadorTextRect.move(x, y)

    jogadorLvl = fonte.render("Lvl: " + str(jogador.combateDict["lvl"]), 1, (branco), (preto))
    jogadorLvlRect = jogadorLvl.get_rect()
    jogadorLvlRect = jogadorLvlRect.move(jogadorTextRect.left, jogadorTextRect.bottom + 2)

    jogadorVida = fonte.render("Vida: " + str(jogador.combateDict["vidaCheia"]) + "/" + str(jogador.combateDict["vida"]), 1, (branco), (preto))
    jogadorVidaRect = jogadorVida.get_rect()
    jogadorVidaRect = jogadorVidaRect.move(jogadorTextRect.left, jogadorLvlRect.bottom + 2)

    jogadorAtaque = fonte.render("Ataque: " + str(jogador.combateDict["ataque"]), 1, (branco), (preto))
    jogadorAtaqueRect = jogadorAtaque.get_rect()
    jogadorAtaqueRect = jogadorAtaqueRect.move(jogadorTextRect.left, jogadorVidaRect.bottom + 2)

    jogadorCritico = fonte.render("Critico: " + str(jogador.combateDict["critico"]), 1, (branco), (preto))
    jogadorCriticoRect = jogadorCritico.get_rect()
    jogadorCriticoRect = jogadorCriticoRect.move(jogadorTextRect.left, jogadorAtaqueRect.bottom + 2)

    jogadorDefesa = fonte.render("Defesa: " + str(jogador.combateDict["defesa"]), 1, (branco), (preto))
    jogadorDefesaRect = jogadorDefesa.get_rect()
    jogadorDefesaRect = jogadorDefesaRect.move(jogadorTextRect.left, jogadorCriticoRect.bottom + 2)

    jogadorChanceDefesa = fonte.render("Chance de Defesa: " + str(jogador.combateDict["chanceDefesa"]), 1, (branco), (preto))
    jogadorChanceDefesaRect = jogadorChanceDefesa.get_rect()
    jogadorChanceDefesaRect = jogadorChanceDefesaRect.move(jogadorTextRect.left, jogadorDefesaRect.bottom + 2)


    screen.blit(jogadorText, jogadorTextRect)
    screen.blit(jogadorLvl, jogadorLvlRect)
    screen.blit(jogadorVida, jogadorVidaRect)
    screen.blit(jogadorAtaque, jogadorAtaqueRect)
    screen.blit(jogadorCritico, jogadorCriticoRect)
    screen.blit(jogadorDefesa, jogadorDefesaRect)
    screen.blit(jogadorChanceDefesa, jogadorChanceDefesaRect)

    return jogadorLvlRect

def MobStats():
    
    quantidadeMobs = 0
    
    for key in jogador.mobAndar:
        if jogador.mobAndar[key] <= jogador.dungeonStats["andarAtual"]:
            quantidadeMobs += 1
                
    #print "\n numero de mobs: " + str(quantidadeMobs)

    ######Status do Mob#########
        
    jogador.mobStats["mobAtual"] = randint(1, quantidadeMobs)
    jogador.mobStats["mobLevel"] = (jogador.mobStats["mobAtual"] - 1) + jogador.dungeonStats["andarAtual"]
    
    randVida = randint(1, (jogador.mobStats["mobLevel"] * jogador.mobStats["mobAtual"]))
    
    if jogador.mobStats["mobAtual"] < jogador.mobStats["mobLevel"] and jogador.mobStats["mobAtual"] != jogador.mobStats["mobLevel"]:
        randVida2 = randint(jogador.mobStats["mobAtual"], jogador.mobStats["mobLevel"])
    elif jogador.mobStats["mobLevel"] < jogador.mobStats["mobAtual"] and jogador.mobStats["mobAtual"] != jogador.mobStats["mobLevel"]:
        randVida2 = randint(jogador.mobStats["mobLevel"], jogador.mobStats["mobAtual"])
    else:
        randVida2 = randint(jogador.mobStats["mobLevel"], jogador.mobStats["mobAtual"] + 1)

    #print randVida
    #print randVida2    
    jogador.mobStats["mobVida"] = ((jogador.mobBase["vida"] * randVida) + (jogador.mobStats["mobLevel"] / 3)) * randVida2
    jogador.mobStats["mobVidaCheia"] = jogador.mobStats["mobVida"]
    
    randAtaque = randint(1, (jogador.mobStats["mobLevel"] * jogador.mobStats["mobAtual"]))
    jogador.mobStats["mobAtaque"] = (jogador.mobBase["ataque"] * randAtaque) + (jogador.mobStats["mobLevel"] / 3)
    
    randDefesa = randint(1, (jogador.mobStats["mobLevel"] * jogador.mobStats["mobAtual"]))
    jogador.mobStats["mobDefesa"] = (jogador.mobBase["defesa"] * randDefesa) + (jogador.mobStats["mobLevel"] / 3)

    #print "Achou outro Mob: " + str(jogador.mobList[str(mobAtual)])


def SelecionarItem(andarAtual):

    dictLoad = jogador.andarDropList
    randomSelecionado = 0
    itemSelecionado = 0
    chance = 0
    loop = 0
    loopSelecionado = 0

    randomSelecionado = randint(1, 100)
    #print "Andar Atual: " + str(andarAtual)
    #print "Valor do Random: " + str(randomSelecionado)

    for key in dictLoad[str(andarAtual)]:
        #print "chave da vez: " + key
        chance += dictLoad[str(andarAtual)][key]["chance"]
        #print "Chance: " + str(dictLoad[str(andarAtual)][key]["chance"])
        #print "Chance Total: " + str(chance)
        
        if randomSelecionado <= chance:
            for key in dictLoad[str(andarAtual)]:
                if loopSelecionado == loop:
                    itemSelecionado = key
                    #print "Item Selecionado: " + itemSelecionado
                    return itemSelecionado
                
                loopSelecionado += 1
                
        loop += 1
        #print "Loop: " + str(loop) + " Loop Selecionado: " + str(loopSelecionado)
    
def MobDrop():

    andarAtual = jogador.dungeonStats["andarAtual"]
    tamanhoList = len(jogador.andarDropList)
    loopLista = 2
    multiplicador = 1
    quantidade = 0
    multiplicou = False

    #print "\nAndar Atual Antes de Alterar: " + str(andarAtual)

    if tamanhoList < andarAtual:
        while loopLista <= tamanhoList:
            if andarAtual%loopLista == 0 and multiplicou == False:
                multiplicador = andarAtual / loopLista
                multiplicou = True
                andarAtual = loopLista
                #print "Loop Lista: " + str(loopLista)
            elif multiplicou == False and loopLista == tamanhoList:
                if andarAtual%1 == 0:
                    multiplicador = andarAtual
                    multiplicou = True
                    andarAtual = 1
            loopLista += 1
        #print "Multiplicador: " + str(multiplicador)

    itemSelecionado = SelecionarItem(andarAtual)

    quantidade = jogador.andarDropList[str(andarAtual)][itemSelecionado]["quantidade"]* multiplicador

    if itemSelecionado not in jogador.jogadorInv:
        #print "Quantidade: " + str(quantidade)
        jogador.jogadorInv[itemSelecionado] = quantidade
        
    else:
        jogador.jogadorInv[itemSelecionado] += quantidade
        
    #print itemSelecionado + " inventario : " + str(jogador.jogadorInv[itemSelecionado])

    jogador.mobStats["mobDrop"] = itemSelecionado
    jogador.mobStats["mobDropQuantidade"] = quantidade


def ZerarVidaMob():

    MobDrop()
            
    jogador.dungeonStats["mobsMortos"] += 1
            
    if jogador.dungeonStats["mobsMortos"] / (5 * jogador.dungeonStats["andarAtual"]) > 0:
        jogador.dungeonStats["andarAtual"] += 1
                
    exp = jogador.mobBase["exp"] + ((jogador.mobStats["mobAtual"] * jogador.mobStats["mobLevel"]) * jogador.combateDict["lvl"])
    jogador.dungeonStats["expTotal"] += exp
    jogador.combateDict["exp"] += exp
    LevelUp(jogador.combateDict, "lvl", "exp")
            
    MobStats()


def InicializarCombate():
    
    jogador.dungeonStats["andarAtual"] = 1
    jogador.dungeonStats["mobsMortos"] = 0
    jogador.dungeonStats["expTotal"] = 0
    jogador.mobStats["mobDrop"] = ""
    jogador.mobStats["mobDropQuantidade"] = 0
        
    MobStats()


def DungeonLoop(StatusRect):

    mobPosX = 200

    ####Combate########
    dano = 0
    danoMob = 0
    critico = 1
    ataqueCriticoChance = randint(1,100)
    defesaChance = randint(1,100)
        
    if ataqueCriticoChance <= jogador.combateDict["critico"]:
        critico = 2
    dano = (jogador.combateDict["ataque"] * critico) - (jogador.mobStats["mobDefesa"] / 2)
    if dano > jogador.mobStats["mobVida"]:
        jogador.mobStats["mobVida"] = 0
    else:
        jogador.mobStats["mobVida"] -= dano

    if jogador.mobStats["mobVida"] > 0:
        if defesaChance <= jogador.combateDict["chanceDefesa"]:
            montanteDefendido = jogador.mobStats["mobAtaque"] - jogador.combateDict["defesa"]
            if montanteDefendido > 0:
                danoMob = montanteDefendido
        else:
            danoMob = jogador.mobStats["mobAtaque"]
                
        jogador.combateDict["vida"] -= danoMob
        
    ###########Inicio das informacoes de luta na tela###############

    Menu(preto)
    
    dungeonLevel = fonte.render("Andar: " + str(jogador.dungeonStats["andarAtual"]), 1, (branco), (vermelho_escuro))
    dungeonLevelRect = dungeonLevel.get_rect()
    posx = (scrRect.width / 3) - (dungeonLevelRect.width / 2)
    dungeonLevelRect = dungeonLevelRect.move(posx, StatusRect.bottom + 5)

    ######Eu#######

    jogadorLvlRect = JogadorStats(10, dungeonLevelRect.bottom + 5)

    #######Mob#######
        
    mobNome = fonte.render(str(jogador.mobList[str(jogador.mobStats["mobAtual"])]), 1, (branco), (preto))
    mobNomeRect = mobNome.get_rect()
    mobNomeRect = mobNomeRect.move(mobPosX, dungeonLevelRect.bottom + 5)

    mobLvl = fonte.render("Lvl: " + str(jogador.mobStats["mobLevel"]), 1, (branco), (preto))
    mobLvlRect = mobLvl.get_rect()
    mobLvlRect = mobLvlRect.move(mobPosX, mobNomeRect.bottom + 2)

    mobVidaTxt = fonte.render("Vida: " + str(jogador.mobStats["mobVidaCheia"]) + "/" +
                                             str(jogador.mobStats["mobVida"]), 1, (branco), (preto))
    mobVidaTxtRect = mobVidaTxt.get_rect()
    mobVidaTxtRect = mobVidaTxtRect.move(mobPosX, mobLvlRect.bottom + 2)

    mobAtaqueTxt = fonte.render("Ataque: " + str(jogador.mobStats["mobAtaque"]), 1, (branco), (preto))
    mobAtaqueTxtRect = mobAtaqueTxt.get_rect()
    mobAtaqueTxtRect = mobAtaqueTxtRect.move(mobPosX, mobVidaTxtRect.bottom + 2)

    mobDefesaTxt = fonte.render("Defesa: " + str(jogador.mobStats["mobDefesa"]), 1, (branco), (preto))
    mobDefesaTxtRect = mobDefesaTxt.get_rect()
    mobDefesaTxtRect = mobDefesaTxtRect.move(mobPosX, mobAtaqueTxtRect.bottom + 2)

    #####Status da Batalha####

    danoTexto = fonte.render(("Voce tirou:  " + str(dano) + " Mob tirou:  " + str(danoMob)), 1, (branco), (preto))
    danoTextoRect = danoTexto.get_rect()
    danoTextoRect = danoTextoRect.move(10, mobDefesaTxtRect.bottom + 40)

    expTotalTexto = fonte.render("Voce ganhou " + str(jogador.dungeonStats["expTotal"]) + " Exp", 1, (branco), (preto))
    expTotalRect = expTotalTexto.get_rect()
    expTotalRect = expTotalRect.move(10, danoTextoRect.bottom + 2)

    mobsMortosTexto = fonte.render("Mobs Mortos: " + str(jogador.dungeonStats["mobsMortos"]), 1, (branco), (preto))
    mobsMortosRect = mobsMortosTexto.get_rect()
    mobsMortosRect = mobsMortosRect.move(expTotalRect.left, expTotalRect.bottom + 2)

    mobsDrop = fonte.render("Mobs Dropou: " + str(jogador.mobStats["mobDropQuantidade"]) + " "  + str(jogador.mobStats["mobDrop"]), 1, (branco), (preto))
    mobsDropRect = mobsDrop.get_rect()
    mobsDropRect = mobsDropRect.move(expTotalRect.left, mobsMortosRect.bottom + 2)

    ####Blit e Update###########

    screen.blit(dungeonLevel, dungeonLevelRect)
    screen.blit(danoTexto, danoTextoRect)
    screen.blit(expTotalTexto, expTotalRect)
    screen.blit(mobsMortosTexto, mobsMortosRect)
    screen.blit(mobsDrop, mobsDropRect)

    screen.blit(mobNome,mobNomeRect)
    screen.blit(mobLvl, mobLvlRect)
    screen.blit(mobVidaTxt, mobVidaTxtRect)
    screen.blit(mobAtaqueTxt, mobAtaqueTxtRect)
    screen.blit(mobDefesaTxt, mobDefesaTxtRect)
        

def TerminoCombate():

    jogador.combateDict["ultimaDungeon"] = jogador.dungeonStats["andarAtual"]
    if jogador.combateDict["ultimaDungeon"] > jogador.combateDict["maiorDungeon"]:
        jogador.combateDict["maiorDungeon"] = jogador.combateDict["ultimaDungeon"]
    jogador.combateDict["mobsMortosTotal"] += jogador.dungeonStats["mobsMortos"]

    Menu(preto)

    redRect = pygame.draw.rect(screen, vermelho, ((scrRect.width / 2) - 200, (scrRect.height / 2) - 100, 400, 200))

    expTotalTexto = fonte.render("Voce ganhou " + str(jogador.dungeonStats["expTotal"]) + " Exp", 1, (branco), (preto))
    expTotalRect = expTotalTexto.get_rect()
    expTotalRect = expTotalRect.move((redRect.left + redRect.width / 2) - (expTotalRect.width / 2),
                                     (redRect.top + redRect.height / 2) - (expTotalRect.height / 2))

    mobsMortosTexto = fonte.render("Mobs Mortos: " + str(jogador.dungeonStats["mobsMortos"]), 1, (branco), (preto))
    mobsMortosRect = mobsMortosTexto.get_rect()
    mobsMortosRect = mobsMortosRect.move(expTotalRect.left, expTotalRect.bottom + 2)
    
    screen.blit(expTotalTexto, expTotalRect)
    screen.blit(mobsMortosTexto, mobsMortosRect)

    

def Menu(cor):

    screen.fill((cor))
    
    Bag = fonte.render("Bag", 1, (branco), (preto))
    BagRect = Bag.get_rect()
    
    Status = fonte.render("Status", 1, (branco), (preto))
    StatusRect = Status.get_rect()
    StatusRect = StatusRect.move(BagRect.right + 5, 0)

    Skills = fonte.render("Skills", 1, (branco), (preto))
    SkillsRect = Skills.get_rect()
    SkillsRect = SkillsRect.move(StatusRect.right + 5, 0)

    Dungeon = fonte.render("Dungeon", 1, (branco), (vermelho))
    DungeonRect = Dungeon.get_rect()
    DungeonRect = DungeonRect.move(SkillsRect.right + 5, 0)

    Save = fonte.render("Save", 1, (branco), (preto))
    SaveRect = Save.get_rect()
    SaveRect = SaveRect.move(DungeonRect.right + 5, 0)

    screen.blit(Dungeon, DungeonRect)
    screen.blit(Save, SaveRect)
    screen.blit(Bag, BagRect)
    screen.blit(Status, StatusRect)
    screen.blit(Skills, SkillsRect)
        
    return BagRect, StatusRect, SkillsRect, SaveRect, DungeonRect

def Bag(StatusRect):

    Menu(branco)

    x = 0
    rectsINV = [] 
    
    for key in jogador.jogadorInv:
        Iten = fonte.render(str(key) + ": "  + str(jogador.jogadorInv[key]), 1, (branco), (verde))
        rectsINV.append(Iten.get_rect())
        
        if x == 0:
            rectsINV[x] = rectsINV[x].move(0, StatusRect.bottom + 5)
        else:
            rectsINV[x] = rectsINV[x].move(0, rectsINV[x - 1].bottom + 5)
            
        screen.blit(Iten, rectsINV[x])
        x = x + 1
        
    return rectsINV

def Status(StatusRect):
    
    Menu(branco)

    textoTempo = fonte.render("Tempo Jogado", 1, (preto))
    textoTempoRect = textoTempo.get_rect()
    textoTempoRect = textoTempoRect.move(0, StatusRect.bottom + 5)

    text = fonte.render((Tempo(tempo)), 1, (preto))
    textRect = text.get_rect()
    textRect = textRect.move(0, textoTempoRect.bottom + 2)

    textoLvl = fonte.render("Mining Lvl: " + str(jogador.jogadorDict["miningLvl"]), 1, (preto))
    textoLvlRect = textoLvl.get_rect()
    textoLvlRect = textoLvlRect.move(0, textRect.bottom + 5)

    textoXP = fonte.render("Mining Exp: " + str(jogador.jogadorDict["miningExp"]), 1, (preto))
    textoXpRect = textoXP.get_rect()
    textoXpRect = textoXpRect.move(0, textoLvlRect.bottom + 2)

    textoLvlSlave = fonte.render("SlaveMaster Lvl: " + str(jogador.jogadorDict["slaveMasterLvl"]), 1, (preto))
    textoLvlSlaveRect = textoLvlSlave.get_rect()
    textoLvlSlaveRect = textoLvlSlaveRect.move(0, textoXpRect.bottom + 5)

    textoXPSlave = fonte.render("SlaveMaster Exp: " + str(jogador.jogadorDict["slaveMasterExp"]), 1, (preto))
    textoXpSlaveRect = textoXPSlave.get_rect()
    textoXpSlaveRect = textoXpSlaveRect.move(0, textoLvlSlaveRect.bottom + 2)

    textoLvlCombate = fonte.render("Combate Lvl: " + str(jogador.combateDict["lvl"]), 1, (preto))
    textoLvlCombateRect = textoLvlCombate.get_rect()
    textoLvlCombateRect = textoLvlCombateRect.move(0, textoXpSlaveRect.bottom + 5)

    textoXPCombate = fonte.render("Combat Exp: " + str(jogador.combateDict["exp"]), 1, (preto))
    textoXpCombateRect = textoXPCombate.get_rect()
    textoXpCombateRect = textoXpCombateRect.move(0, textoLvlCombateRect.bottom + 2)

    textoPontosCombate = fonte.render("Pontos para Distribuir: " + str(jogador.combateDict["pontos"]), 1, (preto))
    textoPontosCombateRect = textoPontosCombate.get_rect()
    textoPontosCombateRect = textoPontosCombateRect.move(0, textoXpCombateRect.bottom + 2)

    screen.blit(textoLvlCombate, textoLvlCombateRect)
    screen.blit(textoXPCombate, textoXpCombateRect)
    screen.blit(textoPontosCombate, textoPontosCombateRect)
    screen.blit(textoLvlSlave, textoLvlSlaveRect)
    screen.blit(textoXPSlave, textoXpSlaveRect)
    screen.blit(textoLvl, textoLvlRect)
    screen.blit(textoXP, textoXpRect)
    screen.blit(text, textRect)
    screen.blit(textoTempo, textoTempoRect)

    #pygame.display.update()

def LevelUp(utilizador, lvl, exp):
    
    xpUpar = ((utilizador[lvl] * 100) + utilizador[lvl]) * ((utilizador[lvl] * 5) - (utilizador[lvl] * 3) / utilizador[lvl])
    while utilizador[exp] >= xpUpar:
        utilizador[exp] -= xpUpar
        utilizador[lvl] += 1
        if utilizador == jogador.combateDict:
            utilizador["pontos"] += (1 + utilizador["lvl"]) / 2

    if lvl == "slaveMasterLvl":
        if (utilizador[lvl] / 5) + 1 > len(jogador.slavesDict):
            slaveAtual = "slave" + str(len(jogador.slavesDict) + 1)
            jogador.slavesDict[slaveAtual] = {}
            for key in jogador.slavesDictArvore:
                if key not in jogador.slavesDict[slaveAtual]:
                    if key == "nome":
                        jogador.slavesDict[slaveAtual][key] = "Slave " + str(len(jogador.slavesDict))
                    else:
                        jogador.slavesDict[slaveAtual][key] = jogador.slavesDictArvore[key]
            #print jogador.slavesDict
       

def GastarPontos(atributo):

    if atributo == "chanceDefesaBase" or atributo == "criticoBase":
        jogador.combateDict[atributo] += 1
    else:
        jogador.combateDict[atributo] += jogador.combateBase[atributo] * jogador.combateDict["lvl"]
    jogador.combateDict["pontos"] -= 1
        

def TotalLvlExp(lvl, exp):
###############################REFAZER!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    jogador.jogadorDict["totalLvl"] += 1
    
    x = lvl - 1
    xpUpar = 0
    while x < lvl:
        xpUpar += ((x * 100) + x) * ((x * 5) - (x * 3) / x)
        x += 1
        
    jogador.jogadorDict["totalExp"] += xpUpar

#########################CLASSE JOGADOR#########################################
class Jogador:

    jogadorDict = {

        "nome": "",
        "totalLvl": 3,
        "totalExp": 0,
        "miningLvl": 1,
        "miningExp": 0,
        "slaveMasterLvl": 1,
        "slaveMasterExp":0,
        "tempoMining": 0,
        "pedraAtual": 0,
        "tempoTotalJogado": 0,
        "inventario": {},
        "slavesDict": {},
        "combateDict": {},
        "dungeonStats": {},
        "mobStats": {}
        
        }

    combateBase = {
        "vidaCheia": 75,
        "ataqueBase": 10,
        "criticoBase": 1,
        "defesaBase": 5,
        "chanceDefesaBase": 5,
        }

    combateDict = {
        "lvl": 1,
        "exp": 0,
        "pontos": 0,
        "vidaCheia": 100,
        "vida": 50,
        "ataqueBase": 10,
        "ataque": 10,
        "criticoBase": 1,
        "critico": 1,
        "defesaBase": 5,
        "defesa": 5,
        "chanceDefesaBase": 5,
        "chanceDefesa": 5,
        "ultimaDungeon": 1,
        "maiorDungeon": 1,
        "mobsMortosTotal": 0,
        }

    jogadorInv = {}
    catalogoMining = {}
    catalogoMiningLevel = {}

    slavesDict = {

        "slave1": {
            "nome": "Slave 1",
            "miningLvl": 1,
            "miningExp": 0,
            "tempoMining": 0,
            "pedraAtual": 0,
            "data": 0,
            }
        
        }

    slavesDictArvore = {
        "nome": "",
        "miningLvl": 1,
        "miningExp": 0,
        "tempoMining": 0,
        "pedraAtual": 0,
        "data": 0,
        }


    andarDropList = {}
    mobList = {}
    mobAndar = {}
    mobBase = {
        "vida": 10,
        "ataque": 3,
        "defesa": 2,
        "exp": 10
        }

    mobStats = {
        "mobAtual": 0,
        "mobLevel": 0,
        "mobVidaCheia": 0,
        "mobVida": 0,
        "mobAtaque": 0,
        "mobDefesa": 0,
        "mobDrop": 0,
        "mobDropQuantidade": 0,
        }

    dungeonStats = {
        "mobsMortos": 0,
        "andarAtual": 0,
        "expTotal": 0,
        "loopCombate": 0,
        }


    def __init__(self, nome, var = ""):
        self.jogadorDict["nome"] = nome
        self.LoadMining()
        self.LoadMob()
        self.LoadAndarDefinicoes()
        if var == "load":
            self.Load(nome)
    
    @classmethod
    def Load(self, nome):

        try:
            nameLoad = nome + ".txt"
            dictLoad = json.load(open(nameLoad))
        except:
            print "erro load arquivo"
            raise
            
        
        for keys in self.jogadorDict:
            if keys not in dictLoad:
                dictLoad[keys] = self.jogadorDict[keys]

        slaves = dictLoad["slavesDict"]
        for keys in self.slavesDict:
            if keys not in slaves:
                slaves[keys] = self.slavesDict[keys]

        combate = dictLoad["combateDict"]
        for keys in self.combateDict:
            if keys not in combate:
                combate[keys] = self.combateDict[keys]

        dungeon = dictLoad["dungeonStats"]
        for keys in self.dungeonStats:
            if keys not in dungeon:
                dungeon[keys] = self.dungeonStats[keys]

        mob = dictLoad["mobStats"]
        for keys in self.mobStats:
            if keys not in mob:
                mob[keys] = self.mobStats[keys]

        self.jogadorInv = dictLoad["inventario"]
        self.slavesDict = slaves
        self.jogadorDict = dictLoad
        self.combateDict = combate
        self.dungeonStats = dungeon
        self.mobStats = mob

        #self.TempoOffline()

    @classmethod
    def LoadMining(self):

        nome = "catalogoMining" + ".txt"

        try:
            arquivo = json.load(open(nome))
        except:
            raise

        self.catalogoMining = arquivo
        
        self.catalogoMiningLevel = self.catalogoMining["level"]
        del self.catalogoMining["level"]

    @classmethod
    def LoadMob(self):

        nome = "mobsCatalogo" + ".txt"

        try:
            arquivo = json.load(open(nome))
        except:
            print "erro no load mob"
            raise

        self.mobList = arquivo
        self.mobAndar = self.mobList["andar"]
        del self.mobList["andar"]
        
        print "Lista de Mobs: " + str(self.mobList)
        #print self.mobAndar

    @classmethod
    def LoadAndarDefinicoes(self):

        nome = "dungeonInformacoes" + ".txt"

        try:
            arquivo = json.load(open(nome))
        except:
            print "erro no load mob"
            raise

        self.andarDropList = arquivo["andarDrop"]

        print "Drop por Andar" + str(self.andarDropList)

    #@classmethod
    def TempoOffline(self):

        for keys in self.slavesDict:
            

            tempoOff = time.localtime(time.time())
            tempoSaida = time.strptime(self.slavesDict[keys]["data"], "%Y/%m/%d %H:%M:%S")
            tempoDict = {
                "ano": 0,
                "mes": 0,
                "dia": 0,
                "hora": 0,
                "min": 0,
                "seg": 0
            }
        
            tempoDict["ano"] = tempoOff.tm_year - tempoSaida.tm_year
            tempoDict["mes"] = tempoOff.tm_mon - tempoSaida.tm_mon
            tempoDict["dia"] = tempoOff.tm_mday - tempoSaida.tm_mday
            tempoDict["hora"] = tempoOff.tm_hour - tempoSaida.tm_hour
            tempoDict["min"] = tempoOff.tm_min - tempoSaida.tm_min
            tempoDict["seg"] = tempoOff.tm_sec - tempoSaida.tm_sec

            while (tempoDict["mes"] < 0 or tempoDict["dia"] < 0 or tempoDict["hora"] < 0
                   or tempoDict["min"] < 0 or tempoDict["seg"] < 0):
                for key in tempoDict:
                    if tempoDict[key] < 0:
                        if key == "mes":
                            tempoDict["ano"] -= 1
                            tempoDict["mes"] += 12
                        elif key == "dia":
                            tempoDict["mes"] -= 1
                            tempoDict["dia"] += 30
                        elif key == "hora":
                            tempoDict["dia"] -= 1
                            tempoDict["hora"] += 24
                        elif key == "min":
                            tempoDict["hora"] -= 1
                            tempoDict["min"] += 60
                        elif key == "seg":
                            tempoDict["min"] -= 1
                            tempoDict["seg"] += 60

            print tempoDict

            tempoTotal = 0

            tempoDict["mes"] += (tempoDict["ano"] * 12)
            tempoDict["dia"] += (tempoDict["mes"] * 30)
            tempoDict["hora"] += (tempoDict["dia"] * 24)
            tempoDict["min"] += (tempoDict["hora"] * 60)
            tempoTotal = tempoDict["seg"] + (tempoDict["min"] * 60)

            
            pedras = tempoTotal / (40 + ((self.slavesDict[keys]["pedraAtual"]) * 20))
            
            print "tempoTotal: " + str(tempoTotal)
            print str(self.catalogoMining[str(self.slavesDict[keys]["pedraAtual"])]) + ": " + str(pedras)
        
            #tempoTotal -= (40 + ((self.slavesDict["slave1"]["pedraAtual"]) * 20)) * pedras
            #print "tempoTotal: " + str(tempoTotal)

            tempoTotal = self.slavesDict[keys]["tempoMining"]
            pedraAtual = self.slavesDict[keys]["pedraAtual"]
            self.slavesDict[keys]["tempoMining"] = ((40 + ((self.slavesDict[keys]["pedraAtual"]) * 20)) * pedras)
        
            #print "tempoMining: " + str(self.slavesDict["tempoMining"])
            #print "Inventario: " + str(self.jogadorDict["inventario"])
        
            while self.slavesDict[keys]["tempoMining"] > 0:
                Mining(self.slavesDict[keys])

            #print "finalizou while no load do idle"

            self.slavesDict[keys]["tempoMining"] = tempoTotal
            self.slavesDict[keys]["pedraAtual"] = pedraAtual
            #print "tempoMining: " + str(self.slavesDict["tempoMining"])
            #print "Inventario: " + str(self.jogadorDict["inventario"])
            #print "Slavexp: " + str(self.jogadorDict["slaveMasterExp"])
        

    def Save(self):

        
        nomeTXT = self.jogadorDict["nome"] + ".txt"
        
        for key in self.slavesDict:
            self.slavesDict[key]["data"] = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        self.jogadorDict["inventario"] = self.jogadorInv
        self.jogadorDict["slavesDict"] = self.slavesDict
        self.jogadorDict["combateDict"] = self.combateDict
        self.jogadorDict["mobStats"] = self.mobStats
        self.jogadorDict["dungeonStats"] = self.dungeonStats
        
        #print "\n" + str(self.jogadorDict["inventario"])

        try:
            json.dump(self.jogadorDict, open(nomeTXT, 'w'))
            print "\n" + str(self.jogadorDict)
        except:
            print "erro json dump arquivo"
            raise
    

#########################Informacoes basicas####################################


verde            = (  0, 155,   0)
branco           = (255, 255, 255)
branco_ostra     = (234, 230, 202)
preto            = (  0,   0,   0)
cinza            = (185, 185, 185)
cinza_claro      = (200, 200, 200)
cinza_escuro     = (100, 100, 100)
vermelho         = (255,   0,   0)
vermelho_escuro  = (100,   0,   0)

screen = pygame.display.set_mode((600, 400))
scrRect = screen.get_rect()
screen.fill((branco))
pygame.display.update()
pygame.init()

jogador = Jogador("Teste", "load")
jogador.TempoOffline()

fonte = pygame.font.Font(None, 22)

clock = pygame.time.Clock()
tempo = pygame.time.get_ticks() / 1000
tempo1 = tempo - 1
tempoCombate = tempo
tempoSoma = jogador.jogadorDict["tempoTotalJogado"]

varAtualizacao = 0
combate = False





#########################Call das funcoes########################################


BagRect, StatusRect, SkillsRect, SaveRect, DungeonRect = Menu(branco)
Status(StatusRect)
entrarDungeonRect, botaoVidaRect, botaoAtaqueRect, botaoDefesaRect, botaoChanceDefesaRect, botaoCriticoRect = Dungeon(StatusRect)

MiningRect, SlavesRect = Skills(StatusRect)
minerioRect = []
minerioRect = MiningSCR(StatusRect)

rectsINV = []
rectsINV = Bag(StatusRect)



#################################################################################


while 1:
    tempo = pygame.time.get_ticks() / 1000
    mouse = pygame.mouse.get_pos()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

        if event.type == pygame.MOUSEBUTTONDOWN:

            x = 0
            while x < len(minerioRect):
                if minerioRect[x].collidepoint(mouse) and (jogador.jogadorDict["pedraAtual"] == 0
                                                           or jogador.jogadorDict["pedraAtual"] == x + 1):

                    jogador.jogadorDict["tempoMining"] += (40 + ((x + 1) * 20))
                    jogador.jogadorDict["pedraAtual"] = x + 1
                x += 1
                    

            if MiningRect.collidepoint(mouse) and varAtualizacao == 2:
                varAtualizacao = 3
            elif SlavesRect.collidepoint(mouse) and varAtualizacao == 2:
                varAtualizacao = 4
            elif BagRect.collidepoint(mouse):
                Bag(StatusRect)
                varAtualizacao = 0
            elif SaveRect.collidepoint(mouse):
                jogador.jogadorDict["tempoTotalJogado"] = tempo + tempoSoma
                jogador.Save()
            elif StatusRect.collidepoint(mouse):
                varAtualizacao = 1
            elif SkillsRect.collidepoint(mouse):
                varAtualizacao = 2
            elif DungeonRect.collidepoint(mouse):
                varAtualizacao = 5
            elif entrarDungeonRect.collidepoint(mouse) and varAtualizacao == 5:
                varAtualizacao = 6
                combate = True

            if jogador.combateDict["pontos"] > 0 and combate == False:
                if botaoVidaRect.collidepoint(mouse) and varAtualizacao == 5:
                    GastarPontos("vidaCheia")
                    jogador.combateDict["vida"] = jogador.combateDict["vidaCheia"]
                elif botaoAtaqueRect.collidepoint(mouse) and varAtualizacao == 5:
                    GastarPontos("ataqueBase")
                    jogador.combateDict["ataque"] = jogador.combateDict["ataqueBase"]
                elif botaoDefesaRect.collidepoint(mouse) and varAtualizacao == 5:
                    GastarPontos("defesaBase")
                    jogador.combateDict["defesa"] = jogador.combateDict["defesaBase"]
                elif botaoChanceDefesaRect.collidepoint(mouse) and varAtualizacao == 5:
                    GastarPontos("chanceDefesaBase")
                    jogador.combateDict["chanceDefesa"] = jogador.combateDict["chanceDefesaBase"]
                elif botaoCriticoRect.collidepoint(mouse) and varAtualizacao == 5:
                    GastarPontos("criticoBase")
                    jogador.combateDict["critico"] = jogador.combateDict["criticoBase"]

                

    if tempo != tempo1:
        tempo1 = tempo  

        if jogador.jogadorDict["tempoMining"] > 0:
            #print "jogador Tempo"
            Mining(jogador.jogadorDict)
            
        for key in jogador.slavesDict:
            #print key
            #print jogador.slavesDict[key]["tempoMining"]
            if jogador.slavesDict[key]["tempoMining"] > 0:
                Mining(jogador.slavesDict[key])
                
            x = 1
            if jogador.slavesDict[key]["pedraAtual"] == 0:
            
                while jogador.slavesDict[key]["miningLvl"] > jogador.catalogoMiningLevel[str(x + 1)]:
                    x += 1
                    #print "catalogo Mining: " + str(jogador.catalogoMining[str(x)])
                    #print "mining lvl: " + str(jogador.slavesDict[key]["miningLvl"])
                jogador.slavesDict[key]["tempoMining"] += (40 + ((x) * 20))
                jogador.slavesDict[key]["pedraAtual"] = x
                #print "pedra Atual: " + str(jogador.slavesDict[key]["pedraAtual"])
            #print "terminou isso"


    if varAtualizacao == 1:
        Status(StatusRect)
    elif varAtualizacao == 2:
        Skills(StatusRect)
    elif varAtualizacao == 3:
        MiningSCR(StatusRect)
    elif varAtualizacao == 4:
        SlavesSCR(StatusRect)
    elif varAtualizacao == 5:
        Dungeon(StatusRect)
        
    #####Combate########
    elif varAtualizacao == 6 or combate == True:
        varAtualizacao = 0

        if jogador.dungeonStats["loopCombate"] == 0:
            InicializarCombate()
            jogador.dungeonStats["loopCombate"] = 1
            DungeonLoop(StatusRect)

        if tempoCombate < tempo:
            tempoCombate = tempo
            DungeonLoop(StatusRect)

        if jogador.combateDict["vida"] <= 0:
            combate = False
            jogador.dungeonStats["loopCombate"] = 0
            jogador.combateDict["vida"] = jogador.combateDict["vidaCheia"]
            TerminoCombate()
            
        if jogador.mobStats["mobVida"] <= 0 and combate == True:
            ZerarVidaMob()


    pygame.display.update()

    clock.tick(20)
