import tkinter as tk
import random

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe")
        
        self.board = [' ' for _ in range(9)]  # Liste pour le plateau de jeu
        self.current_player = 'X'  # Le joueur 'X' commence
        
        # Création de l'interface graphique
        self.buttons = [tk.Button(root, text=' ', width=10, height=3,
                                  font=('Arial', 24), command=lambda i=i: self.make_move(i)) 
                        for i in range(9)]
        
        # Placement des boutons sur le plateau
        for i, button in enumerate(self.buttons):
            row = i // 3
            col = i % 3
            button.grid(row=row, column=col)
        
    def make_move(self, index):
        """Gère le tour du joueur ou de l'IA"""
        if self.board[index] == ' ' and self.current_player == 'X':  # Le joueur fait un mouvement
            self.board[index] = 'X'
            self.buttons[index].config(text='X')
            if self.check_win('X'):
                self.end_game("Vous avez gagné !")
            elif ' ' not in self.board:
                self.end_game("Égalité !")
            else:
                self.current_player = 'O'
                self.ai_move()  # Tour de l'IA

    def ai_move(self):
        """L'IA fait son mouvement en utilisant l'algorithme Minimax"""
        best_move = self.minimax(self.board, 'O')
        index = best_move['index']
        self.board[index] = 'O'
        self.buttons[index].config(text='O')
        if self.check_win('O'):
            self.end_game("L'IA a gagné !")
        elif ' ' not in self.board:
            self.end_game("Égalité !")
        else:
            self.current_player = 'X'

    def minimax(self, board, player):
        """Algorithme Minimax pour choisir le meilleur coup"""
        # Obtenir les coups possibles
        available_moves = [i for i, spot in enumerate(board) if spot == ' ']
        
        if self.check_win('O'):  # Si l'IA a gagné
            return {'score': 1}
        elif self.check_win('X'):  # Si le joueur a gagné
            return {'score': -1}
        elif not available_moves:  # Égalité
            return {'score': 0}

        moves = []
        
        for move in available_moves:
            board[move] = player
            if player == 'O':
                result = self.minimax(board, 'X')  # Tour suivant du joueur
                moves.append({'index': move, 'score': result['score']})
            else:
                result = self.minimax(board, 'O')  # Tour suivant de l'IA
                moves.append({'index': move, 'score': result['score']})
            board[move] = ' '  # Annuler le coup pour essayer le suivant
        
        # Choisir le meilleur coup en fonction du joueur actuel
        if player == 'O':
            best_move = max(moves, key=lambda x: x['score'])  # Maximiser pour l'IA
        else:
            best_move = min(moves, key=lambda x: x['score'])  # Minimiser pour le joueur
        
        return best_move

    def check_win(self, player):
        """Vérifie s'il y a un gagnant"""
        winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Lignes horizontales
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Lignes verticales
            [0, 4, 8], [2, 4, 6]              # Diagonales
        ]
        for combo in winning_combinations:
            if all(self.board[i] == player for i in combo):
                return True
        return False

    def end_game(self, message):
        """Termine la partie"""
        for button in self.buttons:
            button.config(state='disabled')
        result_label = tk.Label(self.root, text=message, font=('Arial', 24))
        result_label.grid(row=3, column=0, columnspan=3)

# Création de la fenêtre principale Tkinter
root = tk.Tk()
game = TicTacToe(root)
root.mainloop()
