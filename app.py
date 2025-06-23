from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)

# Mock user data
user_balance = 500  # JMD
tickets = []
cashpot_tickets = []

# Cash Pot emojis for responses
CASH_POT_EMOJIS = {
    'duppy': '👻', 'small_man': '👦🏽', 'dead': '⚰️', 'egg': '🥚', 'thief': '🦹',
    'strong_man': '🏋🏽', 'married_woman': '👰', 'belly': '🤰', 'cow': '🐄',
    'white_woman': '👩🏻', 'small_house': '🏠', 'goat': '🐐', 'dog': '🐶', 'rat': '🐀',
    'big_man': '👨🏽', 'fresh_water': '💧', 'johncrow': '🦅', 'white_man': '👨🏻',
    'baby': '👶', 'horse': '🐎', 'big_house': '🏰', 'church': '⛪', 'gold': '🪙',
    'fire': '🔥', 'fish': '🐟', 'weak_man': '🙍🏽‍♂️', 'old_woman': '👵', 'old_man': '👴',
    'black_man': '👨🏿', 'ring': '💍', 'young_girl': '👧', 'drop_pan': '🎰',
    'silver': '🥈', 'fowl': '🐔', 'crocodile': '🐊', 'chinese_man': '👨‍🦲'
}

# Predefined responses in standard English
RESPONSES = {
    'welcome': 'Welcome to Toll-Rizz, Mr. Brown! Say "buy ticket" to get started. Your balance is {balance} JMD.',
    'drive_start': 'Did you have any dreams during your sleep last night? If you tell me, I can give you ideas about lucky picks in the draw this week.',
    'hey_rizz': 'Hello! Say "buy ticket" to purchase a ticket.',
    'buy_success': 'Ticket #{ticket_number} purchased for {toll_name}! 100 JMD deducted.',
    'buy_cashpot_success': 'Ticket purchased for {cashpot_name} {emoji}!',
    'buy_no_toll': 'Please select a toll first.',
    'buy_insufficient': 'Insufficient balance. Your balance is {balance} JMD.',
    'time_t1': 'It takes approximately 30 minutes to reach the May Pen toll.',
    'time_t2': 'The Spanish Town toll is approximately 20 minutes away.',
    'time_no_toll': 'Please select a toll to check the time.',
    'dream_error': 'I did not hear a Cash Pot word. Please try saying "Cow" or "Goat".',
    'voice_error': 'I could not hear you, Mr. Brown. Please try again.',
    # Cash Pot responses
    'duppy': 'Ghost in your dream? Choose number 1. Spirits may bring luck this week.',
    'small_man': 'Small Man? Choose number 2. Small investments may yield significant returns.',
    'dead': 'Death in your dream? Choose number 3. New beginnings may bring success in the lottery.',
    'egg': 'Egg? Choose number 4. Something valuable is about to emerge.',
    'thief': 'Thief? Choose number 5. A smart decision could lead to gains.',
    'strong_man': 'Strong Man? Choose number 6. Your strength will lead to victories.',
    'married_woman': 'Married Woman? Choose number 7. Stability will bring you luck.',
    'belly': 'Belly? Choose number 8. Prosperity is increasing.',
    'cow': 'Cow in your dream? Choose number 9. Wealth and abundance are on the way.',
    'white_woman': 'White Woman? Choose number 10. Unexpected opportunities may arise.',
    'small_house': 'Small House? Choose number 11. A solid foundation will lead to growth.',
    'goat': 'Goat? Choose number 12. Persistence will lead to rewards.',
    'dog': 'Dog? Choose number 13. Loyalty will bring opportunities.',
    'rat': 'Rat? Choose number 14. Quick actions could yield profits.',
    'big_man': 'Big Man? Choose number 15. Influence will bring success.',
    'fresh_water': 'Fresh Water? Choose number 16. New opportunities are emerging.',
    'johncrow': 'Vulture? Choose number 17. Clearing obstacles will bring luck.',
    'white_man': 'White Man? Choose number 18. Foreign opportunities may bring rewards.',
    'baby': 'Baby? Choose number 19. New projects will prosper.',
    'horse': 'Horse? Choose number 20. Speed and energy will lead to wins.',
    'big_house': 'Big House? Choose number 21. Significant wealth is possible.',
    'church': 'Church? Choose number 22. Blessings will bring luck.',
    'gold': 'Gold? Choose number 23. Wealth and success are near.',
    'fire': 'Fire? Choose number 24. Passion will drive success in the lottery.',
    'fish': 'Fish? Choose number 25. Abundance is flowing your way.',
    'weak_man': 'Weak Man? Choose number 26. Small efforts will yield results.',
    'old_woman': 'Old Woman? Choose number 27. Wisdom will bring success.',
    'old_man': 'Old Man? Choose number 28. Experience will lead to gains.',
    'black_man': 'Black Man? Choose number 29. Strength will bring luck.',
    'ring': 'Ring? Choose number 30. Commitment will yield rewards.',
    'young_girl': 'Young Girl? Choose number 31. New ideas will spark success.',
    'drop_pan': 'Drop Pan? Choose number 32. Luck is coming your way.',
    'silver': 'Silver? Choose number 33. Steady growth will bring rewards.',
    'fowl': 'Fowl? Choose number 34. Small bets will yield profits.',
    'crocodile': 'Crocodile? Choose number 35. Strategic moves will bring luck.',
    'chinese_man': 'Chinese Man? Choose number 36. Smart decisions will bring success.'
}

@app.route('/')
def index():
    return render_template('index.html',
                           balance=user_balance,
                           tickets=tickets,
                           profile_img='https://via.placeholder.com/50',
                           welcome=RESPONSES['welcome'].format(balance=user_balance),
                           drive_start=RESPONSES['drive_start'])

@app.route('/buy-ticket', methods=['POST'])
def buy_ticket():
    global user_balance, tickets
    toll = request.form.get('toll')
    if not toll:
        return jsonify({'error': RESPONSES['buy_no_toll']}), 400

    ticket_price = 100  # JMD
    if user_balance < ticket_price:
        return jsonify({'error': RESPONSES['buy_insufficient'].format(balance=user_balance)}), 400

    user_balance -= ticket_price
    ticket_number = random.randint(100000, 999999)
    toll_name = 'May Pen' if toll == 'T1' else 'Spanish Town'
    tickets.append({'toll': toll, 'ticket_number': ticket_number})
    return jsonify({
        'message': RESPONSES['buy_success'].format(ticket_number=ticket_number, toll_name=toll_name),
        'balance': user_balance
    })

@app.route('/buy-cashpot', methods=['POST'])
def buy_cashpot():
    global user_balance, cashpot_tickets
    cashpot = request.form.get('cashpot')
    if not cashpot or cashpot not in CASH_POT_EMOJIS:
        return jsonify({'error': RESPONSES['dream_error']}), 400

    ticket_price = 100  # JMD
    if user_balance < ticket_price:
        return jsonify({'error': RESPONSES['buy_insufficient'].format(balance=user_balance)}), 400

    user_balance -= ticket_price
    cashpot_name = ' '.join(word.capitalize() for word in cashpot.split('_'))
    cashpot_tickets.append({'cashpot': cashpot, 'emoji': CASH_POT_EMOJIS[cashpot]})
    return jsonify({
        'message': RESPONSES['buy_cashpot_success'].format(cashpot_name=cashpot_name, emoji=CASH_POT_EMOJIS[cashpot]),
        'balance': user_balance
    })

@app.route('/calculate-time', methods=['POST'])
def calculate_time():
    toll = request.form.get('toll')
    if not toll:
        return jsonify({'error': RESPONSES['time_no_toll']}), 400
    message = RESPONSES['time_t1'] if toll == 'T1' else RESPONSES['time_t2']
    return jsonify({'message': message})

@app.route('/interpret-dream', methods=['POST'])
def interpret_dream():
    dream = request.form.get('dream')
    if not dream or len(dream.strip()) < 3:
        return jsonify({'error': RESPONSES['dream_error']}), 400
    dream_lower = dream.lower()
    for key in RESPONSES:
        if key in dream_lower and key not in ['welcome', 'drive_start', 'hey_rizz', 'buy_success', 'buy_cashpot_success',
                                             'buy_no_toll', 'buy_insufficient', 'time_t1', 'time_t2', 'time_no_toll',
                                             'dream_error', 'voice_error']:
            return jsonify({'message': RESPONSES[key]})
    return jsonify({'error': RESPONSES['dream_error']})

if __name__ == '__main__':
    app.run(debug=True)