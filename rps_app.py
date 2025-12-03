from flask import Flask, render_template, jsonify, request
import random

app = Flask(__name__)

CHOICES = ['rock', 'paper', 'scissors']

def determine_winner(player_choice, computer_choice):
    if player_choice == computer_choice:
        return 'tie'
    
    win_conditions = {
        'rock': 'scissors',
        'paper': 'rock',
        'scissors': 'paper'
    }
    
    if win_conditions[player_choice] == computer_choice:
        return 'player'
    else:
        return 'computer'

@app.route('/')
def index():
    return render_template('rps.html')

@app.route('/api/play', methods=['POST'])
def play():
    data = request.json
    player_choice = data.get('choice')
    
    if player_choice not in CHOICES:
        return jsonify({'error': 'Invalid choice'}), 400
    
    computer_choice = random.choice(CHOICES)
    winner = determine_winner(player_choice, computer_choice)
    
    return jsonify({
        'player_choice': player_choice,
        'computer_choice': computer_choice,
        'winner': winner
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
