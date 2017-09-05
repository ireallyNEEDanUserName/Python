import pygame, json
import definicoes, start


def Load():

    fileName = "dadosSprites.txt"

    definicoes.defIten = json.load(open(fileName))

    definicoes.itensDef = definicoes.defIten["itensDef"]

    for keys in definicoes.itensDef:
        definicoes.stats[definicoes.itensDef[keys]] = definicoes.defIten[definicoes.itensDef[keys]]

    for keys in definicoes.itensDef:
        stats = definicoes.stats[keys]
        definicoes.sprites[keys] = pygame.image.load("sprites/" + stats["img"]).convert_alpha()
        stats["rect"] = definicoes.sprites[keys].get_rect()






