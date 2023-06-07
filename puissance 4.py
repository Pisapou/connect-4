import random
import math
import numpy as np
import pygame

##############################################################################
#                          VARIABLES MODIFIABLES                             #
##############################################################################


LIGNES = 6
COLONNES = 7

PLAYER = 1
IA = 2

BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WINNER = (0, 255, 0)

CASE = 100
RAYON = int(CASE/2 - 5)
    
    
##############################################################################
#                              FONCTION JEU                                  #
##############################################################################


def init_board(): # Créer le plateau
    board = np.zeros((LIGNES, COLONNES))
    return board

def pose_piece(board, ligne, colonne, piece): # Pose une piece
    board[ligne][colonne] = piece
    return None
    
def coup_valide(board, col): # Vérifie s'il y a au moins un case vide dans la colonne
    return board[0][col] == 0

def get_top_ligne(board, col): # Trouve la ligne la plus basse jouable d'une colonne
    for l in range(LIGNES-1, -1, -1):
        if board[l][col] == 0:
            return l
        
def get_coups_valides(board): # Renvoie toutes les colonnes "jouable"
    valid_locations = []
    for col in range(COLONNES):
        if coup_valide(board, col):
            valid_locations.append(col)
    return valid_locations

def inverse_joueur(joueur): # Inverse le joueur (1 <-> 2)
    if joueur == 1:
        return 2
    return 1

def upd_board_fin(board,piece): # Change la valeur de l'alignement gagnant en 3
    for pos in pos_partie_gagnante(board, piece):
        board[pos[0]][pos[1]] = 3
    return None

    
    
##############################################################################
#                                  SCANS                                     #
##############################################################################


def partie_gagnante(board, piece):
    """
    param: le plateau board (matrice numpy), et le joueur piece (1 ou 2)
    renvoie: True si le joueur piece a gagné, False sinon
    """
    for c in range(COLONNES-3):
        for l in range(LIGNES):
            if board[l][c] == piece and board[l][c+1] == piece and board[l][c+2] == piece and board[l][c+3] == piece:
                return True

    for c in range(COLONNES):
        for l in range(LIGNES-3):
            if board[l][c] == piece and board[l+1][c] == piece and board[l+2][c] == piece and board[l+3][c] == piece:
                return True

    for c in range(COLONNES-3):
        for l in range(3, LIGNES):
            if board[l][c] == piece and board[l-1][c+1] == piece and board[l-2][c+2] == piece and board[l-3][c+3] == piece:
                return True

    for c in range(3,COLONNES):
        for l in range(3, LIGNES):
            if board[l][c] == piece and board[l-1][c-1] == piece and board[l-2][c-2] == piece and board[l-3][c-3] == piece:
                return True
            
    return False


def pos_partie_gagnante(board, piece):
    """
    param: le plateau board (matrice numpy), et le joueur piece (1 ou 2)
    renvoie: Les coordonnée de l'alignement de 4 gagnants sous le format ((l1,c1),(l2,c2),...)
    """
    for c in range(COLONNES-3):
        for l in range(LIGNES):
            if board[l][c] == piece and board[l][c+1] == piece and board[l][c+2] == piece and board[l][c+3] == piece:
                return ((l,c),(l,c+1),(l,c+2),(l,c+3))

    for c in range(COLONNES):
        for l in range(LIGNES-3):
            if board[l][c] == piece and board[l+1][c] == piece and board[l+2][c] == piece and board[l+3][c] == piece:
                return ((l,c),(l+1,c),(l+2,c),(l+3,c))

    for c in range(COLONNES-3):
        for l in range(3, LIGNES):
            if board[l][c] == piece and board[l-1][c+1] == piece and board[l-2][c+2] == piece and board[l-3][c+3] == piece:
                return ((l-1,c+1),(l-2,c+2),(l,c),(l-3,c+3))

    for c in range(3,COLONNES):
        for l in range(3, LIGNES):
            if board[l][c] == piece and board[l-1][c-1] == piece and board[l-2][c-2] == piece and board[l-3][c-3] == piece:
                return ((l,c),(l-1,c-1),(l-2,c-2),(l-3,c-3))
            
    return None # On ne devrait jamais renvoyer None car cette fonction est executé uniquement lorsqu'il y a un gagnant


def evaluate_window(window, piece):
    """
    param: une fenêtre window (une liste de 4 entier (0, 1 ou 2)), et le joueur piece (1 ou 2)
    renvoie: un score attribué à cette fenêtre en fonction du nombre de piece dans celle-ci
    """
    score = 0
    
    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(0) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(0) == 2:
        score += 2

    if window.count(inverse_joueur(piece)) == 3 and window.count(0) == 1:
        score -= 4 

    return score 


def score_position(board, piece):
    """
    param: le plateau board (matrice numpy), et le joueur piece (1 ou 2)
    renvoie: un score attribué à la position actuelle du plateau board
    """
    score = 0
    colonne_centre = [int(i) for i in list(board[:,COLONNES//2])] # On privilégie la colonne du centre
    compte_centre = colonne_centre.count(piece)
    score += compte_centre * 6

    for l in range(LIGNES):
        ligne = [int(i) for i in list(board[l,:])]
        for c in range(COLONNES - 3):
            window = ligne[c:c + 4]
            score += evaluate_window(window, piece)

    for c in range(COLONNES):
        colonne = [int(i) for i in list(board[:,c])]
        for l in range(LIGNES-3):
            window = colonne[l:l+4]
            score += evaluate_window(window, piece)

    for l in range(3,LIGNES):
        for c in range(COLONNES - 3):
            window = [board[l-i][c+i] for i in range(4)]
            score += evaluate_window(window, piece)

    for l in range(3,LIGNES):
        for c in range(3,COLONNES):
            window = [board[l-i][c-i] for i in range(4)]
            score += evaluate_window(window, piece)

    return score


def fin(board):
    """
    param: le plateau board (matrice numpy)
    renvoie: True si le jeu est finis (un gagne ou partie nulle), False sinon
    """
    return partie_gagnante(board, PLAYER) or partie_gagnante(board, IA) or len(get_coups_valides(board)) == 0

    

        
##############################################################################
#                           INTERFACE GRAPHIQUE                              #
##############################################################################


def draw_board(board):
    """
    param: le plateau board (matrice numpy)
    effet: Redessine le plateau actuelle (de 0)
    renvoie: None
    """
    pygame.draw.rect(screen, BLUE, (0, CASE, CASE*COLONNES, CASE*LIGNES))
    for c in range(COLONNES):
        for l in range(LIGNES):
            if board[l][c] == 0:
                pygame.draw.circle(screen, BLACK, (int(c*CASE+CASE/2), int(l*CASE+CASE+CASE/2)), RAYON)
            elif board[l][c] == 1:
                pygame.draw.circle(screen, RED, (int(c*CASE+CASE/2), int(l*CASE+CASE+CASE/2)), RAYON)
            elif board[l][c] == 2:
                pygame.draw.circle(screen, YELLOW, (int(c*CASE+CASE/2), int(l*CASE+CASE+CASE/2)), RAYON)
            else:
                pygame.draw.circle(screen, WINNER, (int(c*CASE+CASE/2), int(l*CASE+CASE+CASE/2)), RAYON)

    pygame.display.update()
    
    return None


##############################################################################
#                               ALGO MINIMAX                                 #
##############################################################################
    

def minimax(board, prof, alpha, beta, maximizing):
    """
    Bon, un peu la flemme, vous connaissez de toute façon
    """

    coups_possibles = get_coups_valides(board)
    fin_partie = fin(board)

    if prof <= 0 or fin_partie:
        if fin_partie:
            if partie_gagnante(board, IA):
                return (None, math.inf)
            elif partie_gagnante(board, PLAYER):
                return (None, -math.inf)
            else:
                return (None, 0)
        else: 
            return (None, score_position(board, IA))


    if maximizing: # C'est à l'IA -> on prend le max
        
        
        maxi = -math.inf
        best_coup = random.choice(coups_possibles)

        for coup in coups_possibles:
            ligne = get_top_ligne(board, coup)
            temp = board.copy()
            pose_piece(temp, ligne, coup, IA)
            score_temp = minimax(temp, prof-1, alpha, beta, False)[1]
            
            if score_temp > maxi:
                maxi = score_temp
                best_coup = coup
                
            alpha = max(maxi, alpha) 
            if alpha >= beta:
                break

        return (best_coup, maxi)


    else: # C'est au joueur -> on prend le min
        
        
        mini = math.inf
        best_coup = random.choice(coups_possibles)
        
        for coup in coups_possibles:
            ligne = get_top_ligne(board, coup)
            temp = board.copy()
            pose_piece(temp, ligne, coup, PLAYER)
            score_temp = minimax(temp, prof-1, alpha, beta, True)[1]
            
            if score_temp < mini:
                mini = score_temp
                best_coup = coup
                
            beta = min(mini, beta) 
            if alpha >= beta:
                break
            
        return (best_coup,mini)


##############################################################################
#                                  MAIN                                      #
##############################################################################


board = init_board()

run = True
en_cours = True
turn = IA # Qui commence ?

pygame.init()

largeur = COLONNES * CASE
hauteur = (LIGNES + 1) * CASE
size = (largeur, hauteur)
screen = pygame.display.set_mode(size)

font = pygame.font.SysFont("arial", 75)

draw_board(board)


while run:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEMOTION and en_cours:
            pygame.draw.rect(screen, BLACK, (0, 0, largeur, CASE))
            xpos = pygame.mouse.get_pos()[0]
            if turn == PLAYER:
                pygame.draw.circle(screen, RED, (xpos, int(CASE/2)), RAYON )
            pygame.display.update()
            
        if event.type == pygame.MOUSEBUTTONDOWN and en_cours:
            pygame.draw.rect(screen, BLACK, (0,0, largeur, CASE))

            if turn == PLAYER:

                xpos = event.pos[0] 
                colonne = int(xpos/CASE)

                if coup_valide(board, colonne):
                    ligne = get_top_ligne(board, colonne)
                    pose_piece(board, ligne, colonne, PLAYER)
                    if partie_gagnante(board, PLAYER):
                        print("Le joueur a gagné")
                        upd_board_fin(board,PLAYER)
                        texte = font.render("TROP FORT", 1, RED)
                        screen.blit(texte, (100, 10))
                        en_cours = False
                    elif fin(board):
                        en_cours = False

                draw_board(board)

                turn = inverse_joueur(turn)
      
    if turn == IA and run and en_cours:

        colonne, score = minimax(board, 5, -math.inf, math.inf, True) # 5 profondeurs ~ <2sec

        if coup_valide(board, colonne):
            ligne = get_top_ligne(board, colonne)
            pose_piece(board, ligne, colonne, IA)
            if partie_gagnante(board, IA):
                print("L'IA a gagné!")
                upd_board_fin(board,IA)
                texte = font.render("TROP NUL!", 1, YELLOW)
                screen.blit(texte, (100, 10))
                en_cours = False
            elif fin(board):
                en_cours = False
                
        draw_board(board)    

        turn = inverse_joueur(turn)
        
pygame.quit()
