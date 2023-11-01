from queue import PriorityQueue
import pygame
import sys
class Node:
    def __init__(self, state, parent=None, move=None, depth=0, cost=0):
        self.state = state
        self.parent = parent
        self.move = move
        self.depth = depth
        self.cost = cost

    def __lt__(self, other):
        return self.cost < other.cost

    def __eq__(self, other):
        return self.state == other.state

class Puzzle:
    def __init__(self, initial_state, goal_state):
        self.initial_state = initial_state
        self.goal_state = goal_state

    def get_blank_pos(self, state):
        return state.index(0)

    def get_successors(self, state):
        successors = []
        blank_pos = self.get_blank_pos(state)

        if blank_pos not in [0, 1, 2]:
            new_state = state[:]
            new_state[blank_pos], new_state[blank_pos-3] = new_state[blank_pos-3], new_state[blank_pos]
            successors.append(Node(new_state))

        if blank_pos not in [0, 3, 6]:
            new_state = state[:]
            new_state[blank_pos], new_state[blank_pos-1] = new_state[blank_pos-1], new_state[blank_pos]
            successors.append(Node(new_state))

        if blank_pos not in [6, 7, 8]:
            new_state = state[:]
            new_state[blank_pos], new_state[blank_pos+3] = new_state[blank_pos+3], new_state[blank_pos]
            successors.append(Node(new_state))

        if blank_pos not in [2, 5, 8]:
            new_state = state[:]
            new_state[blank_pos], new_state[blank_pos+1] = new_state[blank_pos+1], new_state[blank_pos]
            successors.append(Node(new_state))

        return successors

    def manhattan_distance(self, state):
        distance = 0
        for i in range(9):
            if state[i] == 0:
                continue
            distance += abs(i % 3 - state[i] % 3) + abs(i // 3 - state[i] // 3)
        return distance

    def a_search(self):
        start_node = Node(self.initial_state)
        start_node.cost = self.manhattan_distance(start_node.state)
        frontier = PriorityQueue()
        frontier.put(start_node)

        explored = set()

        while not frontier.empty():
            current_node = frontier.get()

            if current_node.state == self.goal_state:
                path = []
                while current_node.parent is not None:
                    path.append(current_node.move)
                    current_node = current_node.parent
                path.reverse()
                return path

            explored.add(tuple(current_node.state))

            for successor in self.get_successors(current_node.state):
                if tuple(successor.state) not in explored:
                    successor.parent = current_node
                    successor.depth = current_node.depth + 1
                    successor.cost = self.manhattan_distance(successor.state)
                    successor.move = self.get_move(current_node.state, successor.state)
                    frontier.put(successor)

        return None

    def get_move(self, state1, state2):
        blank1 = self.get_blank_pos(state1)
        blank2 = self.get_blank_pos(state2)

        if blank2 == blank1 - 3:
            return '↑'
        elif blank2 == blank1 + 3:
            return '↓'
        elif blank2 == blank1 - 1:
            return '←'
        elif blank2 == blank1 + 1:
            return '→'

def PygameShow(Path, playSpeed=500):#老师如果需要加快运算速度可改playSpeed参数，单位是ms，可改成1ms迅速显示结果
    pygame.init()
    size = width, height = 300, 300
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("E02114057裴政-8数码问题")
    font = pygame.font.Font(None, 30)
    clock = pygame.time.Clock()
    tile_size = 100
    tile_margin = 5
    colors = [(255, 255, 255), (0, 0, 255)]
    tiles = []
    for i in range(9):
        tile = pygame.Surface((tile_size, tile_size))
        tile.fill(colors[i % 2])
        rect = tile.get_rect()
        col = i % 3
        row = i // 3
        rect.x = tile_margin + (tile_size + tile_margin) * col
        rect.y = tile_margin + (tile_size + tile_margin) * row
        tiles.append((tile, rect))
    for move in path:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        screen.fill((0, 0, 0))
        for i in range(9):
            if puzzle.initial_state[i] == 0:
                continue
            screen.blit(font.render(str(puzzle.initial_state[i]), True, (0, 0, 0)), tiles[i][1])
        pygame.display.flip()
        pygame.time.delay(playSpeed)
        blank_pos = puzzle.get_blank_pos(puzzle.initial_state)
        if move == '↑':
            puzzle.initial_state[blank_pos], puzzle.initial_state[blank_pos - 3] = puzzle.initial_state[
                blank_pos - 3], puzzle.initial_state[blank_pos]
        elif move == '↓':
            puzzle.initial_state[blank_pos], puzzle.initial_state[blank_pos + 3] = puzzle.initial_state[
                blank_pos + 3], puzzle.initial_state[blank_pos]
        elif move == '←':
            puzzle.initial_state[blank_pos], puzzle.initial_state[blank_pos - 1] = puzzle.initial_state[
                blank_pos - 1], puzzle.initial_state[blank_pos]
        elif move == '→':
            puzzle.initial_state[blank_pos], puzzle.initial_state[blank_pos + 1] = puzzle.initial_state[
                blank_pos + 1], puzzle.initial_state[blank_pos]
        for i in range(9):
            tile, rect = tiles[i]
            col = i % 3
            row = i // 3
            rect.x = tile_margin + (tile_size + tile_margin) * col
            rect.y = tile_margin + (tile_size + tile_margin) * row
            screen.blit(tile, rect)
            if puzzle.initial_state[i] == 0:
                continue
            screen.blit(font.render(str(puzzle.initial_state[i]), True, (0, 0, 0)), rect)
        pygame.display.flip()
        pygame.time.wait(1)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        screen.fill((0, 0, 0))
        for i in range(9):
            tile, rect = tiles[i]
            col = i % 3
            row = i // 3
            rect.x = tile_margin + (tile_size + tile_margin) * col
            rect.y = tile_margin + (tile_size + tile_margin) * row
            screen.blit(tile, rect)
            if puzzle.initial_state[i] == 0:
                continue
            screen.blit(font.render(str(puzzle.initial_state[i]), True, (0, 0, 0)), rect)
        pygame.display.flip()
        pygame.time.delay(playSpeed)
        clock.tick(60)

def GetInput():
    soltuion=input("请问是否采用案例输入？y/n")
    if soltuion=='y':
        initial_state = [2, 3, 1, 8, 0, 4, 7, 6, 5]
        goal_state = [1, 2, 3, 8, 0, 4, 7, 6, 5]
        print("起始状态: " + str(initial_state))
        print("终止状态; " + str(goal_state))
        return initial_state,goal_state
    elif soltuion=='n':
        initial_state= []
        for i in range(9):
            num = int(input("输入起始状态一个数字: "))
            initial_state.append(num)
        goal_state = []
        for i in range(9):
            num = int(input("输入终止状态一个数字: "))
            goal_state.append(num)
        print("起始状态: " + str(initial_state))
        print("终止状态; " + str(goal_state))
        return initial_state,goal_state
    else:
        print("您输入的不对！请重新输入:-)")

if __name__ == '__main__':
    initial_state,goal_state = GetInput()
    puzzle = Puzzle(initial_state, goal_state)
    path = puzzle.a_search()
    if path is None:
        print('没有找到解决方案')
    else:
        print('找到的解决方法需要移动', len(path), '步，这样移动:', path)

    PygameShow(path,1)
