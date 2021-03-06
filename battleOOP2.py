class Board():

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def setBoard(self):
        self.board = [[u'\u00B7'] * self.y for _ in range(self.x)]
        return self.board

    def setEnemyBoard(self):
        self.enemy_board = [[u'\u00B7'] * self.y for _ in range(self.x)]
        return self.enemy_board

    def changeBoardMiss(self, row, col): self.board[row][col] = '*'

    def changeBoardHit(self, row, col): self.board[row][col] = 'X'

    def changeBoardMissDiagonal(self, move, enemy):
        if not self.outOfBoard(move[1] - 1, move[0] - 1): enemy.changeBoardMiss(move[1] - 1, move[0] - 1)
        if not self.outOfBoard(move[1] + 1, move[0] + 1): enemy.changeBoardMiss(move[1] + 1, move[0] + 1)
        if not self.outOfBoard(move[1] - 1, move[0] + 1): enemy.changeBoardMiss(move[1] - 1, move[0] + 1)
        if not self.outOfBoard(move[1] + 1, move[0] - 1): enemy.changeBoardMiss(move[1] + 1, move[0] - 1)
        if not self.outOfBoard(move[1] - 1, move[0] - 1): self.enemy_board[move[1] - 1][move[0] - 1] = '*'
        if not self.outOfBoard(move[1] + 1, move[0] + 1): self.enemy_board[move[1] + 1][move[0] + 1] = '*'
        if not self.outOfBoard(move[1] - 1, move[0] + 1): self.enemy_board[move[1] - 1][move[0] + 1] = '*'
        if not self.outOfBoard(move[1] + 1, move[0] - 1): self.enemy_board[move[1] + 1][move[0] - 1] = '*'

    def changeBoardKill(self, move, enemy):
        if not self.outOfBoard(move[1] - 1, move[0]) and self.enemy_board[move[1] - 1][move[0]] != 'X': self.enemy_board[move[1] - 1][move[0]] = '*'
        if not self.outOfBoard(move[1], move[0] - 1) and self.enemy_board[move[1]][move[0] - 1] != 'X': self.enemy_board[move[1]][move[0] - 1] = '*'
        if not self.outOfBoard(move[1] + 1, move[0]) and self.enemy_board[move[1] + 1][move[0]] != 'X': self.enemy_board[move[1] + 1][move[0]] = '*'
        if not self.outOfBoard(move[1], move[0] + 1) and self.enemy_board[move[1]][move[0] + 1] != 'X': self.enemy_board[move[1]][move[0] + 1] = '*'
        if not self.outOfBoard(move[1] - 1, move[0]) and enemy.board[move[1] - 1][move[0]] != 'X': enemy.changeBoardMiss(move[1] - 1, move[0])
        if not self.outOfBoard(move[1], move[0] - 1) and enemy.board[move[1]][move[0] - 1] != 'X': enemy.changeBoardMiss(move[1], move[0] - 1)
        if not self.outOfBoard(move[1] + 1, move[0]) and enemy.board[move[1] + 1][move[0]] != 'X': enemy.changeBoardMiss(move[1] + 1, move[0])
        if not self.outOfBoard(move[1], move[0] + 1) and enemy.board[move[1]][move[0] + 1] != 'X': enemy.changeBoardMiss(move[1], move[0] + 1)

    def changeBoardShip(self, ship):
        if len(ship) == 1:
            for coord in ship:
                col, row = coord
                self.board[row][col] = '>'

        elif ship[0][0] == ship[1][0]:
            for coord in ship:
                col, row = coord
                self.board[row][col] = '^'
        else:
            for coord in ship:
                col, row = coord
                self.board[row][col] = '>'

    def printBoard(self):
        print('  ', end = ' ')
        for i in range(self.y):
            print (string.ascii_letters[i], end = ' ')
        print('{:^25}'.format(' '), end = ' ')
        for i in range(self.y):
            print(string.ascii_letters[i], end = ' ')
        print()
        for i,j in enumerate(self.board):
            if i < 9:
                print('0' + str(i + 1), ' '.join(j), '{:^22}'.format(' '), '0' + str(i + 1), ' '.join(self.enemy_board[i]))
            else:
                print(i + 1, ' '.join(j), '{:^22}'.format(' '), i + 1, ' '.join(self.enemy_board[i]))

    def modCoords(self, coords):
            res = []
            try:
                for coord in coords:
                    coord = coord.split('-')
                    coord[1] = int(coord[1]) - 1
                    i = 0
                    for letter in string.ascii_letters:
                        if coord[0] == letter:
                            coord[0] = i
                            break
                        i += 1
                    res.append([coord[0], coord[1]])
                return res
            except:
                print('Неверно введены координаты!')
                return False

    def checkCoord(self, coord):
        if coord[0] >= self.y or coord[1] >= self.x or coord[0] < 0 or coord[1] < 0:
            return False

        for ship in self.ships:
            if coord in ship or [coord[0] - 1, coord[1]] in ship or [coord[0], coord[1] - 1] in ship or \
                                [coord[0] - 1, coord[1] - 1] in ship or [coord[0] + 1, coord[1]] in ship or \
                                [coord[0], coord[1] + 1] in ship or [coord[0] + 1, coord[1] + 1] in ship or \
                                [coord[0] + 1, coord[1] - 1] in ship or [coord[0] - 1, coord[1] + 1] in ship:
                return False
        return True

    def getShip(self, coords):
        ship = []
        if len(coords) > 1:
            for i in range(len(coords) - 1):
                if coords[i][0] == coords[i+1][0]:
                    if coords[i+1][1] - coords[i][1] != 1:
                        return False
                elif coords[i][1] == coords[i+1][1]:
                    if coords[i+1][0] - coords[i][0] != 1:
                        return False
                else:
                    return False
        for coord in coords:
            if self.checkCoord(coord):
                ship.append(coord)
            else:
                return False
        return ship

    def addShip(self, size):
            self.choosen.append(size)
            i = 0
            for ship in self.ships:
                if len(ship) == size:
                    i += 1
            print('Необходимо добавить {} {}-палубных корабля'.format(5-size - i,  size))
            cont()
            for _ in range(5-size - i):
                clear()
                print('Расстановка кораблей для {}'.format(self.name))
                self.printBoard()

                if size == 1:
                    coords = [input('Введите координаты: ')]
                    if self.modCoords(coords):
                        coords = self.modCoords(coords)
                    else:
                        self.choosen.remove(size)
                        return self.addShip(size)

                else:
                    coords = input('Введите координаты: ').split(';')
                    if self.modCoords(coords):
                        coords = self.modCoords(coords)
                    else:
                        self.choosen.remove(size)
                        return self.addShip(size)
                if len(coords) != size:
                    print('Неверное количество координат')
                    cont()
                    return self.addShip(size)
                if self.getShip(coords) != False:
                    ship = self.getShip(coords)
                    self.ships.append(ship)
                    self.changeBoardShip(ship)
                    clear()
                    self.printBoard()
                else:
                    print('В выбранные координаты нельзя поставить корабль!')
                    self.choosen.remove(size)
                    return self.addShip(size)

    def setRandShip(self):
        sizes = [4,3,2,1]
        for size in sizes:
            i = 0
            while i != 5 - size:
                first_coord = random.randint(0, 9)
                second_coord = random.randint(0, 9)
                position = random.randint(1, 2)
                if size == 1: coords = [[random.randint(0, 9), random.randint(0, 9)]]
                else:
                    if position == 1: coords = [[first_coord + j, second_coord] for j in range(1, size+1)] 
                    elif position == 2: coords = [[first_coord, second_coord + j] for j in range(1, size+1)]   
                if self.getShip(coords) != False:
                    ship = self.getShip(coords)
                    self.ships.append(ship)
                    self.changeBoardShip(ship)
                    i += 1
        if len(self.ships) == 10: return True
            
    def setShip(self):
        try:
            clear()
            print('Расстановка кораблей для {}'.format(self.name))
            self.printBoard()
            size = int(input('Выберите размер корабля\n1. 1-палубный\n2. 2-палубный\n3. 3-палубный\n4. 4-палубный\n\nВыбор: '))
            if size not in range(1,5):
                print('Необходимо ввести число от 1 до 5!')
                cont()
                return self.setShip()
        except ValueError:
            print('Необходимо ввести число!')
            cont()
            return self.setShip()
        if size in self.choosen:
                print('Кораблей данной категории больше нет!')
                cont()
                return self.setShip()
        self.addShip(size)
        if len(self.ships) == 1: return True

class Player(Board):

    def __init__(self, name, x, y):
        super().__init__(x, y)
        self.name = name
        self.ships = []
        self.choosen = []
        self.killed_ships = [[] for _ in range(10)]
        self.hit = False
        self.status = False

    def outOfBoard(self, row, col):
        if row >= self.x or col >= self.y:
            return True
        elif row < 0 or col < 0:
            return True
        else:
            return False

    def getMove(self, enemy, option = 'console', first_coord = None, second_coord = None):
        if option == 'console':
            clear()
            self.printBoard()
            move = [input('Ход игрока {} (пример ввода: а-1): '.format(self.name))]
            try:
                move = self.modCoords(move)[0]
            except TypeError:
                cont()
                return self.getMove(enemy)

            if self.outOfBoard(move[1], move[0]):
                print('Вы вышли за границу поля')
                cont()
                return self.getMove(enemy)
        elif option == 'gui':
            move = [first_coord, second_coord]

        for i, ship in enumerate(enemy.ships):
            if move in ship:
                enemy.changeBoardHit(move[1], move[0])
                self.enemy_board[move[1]][move[0]] = 'X'
                self.changeBoardMissDiagonal(move, enemy)
                self.killed_ships[i].append(move)
                ship.remove(move)
                if len(ship) == 0:
                    print('\nУБИЛ!!!')
                    for move in self.killed_ships[i]:
                        self.changeBoardKill(move, enemy)
                    enemy.ships.remove(ship)
                    if len(enemy.ships) == 0:
                        self.status = True
                        break
                    if option == 'gui':
                        return True
                        break
                if option == 'gui':
                    return True
                    break
                elif option == 'console':
                    return self.getMove(enemy)
                    break

            if self.enemy_board[move[1]][move[0]] == '*' or \
               self.enemy_board[move[1]][move[0]] == 'X':
                if option == 'gui':
                    return True
                    break
                elif option == 'console':
                    print('Туда ты уже стрелял!')
                    return self.getMove(enemy)
                    break
        else:
            self.enemy_board[move[1]][move[0]] = '*'
            enemy.changeBoardMiss(move[1], move[0])
            if option == 'console':
                clear()
                self.printBoard()
                cont()
            elif option == 'gui':
                return False

    def getCompMove(self, enemy, option = 'console'):
        if self.hit == True:
            move = False
            for ship in self.killed_ships:
                if len(ship) > 0:
                    for hit in ship:
                        first_coord, second_coord = random.choice([[hit[0]+1, hit[1]], [hit[0]-1, hit[1]], [hit[0], hit[1]+1], [hit[0], hit[1]-1]])
                        if (not self.outOfBoard(first_coord, second_coord)) and (enemy.board[second_coord][first_coord] != '*') \
                         and (enemy.board[second_coord][first_coord] != 'X'):
                            move = [first_coord, second_coord]
                            break
                if move:
                    break
            else:
                if option == 'gui':
                    return self.getCompMove(enemy, option = 'gui')
                elif option == 'console':
                    return self.getCompMove(enemy)

        elif self.hit == False:
            first_coord = random.randint(0, 9)
            second_coord = random.randint(0, 9)
            move = [first_coord, second_coord]
        for i, ship in enumerate(enemy.ships):
            if self.enemy_board[move[1]][move[0]] == '*' or \
               self.enemy_board[move[1]][move[0]] == 'X':
                if option == 'gui':
                    return self.getCompMove(enemy, option = 'gui')
                    break
                elif option == 'console':
                    return self.getMove(enemy)
                    break
            if move in ship:
                self.hit = True
                enemy.changeBoardHit(move[1], move[0])
                self.changeBoardMissDiagonal(move, enemy)
                self.killed_ships[i].append(move)
                ship.remove(move)
                if len(ship) == 0:
                    self.hit = False
                    print('\nУБИЛ!!!')
                    for move in self.killed_ships[i]:
                        self.enemy_board[move[1]][move[0]] = 'X'
                        self.changeBoardKill(move, enemy)
                    enemy.ships.remove(ship)
                    self.killed_ships[i].clear()
                    if len(enemy.ships) == 0:
                        self.status = True
                        break
                if option == 'gui':
                    return self.getCompMove(enemy, option = 'gui')    
                    break    
                elif option == 'console':
                    return self.getCompMove(enemy)
                    break
        else:
            enemy.changeBoardMiss(move[1], move[0])
            if option == 'gui':
                return False

class Game():

    def setPlayers(self, message):
        try:
            num_of_players = int(input(message))
        except ValueError:
            print('Введите число!')
            return self.setPlayers()
        if num_of_players < 1 or num_of_players > 2:
            print('Необходимо ввести число от 1 до 2!')
            return self.setPlayers()
        return num_of_players

    def startGame(self):
        clear()
        num_of_players = self.setPlayers('Введите количество игроков (1/2): ')

        if num_of_players == 1:
            who = self.setPlayers('1. Player vs Computer\n2. Computer vs Computer\nВыбор: ')
            board = Board(10, 10)
            if who == 2:
                computer1 = Player('Computer 1', 10, 10)
                computer2 = Player('Computer 2', 10, 10)
                computer1.setBoard()
                computer1.setEnemyBoard()
                computer2.setEnemyBoard()
                computer2.setBoard()
                computer1.setRandShip()
                computer2.setRandShip()
                while True:
                    computer1.getCompMove(computer2)
                    if computer1.status == True:
                        print('   Победил {}'.format(computer1.name))
                        break

                    computer2.getCompMove(computer1)
                    if computer2.status == True:
                        print('   Победил {}'.format(computer2.name))
                        break
            elif who == 1:
                player_name = input('Введите имя (Player): ')
                if player_name == '': player_name = 'Player'
                player = Player(player_name, 10, 10)
                computer = Player('Computer', 10, 10)
                player.setBoard()
                player.setEnemyBoard()
                computer.setBoard()
                computer.setEnemyBoard()
                choise = int(input('Выберите способ расстановки кораблей\n1. Руками\n2. Рандомно\nВыбор: '))
                if choise == 1:
                    for _ in range(10):
                        if player.setShip() == True:
                            print('Все корабли для {} успешно расставлены!'.format(player.name))
                            cont()
                            break
                    computer.setRandShip()
                elif choise == 2:
                    player.setRandShip()
                    computer.setRandShip()
                while True:
                    player.getMove(computer)
                    if player.status == True:
                        print('   Победил {}'.format(player.name))
                        break
                    computer.getCompMove(player)
                    if computer.status == True:
                        print('   Победил {}'.format(computer.name))
                        break

        elif num_of_players == 2:
            player1_name = input('Введите имя (Player1): ')
            player2_name = input('Введите имя (Player2): ')

            if player1_name == '': player1_name = 'Player1'
            if player2_name == '': player2_name = 'Player2'

            choise = int(input('Выберите способ расстановки кораблей\n1. Руками\n2. Рандомно\nВыбор: '))
            board = Board(10, 10)
            player1 = Player(player1_name, 10, 10)
            player2 = Player(player2_name, 10 ,10)
            player1.setBoard()
            player1.setEnemyBoard()
            player2.setEnemyBoard()
            player2.setBoard()
            clear()
            players = [player1, player2]
            if choise == 1:
                for player in players:
                    clear()
                    for _ in range(1):
                        if player.setShip() == True:
                            print('Все корабли для {} успешно расставлены!'.format(player.name))
                            cont()
                            break
            elif choise == 2:
                for player in players:
                    if player.setRandShip() == True:
                        print('Все корабли для {} успешно расставлены!'.format(player.name))
                        cont()
        
            done = False
            while not done:
                i = 1
                for player in players:
                    player.getMove(players[i])
                    i -= 1
                    if player.status == True:
                        done = True
                        cont()
                        clear()
                        print('   Победил {}'.format(player.name))
                        player.printBoard()
                        break
                    clear()
                    print('Ход следующего игрока!')
                    cont()

class Gui():

    def __init__(self):
        self.canvas = Canvas(root, width = 830, height = 500, bg = 'lightblue', cursor = 'plus')
        self.canvas.bind('<Button-1>', self.move)
        self.num_of_players = None
        self.canvas.pack()

    def makeBaner(self):
        baner = Toplevel()
        baner.geometry('800x500+100+100')
        Label(baner, text = 'Переход хода!').pack()
        Button(baner, text = 'Нажми, если готов', command = baner.destroy).pack()
        baner.focus_set()
        baner.grab_set()
        baner.wait_window()

    def setPlayers(self, number):
        board = Board(10, 10)
        self.player1 = Player('Player1', 10, 10)
        self.player1.setBoard()
        self.player1.setEnemyBoard()
        self.player1.setRandShip()
        self.player1.flag = True
        self.player2 = Player('Player2', 10, 10)
        self.player2.setBoard()
        self.player2.setEnemyBoard()
        self.player2.setRandShip()
        self.player2.flag = False
        if number == 1:
            self.player2.name = 'Computer'
            self.makeBoard(self.player1)
            self.makeEnemyBoard(self.player1)
        elif number == 2:
            self.makeBoard(self.player1)
            self.makeEnemyBoard(self.player1)

    def makeBoard(self, player):
        y = 30
        for row in player.board:
            x = 30
            for col in row:
                if col == u'\u00B7': self.canvas.create_rectangle(x, y, x + 30, y + 30, fill = 'blue', tag = '{}-{}'.format(x // 30 - 1, y // 30 - 1))
                elif col == 'X': self.canvas.create_rectangle(x, y, x + 30, y + 30, fill = 'lightgreen', tag = '{}-{}'.format(x // 30 - 1, y // 30 - 1))
                elif col == '*': self.canvas.create_oval(x + 10, y + 10, x + 20, y + 20, fill = 'gray', tag = '{}-{}'.format(x // 30 - 1, y // 30 - 1))
                else: self.canvas.create_rectangle(x, y, x + 30, y + 30, fill = 'yellow', tag = '{}-{}'.format(x // 30 - 1, y // 30 - 1))
                x += 30
            y += 30

    def makeEnemyBoard(self, player):
        y = 30
        for row in player.enemy_board:
            x = 500
            for col in row:
                if col == u'\u00B7': self.canvas.create_rectangle(x, y, x + 30, y + 30, fill = 'blue', tag = '{}-{}'.format(x // 30 - 1, y // 30 - 1))
                elif col == 'X': self.canvas.create_rectangle(x, y, x + 30, y + 30, fill = 'lightgreen', tag = '{}-{}'.format(x // 30 - 1, y // 30 - 1))
                elif col == '*': self.canvas.create_oval(x + 10, y + 10, x + 20, y + 20, fill = 'gray', tag = '{}-{}'.format(x // 30 - 1, y // 30 - 1))
                x += 30
            y += 30

    def one_player(self):
        self.setPlayers(1)
        self.num_of_players = 1

    def two_players(self):
        self.setPlayers(2)
        self.num_of_players = 2

    def game_over(self, winner):
        baner = Toplevel()
        baner.geometry('500x200+100+100')
        Label(baner, text = 'Конец игры!').pack()
        Label(baner, text = 'Победил - {}'.format(winner.name)).pack()
        Button(baner, text = 'Нажми, чтобы выйти!', command = root.destroy).pack()
        baner.focus_set()
        baner.grab_set()
        baner.wait_window()

    def move(self, event):
        first_coord = event.x
        second_coord = event.y
        y = 30
        for row in self.player1.board:
            x = 500
            for col in row:
                if first_coord > x and first_coord < x + 30: first_coord = x
                if second_coord > y and second_coord < y + 30: second_coord = y
                x += 30
            y += 30
        first_coord = first_coord // 30 - 1
        second_coord = second_coord // 30 - 1  
        if self.num_of_players == 2:
            if self.player1.flag == True:
                if self.player1.getMove(self.player2, option = 'gui', first_coord = first_coord - 15, second_coord = second_coord) == False:
                    self.player1.flag = False
                    self.player2.flag = True
                    self.makeBoard(self.player1)
                    self.makeEnemyBoard(self.player1)
                    self.makeBaner()
                    self.makeBoard(self.player2)
                    self.makeEnemyBoard(self.player2)
                else:
                    self.makeBoard(self.player1)
                    self.makeEnemyBoard(self.player1)

            elif self.player2.flag == True:
                if self.player2.getMove(self.player1, option = 'gui', first_coord = first_coord - 15, second_coord = second_coord) == False:
                    self.player2.flag = False
                    self.player1.flag = True
                    self.makeBoard(self.player2)
                    self.makeEnemyBoard(self.player2)
                    self.makeBaner()
                    self.makeBoard(self.player1)
                    self.makeEnemyBoard(self.player1)
                else:
                    self.makeBoard(self.player2)
                    self.makeEnemyBoard(self.player2)

        elif self.num_of_players == 1:
            if self.player1.flag == True:
                if self.player1.getMove(self.player2, option = 'gui', first_coord = first_coord - 15, second_coord = second_coord) == False:
                    self.player1.flag = False
                    self.makeBoard(self.player1)
                    self.makeEnemyBoard(self.player1)
                    if self.player2.getCompMove(self.player1, option = 'gui') == False:
                        self.player1.flag = True
                        self.makeBoard(self.player1)
                        self.makeEnemyBoard(self.player1)
                    else:
                        self.makeBoard(self.player1)
                        self.makeEnemyBoard(self.player1)
                        if self.player2.status == True:
                            self.game_over(self.player2)
                else:
                    self.player1.flag = True
                    self.makeBoard(self.player1)
                    self.makeEnemyBoard(self.player1)
                    if self.player1.status == True:
                        self.game_over(self.player1)

if __name__ == '__main__':
    import string, random, sys, os
    from tkinter import *

    def cont(): return input('Введите символ чтобы продолжить')
    def clear():
        if sys.platform.startswith('win'):
            return os.system('cls')
        else:
            return os.system('clear')

    mode = input('Do you want to use GUI?(y/n): ')

    if mode == 'y' or mode == 'yes' or mode == '':

        def one_player(): gui.one_player()
        def two_players(): gui.two_players()
            
        root = Tk()
        root.resizable(False, False)

        gui = Gui()

        menu = Menu(root)
        root.config(menu = menu)
        first_m = Menu(menu)
        menu.add_cascade(label = 'Новая игра', menu = first_m)
        first_m.add_command(label = '1 игрок', command = one_player)
        first_m.add_command(label = '2 игрока', command = two_players)
        first_m.add_command(label = 'Выход', command = root.destroy)
        
        root.mainloop()

    else:
        game = Game()
        game.startGame()
        input('Конец игры!')

