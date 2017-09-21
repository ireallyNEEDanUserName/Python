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



################################Barra de Informacoes#############################
def Informacoes(Texto):

    jogador.textoBottom.append(Texto)
    stringLoop = []
    x = len(jogador.textoBottom)
    
    if x >= 20:
        for f in range(1, 4, 1):
            stringLoop.append(jogador.textoBottom[x - f])
        jogador.textoBottom = stringLoop
        x = len(jogador.textoBottom)
        
    y = 2
    z = 0

    while y >= 0:
        rect = pygame.draw.rect(screen, branco_ostra, (0, (scrRect.bottom + (y * 20)), scrRect.width, 20))

        if x > z:
            z += 1
            textoInf = jogador.textoBottom[x - z]
        else:
            textoInf = ""

        textoBarra = fonte.render(textoInf, 1, (preto), (branco_ostra))
        textoRect = textoBarra.get_rect()
        textoRect = textoRect.move((scrRect.width / 2) - (textoRect.width / 2), rect.top + 2 )

        screen.blit(textoBarra, textoRect)
        y -= 1
        
            

    pygame.display.update()

################################################################################

def VerificarEquipamento(chave):
    
    for chaveEquip in jogador.itensCategoria["Equipamento"]:
        if chave in jogador.itensCategoria["Equipamento"][chaveEquip]:
            chaveTipo = chaveEquip
            return chaveEquip

    return False

def VerificarIten(chave):

    for key in jogador.catalogoMining:
        if chave == jogador.catalogoMining[key]:
            return "ores"
    for key in jogador.catalogoSmithing:
        if chave == jogador.catalogoSmithing[key]:
            return "barra"
    if chave in jogador.itensSprites:
        return "outros"

    return False
    
    
    
###############MINING###########################################################

def Skills():

    Menu(branco)

    posx = 10

    textoHabilidades = fonte.render("Habilidades", 1, (verde), (branco_ostra))
    textoHabilidadesRect = textoHabilidades.get_rect()
    textoHabilidadesRect = textoHabilidadesRect.move(meioDaTela - (textoHabilidadesRect.width / 2), menuRectFundo.bottom + 5)

    Mining = fonte.render("Mining", 3, (branco), (preto))
    MiningRect = Mining.get_rect().move(posx, textoHabilidadesRect.bottom + 5)

    Smithing = fonte.render("Smithing", 3, (branco), (preto))
    SmithingRect = Smithing.get_rect().move(MiningRect.left, MiningRect.bottom + 5)
    
    Slaves = fonte.render("Slaves", 3, (branco), (vermelho_escuro))
    SlavesRect = Slaves.get_rect().move(SmithingRect.left, SmithingRect.bottom + 5)

    screen.blit(textoHabilidades, textoHabilidadesRect)
    screen.blit(Mining, MiningRect)
    screen.blit(Slaves, SlavesRect)
    screen.blit(Smithing, SmithingRect)
    

    return MiningRect, SlavesRect, SmithingRect

def ReforcarSCR():

    Menu(branco)

    posx = 10

    textoCategoria = fonte.render("Itens para Melhorar", 1, (verde), (branco_ostra))
    textoCategoriaRect = textoCategoria.get_rect()
    textoCategoriaRect = textoCategoriaRect.move(meioDaTela - (textoCategoriaRect.width / 2), menuRectFundo.bottom + 5)

    Smithing = fonte.render("Smithing", 3, (branco), (preto))
    SmithingRect = Smithing.get_rect()
    SmithingRect = SmithingRect.move(textoCategoriaRect.left - (SmithingRect.width + 10), menuRectFundo.bottom + 5)

    textoTempoReforcar = fonte.render("Tempo para Reforcar", 1, (preto))
    textoTempoReforcarRect = textoTempoReforcar.get_rect()
    textoTempoReforcarRect = textoTempoReforcarRect.move(posx, SmithingRect.bottom + 25)
    
    texttempoReforcar = fonte.render((Tempo(jogador.jogadorDict["tempoReforcar"] - tempoSoma)), 1, (preto))
    texttempoReforcarRect = texttempoReforcar.get_rect()
    texttempoReforcarRect = texttempoReforcarRect.move(textoTempoReforcarRect.left, textoTempoReforcarRect.bottom + 3)

    screen.blit(Smithing, SmithingRect)
    screen.blit(textoTempoReforcar, textoTempoReforcarRect)
    screen.blit(texttempoReforcar, texttempoReforcarRect)
    screen.blit(textoCategoria, textoCategoriaRect)


    y = 0
    rectsReforcado = []
    chaveSelecionado = []
    melhoria = []
    chaveTipo = False
    
    for key in jogador.jogadorInv:
        chaveTipo = VerificarEquipamento(key)
        if chaveTipo != False:
            for chave in jogador.jogadorInv[key]:
                if jogador.jogadorDict["smithingLvl"] >= (int(jogador.itensSmithing[chaveTipo][key]["level"]) + int(chave)):
                
                    Smithing = fonte.render(key + "+" + str(chave) + " -> " + str(jogador.jogadorInv[key][chave]), 1, (branco), (preto))
                    rectsReforcado.append(Smithing.get_rect())
        
                    if y == 0:
                        rectsReforcado[y] = rectsReforcado[y].move(texttempoReforcarRect.left, texttempoReforcarRect.bottom + 7)
                    else:
                        rectsReforcado[y] = rectsReforcado[y].move(rectsReforcado[y - 1].left, rectsReforcado[y - 1].bottom + 2)
            
                    screen.blit(Smithing, rectsReforcado[y])
                    chaveSelecionado.append(key + "+" + str(chave))
                    y += 1
            chaveTipo = False

    if len(chaveSelecionado) == 0:
        return rectsReforcado, False, SmithingRect
    else:
        return rectsReforcado, chaveSelecionado, SmithingRect

def ReforcarSelecionado(itenSelecionado):

    chave2, valor = SepararNumero(itenSelecionado)

    
    quantidadeNecessaria = 2

    chaveTipo = VerificarEquipamento(chave2)

    #print chave2, valor
    if int(jogador.jogadorInv[chave2][str(valor)]) >= quantidadeNecessaria:

        jogador.jogadorDict["tempoReforcar"] += (jogador.itensSmithing[chaveTipo][chave2]["tempo"] * quantidadeNecessaria)
        jogador.jogadorDict["itenMelhorando"] = itenSelecionado
        jogador.jogadorInv[chave2][str(valor)] -= quantidadeNecessaria

        if jogador.jogadorInv[chave2][str(valor)] == 0:
            del jogador.jogadorInv[chave2][str(valor)]
            return True
    else:
        Informacoes("Quantia de itens insuficientes: " + str(quantidadeNecessaria))
        

def SepararNumero(itenSelecionado):

    numeros = "0123456789"
    valor = 0
    chave2 = ""

    for x in range(0, len(itenSelecionado)):
        if itenSelecionado[x] == "+": 
            pass
        elif itenSelecionado[x] in numeros:
            valor = int(itenSelecionado[x])
        else:
            chave2 += itenSelecionado[x]

    return chave2, valor

def MelhorarTempo(utilizador):

    chave, valor = SepararNumero(jogador.jogadorDict["itenMelhorando"])
    chaveTipo = VerificarEquipamento(chave)

    jogador.jogadorDict["tempoReforcar"] -= 1
    exp = 0

    tempo = jogador.itensSmithing[chaveTipo][chave]["tempo"] * (2 + valor)

    if jogador.jogadorDict["tempoReforcar"] == 0 or jogador.jogadorDict["tempoReforcar"] % tempo == 0:
        if chave in jogador.jogadorInv:
            if str(valor + 1) in jogador.jogadorInv[chave]:
                jogador.jogadorInv[chave][str(valor + 1)] += 1
            else:
                jogador.jogadorInv[chave][str(valor + 1)] = 1
        else:
            jogador.jogadorInv[chave] = {str(valor + 1): 1}

        exp = jogador.itensSmithing[chaveTipo][chave]["exp"] * (valor + 1)
        Informacoes("Voce ganhou " + str(exp) + " exp melhorando " + str(chave))

        LevelUp(utilizador, "smithingLvl", "smithingExp")

def SmithingSCR():

    Menu(branco)

    textoCategoria = fonte.render("Categorias de Itens", 1, (verde), (branco_ostra))
    textoCategoriaRect = textoCategoria.get_rect()
    textoCategoriaRect = textoCategoriaRect.move((meioDaTela - (textoCategoriaRect.width / 2)), menuRectFundo.bottom + 5)

    screen.blit(textoCategoria, textoCategoriaRect)

    posx = 10

    y = 0
    chave = []
    textoRect = []

    for key in jogador.itensSmithing:
        textoKey = fonte.render(key, 1, (branco), (preto))
        textoRect.append(textoKey.get_rect())

        if y == 0:
            textoRect[y] = textoRect[y].move(posx, textoCategoriaRect.bottom + 5)
        else:
            textoRect[y] = textoRect[y].move(textoRect[y - 1].left, textoRect[y - 1].bottom + 5)
        chave.append(key)
        screen.blit(textoKey, textoRect[y])
        y += 1

    textoKey = fonte.render("Reforcar Iten", 1, (branco), (preto))
    textoRect.append(textoKey.get_rect())
    textoRect[y] = textoRect[y].move(textoRect[y - 1].left, textoRect[y - 1].bottom + 5)
    chave.append("Reforcar")
    screen.blit(textoKey, textoRect[y])

    if len(textoRect) == 0:
        return textoRect, False
    else:
        return textoRect, chave
    

def ItenSmithing(chave):

    Menu(branco)

    posx = 10

    Smithing = fonte.render("Smithing", 3, (branco), (preto))
    SmithingRect = Smithing.get_rect()
    SmithingRect = SmithingRect.move(meioDaTela - (SmithingRect.width / 2), menuRectFundo.bottom + 5)

    textoTempoSmithing = fonte.render("Tempo para Forjar", 1, (preto))
    textoTempoSmithingRect = textoTempoSmithing.get_rect()
    textoTempoSmithingRect = textoTempoSmithingRect.move(posx, SmithingRect.bottom + 25)
    
    texttempoSmithing = fonte.render((Tempo(jogador.jogadorDict["tempoSmithing"] - tempoSoma)), 1, (preto))
    texttempoSmithingRect = texttempoSmithing.get_rect()
    texttempoSmithingRect = texttempoSmithingRect.move(textoTempoSmithingRect.left, textoTempoSmithingRect.bottom + 3)

    screen.blit(Smithing, SmithingRect)
    screen.blit(textoTempoSmithing, textoTempoSmithingRect)
    screen.blit(texttempoSmithing, texttempoSmithingRect)

    x = 1
    y = 0
    rectsSmithing = []
    chaveSelecionado = []


    for key in jogador.itensSmithing[chave]:
        if jogador.jogadorDict["smithingLvl"] >= int(jogador.itensSmithing[chave][key]["level"]):
            Smithing = fonte.render(key, 1, (branco), (preto))
            rectsSmithing.append(Smithing.get_rect())
        
            if y == 0:
                rectsSmithing[y] = rectsSmithing[y].move(texttempoSmithingRect.left, texttempoSmithingRect.bottom + 7)
            else:
                rectsSmithing[y] = rectsSmithing[y].move(rectsSmithing[y - 1].left, rectsSmithing[y - 1].bottom + 2)
            
            screen.blit(Smithing, rectsSmithing[y])
            chaveSelecionado.append(key)
            y += 1       
        x = x + 1

    return rectsSmithing, chaveSelecionado, SmithingRect

def ForjarItenSelecionado(chaveSmithing, itenDeSmithingSelecionado):

    itenAtual = jogador.itensSmithing[chaveSmithing][itenDeSmithingSelecionado]

    continuar = False

    if jogador.jogadorDict["itenForjando"] == itenDeSmithingSelecionado or jogador.jogadorDict["itenForjando"] == "":
        if itenAtual["oreNecessario"] in jogador.jogadorInv:
            if "Preto" in itenDeSmithingSelecionado or "Preta" in itenDeSmithingSelecionado:
                if itenAtual["outros"] in jogador.jogadorInv:
                    if jogador.jogadorInv[itenAtual["outros"]] >= itenAtual["outrosQuantidade"] :
                        jogador.jogadorInv[itenAtual["outros"]] -= itenAtual["outrosQuantidade"]
                        continuar = True
                        if jogador.jogadorInv[itenAtual["outros"]] < 0:
                            del jogador.jogadorInv[itenAtual["outros"]]
                    else:
                        Informacoes(itenAtual["outros"] + " Insuficiente")
            else:
                continuar = True
                    
            if continuar == True:        
                if (jogador.jogadorInv[itenAtual["oreNecessario"]] >= itenAtual["quantidade"]):
            
                    jogador.jogadorInv[itenAtual["oreNecessario"]] -= itenAtual["quantidade"]
                    jogador.jogadorDict["tempoSmithing"] += itenAtual["tempo"]
                    jogador.jogadorDict["itenForjando"] = itenDeSmithingSelecionado
                    if jogador.jogadorInv[itenAtual["oreNecessario"]] <= 0:
                        del jogador.jogadorInv[itenAtual["oreNecessario"]] 
            
                else:
                    Informacoes("Barras Insuficientes")
        else:
            Informacoes("Voce nao possui a barra necessaria!!")
    else:
        Informacoes("Fazendo outro iten: " + str(jogador.jogadorDict["itenForjando"]))

def SmithingTempo(utilizador):

    exp = 0


    categoriaItenSmithing = VerificarEquipamento(jogador.jogadorDict["itenForjando"])

    if categoriaItenSmithing != False:

        utilizador["tempoSmithing"] -= 1

        if (utilizador["tempoSmithing"] == 0 or
            utilizador["tempoSmithing"] % jogador.itensSmithing[categoriaItenSmithing][jogador.jogadorDict["itenForjando"]]["tempo"] == 0):

            if jogador.jogadorDict["itenForjando"] not in jogador.jogadorInv:
                jogador.jogadorInv[jogador.jogadorDict["itenForjando"]] = {"0": 1}
            elif "0" not in jogador.jogadorInv[jogador.jogadorDict["itenForjando"]]:
                jogador.jogadorInv[jogador.jogadorDict["itenForjando"]]["0"] = 1
            else:
                jogador.jogadorInv[jogador.jogadorDict["itenForjando"]]["0"] += 1

            exp = (jogador.itensSmithing[categoriaItenSmithing][jogador.jogadorDict["itenForjando"]]["exp"] + jogador.jogadorDict["smithingLvl"])
        
            utilizador["smithingExp"] += exp
            Informacoes("Voce ganhou " + str(exp) + " exp de smithing")
        
            LevelUp(utilizador, "smithingLvl", "smithingExp")

            if utilizador["tempoSmithing"] == 0:
                jogador.jogadorDict["itenForjando"] = ""
            

def ForjarBarra(Chave):

    keyChave = 0
    quantidade = 1
    chance = 0
    chanceMaisIten = 0
    random = 0
    lvl = jogador.jogadorDict["smithingLvl"]
    texto = ""

    rect = "Rect do sucesso"

    for key in jogador.catalogoMining:
        if Chave == jogador.catalogoMining[key]:
            keyChave = key

    
    if int(jogador.jogadorInv[Chave]) > int(keyChave):
        
        if keyChave != 0:
        
            chanceMaisIten = (jogador.jogadorDict["smithingLvl"] / jogador.catalogoMiningLevel[keyChave]) + jogador.jogadorDict["smithingLvl"]
        
            if jogador.catalogoMiningLevel[keyChave] <= jogador.jogadorDict["smithingLvl"]:
                chance = (100 / (jogador.catalogoMiningLevel[keyChave] +
                                 jogador.jogadorDict["smithingLvl"])) * jogador.jogadorDict["smithingLvl"]

                random = randint(1, 100)
                if chance >= random:
                    random = randint(1, 100)
                    if random <= chanceMaisIten:
                        quantidade += jogador.jogadorDict["smithingLvl"]
                
                    jogador.jogadorInv[Chave] -= int(keyChave)
                    if jogador.catalogoSmithing[keyChave] not in jogador.jogadorInv:
                        jogador.jogadorInv[jogador.catalogoSmithing[keyChave]] = quantidade
                    else:
                        jogador.jogadorInv[jogador.catalogoSmithing[keyChave]] += quantidade
                
                    jogador.jogadorDict["smithingExp"] += 10 * (int(keyChave) * jogador.jogadorDict["smithingLvl"])
                    LevelUp(jogador.jogadorDict, "smithingLvl", "smithingExp")

                    if lvl == jogador.jogadorDict["smithingLvl"]:
                        stringItem = str(jogador.catalogoSmithing[keyChave])
                        texto = "Sucesso da Forja / Voce fez " + str(quantidade) + " " + stringItem
                    
                    else:
                        texto = "Parabens voce upou um level de: " + str(lvl)
                
                else:
                    texto = "Falhou na Forja"
                    jogador.jogadorInv[Chave] -= int(keyChave)
            else:
                texto = "Level Insuficiente!!! Necessario: " + str(jogador.catalogoMiningLevel[keyChave])
        else:
            texto = "Nada o que fazer com o Item"
    else:
        texto = "Ores Insuficientes"

    if jogador.jogadorInv[Chave] <= 0:
        del jogador.jogadorInv[Chave]
        
    return texto

def MiningSCR():
    Menu(branco)

    textoTempoMinerar = fonte.render("Tempo para Minerar", 1, (preto))
    textoTempoMinerarRect = textoTempoMinerar.get_rect()
    textoTempoMinerarRect = textoTempoMinerarRect.move(0, menuRectFundo.bottom + 5)
    
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

def Mining(utilizador, load = False):

    exp = 0
    
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
                exp = 10 * (utilizador["pedraAtual"] * utilizador["miningLvl"])
                utilizador2["miningExp"] += exp
                Informacoes("Voce ganhou " + str(exp) + " exp de mining")
            elif x == "slave":
                exp = 10 * utilizador["pedraAtual"]
                utilizador2["miningExp"] += exp
                utilizador2["slaveMasterExp"] += utilizador["pedraAtual"]
                utilizador["miningExp"] += (utilizador["pedraAtual"] * 4)
                Informacoes("Slave ganhou " + str(exp) + " exp de mining")
                
                LevelUp(utilizador, "miningLvl", "miningExp")
                if load == False:
                    LevelUp(utilizador2, "slaveMasterLvl", "slaveMasterExp")
            
           
            LevelUp(utilizador2, "miningLvl", "miningExp")
            

            if utilizador["tempoMining"] == 0:
                utilizador["pedraAtual"] = 0
                

def SlavesSCR():
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
            rectsSlavesNome[x] = rectsSlavesNome[x].move(5, menuRectFundo.bottom + 10)
            rectsSlavesLvl[x] = rectsSlavesLvl[x].move(rectsSlavesNome[x].right + 5, rectsSlavesNome[x].top)
            rectsSlavesPedra[x] = rectsSlavesPedra[x].move(rectsSlavesLvl[x].right + 5, rectsSlavesLvl[x].top)
            rectsSlaveTempo[x] = rectsSlaveTempo[x].move(rectsSlavesPedra[x].right + 5, rectsSlavesPedra[x].top)
            
        else:
            rectsSlavesNome[x] = rectsSlavesNome[x].move(5, rectsSlavesNome[x - 1].bottom + 2)
            rectsSlavesLvl[x] = rectsSlavesLvl[x].move(rectsSlavesNome[x].right + 5, rectsSlavesNome[x - 1].bottom + 2)
            rectsSlavesPedra[x] = rectsSlavesPedra[x].move(rectsSlavesLvl[x].right + 5, rectsSlavesNome[x - 1].bottom + 2)
            rectsSlaveTempo[x] = rectsSlaveTempo[x].move(rectsSlavesPedra[x].right + 5, rectsSlavesNome[x - 1].bottom + 2)
    
        screen.blit(nomeSlave, rectsSlavesNome[x])
        screen.blit(slavePedra, rectsSlavesPedra[x])
        screen.blit(tempoSkill, rectsSlaveTempo[x])
        screen.blit(slaveLvl, rectsSlavesLvl[x])

        x += 1

def Dungeon():
    Menu(preto)
    
    dungeonLevel = fonte.render("Ultimo Andar Alcancado: " + str(jogador.combateDict["ultimaDungeon"]), 1, (branco), (vermelho_escuro))
    dungeonLevelRect = dungeonLevel.get_rect()
    dungeonLevelRect = dungeonLevelRect.move(100, menuRectFundo.bottom + 5)

    dungeonLevelMaximo = fonte.render("Maior Andar Alcancado: " + str(jogador.combateDict["maiorDungeon"]), 1, (branco), (vermelho_escuro))
    dungeonLevelMaximoRect = dungeonLevelMaximo.get_rect()
    dungeonLevelMaximoRect = dungeonLevelMaximoRect.move(dungeonLevelRect.right + 5, dungeonLevelRect.top)

    mobsMaximo = fonte.render("Total de Mobs Mortos: " + str(jogador.combateDict["mobsMortosTotal"]), 1, (branco), (vermelho_escuro))
    mobsMaximoRect = mobsMaximo.get_rect()
    mobsMaximoRect = mobsMaximoRect.move(100, dungeonLevelMaximoRect.bottom + 5)
    
    entrarDungeon = fonte.render("Entrar", 1, (branco), (vermelho_escuro))
    entrarDungeonRect = entrarDungeon.get_rect()
    entrarDungeonRect = entrarDungeonRect.move(mobsMaximoRect.right + 5, dungeonLevelMaximoRect.bottom + 5)

    ########Status Player############
    jogadorLvlRect = JogadorStats(110, entrarDungeonRect.bottom + 20)

    ######Botoes para Upar############
    botaoVida = fonte.render(" + ", 1, (branco), (vermelho))
    botaoVidaRect = botaoVida.get_rect()
    botaoVidaRect = botaoVidaRect.move(jogadorLvlRect.right + 150, jogadorLvlRect.bottom + 2)

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

    jogadorLvl = fonte.render("Lvl: " + str(jogador.combateDict["CombateLvl"]), 1, (branco), (preto))
    jogadorLvlRect = jogadorLvl.get_rect()
    jogadorLvlRect = jogadorLvlRect.move(jogadorTextRect.left, jogadorTextRect.bottom + 2)

    jogadorVida = fonte.render("Vida: " + str(jogador.combateDict["vida"]) + "/" + str(jogador.combateDict["vidaCheia"]), 1, (branco), (preto))
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
  
    jogador.mobStats["mobVida"] = ((jogador.mobBase["vida"] * randVida) + (jogador.mobStats["mobLevel"] / 3)) * randVida2
    jogador.mobStats["mobVidaCheia"] = jogador.mobStats["mobVida"]
    
    randAtaque = randint((jogador.mobStats["mobAtual"] + jogador.mobStats["mobLevel"]),
                         (jogador.mobStats["mobLevel"] * jogador.mobStats["mobAtual"]) + jogador.mobStats["mobAtual"])
    jogador.mobStats["mobAtaque"] = (jogador.mobBase["ataque"] * randAtaque) + jogador.mobStats["mobLevel"]
    
    randDefesa = randint(1, (jogador.mobStats["mobLevel"] * jogador.mobStats["mobAtual"]))
    jogador.mobStats["mobDefesa"] = (jogador.mobBase["defesa"] * randDefesa) + jogador.mobStats["mobLevel"]


def SelecionarItem(andarAtual):

    dictLoad = jogador.andarDropList
    randomSelecionado = 0
    itemSelecionado = 0
    chance = 0
    loop = 0
    loopSelecionado = 0

    randomSelecionado = randint(1, 100)

    for key in dictLoad[str(andarAtual)]:
        chance += dictLoad[str(andarAtual)][key]["chance"]
        
        if randomSelecionado <= chance:
            for key in dictLoad[str(andarAtual)]:
                if loopSelecionado == loop:
                    itemSelecionado = key
                    return itemSelecionado
                
                loopSelecionado += 1
                
        loop += 1
    
def MobDrop():

    andarAtual = jogador.dungeonStats["andarAtual"]
    loopLista = 0
    multiplicador = 1
    quantidade = 0

    resultadoMod = 0
    resultadoDiv = 0

    
    if str(andarAtual) not in jogador.andarDropList:
        
        for keys in jogador.andarDropList:
            key = int(keys)
            if loopLista == 0:
                resultadoMod = andarAtual%key
                resultadoDiv = andarAtual/key
                multiplicador = key
            else:
                if (andarAtual%key) <= resultadoMod:
                    if (andarAtual/key) <= resultadoDiv:
                        resultadoMod = andarAtual%key
                        resultadoDiv = andarAtual/key
                        multiplicador = key
            
            loopLista += 1
        andarAtual = multiplicador
        multiplicador = (multiplicador / 2) + 1

    itemSelecionado = SelecionarItem(andarAtual)
    tipoIten = VerificarEquipamento(itemSelecionado)
    
    if itemSelecionado != None:
        quantidade = jogador.andarDropList[str(andarAtual)][itemSelecionado]["quantidade"] * multiplicador
        
        if itemSelecionado not in jogador.jogadorInv:
            if tipoIten == False:
                jogador.jogadorInv[itemSelecionado] = int(quantidade)
            else:
                jogador.jogadorInv[itemSelecionado] = {"0": int(quantidade)}
        else:
            if tipoIten == False:
                jogador.jogadorInv[itemSelecionado] += int(quantidade)
            else:
                if "0" not in jogador.jogadorInv[itemSelecionado]:
                    print jogador.jogadorInv[itemSelecionado]
                    jogador.jogadorInv[itemSelecionado]["0"] = int(quantidade)
                else:
                    jogador.jogadorInv[itemSelecionado]["0"] += int(quantidade)

        jogador.mobStats["mobDrop"] = itemSelecionado
        jogador.mobStats["mobDropQuantidade"] = quantidade
    else:
        jogador.mobStats["mobDrop"] = "Nada"
        jogador.mobStats["mobDropQuantidade"] = ""

def ZerarVidaMob():

    MobDrop()
            
    jogador.dungeonStats["mobsMortos"] += 1
            
    if jogador.dungeonStats["mobsMortos"] / (5 * jogador.dungeonStats["andarAtual"]) > 0:
        jogador.dungeonStats["andarAtual"] += 1
                
    exp = jogador.mobBase["exp"] + ((jogador.mobStats["mobAtual"] * jogador.mobStats["mobLevel"]) * jogador.combateDict["CombateLvl"])
    jogador.dungeonStats["expTotal"] += exp
    jogador.combateDict["exp"] += exp
    LevelUp(jogador.combateDict, "CombateLvl", "exp")
            
    MobStats()


def InicializarCombate():
    
    jogador.dungeonStats["andarAtual"] = 1
    jogador.dungeonStats["mobsMortos"] = 0
    jogador.dungeonStats["expTotal"] = 0
    jogador.mobStats["mobDrop"] = ""
    jogador.mobStats["mobDropQuantidade"] = 0
        
    MobStats()


def Flash(loop, pos):

    efeito = pygame.image.load("efeitos/esplosao" + str(loop) + ".png")
    efeito = pygame.transform.scale(efeito, (96,96))
    convert = efeito.convert()
    convert = efeito.set_colorkey((219,219,219))

    screen.blit(efeito, pos)

def DungeonLoop():

    mobPosX = 220

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
    posx = (scrRect.width / 2) - (dungeonLevelRect.width / 2)
    dungeonLevelRect = dungeonLevelRect.move(posx, menuRectFundo.bottom + 5)

    ######Eu#######

    jogadorLvlRect = JogadorStats(10, dungeonLevelRect.bottom + 5)

    #######Mob#######

    mobFigura = pygame.image.load(jogador.mobSprite[str(jogador.mobStats["mobAtual"])])
    convert = mobFigura.convert()
    convert = mobFigura.set_colorkey((0,128,0))
    rectFigura = mobFigura.get_rect()
    rectFigura = rectFigura.move(dungeonLevelRect.centerx, dungeonLevelRect.bottom + 10)

    #if jogador.mobStats["mobVida"] > 0:
     #   print rectFigura
      #  jogador.posAnimacao = (rectFigura.centerx, rectFigura.centery)
       # print jogador.posAnimacao, dungeonLevelRect.bottom + 10
        #Flash(1, jogador.posAnimacao)

    mobNome = fonte.render(str(jogador.mobList[str(jogador.mobStats["mobAtual"])]), 1, (branco), (preto))
    mobNomeRect = mobNome.get_rect()
    mobNomeRect = mobNomeRect.move(mobPosX * 2, dungeonLevelRect.bottom + 5)

    mobLvl = fonte.render("Lvl: " + str(jogador.mobStats["mobLevel"]), 1, (branco), (preto))
    mobLvlRect = mobLvl.get_rect()
    mobLvlRect = mobLvlRect.move(mobNomeRect.left, mobNomeRect.bottom + 2)

    mobVidaTxt = fonte.render("Vida: " + str(jogador.mobStats["mobVida"]) + "/" +
                                             str(jogador.mobStats["mobVidaCheia"]), 1, (branco), (preto))
    mobVidaTxtRect = mobVidaTxt.get_rect()
    mobVidaTxtRect = mobVidaTxtRect.move(mobNomeRect.left, mobLvlRect.bottom + 2)

    mobAtaqueTxt = fonte.render("Ataque: " + str(jogador.mobStats["mobAtaque"]), 1, (branco), (preto))
    mobAtaqueTxtRect = mobAtaqueTxt.get_rect()
    mobAtaqueTxtRect = mobAtaqueTxtRect.move(mobNomeRect.left, mobVidaTxtRect.bottom + 2)

    mobDefesaTxt = fonte.render("Defesa: " + str(jogador.mobStats["mobDefesa"]), 1, (branco), (preto))
    mobDefesaTxtRect = mobDefesaTxt.get_rect()
    mobDefesaTxtRect = mobDefesaTxtRect.move(mobNomeRect.left, mobAtaqueTxtRect.bottom + 2)

    #####Status da Batalha####

    rectStatusBatalha = pygame.draw.rect(screen, vermelho_escuro, ((scrRect.width / 2) - 150, mobDefesaTxtRect.bottom + 60,
                                                                300, 100))

    danoTexto = fonte.render(("Voce tirou:  " + str(dano) + " Mob tirou:  " + str(danoMob)), 1, (branco), (preto))
    danoTextoRect = danoTexto.get_rect()
    danoTextoRect = danoTextoRect.move(rectStatusBatalha.left + 10, rectStatusBatalha.top + 10)

    expTotalTexto = fonte.render("Voce ganhou " + str(jogador.dungeonStats["expTotal"]) + " Exp", 1, (branco), (preto))
    expTotalRect = expTotalTexto.get_rect()
    expTotalRect = expTotalRect.move(danoTextoRect.left, danoTextoRect.bottom + 2)

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
    screen.blit(mobFigura, rectFigura)
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

def Equipar(item):

    string, valor = SepararNumero(item)
    tipoItem = VerificarEquipamento(string)
    statsTotal = StatusEquipamento(tipoItem, string, valor)

    if tipoItem == "Espada":
        jogador.jogadorEquip["PrimeiraMao"] = item
        jogador.combateDict["ataque"] = jogador.combateDict["ataqueBase"] + statsTotal
        print jogador.combateDict["ataque"]
        Informacoes("Ataque: " + str(jogador.combateDict["ataque"]))
    elif tipoItem == "Capacete":
        jogador.jogadorEquip["Cabeca"] = item
        jogador.combateDict["defesa"] = jogador.combateDict["defesaBase"] + statsTotal
        print jogador.combateDict["defesa"]
        Informacoes("Defesa: " + str(jogador.combateDict["defesa"]))


def Menu(cor):

    screen.fill(cor, scrRect)
    screen.fill(branco_ostra, menuRectFundo)
    
    Bag = fonte.render("Bag", 1, (branco), (preto))
    BagRect = Bag.get_rect()
    BagRect = BagRect.move((menuRectFundo.width / 4) - BagRect.width, (menuRectFundo.height / 2) - (BagRect.height / 2))
    
    Status = fonte.render("Status", 1, (branco), (preto))
    StatusRect = Status.get_rect()
    StatusRect = StatusRect.move(BagRect.right + 5, BagRect.top)

    Equipar = fonte.render("Equipar", 1, (branco), (preto))
    EquiparRect = Equipar.get_rect()
    EquiparRect = EquiparRect.move(StatusRect.right + 5, StatusRect.top)

    Skills = fonte.render("Skills", 1, (branco), (preto))
    SkillsRect = Skills.get_rect()
    SkillsRect = SkillsRect.move(EquiparRect.right + 5, EquiparRect.top)

    Dungeon = fonte.render("Dungeon", 1, (branco), (vermelho))
    DungeonRect = Dungeon.get_rect()
    DungeonRect = DungeonRect.move(SkillsRect.right + 5, SkillsRect.top)

    Save = fonte.render("Save", 1, (branco), (preto))
    SaveRect = Save.get_rect()
    SaveRect = SaveRect.move(DungeonRect.right + 5, DungeonRect.top)

    screen.blit(Equipar, EquiparRect)
    screen.blit(Dungeon, DungeonRect)
    screen.blit(Save, SaveRect)
    screen.blit(Bag, BagRect)
    screen.blit(Status, StatusRect)
    screen.blit(Skills, SkillsRect)
        
    return BagRect, StatusRect, EquiparRect, SkillsRect, SaveRect, DungeonRect

def Bag():

    Menu(marron_escuro)

    tipoItens = fonte.render("Itens", 1, (branco), (verde))
    tipoItensRect = tipoItens.get_rect()
    tipoItensRect = tipoItensRect.move((scrRect.width / 3) - (tipoItensRect.width / 2), menuRectFundo.bottom + 10)

    equipamentos = fonte.render("Equipamentos", 1, (branco), (verde))
    equipamentosRect = equipamentos.get_rect()
    equipamentosRect = equipamentosRect.move(tipoItensRect.right + 5, tipoItensRect.top)

    screen.blit(equipamentos, equipamentosRect)
    screen.blit(tipoItens, tipoItensRect)

    x = 0
    y = 0
    z = 0
    rectsINV = []
    chaves = []
    entrou = False
    oreBarra = False
    
    for key in jogador.jogadorInv:
        chaveTipo = VerificarEquipamento(key)
        chaveIten = VerificarIten(key)

        if chaveTipo == False:
            if chaveIten == False:
                iten = fonte.render(str(key) + ": "  + str(jogador.jogadorInv[key]), 1, (branco), (verde))
                entrou = True

            elif chaveIten == "ores":
                chaveOre = 0
                for keys in jogador.catalogoMining:
                    if key == jogador.catalogoMining[keys]:
                        chaveOre = keys
                    
                iten = pygame.image.load(jogador.catalogoMiningSprites[chaveOre])
                iten = pygame.transform.scale(iten, (32,32))

                oreBarra = True
                entrou = True

            elif chaveIten == "barra":
                chaveBarra = 0
                for keys in jogador.catalogoSmithing:
                    if key == jogador.catalogoSmithing[keys]:
                        chaveBarra = keys

                iten = pygame.image.load(jogador.catalogoBarraSprites[chaveBarra])
                #iten = pygame.transform.scale(iten, (32,32))
        
                oreBarra = True
                entrou = True

            elif chaveIten == "outros":
            
                iten = pygame.image.load(jogador.itensSprites[key])
                #iten = pygame.transform.scale(iten, (32,32))

                entrou = True
                oreBarra = True

            if entrou == True:

                rectsINV.append(iten.get_rect())
                chaves.append(key)

                if x == 0:
                    rectsINV[x] = rectsINV[x].move(12, equipamentosRect.bottom + 10)
                else:
                    if ((rectsINV[x - 1].right + 12) + rectsINV[x].width) > scrRect.width:
                        y += rectsINV[x].height
                        z += scrRect.width
                        rectsINV[x] = rectsINV[x].move(12, rectsINV[x - 1].top + y + 10)
                        
                    else:
                        rectsINV[x] = rectsINV[x].move(rectsINV[x - 1].right + 12, rectsINV[x - 1].top)  
                
                screen.blit(iten, rectsINV[x])
                x += 1
                entrou = False
            
            if oreBarra == True:
            
                if jogador.jogadorInv[key] > 1000:
                    valor = jogador.jogadorInv[key] / 1000
                    itenStringQuantidade = fonte.render(str(valor) + "k", 1, (dourado))
                else:
                    itenStringQuantidade = fonte.render(str(jogador.jogadorInv[key]), 1, (dourado))

                convert = itenStringQuantidade.convert()
                convert = itenStringQuantidade.set_colorkey((255,255,255))
                screen.blit(itenStringQuantidade,
                            (rectsINV[x - 1].left, rectsINV[x - 1].top - 3))
                oreBarra = False

    return rectsINV, chaves, equipamentosRect

def BagEquipamento():

    Menu(branco)

    x = 0
    y = 0
    z = 0
    rectsINV = []
    chaves = []

    botaoEquipar = fonte.render("Equipar", 1, (branco), (preto))
    botaoEquiparRect = botaoEquipar.get_rect().move(10, menuRectFundo.bottom + 10)

    tipoItens = fonte.render("Itens", 1, (branco), (verde))
    tipoItensRect = tipoItens.get_rect()
    tipoItensRect = tipoItensRect.move((scrRect.width / 3) - (tipoItensRect.width / 2), menuRectFundo.bottom + 10)

    equipamentos = fonte.render("Equipamentos", 1, (branco), (verde))
    equipamentosRect = equipamentos.get_rect()
    equipamentosRect = equipamentosRect.move(tipoItensRect.right + 5, tipoItensRect.top)

    screen.blit(botaoEquipar, botaoEquiparRect)
    screen.blit(equipamentos, equipamentosRect)
    screen.blit(tipoItens, tipoItensRect)
    
    for key in jogador.jogadorInv:
        chaveTipo = VerificarEquipamento(key)
        if not chaveTipo == False:
            for keys in jogador.jogadorInv[key]:

                itenString = fonte.render("+" + keys, 1, (preto), (branco))
                itenStringQuantidade = fonte.render(str(jogador.jogadorInv[key][keys]), 1, (preto), (branco))
                iten = pygame.image.load(jogador.itensStats[chaveTipo][key]["Sprite"])

                if chaveTipo == "Espada":
                    iten = pygame.transform.smoothscale(iten, (48,48))
                else:
                    iten = pygame.transform.smoothscale(iten, (32,48))

                convertIten = iten.convert()
                convertIten = iten.set_colorkey((branco))
                    
                convert = itenString.convert()
                convert = itenString.set_colorkey((branco))

                convert2 = itenStringQuantidade.convert()
                convert2 = itenStringQuantidade.set_colorkey((branco))
                    
                rectsINV.append(iten.get_rect())
                chaves.append(key+keys)
                
                if x == 0:
                    rectsINV[x] = rectsINV[x].move(10, equipamentosRect.bottom + 10)
                else:
                    if ((rectsINV[x - 1].right + 10) + rectsINV[x].width) > scrRect.width:
                        y += rectsINV[x].height
                        z += scrRect.width
                        rectsINV[x] = rectsINV[x].move(10, rectsINV[x - 1].top + y + 10)
                        
                    else:
                        rectsINV[x] = rectsINV[x].move(rectsINV[x - 1].right + 10, rectsINV[x - 1].top)                        
                        
                    
                screen.blit(iten, rectsINV[x])
                screen.blit(itenString, (rectsINV[x].left - 2, rectsINV[x].top))
                screen.blit(itenStringQuantidade, (rectsINV[x].right +5 - itenStringQuantidade.get_width(), rectsINV[x].bottom + 2 - itenStringQuantidade.get_height()))
                x += 1
                
    if len(rectsINV) > 0:
        return tipoItensRect, rectsINV, chaves, botaoEquiparRect
    else:
        return tipoItensRect, False, False, botaoEquiparRect

def StatusEquipamento(tipo, iten, melhoria):

    if tipo == "Espada":
        tipoStats = "Ataque"
    if tipo == "Capacete":
        tipoStats = "Defesa"
        
    base = jogador.itensStats[tipo][iten][tipoStats]
    statsTotal = base
        
    for x in range(1, int(melhoria) + 1, 1):
        statsTotal += base * pow(x,2)

    return statsTotal


def ItenOpcoes(rect, chave):

    ore = False

    optDezRect = ""

    for key in jogador.catalogoMining:
        if chave == jogador.catalogoMining[key]:
            ore = True

    if ore == True:
        optTexto = fonte.render("Forjar", 1, (preto), (branco_ostra))
        optDezTexto = fonte.render("x10", 1, (preto), (branco_ostra))
    else:
        optTexto = fonte.render("Nada Ainda", 1, (preto), (branco_ostra))
        
    optRect = optTexto.get_rect().move(scrRect.right - 100, scrRect.bottom - 20)
    screen.blit(optTexto, optRect)
    
    if ore == True:
        optDezRect = optDezTexto.get_rect().move(optRect.right + 3, optRect.top)
        screen.blit(optDezTexto, optDezRect)


    return optRect, optDezRect
    
            

def Status():
    
    Menu(branco)

    posx = 200

    textoTempo = fonte.render("Tempo Jogado", 1, (preto))
    textoTempoRect = textoTempo.get_rect().move(0, menuRectFundo.bottom + 5)

    text = fonte.render((Tempo(tempo)), 1, (preto))
    textRect = text.get_rect().move(0, textoTempoRect.bottom + 2)

    textoLvl = fonte.render("Mining Lvl: " + str(jogador.jogadorDict["miningLvl"]), 1, (verde), (branco))
    textoLvlRect = textoLvl.get_rect().move(0, textRect.bottom + 5)

    textoXP = fonte.render("Mining Exp: " + str(jogador.jogadorDict["miningExp"]), 1, (verde), (branco))
    textoXpRect = textoXP.get_rect().move(posx, textRect.bottom + 5)

    textoLvlSmithing = fonte.render("Smithing Lvl: " + str(jogador.jogadorDict["smithingLvl"]), 1, (verde), (branco))
    textoLvlSmithingRect = textoLvlSmithing.get_rect().move(0, textoXpRect.bottom + 5)

    textoXPSmithing = fonte.render("Smithing Exp: " + str(jogador.jogadorDict["smithingExp"]), 1, (verde), (branco))
    textoXPSmithingRect = textoXPSmithing.get_rect().move(posx, textoXpRect.bottom + 5)

    textoLvlSlave = fonte.render("SlaveMaster Lvl: " + str(jogador.jogadorDict["slaveMasterLvl"]), 1, (verde), (branco))
    textoLvlSlaveRect = textoLvlSlave.get_rect().move(0, textoXPSmithingRect.bottom + 5)

    textoXPSlave = fonte.render("SlaveMaster Exp: " + str(jogador.jogadorDict["slaveMasterExp"]), 1, (verde), (branco))
    textoXpSlaveRect = textoXPSlave.get_rect().move(posx, textoXPSmithingRect.bottom + 5)

    textoLvlCombate = fonte.render("Combate Lvl: " + str(jogador.combateDict["CombateLvl"]), 1, (verde), (branco))
    textoLvlCombateRect = textoLvlCombate.get_rect().move(0, textoXpSlaveRect.bottom + 5)

    textoXPCombate = fonte.render("Combat Exp: " + str(jogador.combateDict["exp"]), 1, (verde), (branco))
    textoXpCombateRect = textoXPCombate.get_rect().move(posx, textoXpSlaveRect.bottom + 5)

    textoPontosCombate = fonte.render("Pontos para Distribuir: " + str(jogador.combateDict["pontos"]), 1, (verde), (branco))
    textoPontosCombateRect = textoPontosCombate.get_rect().move(0, textoXpCombateRect.bottom + 2)

    screen.blit(textoLvlSmithing, textoLvlSmithingRect)
    screen.blit(textoXPSmithing, textoXPSmithingRect)
    screen.blit(textoLvlCombate, textoLvlCombateRect)
    screen.blit(textoXPCombate, textoXpCombateRect)
    screen.blit(textoPontosCombate, textoPontosCombateRect)
    screen.blit(textoLvlSlave, textoLvlSlaveRect)
    screen.blit(textoXPSlave, textoXpSlaveRect)
    screen.blit(textoLvl, textoLvlRect)
    screen.blit(textoXP, textoXpRect)
    screen.blit(text, textRect)
    screen.blit(textoTempo, textoTempoRect)


def LevelUp(utilizador, lvl, exp):
    
    xpUpar = ((utilizador[lvl] * 100) + utilizador[lvl]) * ((utilizador[lvl] * 5) - (utilizador[lvl] * 3) / utilizador[lvl])
    while utilizador[exp] >= xpUpar:
        Informacoes("Parabens voce upou um level de: " + str(lvl))
        utilizador[exp] -= xpUpar
        utilizador[lvl] += 1
        if utilizador == jogador.combateDict:
            pontos = (1 + utilizador["CombateLvl"]) / 4
            if pontos <= 10:
                utilizador["pontos"] += pontos
            else:
                utilizador["pontos"] += 10

    if lvl == "slaveMasterLvl":
        if (utilizador[lvl] / 5) + 1 > len(jogador.slavesDict):
            NovoSlave()
            
       
def NovoSlave():

    slaveAtual = "slave" + str(len(jogador.slavesDict) + 1)

    jogador.slavesDict[slaveAtual] = {}
    for key in jogador.slavesDictArvore:
        if key not in jogador.slavesDict[slaveAtual]:
            if key == "nome":
                jogador.slavesDict[slaveAtual][key] = "Slave " + str(len(jogador.slavesDict))
            else:
                jogador.slavesDict[slaveAtual][key] = jogador.slavesDictArvore[key]
    

def GastarPontos(atributo):

    if atributo == "chanceDefesaBase" or atributo == "criticoBase":
        jogador.combateDict[atributo] += 1
    else:
        jogador.combateDict[atributo] += jogador.combateBase[atributo] * jogador.combateDict["CombateLvl"]
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
        "smithingLvl": 1,
        "smithingExp": 0,
        "tempoSmithing": 0,
        "tempoReforcar": 0,
        "itenMelhorando": "",
        "itenForjando": "",
        "slaveMasterLvl": 1,
        "slaveMasterExp":0,
        "tempoMining": 0,
        "pedraAtual": 0,
        "tempoTotalJogado": 0,
        "inventario": {},
        "jogadorEquip": {},
        "slavesDict": {},
        "combateDict": {},
        "dungeonStats": {},
        "mobStats": {}
        
        }

    jogadorEquip  = {
        "Cabeca": "",
        "Peito": "",
        "Calca": "",
        "PrimeiraMao": "",
        "SegundaMao": "",
        "Luva": "",
        "Bota": ""
        }

    combateBase = {
        "vidaCheia": 75,
        "ataqueBase": 10,
        "criticoBase": 1,
        "defesaBase": 5,
        "chanceDefesaBase": 5,
        }

    combateDict = {
        "CombateLvl": 1,
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

    posAnimacao = 0
    textoBottom = []
    jogadorInv = {}
    catalogoMining = {}
    catalogoMiningLevel = {}
    catalogoMiningSprites = {}
    catalogoBarraSprites = {}
    catalogoSmithing = {}
    itensSmithing = {}
    itenCategoria = {}
    itensStats = {}
    itensSprites = {}

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
    mobSprite = {}
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
        self.LoadSmithing()
        self.LoadItens()
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

        equip = dictLoad["jogadorEquip"]
        for keys in self.jogadorEquip:
            if keys not in equip:
                equip[keys] = self.jogadorEquip[keys]

        dungeon = dictLoad["dungeonStats"]
        for keys in self.dungeonStats:
            if keys not in dungeon:
                dungeon[keys] = self.dungeonStats[keys]

        mob = dictLoad["mobStats"]
        for keys in self.mobStats:
            if keys not in mob:
                mob[keys] = self.mobStats[keys]

        self.jogadorInv = dictLoad["inventario"]
        self.jogadorEquip = equip
        self.slavesDict = slaves
        self.jogadorDict = dictLoad
        self.combateDict = combate
        self.dungeonStats = dungeon
        self.mobStats = mob

    @classmethod
    def LoadMining(self):

        nome = "catalogoMining" + ".txt"

        try:
            arquivo = json.load(open(nome))
        except:
            raise

        self.catalogoMining = arquivo

        self.catalogoBarraSprites = self.catalogoMining["barraSprites"]
        self.catalogoMiningSprites = self.catalogoMining["spritesOres"]
        self.catalogoSmithing = self.catalogoMining["barra"]
        self.catalogoMiningLevel = self.catalogoMining["level"]

        del self.catalogoMining["barraSprites"]
        del self.catalogoMining["spritesOres"]
        del self.catalogoMining["level"]
        del self.catalogoMining["barra"]

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
        self.mobSprite = self.mobList["sprite"]
        
        del self.mobList["andar"]
        del self.mobList["sprite"]

        #print "Lista de Mobs: " + str(self.mobList)
        #print self.mobAndar

    @classmethod
    def LoadSmithing(self):

        nome = "itensSmithing" + ".txt"

        try:
            arquivo = json.load(open(nome))
        except:
            raise

        self.itensSmithing = arquivo

        #print self.itensSmithing

    @classmethod
    def LoadAndarDefinicoes(self):

        nome = "dungeonInformacoes" + ".txt"

        try:
            arquivo = json.load(open(nome))
        except:
            print "erro no load mob"
            raise

        self.andarDropList = arquivo["andarDrop"]

    @classmethod
    def LoadItens(self):
        
        nome = "itens" + ".txt"
        stats = "itensStats" + ".txt"
        sprites = "catalogoItensSprites" + ".txt"

        try:
            arquivo = json.load(open(nome))
            arquivo2 = json.load(open(stats))
            arquivo3 = json.load(open(sprites))
        except:
            print "erro no load mob"
            raise

        self.itensSprites = arquivo3
        self.itensCategoria = arquivo
        self.itensStats = arquivo2

        #print self.itensCategoria

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

            tempoTotal = self.slavesDict[keys]["tempoMining"]
            pedraAtual = self.slavesDict[keys]["pedraAtual"]
            self.slavesDict[keys]["tempoMining"] = ((40 + ((self.slavesDict[keys]["pedraAtual"]) * 20)) * pedras)

            loopFora = 0
            while self.slavesDict[keys]["tempoMining"] > 0:
                loopFora += 1
                Mining(self.slavesDict[keys], True)
                if loopFora % 10000 == 0:
                    print loopFora
            self.slavesDict[keys]["tempoMining"] = tempoTotal
            self.slavesDict[keys]["pedraAtual"] = pedraAtual

        LevelUp(self.jogadorDict, "slaveMasterLvl", "slaveMasterExp")        

    def Save(self):

        
        nomeTXT = self.jogadorDict["nome"] + ".txt"
        
        for key in self.slavesDict:
            self.slavesDict[key]["data"] = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        self.jogadorDict["inventario"] = self.jogadorInv
        self.jogadorDict["jogadorEquip"] = self.jogadorEquip
        self.jogadorDict["slavesDict"] = self.slavesDict
        self.jogadorDict["combateDict"] = self.combateDict
        self.jogadorDict["mobStats"] = self.mobStats
        self.jogadorDict["dungeonStats"] = self.dungeonStats
        
        #print "\n" + str(self.jogadorDict["inventario"])

        try:
            json.dump(self.jogadorDict, open(nomeTXT, 'w'))
            print "\n" + str(self.jogadorDict)
            Informacoes("Jogo Salvo")
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
marron           = (185, 122,  87)
marron_escuro    = (124,  78,  52)
dourado          = (255, 201,  14)



screen = pygame.display.set_mode((600, 400))
scrRect = screen.get_rect()
scrRect.height = scrRect.height - 60

menuRectFundo = screen.get_rect()
menuRectFundo.height = 25

meioDaTela = scrRect.width / 2

screen.fill((branco))
pygame.display.update()
pygame.init()

fonte = pygame.font.Font(None, 22)

jogador = Jogador("Lust2", "load") #Remover o load e comentar o TempoOffline() para novo jogador.
jogador.TempoOffline()


#####################Variaves###################
clock = pygame.time.Clock()
tempo = pygame.time.get_ticks() / 1000
tempo1 = tempo - 1
tempoCombate = tempo
tempoCombateGet = pygame.time.get_ticks() / 500

tempoAnimacao = pygame.time.get_ticks() / 150
tempoAnimacao2 = tempoAnimacao - 1
xAnimacao = 0

tempoSoma = jogador.jogadorDict["tempoTotalJogado"]

varAtualizacao = 0
combate = False

opcoes = "Rect das Opcoes"
opcoesAparecendo = False
loopOpcoes = 0
loopOpcoesSelecionada = 0
loopOpcoesDesselecionar = 0

rectsINV = []
chaves = []
selecionarOutroIten = False

minerioRect = []
minerioSelecionado = False

smithingSelecionado = False
reforcarSelecionado = False
diminuiuBag = False

textoBottom = []

equipClicado = False
itemAEquipar = ""

#########################Call das funcoes########################################


BagRect, StatusRect, EquiparRect, SkillsRect, SaveRect, DungeonRect = Menu(branco)
Status()

entrarDungeonRect, botaoVidaRect, botaoAtaqueRect, botaoDefesaRect, botaoChanceDefesaRect, botaoCriticoRect = Dungeon()

MiningRect, SlavesRect, SmithingRect = Skills()
minerioRect = MiningSCR()

smithingTextoRect, chaveSmithing = SmithingSCR()
if chaveSmithing != False:
    categoriaItenSmithing = chaveSmithing[0]
    
rectsSmithingEscolhido, itenSmithingEscolhido, voltarSmithing = ItenSmithing(categoriaItenSmithing)
itenDeSmithingSelecionado = itenSmithingEscolhido[0]

reforcarRect, reforcarChave, voltarSmithing = ReforcarSCR()
if reforcarChave != False and jogador.jogadorDict["itenMelhorando"] == "":
    itenReforcarSelecionado = reforcarChave[0]
else:
    itenReforcarSelecionado = jogador.jogadorDict["itenMelhorando"]

tipoItensRect, rectsEquipamento, chavesEquipamento, botaoEquiparRect = BagEquipamento()
rectsINV, chaves, equipamentosRect = Bag()


#################################################################################


while 1:
    tempo = pygame.time.get_ticks() / 1000
    tempoAnimacao = pygame.time.get_ticks() / 150
    tempoCombateGet = pygame.time.get_ticks() / 500
    mouse = pygame.mouse.get_pos()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

        if event.type == pygame.MOUSEBUTTONDOWN:

            ############INFORMACOES DOS EQUIPAMENTOS##########################
            if varAtualizacao == 9:
                compEquip = len(rectsEquipamento)
                e = 0
                equipClicado = False
                while e < compEquip:
                    if equipClicado == False:
                        if rectsEquipamento[e].collidepoint(mouse):
                            
                            compChaves = len(chavesEquipamento[e])
                            equipClicado = True
                            
                            string, valor = SepararNumero(chavesEquipamento[e])
                            chaveTipo = VerificarEquipamento(string)
                            statsTotal = StatusEquipamento(chaveTipo, string, valor)


                            itemAEquipar = chavesEquipamento[e]
                            tipo = ""
                            
                            if chaveTipo == "Espada":
                                tipo = " | Ataque: "
                            elif chaveTipo == "Capacete":
                                tipo = " | Defesa: "
                            Informacoes(string + " +" + str(valor) +
                                        " | Level Necessario: " + str(jogador.itensStats[chaveTipo][string]["LvlNecessario"]) +
                                        tipo + str(statsTotal))
                            
                    e += 1

            ############ESCOLHER UM TIPO DE ITEN PARA FORJAR##################
            if varAtualizacao == 7:
                x = 0
                if smithingSelecionado == False or reforcarSelecionado == False:
                    while x < len(smithingTextoRect):
                        if smithingTextoRect[x].collidepoint(mouse) and chaveSmithing[x] != "Reforcar":
                            smithingSelecionado = True
                            categoriaItenSmithing = chaveSmithing[x]
                            rectsSmithingEscolhido, itenSmithingEscolhido, voltarSmithing = ItenSmithing(categoriaItenSmithing)
                            
                        elif smithingTextoRect[x].collidepoint(mouse) and chaveSmithing[x] == "Reforcar":
                            reforcarRect, reforcarChave, voltarSmithing = ReforcarSCR()
                            reforcarSelecionado = True
                        x += 1
                
                ###########ESCOLHER UM ITEN ESPECIFICO PARA FORJAR################
                z = 0
                if smithingSelecionado == True:
                    while z < len(rectsSmithingEscolhido):
                        if rectsSmithingEscolhido[z].collidepoint(mouse):
                            
                            itenDeSmithingSelecionado = itenSmithingEscolhido[z]
                            ForjarItenSelecionado(categoriaItenSmithing, itenDeSmithingSelecionado)
                            
                        z += 1
                        
                elif reforcarSelecionado == True:
                    while z < len(reforcarRect):
                        if reforcarRect[z].collidepoint(mouse) and (jogador.jogadorDict["tempoReforcar"] == 0 or
                                                                    jogador.jogadorDict["itenMelhorando"] == reforcarChave[z]):

                            itenReforcarSelecionado = reforcarChave[z]
                            diminuiuBag = ReforcarSelecionado(itenReforcarSelecionado)
                            if diminuiuBag == True:
                                reforcarRect, reforcarChave, voltarSmithing = ReforcarSCR()
                                diminuiuBag = False
                            
                        elif reforcarRect[z].collidepoint(mouse) and jogador.jogadorDict["itenMelhorando"] != reforcarChave[z]:
                            Informacoes("Melhorando outro iten: " + str(jogador.jogadorDict["itenMelhorando"]))
                        z += 1
                
            
            ############LOOP PARA ESCOLHER UMA PEDRA PARA MINERAR#############
            if varAtualizacao == 3:
                x = 0
                while x < len(minerioRect):
                    if minerioSelecionado == False:
                        if minerioRect[x].collidepoint(mouse) and (jogador.jogadorDict["pedraAtual"] == 0
                                                                   or jogador.jogadorDict["pedraAtual"] == x + 1):
                            print "click"
                            jogador.jogadorDict["tempoMining"] += (40 + ((x + 1) * 20))
                            jogador.jogadorDict["pedraAtual"] = x + 1
                            minerioSelecionado = True
                        elif minerioRect[x].collidepoint(mouse):
                            Informacoes("Minerandou outra pedra")
                    x += 1
                minerioSelecionado = False
                
            #########LOOP DAS OPCOES DOS ITENS NO INVENTARIO##########
            if varAtualizacao == 0 and opcoesAparecendo == False:
                loopOpcoes = 0
                while loopOpcoes < len(rectsINV):
                    if opcoesAparecendo == False:
                        if rectsINV[loopOpcoes].collidepoint(mouse):
                            opcoes, vezesDez = ItenOpcoes(equipamentosRect, chaves[loopOpcoes])
                            opcoesAparecendo = True
                            loopOpcoesSelecionada = loopOpcoes
                            loopOpcoesDesselecionar = True
                            selecionarOutroIten = False
                            Informacoes(chaves[loopOpcoesSelecionada] + ": " + str(jogador.jogadorInv[chaves[loopOpcoesSelecionada]]))
                    loopOpcoes += 1
                    
            elif varAtualizacao == 0 and opcoesAparecendo == True:
                if opcoes.collidepoint(mouse) and jogador.jogadorInv[chaves[loopOpcoesSelecionada]] > 0:
                    
                    SmithingReturn = ForjarBarra(chaves[loopOpcoesSelecionada])
 
                    if chaves[loopOpcoesSelecionada] in jogador.jogadorInv:
                        screen.fill(branco, opcoes)
                        rectsINV, chaves, equipamentosRect = Bag()
                        opcoes, vezesDez = ItenOpcoes(equipamentosRect, chaves[loopOpcoesSelecionada])
                    else:
                        opcoesAparecendo = False

                    Informacoes(SmithingReturn)

                if vezesDez != "":
                    if vezesDez.collidepoint(mouse) and jogador.jogadorInv[chaves[loopOpcoesSelecionada]] >= 10:
                        loopDez = 0
                        falhas = 0
                        barras = 0
                        while loopDez < 10:
                            SmithingReturn = ForjarBarra(chaves[loopOpcoesSelecionada])
                            if SmithingReturn == "Falhou na Forja":
                                falhas += 1
                            loopDez += 1
    
                        if chaves[loopOpcoesSelecionada] in jogador.jogadorInv:
                            screen.fill(branco, opcoes)
                            screen.fill(branco, vezesDez)
                            rectsINV, chaves, equipamentosRect = Bag()
                            opcoes, vezesDez = ItenOpcoes(equipamentosRect, chaves[loopOpcoesSelecionada])
                        else:
                            opcoesAparecendo = False
                            
                        if "Level Insuficiente" not in SmithingReturn:
                            Informacoes("Voce falhou " + str(falhas) + " vezes, e acertou " + str(10 - falhas))
                        else:
                            Informacoes(SmithingReturn)

                if loopOpcoesDesselecionar == True:

                    if rectsINV[loopOpcoesSelecionada].collidepoint(mouse) or opcoesAparecendo == False:
                        opcoesAparecendo = False
                        screen.fill(branco, opcoes)
                        if vezesDez != "":
                            screen.fill(branco, vezesDez)
                        loopOpcoesSelecionada = 0
                        loopOpcoesDesselecionar = False
                        rectsINV, chaves, equipamentosRect = Bag()
                        Informacoes(chaves[loopOpcoesSelecionada] + ": " + str(jogador.jogadorInv[chaves[loopOpcoesSelecionada]]))
                    else:
                        selecionarOutroIten = False
                        y = 0
                        while y < len(rectsINV):
                            if selecionarOutroIten == False:
                                if rectsINV[y].collidepoint(mouse) and y != loopOpcoesSelecionada:
                                    screen.fill(branco, opcoes)
                                    if vezesDez != "":
                                        screen.fill(branco, vezesDez)
                                    loopOpcoesSelecionada = y
                                    selecionarOutroIten = True
                                    rectsINV, chaves, equipamentosRect = Bag()
                                    opcoes, vezesDez = ItenOpcoes(equipamentosRect, chaves[y])
                                    Informacoes(chaves[loopOpcoesSelecionada] + ": " + str(jogador.jogadorInv[chaves[loopOpcoesSelecionada]]))
                            y += 1
                        
                

            ##########LOOP DAS OPCOES DO MENU E COMBATE#############
            if MiningRect.collidepoint(mouse) and varAtualizacao == 2:
                varAtualizacao = 3
            elif SlavesRect.collidepoint(mouse) and varAtualizacao == 2:
                varAtualizacao = 4
            elif voltarSmithing.collidepoint(mouse) and varAtualizacao == 7:
                varAtualizacao = 7
                smithingSelecionado = False
                reforcarSelecionado = False
            elif SmithingRect.collidepoint(mouse) and varAtualizacao == 2:
                smithingTextoRect, chaveSmithing = SmithingSCR()
                varAtualizacao = 7
                smithingSelecionado = False
                reforcarSelecionado = False
                limparVarSmithing = False
            elif BagRect.collidepoint(mouse) or (tipoItensRect.collidepoint(mouse) and varAtualizacao == 9):
                varAtualizacao = 0
                rectsINV, chaves, equipamentosRect = Bag()
                loopOpcoes = 0
                loopOpcoesDesselecionar = 0
                opcoesAparecendo = False
                loopOpcoesDesselecionar = False
                loopOpcoesDesselecionar = False
                
            elif equipamentosRect.collidepoint(mouse) and varAtualizacao == 0:
                varAtualizacao = 9
                tipoItensRect, rectsEquipamento, chavesEquipamento, botaoEquiparRect = BagEquipamento()
            elif botaoEquiparRect.collidepoint(mouse) and itemAEquipar != "":
                Equipar(itemAEquipar)
                itemAEquipar = ""  
            elif EquiparRect.collidepoint(mouse):
                varAtualizacao = 8
                print "Equipar"
                
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
            ###############OPCOES PARA GASTAR OS PONTOS DE EVOLUCAO##########
            if jogador.combateDict["pontos"] > 0 and combate == False:
                if botaoVidaRect.collidepoint(mouse) and varAtualizacao == 5:
                    GastarPontos("vidaCheia")
                    jogador.combateDict["vida"] = jogador.combateDict["vidaCheia"]
                elif botaoAtaqueRect.collidepoint(mouse) and varAtualizacao == 5:
                    GastarPontos("ataqueBase")
                    jogador.combateDict["ataque"] = jogador.combateDict["ataqueBase"]
                    Equipar(jogador.jogadorEquip["PrimeiraMao"])
                elif botaoDefesaRect.collidepoint(mouse) and varAtualizacao == 5:
                    GastarPontos("defesaBase")
                    jogador.combateDict["defesa"] = jogador.combateDict["defesaBase"]
                    Equipar(jogador.jogadorEquip["Cabeca"])
                elif botaoChanceDefesaRect.collidepoint(mouse) and varAtualizacao == 5:
                    GastarPontos("chanceDefesaBase")
                    jogador.combateDict["chanceDefesa"] = jogador.combateDict["chanceDefesaBase"]
                elif botaoCriticoRect.collidepoint(mouse) and varAtualizacao == 5:
                    GastarPontos("criticoBase")
                    jogador.combateDict["critico"] = jogador.combateDict["criticoBase"]

                
    ##########CONTROLAR O IDLE DE TODO O JOGO NA QUESTAO DO TEMPO########
    if tempo != tempo1:
        tempo1 = tempo  

        if jogador.jogadorDict["tempoMining"] > 0:
            Mining(jogador.jogadorDict)    
        if jogador.jogadorDict["tempoSmithing"] > 0:
            SmithingTempo(jogador.jogadorDict)
        if jogador.jogadorDict["tempoReforcar"] > 0:
            MelhorarTempo(jogador.jogadorDict)
        
            
        for key in jogador.slavesDict:
            if jogador.slavesDict[key]["tempoMining"] > 0:
                Mining(jogador.slavesDict[key])
                
            x = 1
            if jogador.slavesDict[key]["pedraAtual"] == 0:
            
                while jogador.slavesDict[key]["miningLvl"] >= jogador.catalogoMiningLevel[str(x + 1)]:
                    x += 1
                jogador.slavesDict[key]["tempoMining"] += (40 + ((x) * 20))
                jogador.slavesDict[key]["pedraAtual"] = x


    if varAtualizacao == 1:
        Status()
    elif varAtualizacao == 0:
        pass
    elif varAtualizacao == 9:
        pass
    elif varAtualizacao == 2:
        Skills()
    elif varAtualizacao == 3:
        MiningSCR()
    elif varAtualizacao == 4:
        SlavesSCR()
    elif varAtualizacao == 5:
        Dungeon()
    elif varAtualizacao == 7:
        if smithingSelecionado == True:
            ItenSmithing(categoriaItenSmithing)
        elif reforcarSelecionado == True:
            ReforcarSCR()
        else:
            SmithingSCR()
        
    #####Combate########
    elif (varAtualizacao == 6 and combate == True) or combate == True:

        if jogador.dungeonStats["loopCombate"] == 0:
            InicializarCombate()
            jogador.dungeonStats["loopCombate"] = 1
            DungeonLoop()

        if tempoCombate < tempoCombateGet:
            tempoCombate = tempoCombateGet
            DungeonLoop()
            xAnimacao = 1
        '''    
        if tempoAnimacao2 != tempoAnimacao:
            tempoAnimacao2 = tempoAnimacao
            if jogador.posAnimacao != 0:
                xAnimacao += 1
                if xAnimacao <= 9:
                    Flash(xAnimacao, jogador.posAnimacao)
                else:
                    xAnimacao = 0
        '''    

        if jogador.combateDict["vida"] <= 0:
            combate = False
            jogador.dungeonStats["loopCombate"] = 0
            jogador.combateDict["vida"] = jogador.combateDict["vidaCheia"]
            TerminoCombate()
            
        if jogador.mobStats["mobVida"] <= 0 and combate == True:
            ZerarVidaMob()


    pygame.display.update()

    clock.tick(20)
