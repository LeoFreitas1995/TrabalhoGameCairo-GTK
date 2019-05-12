#!/usr/bin/env python
#-*- coding:utf-8 -*-

import gi, os
gi.require_version('Gtk','3.0')
from gi.repository import Gtk, Gdk
import cairo


# 1. constantes
#

# tamanho dos tiles: tile width, tile height
TILE_W      = 32
TILE_H      = 32

# quantos tiles temos?
TOTAL_TILES = 6



# 2. variaveis
#

# informações sobre cada tile: é livre (1) ou sólido (0)?
tiles_info = [1,1,1,0,0,1]

# figuras dos tiles
tiles_img = None


# figura do sprite do jogador
jogador_img = None

# coordenadas do sprite do jogador, em unidades de tiles
jogador_tx   = 1
jogador_ty   = 1


# mapa da fase atual
mapa = None

# tamanho do mapa, em unidades de tiles
mapa_w  = None
mapa_h  = None

# tamanho do mapa, em unidades de pixels
mapa_pw = None
mapa_ph = None




def carrega_mapa(arq):
    global mapa, mapa_w, mapa_h, mapa_pw, mapa_ph
    
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
    global window, jogador_tx, jogador_ty, mapa_w, mapa_h, tiles_info
    
    backup_jogador_tx = jogador_tx
    backup_jogador_ty = jogador_ty

    # altera a posicao do quadrado conforme a tecla
    if event.keyval == Gdk.KEY_Left:
        jogador_tx -= 1
    elif event.keyval == Gdk.KEY_Right:
        jogador_tx += 1
    elif event.keyval == Gdk.KEY_Up:
        jogador_ty -= 1
    elif event.keyval == Gdk.KEY_Down:
        jogador_ty += 1
        
    elif event.keyval == Gdk.KEY_Return:
        print("Enter")
    elif event.keyval == Gdk.KEY_space:
        print("Espaco")
    elif event.keyval == Gdk.KEY_Escape:
        on_close()


    # será que na nova posicao pra onde fomos, colidimos em algo?
    # a priori, não colidimos em nada; vamos ver à seguir...
    colidiu = False
    
    # caiu fora da tela?
    if jogador_tx < 0 or jogador_tx >= mapa_w:
        colidiu = True
        
        # obs.: só fizemos aqui no eixo X. faça no eixo Y tb... 
        

    # esbarrou num tile marcado como "sólido" ?
    tile_img_id = mapa_get( jogador_tx, jogador_ty )
        
    if tiles_info[ tile_img_id ] == 0:
        colidiu = True    
    
    
    # ok, agora chegou a hora de ver se colidiu.
    # se sim, então restaura a posição antiga.
    #
    if colidiu:
        jogador_tx = backup_jogador_tx
        jogador_ty = backup_jogador_ty
        

    # manda repintar a tela
    window.queue_draw()
    return False




def on_draw(widget, cr):
    global jogador_img
    
    # se quiser saber o tamanho atual da janela: w,h
    w = widget.get_allocation().width
    h = widget.get_allocation().height
    
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
    
    # desenha a figura do jogador
    cr.set_source_surface( jogador_img,  px,py )
    cr.paint()


    return False


def on_close(*args):
    Gtk.main_quit()
    return False


def main():
    global window, tiles_img, jogador_img

    # carrega figura do jogador
    jogador_img = cairo.ImageSurface.create_from_png("sprites/jogador.png")
    
    # carrega figuras dos tiles
    tiles_img = []
    for i in range(TOTAL_TILES):
        img = cairo.ImageSurface.create_from_png("tiles/tile%d.png" % i)
        tiles_img.append(img)    

    # carrega mapa da primeira fase
    carrega_mapa("level1.dat")

    
    # cria a janela, configura e manda executar
    window = Gtk.Window()
    window.set_title( "Trabalho CG - Aluno" )
    window.set_app_paintable( True )
    window.set_size_request( mapa_pw, mapa_ph )
    window.connect( "key-press-event", on_key_press )
    window.connect( "draw", on_draw )
    window.connect( "delete-event", on_close )

    window.show_all()
    Gtk.main()


main()
