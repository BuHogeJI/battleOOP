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
        self.win = False

    def setShip(self):

        def modCoords(coords):
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

        def checkCoord(coord):
            if coord[0] > self.y or coord[1] > self.x or coord[0] < 0 or coord[1] < 0:
                return False

            for ship in self.ships:
                if coord in ship or [coord[0] - 1, coord[1]] in ship or [coord[0], coord[1] - 1] in ship or [coord[0] - 1, coord[1] - 1] in ship or [coord[0] + 1, coord[1]] in ship or [coord[0], coord[1] + 1] in ship or [coord[0] + 1, coord[1] + 1] in ship:
                    return False
            return True

        def getShip(coords):
            ship = []
            if len(coords) > 1:
                for i in range(len(coords) - 1):
                    if coords[i][0] + 1 != coords[i+1][0] or coords[i][0] - 1 != coords[i+1][0] or coords[i][1] + 1 != coords[i+1][1] or coords[i][1] - 1 != coords[i+1][1]:
                        print('Нельзя разрывать корабль!')
                        cont()
                        return False
            for coord in coords:
                if checkCoord(coord):
                    ship.append(coord)
                else:
                    print('В выбранные координаты нельзя поставить корабль!')
                    cont()
                    return False

            return ship

        size = int(input('Выберите размер корабля\n1. 1-палубный\n2. 2-палубный\n3. 3-палубный\n4. 4-палубный\n\nВыбор: '))
        if size == 1:
            if size in self.choosen:
                return False
            self.choosen.append(size)
            print('Необходимо ввести 4 1-палубных корабля')
            for _ in range(4):
                coords = input('Введите координаты (пример: a-1): ')
                coords = [coords]
                coords = modCoords(coords)
                print(coords)
                if getShip(coords) != False:
                    ship = getShip(coords)
                    self.ships.append(ship)
                else:
                    return False

        elif size == 2:
            if size in self.choosen:
                return False
            self.choosen.append(size)
            print('Необходимо ввести 3 2-палубных корабля')
            for _ in range(3):
                coords = input('Введите координаты (пример: a-1;a-2): ').split(';')
                coords = modCoords(coords)
                if getShip(coords) != False:
                    ship = getShip(coords)
                    self.ships.append(ship)
                else:
                    return False

        elif size == 3:
            if size in self.choosen:
                return False
            self.choosen.append(size)
            print('Необходимо ввести 2 3-палубных корабля')
            for _ in range(2):
                coords = input('Введите координаты (пример: a-1;a-2;a-3): ').split(';')
                coords = modCoords(coords)
                if getShip(coords) != False:
                    ship = getShip(coords)
                    self.ships.append(ship)
                else:
                    return False

        elif size == 4:
            if size in self.choosen:
                return False
            self.choosen.append(size)
            print('Необходимо ввести 1 4-палубный корабль')
            coords = input('Введите координаты (пример: a-1;a-2;a-3;a-4): ').split(';')
            coords = modCoords(coords)
            if getShip(coords) != False:
                ship = getShip(coords)
                self.ships.append(ship)
            else:
                return False

    def getMove(self, enemy):
        clear()
        self.printBoard()
        move = input('Ход игрока {} (пример ввода: а-1): '.format(self.name)).split('-')
        try:
            move[1] = int(move[1]) - 1
        except ValueError:
            print('Неверный ввод!')
            cont()
            return False

        if len(move) < 2 or len(move[0]) > 1 or move[1] > 26 or move[0] not in string.ascii_letters or move[1] < 0:
            print('Неверный ввод!')
            cont()
            return False

        i = 0
        for letter in string.ascii_letters:
            if move[0] == letter:
                move[0] = i
                break
            i += 1

        if int(move[1]) > self.x or int(move[0]) - 1 > self.y:
            print('Вы вышли за границу поля')
            cont()
            return False

        else:
            for ship in enemy.ships:
                if move in ship:
                    print('Попал')
                    enemy.changeBoardHit(move[0], move[1])
                    self.enemy_board[move[0]][move[1]] = 'X'
                    self.getMove(enemy)

            else:
                self.enemy_board[move[0]][move[1]] = '*'
                enemy.changeBoardMiss(move[0], move[1])
                print('Мимо')

class Game():

    def setPlayers(self):
        try:
            num_of_players = int(input('Введите количество игроков (1/2): '))
        except ValueError:
            print('Введите число!')
            cont()
        if num_of_players < 1 or num_of_players > 2:
            print('Необходимо ввести число от 1 до 2!')
            cont()
            sys.exit()

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
                size = input('\nВведите размер доски (пример: 10х10): ').split('x')
                if size == '':
                    size = ['10', '10']

                elif len(size) != 2 or not size[0].isdigit() or not size[1].isdigit() or int(size[0]) > 26 or int(size[1]) > 26 or int(size[0]) <= 0 or int(size[1]) <= 0:
                    print('Неверный ввод!')
                    loop()

                board = Board(int(size[0]), int(size[1]))
                player1 = Player(player1_name, int(size[0]), int(size[1]))
                player2 = Player(player2_name, int(size[0]), int(size[1]))
                player1.setBoard()
                player1.setEnemyBoard()
                player2.setEnemyBoard()
                player2.setBoard()


                players = [player1, player2]
                for player in players:
                    for _ in range(2):
                        clear()
                        print('Расстановка кораблей для {}'.format(player.name))
                        player.printBoard()
                        player.setShip()
                        for ship in player.ships:
                            player.changeBoardShip(ship)
                while True:
                    i = 1
                    for player in players:
                        player.getMove(players[i])
                        i -= 1



            loop()

        # 	size = input('Введите размер доски (пример: 10х10): ').split('x')
        # 	if len(size) != 2 or not size[0].isdigit() or not size[1].isdigit() or int(size[0]) > 26 or int(size[1]) > 26 or int(size[0]) <= 0 or int(size[1]) <= 0:
        # 		print('Неверный ввод!')
        # 		loop()

        # 	else:
        # 		players = self.setPlayers()
        # 		board = Board(int(size[0]), int(size[1]))
        # 		board.setBoard()
        # 		ship_col, ship_row = board.setShip()
        # 		done = False
        # 		while not done:
        # 			for name in players:

        # 					clear()
        # 					board.printBoard()
        # 					player = Player(name, int(size[0]), int(size[1]))
        # 					try:
        # 						row, col = player.getMove(ship_row, ship_col)
        # 					except TypeError:
        # 						main()

        # 					if player.status == True:
        # 						board.changeBoardWin(row, col)
        # 						board.printBoard()
        # 						print('\n...Конец игры...')
        # 						cont()
        # 						done = True
        # 						sys.exit()
        # 					else:
        # 						clear()
        # 						board.changeBoardMiss(row, col)
        # 						board.printBoard()
        # 						print('\nПромах!')
        # 						cont()
        # 				main()
        # loop()
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

