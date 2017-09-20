import pygame
import json


#################FUNCAO TEMPO######################################################
def Tempo(tempo):

    tempo+= tempoSoma
    
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

#################TODO O GUI DA TELA################################################
def Barra(posX, posY, mouse = 0):
    
    screen.fill(preto)

    textoSave = fonte.render("Save", 1, branco)
    rectSave = pygame.draw.rect(screen, preto, (200, 0, textoSave.get_width(), 20))
    

    textTempo = fonte.render(Tempo(tempo), 1, branco)
    textRect = pygame.draw.rect(screen, preto, (0, 0, textTempo.get_width(), 30))
    

    
    textoLevel = fonte.render(("Level " + str(jogador.jogadorDict["level"])), 1, preto)
    retangulo = pygame.draw.rect(screen, branco_ostra, (posX + 5, posY, screen.get_width() - 10, 30))
    retanguloVerde = pygame.draw.rect(screen, verde, (posX + 5, posY, barraTamX, barraTamY))


    screen.blit(textoSave, (rectSave.centerx - (textoSave.get_width() / 2),
                            rectSave.top))
    screen.blit(textTempo, textRect)
    screen.blit(textoLevel, (retangulo.centerx - (textoLevel.get_width() / 2),
                             retangulo.centery -(textoLevel.get_height() / 2)))

    if(mouse != 0):
        if rectSave.collidepoint(mouse):
            jogador.jogadorDict["tempo"] = tempo + tempoSoma
            jogador.Save()
        elif retangulo.collidepoint(mouse):
            jogador.jogadorDict["clicks"] += 1
            jogador.jogadorDict["xpAtual"] += jogador.jogadorDict["level"]
            Barra(posX, posY+4)
    

    BarraStatus(mouse)


def BarraStatus(mouse = 0):
    rectStatus = pygame.draw.rect(screen, cinza_claro, (0, 90, 300, 120))
    posSupText = rectStatus.top + 50

    textoDireita = fonte.render("-->", 1, preto)
    rectDireita = pygame.draw.rect(screen, cinza, (rectStatus.right - 20, rectStatus.top, 20, 15))
    screen.blit(textoDireita, rectDireita)

    textoEsquerda = fonte.render("<--", 1, preto)
    rectEsquerda = pygame.draw.rect(screen, cinza, (rectStatus.left, rectStatus.top, 20, 15))
    screen.blit(textoEsquerda, rectEsquerda)

    if(mouse != 0):
        if(rectDireita.collidepoint(mouse) and jogador.index < jogador.MAX):
            
            jogador.index  += 1
            print "direita"
            
        elif(rectEsquerda.collidepoint(mouse) and jogador.index  > 0):
            jogador.index  -= 1
            print "esquerda"

    if(jogador.index  == 0):
        textoAtt = fonte.render(("Att: " + str(jogador.jogadorDict["ataque"])), 1, cinza_escuro)
        textoVel = fonte.render(("Vel: " + str(jogador.jogadorDict["velocidade"])), 1, cinza_escuro)
        textoXP = fonte.render(("XP: " + str(jogador.jogadorDict["xpAtual"]) + " / " + str(jogador.xpUpar)), 1, cinza_escuro)
        textoClick = fonte.render(("Clicks: " + str(jogador.jogadorDict["clicks"])), 1, cinza_escuro)
    
        screen.blit(textoAtt, (rectStatus.left, posSupText))
        screen.blit(textoVel, (rectStatus.left, posSupText + textoAtt.get_height()))
        screen.blit(textoXP, (rectStatus.right - textoXP.get_width(), posSupText))
        screen.blit(textoClick, (rectStatus.right - textoClick.get_width(), posSupText + textoXP.get_height()))


################JOGADOR#############################################################
class Jogador:

    xpUpar = 100
    barraEncher = xpUpar / 290

    index = 0
    MAX = 2

    jogadorDict = {
        
        "nome": "",
        "level": 1,
        "ataque": 1,
        "velocidade": 1,
        "xpAtual": 0,
        "xpTotal": 0,
        "tempo": 0,
        "clicks": 0,
        
        }

    def __init__(self, nome):
        self.jogadorDict["nome"] = nome

    @classmethod
    def Load(self, nome):
        
        nameLoad = nome + ".txt"
        dictLoad = json.load(open(nameLoad))

        #print self.jogadorDict["level"]
        
        for keys in self.jogadorDict:
            if keys not in dictLoad:
                dictLoad[keys] = self.jogadorDict[keys]
                #print self.jogadorDict[keys]

        self.jogadorDict = dictLoad
        #print self.jogadorDict

        self.XpNecessario()

    def Save(self):

        nomeTXT = self.jogadorDict["nome"] + ".txt"
        #print nomeTXT

        fileSave = open(nomeTXT, "w")
        #print fileSave
        fileSave.close()
        
        json.dump(self.jogadorDict, open(nomeTXT, 'w'))
        print self.jogadorDict

    def VerfUpou(self, barraTamX):
        
        if(self.jogadorDict["xpAtual"] >= self.xpUpar):
            self.jogadorDict["level"] += 1
            self.jogadorDict["ataque"] = self.jogadorDict["level"] / 3
            self.jogadorDict["velocidade"] = self.jogadorDict["level"] / 2
            self.jogadorDict["xpAtual"] -= self.xpUpar
            self.XpNecessario()
            barraTamX = 0

        return barraTamX

    def XpGanho(self):
        self.jogadorDict["xpAtual"] += self.jogadorDict["level"] + (self.jogadorDict["ataque"] +
                                                                    self.jogadorDict["velocidade"])
        self.jogadorDict["xpTotal"] += self.jogadorDict["level"] + (self.jogadorDict["ataque"] +
                                                                    self.jogadorDict["velocidade"])
    @classmethod
    def XpNecessario(self):

        self.xpUpar = (100 + self.jogadorDict["level"]) * ((self.jogadorDict["level"] * 5) -
                                                           (self.jogadorDict["level"] * 3) / self.jogadorDict["level"])
        self.barraEncher = self.xpUpar / 290
    

    
##########################MAIN SCRIPT###############################################

verde            = (  0, 155,   0)
branco           = (255, 255, 255)
branco_ostra     = (234, 230, 202)
preto            = (  0,   0,   0)
cinza            = (185, 185, 185)
cinza_claro      = (200, 200, 200)
cinza_escuro     = (100, 100, 100)

jogador = Jogador("felipeV3")
jogador.Load("felipeV3")

posX = 0
posY = 35
barraTamX = 0
barraTamY = 30

screen = pygame.display.set_mode((300 , 200))
pygame.display.set_caption('idle NO life')
screen.fill((255,255,255))
pygame.display.update()
pygame.init()

fonte = pygame.font.Font(None, 22)

clock = pygame.time.Clock()
fps = 20

tempo = pygame.time.get_ticks() / 1000
tempo1 = tempo
tempoSoma = jogador.jogadorDict["tempo"]

#tudo que tem na tela, graficos.
Barra(posX, posY)

while 1:
    mouse = pygame.mouse.get_pos()
    tempo = pygame.time.get_ticks() / 1000
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            Barra(posX, posY, mouse)

    if(tempo > tempo1):
        tempo1 = tempo
        jogador.XpGanho()
        
        if(jogador.jogadorDict["xpAtual"] >= (jogador.barraEncher * barraTamX)):
            while((jogador.jogadorDict["xpAtual"] >= (jogador.barraEncher * barraTamX)) and barraTamX < 290):
                barraTamX += 1     

        barraTamX = jogador.VerfUpou(barraTamX)

     
    pygame.display.update()
    Barra(posX, posY)
    clock.tick(fps)
