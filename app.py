from flask import Flask, render_template, jsonify, request
import random

app = Flask(__name__)

class TicTacToe:
    def __init__(self):
        self.board = ['' for _ in range(9)]
        self.current_player = 'X'
        self.game_over = False
        self.winner = None
        
    def make_move(self, position, player):
        if self.board[position] == '' and not self.game_over:
            self.board[position] = player
            if self.check_winner(player):
                self.game_over = True
                self.winner = player
                return True
            elif '' not in self.board:
                self.game_over = True
                self.winner = 'tie'
                return True
            self.current_player = 'O' if player == 'X' else 'X'
            return True
        return False
    
    def check_winner(self, player):
        winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # columns
            [0, 4, 8], [2, 4, 6]               # diagonals
        ]
        for combo in winning_combinations:
            if all(self.board[i] == player for i in combo):
                return True
        return False
    
    def get_winning_line(self):
        winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # columns
            [0, 4, 8], [2, 4, 6]               # diagonals
        ]
        for combo in winning_combinations:
            if self.board[combo[0]] != '' and all(self.board[i] == self.board[combo[0]] for i in combo):
                return combo
        return None
    
    def ai_move(self):
        # Simple AI with some strategy
        # First, try to win
        for i in range(9):
            if self.board[i] == '':
                self.board[i] = 'O'
                if self.check_winner('O'):
                    self.board[i] = ''
                    return i
                self.board[i] = ''
        
        # Block player from winning
        for i in range(9):
            if self.board[i] == '':
                self.board[i] = 'X'
                if self.check_winner('X'):
                    self.board[i] = ''
                    return i
                self.board[i] = ''
        
        # Take center if available
        if self.board[4] == '':
            return 4
        
        # Take corners
        corners = [0, 2, 6, 8]
        available_corners = [i for i in corners if self.board[i] == '']
        if available_corners:
            return random.choice(available_corners)
        
        # Take any available spot
        available = [i for i in range(9) if self.board[i] == '']
        return random.choice(available) if available else None

# Global game instance
game = TicTacToe()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/move', methods=['POST'])
def make_move():
    global game
    data = request.json
    position = data.get('position')
    mode = data.get('mode', 'pvp')
    
    if game.make_move(position, 'X'):
        response = {
            'board': game.board,
            'current_player': game.current_player,
            'game_over': game.game_over,
            'winner': game.winner,
            'winning_line': game.get_winning_line()
        }
        
        # AI move in single player mode
        if mode == 'ai' and not game.game_over:
            ai_pos = game.ai_move()
            if ai_pos is not None:
                game.make_move(ai_pos, 'O')
                response = {
                    'board': game.board,
                    'current_player': game.current_player,
                    'game_over': game.game_over,
                    'winner': game.winner,
                    'winning_line': game.get_winning_line(),
                    'ai_move': ai_pos
                }
        
        return jsonify(response)
    
    return jsonify({'error': 'Invalid move'}), 400

@app.route('/api/reset', methods=['POST'])
def reset_game():
    global game
    game = TicTacToe()
    return jsonify({
        'board': game.board,
        'current_player': game.current_player,
        'game_over': game.game_over,
        'winner': game.winner
    })

@app.route('/api/state', methods=['GET'])
def get_state():
    return jsonify({
        'board': game.board,
        'current_player': game.current_player,
        'game_over': game.game_over,
        'winner': game.winner
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
