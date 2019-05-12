#!/usr/bin/env python
#-*- coding:utf-8 -*-

#########################################################    
#                     EQUIPE                            #
#  Leonardo Freitas, Rômulo Henrique, Edgar dos Santos  #
#                                                       #
#########################################################

import gtk, os, cairo, time, pygame


# 1. constantes
#

# tamanho dos tiles: tile width, tile height
TILE_W      = 32
TILE_H      = 32

# quantos tiles temos?
TOTAL_TILES = 18

#Coordenadas escada

c1 = [6,1]
c2 = [3,14]

escada = [c1, c2]

# 2. variaveis
#

# informações sobre cada tile: é livre (1) ou sólido (0)?
tiles_info = [1,0,0,0,0,2,1,1,1,1,3,1,1,1,1,4,1,1]

# figuras dos tiles
tiles_img = None


# figura do sprite do jogador
jogador_img = None
caveira = None
nadar = None

# coordenadas do sprite do jogador, em unidades de tiles
jogador_tx   = 0
jogador_ty   = 0


# mapa da fase atual
mapa = None

# tamanho do mapa, em unidades de tiles
mapa_w  = None
mapa_h  = None

# tamanho do mapa, em unidades de pixels
mapa_pw = None
mapa_ph = None


#################
#Mob 1
mobe_img = None
mobe_tx = 11
mobe_ty = 4
#Mob 2
mobe_img2 = None
mobe_tx2 = 1
mobe_ty2 = 2
a = 0
b = 0
#################

caveira_flag = None
bateu = False
flag = None

def buraco_escada():
    global escada, c1, c2, jogador_tx, jogador_ty
    for i in range(2):
        if jogador_tx == escada[i][0] and jogador_ty == escada[i][1]:
            if escada[i] == c1:
                jogador_tx = c2[0]
                jogador_ty = c2[1]
                break
            elif escada[i] == c2:
                jogador_tx = c1[0]
                jogador_ty = c1[1]
                break



def carrega_mapa(arq):
    global mapa, mapa_w, mapa_h, mapa_pw, mapa_ph, caveira_flag
    
    mapa = []

    f = open(arq)
    linhas = f.readlines()
    f.close()
        
    for linha in linhas:
        fileira = []
        
        termos = linha.split()
        for termo in termos:
            fileira.append( int(termo) )
        
        mapa_w = len(fileira)
        mapa.append( fileira )
    
    mapa_h = len(mapa)
    
    mapa_pw = mapa_w * TILE_W
    mapa_ph = mapa_h * TILE_H



# lê o número do tile na posicao (tile_x, tile_y) do mapa atual
# obs.: se passar uma posição fora do mapa, retorna ZERO.
#
def mapa_get(tile_x, tile_y):
    if tile_x < 0 or tile_y < 0 or tile_x >= mapa_w or tile_y >= mapa_h:
        return 0        
    return mapa[tile_y][tile_x]


def on_key_press(widget, event):
    global window, jogador_tx, jogador_ty, mapa_w, mapa_h, tiles_info, mobe_tx, mobe_ty
    global caveira_flag, caveira, jogador_img, nadar, bateu, mobe_tx2, mobe_ty2, flag
    
    backup_jogador_tx = jogador_tx
    backup_jogador_ty = jogador_ty

    # altera a posicao do quadrado conforme a tecla
    if event.keyval == gtk.keysyms.Left:
        jogador_tx -= 1
    elif event.keyval == gtk.keysyms.Right:
        jogador_tx += 1
    elif event.keyval == gtk.keysyms.Up:
        jogador_ty -= 1
    elif event.keyval == gtk.keysyms.Down:
        jogador_ty += 1
        
    elif event.keyval == gtk.keysyms.Return:
        print "Enter"
    elif event.keyval == gtk.keysyms.space:
        print "Espaco"
    elif event.keyval == gtk.keysyms.Escape:
        on_close()


    # será que na nova posicao pra onde fomos, colidimos em algo?
    # a priori, não colidimos em nada; vamos ver à seguir...
    colidiu = False
    
    # caiu fora da tela?
    if jogador_tx < 0 or jogador_tx >= mapa_w or jogador_ty < 0 or jogador_ty >= mapa_h:
        colidiu = True
        
    # obs.: só fizemos aqui no eixo X. faça no eixo Y tb... 

    buraco_escada()    

    # esbarrou num tile marcado como "sólido" ?
    tile_img_id = mapa_get( jogador_tx, jogador_ty ) #retorna numero do tile
        
    if tiles_info[ tile_img_id ] == 0:
        colidiu = True   
    ###############################################################################################
    #MORTE
    #VERIFICA MASCARA
    if tiles_info[ tile_img_id ] == 2:
        pygame.mixer.music.load("forro.mp3")
        pygame.mixer.music.play(-1)
        print "caveira"
        caveira_flag = True
        jogador_img = caveira
    
    #VERIFICA NADAR
    elif tiles_info[ tile_img_id ] == 3:
        caveira_flag = None
        jogador_img = nadar
        flag = True

    #VERIFICA SE SAIU
    if tiles_info[ tile_img_id ] == 1 and caveira_flag == None:
        jogador_img = cairo.ImageSurface.create_from_png("sprites/cangaceiro.png")

    
    
    # ok, agora chegou a hora de ver se colidiu.
    # se sim, então restaura a posição antiga.
    #
    if colidiu:
        jogador_tx = backup_jogador_tx
        jogador_ty = backup_jogador_ty

    # manda repintar a tela
    window.queue_draw()
    return False

########################################################################
def updateMob(widget, event):
    global window, mobe_tx, mobe_ty, a, mobe_img, morreu, jogador_tx, jogador_ty, caveira_flag, bateu,x, y
    global jogador_img, mobe_img2, mobe_tx2, mobe_ty2, flag, b
    flag = False
    a += 1
    if a >= 0 and a <= 4:
        mobe_tx += 1   
        mobe_img = cairo.ImageSurface.create_from_png("sprites/bull2.png")
        mobe_tx2 += 1   
        mobe_img2 = cairo.ImageSurface.create_from_png("sprites/bull2.png")
    elif a >= 4 and a <= 8:
        mobe_tx -= 1
        mobe_img = cairo.ImageSurface.create_from_png("sprites/bull1.png")
        mobe_tx2 -= 1
        mobe_img2 = cairo.ImageSurface.create_from_png("sprites/bull1.png")
    else:    
        a = 0

    if jogador_tx == mobe_tx and jogador_ty == mobe_ty or jogador_tx == mobe_tx2 and jogador_ty == mobe_ty2:
        px = jogador_tx * TILE_W
        py = jogador_ty * TILE_H
        print("colidiu")
        #VERIFICA SE MORREU
        if caveira_flag == True:
            pygame.mixer.music.load("theme2.mp3")
            pygame.mixer.music.play(100)
            caveira_flag = None
            jogador_img = cairo.ImageSurface.create_from_png("sprites/cangaceiro.png")
            x = px
            y = py+32
            jogador_tx = x/TILE_W
            jogador_ty = y/TILE_H   
        else:
            pygame.mixer.music.load("bull.mp3")
            pygame.mixer.music.play()
            jogador_tx = 0
            jogador_ty = 0
            jogador_img = cairo.ImageSurface.create_from_png("sprites/cangaceiro.png")
            flag = True
            time.sleep(5)    
    
    ############################################################################################### 
    #TOCA A MUSICA INICIAL
    if flag and jogador_tx == 0 and jogador_ty == 0:
        pygame.mixer.music.load("theme2.mp3")
        pygame.mixer.music.play(100)
    
    #TOCAR MUSICA WINNER
    if jogador_tx == 15 and jogador_ty == 2:
        pygame.mixer.music.load("winner3.mp3")
        pygame.mixer.music.play(100)
    
    #CANGACEIRO DANÇAR
    if jogador_tx == 15 and jogador_ty == 1 or jogador_tx == 16 and jogador_ty == 1 or jogador_tx == 15 and jogador_ty == 0 or jogador_tx == 16 and jogador_ty == 0:
        
        b += 1
        if b >= 0 and b <= 1:
            jogador_img = cairo.ImageSurface.create_from_png("sprites/cangaceirosanfona%d.png" % 1)
        elif b >= 1 and b <= 2:
            jogador_img = cairo.ImageSurface.create_from_png("sprites/cangaceirosanfona%d.png" % 2)
        else:    
            b = 0
        
    time.sleep(0.1)
    window.queue_draw()
########################################################################



def on_expose(widget, event):
    global jogador_img, mobe_img, jogador_tx, jogador_ty, morreu, caveira_flag, nadar, mobe_img2
    global mobe_tx2, mobe_ty2
    
    # se quiser saber o tamanho atual da janela: w,h
    w = widget.get_allocation().width
    h = widget.get_allocation().height
    
    cr = event.window.cairo_create()
    
    cr.set_source_rgb( 0,0,0 )
    cr.paint()


    # desenha o mapa
    for tile_y in range(mapa_h):
        for tile_x in range(mapa_w):
            tile_img_id = mapa_get( tile_x, tile_y )
            
            # converte a coordenada (tile_x, tile_y) para pixels
            px = tile_x * TILE_W
            py = tile_y * TILE_H
            
            cr.set_source_surface( tiles_img[tile_img_id],  px,py )
            cr.paint()
    
    
    # converte coordenada do jogador de tiles para pixels
    px = jogador_tx * TILE_W
    py = jogador_ty * TILE_H

    pxmobe = mobe_tx * TILE_W
    pymobe = mobe_ty * TILE_H

    pxmobe2 = mobe_tx2 * TILE_W
    pymobe2 = mobe_ty2 * TILE_H


    
    # desenha a figura do jogador
    cr.set_source_surface( jogador_img,  px,py )
    cr.paint()

    cr.set_source_surface( mobe_img,  pxmobe,pymobe )
    cr.paint()

    cr.set_source_surface( mobe_img2,  pxmobe2,pymobe2 )
    cr.paint()

    
    return False
        

def on_close(*args):
    gtk.main_quit()
    return False


def main():
    global window, tiles_img, jogador_img, mobe_img, caveira_flag, caveira, nadar, mobe_img2

    pygame.init()
    pygame.mixer.music.load("theme2.mp3")
    pygame.mixer.music.play(100)

    # carrega figura do jogador
    jogador_img = cairo.ImageSurface.create_from_png("sprites/cangaceiro.png")
    mobe_img = cairo.ImageSurface.create_from_png("sprites/bull1.png")
    mobe_img2 = cairo.ImageSurface.create_from_png("sprites/bull1.png")
    caveira = cairo.ImageSurface.create_from_png("sprites/cangaceirocaveira2.png")
    nadar = cairo.ImageSurface.create_from_png("sprites/cangaceironadar.png")
    # carrega figuras dos tiles
    tiles_img = []
    for i in range(TOTAL_TILES):
        img = cairo.ImageSurface.create_from_png("tiles/tile%d.png" % i)
        tiles_img.append(img)    

    # carrega mapa da primeira fase
    carrega_mapa("level1.dat")

    
    # cria a janela, configura e manda executar
    window = gtk.Window()
    window.set_title( "Severino Cavalcante" )
    window.set_app_paintable( True )
    window.set_size_request( mapa_pw, mapa_ph )
    window.connect( "key-press-event", on_key_press )
    window.connect( "expose-event", updateMob )
    window.connect( "expose-event", on_expose )
    window.connect( "delete-event", on_close )

    window.show_all()
    gtk.main()

main()
