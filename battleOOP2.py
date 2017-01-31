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

class Player(Board):

    def __init__(self, name, x, y):
        super().__init__(x, y)
        self.name = name
        self.ships = []
        self.choosen = []
        self.killed_ships = [[] for _ in range(10)]
        self.status = False

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
        for _ in range(4):
            coords = [[random.randint(0, 9), random.randint(0, 9)]]
            if self.getShip(coords) != False:
                ship = self.getShip(coords)
                self.ships.append(ship)
                self.changeBoardShip(ship)
            else:
                return self.setRandShip()
            if len(self.ships) == 4:
                return True

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
        if len(self.ships) == 1:
            return True

    def getMove(self, enemy):

        def outOfBoard(row, col):
            if row >= self.x or col >= self.y:
                return True
            elif row < 0 or col < 0:
                return True
            else:
                return False

        clear()
        self.printBoard()
        move = [input('Ход игрока {} (пример ввода: а-1): '.format(self.name))]
        try:
            move = self.modCoords(move)[0]
        except TypeError:
            cont()
            return self.getMove(enemy)

        if outOfBoard(move[1], move[0]):
            print('Вы вышли за границу поля')
            cont()
            return self.getMove(enemy)

        else:
            for i, ship in enumerate(enemy.ships):
                if move in ship:
                    enemy.changeBoardHit(move[1], move[0])
                    if not outOfBoard(move[1] - 1, move[0] - 1): enemy.changeBoardMiss(move[1] - 1, move[0] - 1)
                    if not outOfBoard(move[1] + 1, move[0] + 1): enemy.changeBoardMiss(move[1] + 1, move[0] + 1)
                    if not outOfBoard(move[1] - 1, move[0] + 1): enemy.changeBoardMiss(move[1] - 1, move[0] + 1)
                    if not outOfBoard(move[1] + 1, move[0] - 1): enemy.changeBoardMiss(move[1] + 1, move[0] - 1)
                    self.enemy_board[move[1]][move[0]] = 'X'
                    if not outOfBoard(move[1] - 1, move[0] - 1): self.enemy_board[move[1] - 1][move[0] - 1] = '*'
                    if not outOfBoard(move[1] + 1, move[0] + 1): self.enemy_board[move[1] + 1][move[0] + 1] = '*'
                    if not outOfBoard(move[1] - 1, move[0] + 1): self.enemy_board[move[1] - 1][move[0] + 1] = '*'
                    if not outOfBoard(move[1] + 1, move[0] - 1): self.enemy_board[move[1] + 1][move[0] - 1] = '*'
                    self.killed_ships[i].append(move)
                    ship.remove(move)
                    if len(ship) == 0:
                        print('\nУБИЛ!!!')
                        for move in self.killed_ships[i]:
                            if not outOfBoard(move[1] - 1, move[0]) and self.enemy_board[move[1] - 1][move[0]] != 'X': self.enemy_board[move[1] - 1][move[0]] = '*'
                            if not outOfBoard(move[1], move[0] - 1) and self.enemy_board[move[1]][move[0] - 1] != 'X': self.enemy_board[move[1]][move[0] - 1] = '*'
                            if not outOfBoard(move[1] + 1, move[0]) and self.enemy_board[move[1] + 1][move[0]] != 'X': self.enemy_board[move[1] + 1][move[0]] = '*'
                            if not outOfBoard(move[1], move[0] + 1) and self.enemy_board[move[1]][move[0] + 1] != 'X': self.enemy_board[move[1]][move[0] + 1] = '*'
                            if not outOfBoard(move[1] - 1, move[0]) and enemy.board[move[1] - 1][move[0]] != 'X': enemy.changeBoardMiss(move[1] - 1, move[0])
                            if not outOfBoard(move[1], move[0] - 1) and enemy.board[move[1]][move[0] - 1] != 'X': enemy.changeBoardMiss(move[1], move[0] - 1)
                            if not outOfBoard(move[1] + 1, move[0]) and enemy.board[move[1] + 1][move[0]] != 'X': enemy.changeBoardMiss(move[1] + 1, move[0])
                            if not outOfBoard(move[1], move[0] + 1) and enemy.board[move[1]][move[0] + 1] != 'X': enemy.changeBoardMiss(move[1], move[0] + 1)

                        enemy.ships.remove(ship)
                        if len(enemy.ships) == 0:
                            self.status = True
                            break
                        cont()
                    return self.getMove(enemy)
                    break

                if self.enemy_board[move[1]][move[0]] == '*' or \
                   self.enemy_board[move[1]][move[0]] == 'X':
                    print('Туда ты уже стрелял!')
                    cont()
                    return self.getMove(enemy)
                    break
            else:
                self.enemy_board[move[1]][move[0]] = '*'
                enemy.changeBoardMiss(move[1], move[0])
                clear()
                self.printBoard()
                cont()

class Game():

    def setPlayers(self):
        try:
            num_of_players = int(input('Введите количество игроков (1/2): '))
        except ValueError:
            print('Введите число!')
            return self.setPlayers()
        if num_of_players < 1 or num_of_players > 2:
            print('Необходимо ввести число от 1 до 2!')
            return self.setPlayers()
        return num_of_players

    def startGame(self):
        clear()
        num_of_players = self.setPlayers()

        if num_of_players == 1:
            pass

        elif num_of_players == 2:
            player1_name = input('Введите имя (Player1): ')
            player2_name = input('Введите имя (Player2): ')

            if player1_name == '': player1_name = 'Player1'
            if player2_name == '': player2_name = 'Player2'

            choise = int(input('Выберите способ расстановки кораблей\n1. Руками\n2. Рандомно\nВыбор: '))

            size = [10, 10]
            board = Board(size[0], size[1])
            player1 = Player(player1_name, size[0], size[1])
            player2 = Player(player2_name, size[0], size[1])
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

if __name__ == '__main__':
    import string, random, sys, os

    def cont(): return input('Введите символ чтобы продолжить')
    def clear():
        if sys.platform.startswith('win'):
            return os.system('cls')
        else:
            return os.system('clear')

    game = Game()
    game.startGame()
    input('Конец игры!')

