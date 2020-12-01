import random

#объявляем переменные для хранения масти\достоинства\ценности карт -всего 52 карты-

suits = ('Червы', 'Бубны', 'Пики', 'Трефы')
ranks = ('Двойка', 'Тройка', 'Четвёрка', 'Пятерка', 'Шестёрка', 'Семёрка', 'Восьмёрка', 'Девятка', 'Десятка', 'Валет', 'Дама', 'Король', 'Туз')
values = {'Двойка':2, 'Тройка':3, 'Четвёрка':4, 'Пятерка':5, 'Шестёрка':6, 'Семёрка':7, 'Восьмёрка':8, 'Девятка':9, 'Десятка':10, 'Валет':10, 'Дама':10, 'Король':10, 'Туз':11}
playing = True

class Card(object):
	"""docstring for Card:
	52 карты, имеет масть, достоинство
	"""
	def __init__(self, suits, ranks):
		self.suits = suits
		self.ranks = ranks

	def __str__(self):
		return self.ranks + '-' + self.suits
		

class Deck:
    
    def __init__(self):
        self.deck = []  # начинаем с пустого списка
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit,rank))  # создаём объекты Card и добавляем их в список
    
    def __str__(self):
        deck_comp = ''  # начинаем с пустой строки
        for card in self.deck:
            deck_comp += '\n '+card.__str__() # добавляем строку print для каждого объекта Card
        return 'В колоде находятся:' + deck_comp

    def shuffle(self):
        random.shuffle(self.deck)
        
    def deal(self):
        single_card = self.deck.pop()
        return single_card

test_deck = Deck()
print(test_deck)


class Hand(object):
	"""docstring for Hand
	В дополнение к хранению карт, которые были получены из колоды, класс Hand можно использовать для вычисления значений этих карт, используя упомянутый ранее словарь. Также Вам нужно скорректировать значения для Тузов при необходимости."""
	def __init__(self):
		self.cards = [] # начинаем с пустого списка, как и в классе Deck
		self.values = 0 #начинам с нулевого значения (начинаем с достоинства, равного нулю)
		self.ace = 0 # добавляем атрибут, чтобы учитывать тузы (туз как 11 и как 1)
	
	def add_card (self,card):
		self.cards.append(card)
		self.values += values[card.ranks]

	def adjust_for_ace(self):
		while self.value > 21 and self.aces:
			self.value -= 10
			self.aces -= 1

class Chips:
	"""docstring for Chips:
	нам нужно хранить начальные фишки Игрока, его ставки и текущие выигрыши/ Сделано с помощью глобальных переменных"""
	def __init__(self):
		self.total = 100  # можно установить значение по умолчанию, или запрашивать значение у пользователя
		self.bet = 0
        
    def win_bet(self):
        self.total += self.bet
    
    def lose_bet(self):
        self.total -= self.bet


def take_bet(chips): #Функция, в которой игрок делает ставки. Ставка не превышает общее кол-во фишек
    
    while True:
        try:
            chips.bet = int(input('Сколько фишек Вы хотите поставить? '))
        except ValueError:
            print('Извините, ставка должна  быть числом!')
        else:
            if chips.bet > chips.total:
                print("Извините, Ваша ставка не должна превышать ",chips.total)
            else:
                break



def hit(deck,hand): #функция, где игрок берет доп карты
    
    hand.add_card(deck.deal())
    hand.adjust_for_ace()





''' Напишите функцию, которая предлагает Игроку взять дополнительную карту или остаться при текущих картах
Эта функция может принимать колоду и карты игрока hand в качестве параметров, и присваивать значения глобальной переменной playing.
Если Игрок запрашивает дополнительную карту, то вызываем функцию hit(), которую мы обсуждали выше. Если Игрок остается при своих картах, то устанавливаем переменную playing в значение False - с помощью этой переменной мы будем контролировать цикл while позже.'''

def hit_or_stand(deck,hand):
    global playing  # для контроля цикла while
    
    while True:
        x = input("Вы хотите взять дополнительную карту (h - Hit) или остаться при текущих картах (s - Stand)? Введите 'h' или 's' ")
        
        if x[0].lower() == 'h':
            hit(deck,hand)  # определённая выше функция hit()

        elif x[0].lower() == 's':
            print("Игрок остается при текущих картах. Ход дилера.")
            playing = False

        else:
            print("Извините, пожалуйста попробуйте снова.")
            continue
        break




''' Пишем функции для отображения карт
В начале игры, и всякий раз когда Игрок берёт дополнительную карту, первая карта Дилера скрыта, а все карты Игрока видны. В конце игры показываются все карты, и Вы можете показать количество очков для каждого из участников. Напишите функции для каждого из этих сценариев.'''

def show_some(player,dealer):
    print("\nКарты Дилера:")
    print(" <карта скрыта>")
    print('',dealer.cards[1])  
    print("\nКарты Игрока:", *player.cards, sep='\n ')
    
def show_all(player,dealer):
    print("\nКарты Дилера:", *dealer.cards, sep='\n ')
    print("Карты Дилера =",dealer.value)
    print("\nКарты Игрока:", *player.cards, sep='\n ')
    print("Карты Игрока =",player.value)




''' Напишите функции для обработки сценариев завершения игры
В качестве параметр по мере необходимости передавайте объекты hand Игрока, hand Дилера и chips.'''

def player_busts(player,dealer,chips):
    print("Игрок превысил 21!")
    chips.lose_bet()

def player_wins(player,dealer,chips):
    print("Игрок выиграл!")
    chips.win_bet()

def dealer_busts(player,dealer,chips):
    print("Дилер превысил 21!")
    chips.win_bet()
    
def dealer_wins(player,dealer,chips):
    print("Дилер выиграл!")
    chips.lose_bet()
    
def push(player,dealer):
    print("Ничья!.")


''' САМА ИГРА'''

while True:
    # приветственное сообщение
    print('Добро пожаловать в игру Блекджэк! Постарайтесь приблизиться к сумме 21 как можно ближе, не превышая её!\n\
    Дилер берёт дополнительные карты до тех пор, пока не получит сумму больше 17. Туз считается как 1 или 11.')
    
    # Создайте и перемешайте колоду карт, выдайте каждому Игроку по две карты
    deck = Deck()
    deck.shuffle()
    
    player_hand = Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())
    
    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())
            
    # Установите количество фишек Игрока
    player_chips = Chips()  # помните, значение по умолчанию равно 100    
    
    # Спросите у Игрока его ставку
    take_bet(player_chips)
    
    # Покажите карты (но оставьте одну и карт Дилера скрытой)
    show_some(player_hand,dealer_hand)
    
    while playing:  # помните, это переменная из нашей функции hit_or_stand 
        
        # Спросите Игрока, хочет ли он взять дополнительную карту или остаться при текущих картах
        hit_or_stand(deck,player_hand) 
        
        # Покажите карты (но оставьте одну и карт Дилера скрытой)
        show_some(player_hand,dealer_hand)  
        
        # Если карты Игрока превысили 21, запустите player_busts() и выйдите из цикла (break)
        if player_hand.value > 21:
            player_busts(player_hand,dealer_hand,player_chips)
            break        


    # Если карты Игрока не превысили 21, перейдите к картам Дилера и берите доп. карты до суммы карт >=17
    if player_hand.value <= 21:
        
        while dealer_hand.value < 17:
            hit(deck,dealer_hand)    
    
        # Показываем все карты
        show_all(player_hand,dealer_hand)
        
        # Выполняем различные варианты завершения игры
        if dealer_hand.value > 21:
            dealer_busts(player_hand,dealer_hand,player_chips)

        elif dealer_hand.value > player_hand.value:
            dealer_wins(player_hand,dealer_hand,player_chips)

        elif dealer_hand.value < player_hand.value:
            player_wins(player_hand,dealer_hand,player_chips)

        else:
            push(player_hand,dealer_hand)        
    
    # Сообщить Игроку сумму его фишек 
    print("\nСумма фишек Игрока - ",player_chips.total)
    
    # Спросить его, хочет ли он сыграть снова
    new_game = input("Хотите ли сыграть снова? Введите 'y' или 'n' ")
    
    if new_game[0].lower()=='y':
        playing=True
        continue
    else:
        print("Спасибо за игру!")
        break
