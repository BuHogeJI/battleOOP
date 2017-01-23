class Board():

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def setBoard(self):
        self.board = [['#'] * self.y for _ in range(self.x)]
        return self.board

    def setEnemyBoard(self):
        self.enemy_board = [['#'] * self.y for _ in range(self.x)]
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
        self.status = False

    def modCoords(self, coords):
            res = []
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

    def setShip(self):

        def checkCoord(coord):
            if coord[0] > self.y or coord[1] > self.x or coord[0] < 0 or coord[1] < 0:
                return False

            for ship in self.ships:
                if coord in ship or [coord[0] - 1, coord[1]] in ship or [coord[0], coord[1] - 1] in ship or \
                                    [coord[0] - 1, coord[1] - 1] in ship or [coord[0] + 1, coord[1]] in ship or \
                                    [coord[0], coord[1] + 1] in ship or [coord[0] + 1, coord[1] + 1] in ship or \
                                    [coord[0] + 1, coord[1] - 1] in ship or [coord[0] - 1, coord[1] + 1] in ship:
                    return False
            return True

        def getShip(coords):
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
                if checkCoord(coord):
                    ship.append(coord)
                else:
                    return False

            return ship

        def addShip(size):
            self.choosen.append(size)
            i = 0
            for ship in self.ships:
                if len(ship) == size:
                    i += 1
            print('Необходимо добавить {} {}-палубных корабля'.format(5-size - i,  size))
            cont()
            for _ in range(5-size - i):
                clear()
                self.printBoard()
                if size == 1:
                    coords = [input('Введите координаты: ')]
                    coords = self.modCoords(coords)
                else:
                    coords = input('Введите координаты: ').split(';')
                    coords = self.modCoords(coords)
                if getShip(coords) != False:
                    ship = getShip(coords)
                    self.ships.append(ship)
                    self.changeBoardShip(ship)
                    clear()
                    self.printBoard()
                else:
                    print('В выбранные координаты нельзя поставить корабль!')
                    self.choosen.remove(size)
                    return addShip(size)

        size = int(input('Выберите размер корабля\n1. 1-палубный\n2. 2-палубный\n3. 3-палубный\n4. 4-палубный\n\nВыбор: '))
        if size in self.choosen:
                print('Кораблей данной категории больше нет!')
                return self.setShip()
        addShip(size)

    def getMove(self, enemy):
        clear()
        self.printBoard()
        move = [input('Ход игрока {} (пример ввода: а-1): '.format(self.name))]
        move = self.modCoords(move)[0]

        if int(move[1]) > self.x or int(move[0]) > self.y:
            print('Вы вышли за границу поля')
            return self.getMove(enemy)

        else:
            for ship in enemy.ships:
                if move in ship:
                    enemy.changeBoardHit(move[1], move[0])
                    self.enemy_board[move[1]][move[0]] = 'X'
                    ship.remove(move)
                    if len(ship) == 0:
                        print('\nУБИЛ!!!')
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
        return int(num_of_players)

    def startGame(self):
        clear()
        num_of_players = self.setPlayers()
        if num_of_players == 1:
            def loop():
                size = input('Введите размер доски (пример: 10х10): ').split('x')
                if len(size) != 2 or not size[0].isdigit() or not size[1].isdigit() or int(size[0]) > 26 or int(size[1]) > 26 or int(size[0]) <= 0 or int(size[1]) <= 0:
                    print('Неверный ввод!')
                    loop()
                else:
                    pass

        elif num_of_players == 2:
            player1_name = input('Введите имя (Player1): ')
            player2_name = input('Введите имя (Player2): ')

            if player1_name == '':
                player1_name = 'Player1'
            if player2_name == '':
                player2_name = 'Player2'

            def loop():
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
                for player in players:
                    clear()
                    for _ in range(2):
                        print('Расстановка кораблей для {}\n'.format(player.name))
                        if player.setShip() == False:
                            cont()
                    else:
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
                            print('\nПобедил {}'.format(player.name))
            loop()

if __name__ == '__main__':
    import string, sys, os

    def cont(): return input('\n.....Введите символ чтобы продолжить.....')
    def clear():
        if sys.platform.startswith('win'):
            return os.system('cls')
        else:
            return os.system('clear')

    game = Game()
    game.startGame()
    input('\nКонец игры!')

