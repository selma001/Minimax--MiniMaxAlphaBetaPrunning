from math import inf
import pygame
import time

MAX = +1 
MIN = -1

class Play:
    
    @staticmethod
    def minimax(node, depth, player=MAX, visualize=False):
        if depth == 0 or (node.leftChild is None and node.rightChild is None):
            node.visited = True  # visited leafs
            return node.value

        if visualize:
            node.visited = True
            node.display(active=True)
            pygame.display.update()
            time.sleep(0.5)

        if player == MAX:
            node.value = -inf
            if node.leftChild:
                child = node.leftChild
                node.value = max(node.value, Play.minimax(child, depth - 1, -player, visualize))
                child.chosen = node.value == child.value  # Set chosen attribute
                node.path = child
            if node.rightChild:
                child = node.rightChild
                node.value = max(node.value, Play.minimax(child, depth - 1, -player, visualize))
                child.chosen = node.value == child.value  # Set chosen attribute
                node.path = child
            pygame.draw.line(screen, (255,0,0), node.position,
                    (node.path.position[0], node.path.position[1]), 3)

        else:  # player == MIN
            node.value = inf
            if node.leftChild:
                child = node.leftChild
                node.value = min(node.value, Play.minimax(child, depth - 1, -player, visualize))
                child.chosen = node.value == child.value  # Set chosen attribute
                node.path = child
                pygame.draw.line(screen, (255,0,0), node.position,
                                 (node.path.position[0], node.path.position[1]), 3)
            if node.rightChild:
                child = node.rightChild
                node.value = min(node.value, Play.minimax(child, depth - 1, -player, visualize))
                child.chosen = node.value == child.value  # Set chosen attribute
                node.path = child
                pygame.draw.line(screen, (255,0,0), node.position,
                                 (node.path.position[0], node.path.position[1]), 3)

        

        if visualize:
            node.display(active=False)
            pygame.display.update()
            time.sleep(0.5)

        return node.value       

    # ... (previous code)

    @staticmethod
    def minimaxAlphaBetaPruning(node, depth, alpha=-inf, beta=+inf, player=MAX, visualize=False):
        if depth == 0 or (node.leftChild is None and node.rightChild is None):
            node.visited = True
            return node.value

        if visualize:
            node.visited = True
            node.display(active=True)
            pygame.display.update()
            time.sleep(0.5)

        font = pygame.font.Font(None, 15)
        text = font.render(f"alpha: {alpha}", True, (0, 0, 0))
        text_rect = text.get_rect(center=(node.position[0] - 50, node.position[1] + 10))
        screen.blit(text, text_rect)
        text = font.render(f"beta: {beta}", True, (0, 0, 0))
        text_rect = text.get_rect(center=(node.position[0] + 50, node.position[1] + 10))
        screen.blit(text, text_rect)
        pygame.display.update()
        time.sleep(0.5)

        if player == MAX:
            node.value = -inf
            if node.leftChild:
                child = node.leftChild
                node.value = max(node.value, Play.minimaxAlphaBetaPruning(child, depth - 1, alpha, beta, -player, visualize))
                alpha = max(alpha, node.value)
                child.chosen = node.value == child.value 
                if alpha >= beta:
                    if visualize:
                        node.display(active=False)
                        pygame.display.update()
                        time.sleep(0.5)
                    return node.value  
            if node.rightChild:
                child = node.rightChild
                node.value = max(node.value, Play.minimaxAlphaBetaPruning(child, depth - 1, alpha, beta, -player, visualize))
                alpha = max(alpha, node.value)
                child.chosen = node.value == child.value 
                if alpha >= beta:
                    if visualize:
                        node.display(active=False)
                        pygame.display.update()
                        time.sleep(0.5)
                    return node.value  
            if visualize:
                node.display(active=False)
                pygame.display.update()
                time.sleep(0.5)
                return node.value
        else:  # player == MIN
            node.value = inf
            if node.leftChild:
                child = node.leftChild
                node.value = min(node.value, Play.minimaxAlphaBetaPruning(child, depth - 1, alpha, beta, -player, visualize))
                beta = min(beta, node.value)
                child.chosen = node.value == child.value 
                if alpha >= beta:
                    if visualize:
                        node.display(active=False)
                        pygame.display.update()
                        time.sleep(0.5)
                    return node.value  
            if node.rightChild:
                child = node.rightChild
                node.value = min(node.value, Play.minimaxAlphaBetaPruning(child, depth - 1, alpha, beta, -player, visualize))
                beta = min(beta, node.value)
                child.chosen = node.value == child.value 
                if alpha >= beta:
                    if visualize:
                        node.display(active=False)
                        pygame.display.update()
                        time.sleep(0.5)
                    return node.value  
            if visualize:
                node.display(active=False)
                pygame.display.update()
                time.sleep(0.5)
            return node.value

class Node:
    def __init__(self, parent=None, side=None, depth=0, value=None):
        self.parent = parent
        self.value = value
        self.path = None        
        self.leftChild = None
        self.rightChild = None
        self.depth = depth  
        self.visited = False  
        self.alpha = None
        self.beta = None
        self.chosen = False 

        if self.parent is None:
            self.position = ((screen.get_width() / 2), (screen.get_height() / (2**depth + 2)))
            if value is None:
                self.value = -float('inf') if side == "L" else float('inf') 
        else:
            if side == "L":
                self.position = (self.parent.position[0] - 30 * (2**(depth-1)), self.parent.position[1] + 70)
            else:
                self.position = (self.parent.position[0] + 30 * (2**(depth-1)), self.parent.position[1] + 70)

    def display(self, visited_color=(11,11, 69), node_color=(64, 64, 64), line_color=(64, 64, 64), player=None, active=False, show_alpha_beta=False):
        triangle_size = 25

        if self.parent:
            orientation = -1 if self.depth % 2 == 0 else 1
        else:
            orientation = 1

        if self.leftChild:
            self.leftChild.display(visited_color, node_color, line_color, player, active)
            if active:
                pygame.draw.line(screen, line_color, self.position,
                                 (self.leftChild.position[0], self.leftChild.position[1]), 3)
        if self.rightChild:
            self.rightChild.display(visited_color, node_color, line_color, player, active)
            if active:
                pygame.draw.line(screen, line_color, self.position,
                                 (self.rightChild.position[0], self.rightChild.position[1]), 3)

        if self.visited:
            color = visited_color
        else:
            color = node_color

        if self.chosen:
            color = (255, 0, 0)
        pygame.draw.polygon(screen, color, [(self.position[0], self.position[1] - orientation * triangle_size),
                                            (self.position[0] - triangle_size, self.position[1] + orientation * triangle_size),
                                            (self.position[0] + triangle_size, self.position[1] + orientation * triangle_size)])


        if self.value is not None:
            font = pygame.font.Font(None, 23)
            text = font.render(str(self.value), True, (255, 255, 255))
            screen.blit(text, (self.position[0] - 10, self.position[1] - 10))
        


class Tree:
    def __init__(self):
        self.root_node = Node(parent=None)

    def createEmptyTree(self, node, depth, values, index=[0]):
        if depth == 0:
            if index[0] < len(values):
                node.value = values[index[0]]
                index[0] += 1
            return

        if node.leftChild is None:
            node.leftChild = Node(parent=node, side="L", depth=depth, value=-float('inf'))
        self.createEmptyTree(node.leftChild, depth - 1, values, index)

        if node.rightChild is None:
            node.rightChild = Node(parent=node, side="R", depth=depth, value=float('inf'))
        self.createEmptyTree(node.rightChild, depth - 1, values, index)


    def drawTree(self, node, depth, player, show_alpha_beta=False):
        if node:
            node.display(node_color=(64, 64, 64), line_color=(64, 64, 64), player=player, show_alpha_beta=show_alpha_beta)
            self.drawTree(node.leftChild, depth - 1, player, show_alpha_beta)
            self.drawTree(node.rightChild, depth - 1, player, show_alpha_beta)



def display_text_screen():
    pygame.init()
    global screen, h, w
    w = 1200
    h = 750
    screen = pygame.display.set_mode(((w, h)))
    pygame.display.set_caption("MINIMAX")

    running = True

    font = pygame.font.Font(None, 36)
    text1 = font.render("Press 1 for Minimax", True, (0, 0, 0))
    text2 = font.render("Press 2 for Minimax with Alpha-Beta Pruning", True, (0, 0, 0))

    while running:
        screen.fill((192, 192, 192))
        screen.blit(text1, ((w - text1.get_width()) / 2, h / 2 - 50))
        screen.blit(text2, ((w - text2.get_width()) / 2, h / 2 + 50))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return "Minimax"
                elif event.key == pygame.K_2:
                    return "Minimax with Alpha-Beta Pruning"

    pygame.quit()


def main():
    algorithm = display_text_screen()

    if algorithm is None:
        return

    pygame.init()
    global screen, h, w
    w = 1200
    h = 750
    screen = pygame.display.set_mode(((w, h)))
    pygame.display.set_caption("MINIMAX / MINIMAX-ALPHA-BETA-PRUNNING")

    tree = Tree()
    values = [10, 5, 7, 11, 12, 8, 9, 8, 5, 12, 11, 12, 9, 8, 7, 10]
    depth = 4

    running = True
    draw = True

    while running:
        screen.fill((192, 192, 192))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if draw:
            tree.createEmptyTree(tree.root_node, depth, values)
            tree.drawTree(tree.root_node, depth, player=MAX, show_alpha_beta=True)
            pygame.display.update()
            draw = False

            if algorithm == "Minimax":
                result = Play.minimax(tree.root_node, depth, player=MAX, visualize=True)
                print(f"The value of the root node using Minimax is: {result}")
            elif algorithm == "Minimax with Alpha-Beta Pruning":
                result = Play.minimaxAlphaBetaPruning(tree.root_node, depth, player=MAX, visualize=True)
                print(f"The value of the root node using Minimax with Alpha-Beta Pruning is: {result}")

    pygame.quit()

if __name__ == "__main__":
    main()
