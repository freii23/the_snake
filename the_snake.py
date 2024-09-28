from random import randint
import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки:
BORDER_COLOR = (93, 216, 228)

# Цвет яблока:
APPLE_COLOR = (255, 0, 0)

# Цвет гнилого яблока:
ROTTEN_COLOR = (63, 64, 57)

# Цвет змейки:
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """
    Базовый класс игрового объекта.
    """
    def __init__(self):
        self.position = (0, 0)
        self.body_color = (255, 0, 0)

    def draw(self):
        """
        Метод для отрисовки игрового объекта.
        Должен быть переопределен в дочерних классах.
        """
        pass


class Snake(GameObject):
    """
    Класс, описывающий змейку в игре.
    """
    def __init__(self):
        super().__init__()
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = SNAKE_COLOR
        self.last = None

    def update_direction(self):
        """
        Обновление направления движения змейки.
        Если указано новое направление, меняет его.
        """
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """
        Логика перемещения змейки.
        Обновляет позицию головы и проверяет столкновения.
        """
        new = self.get_head_pos()
        new_x_pos = new[0] + GRID_SIZE * self.direction[0]
        new_y_pos = new[1] + GRID_SIZE * self.direction[1]

        # Обработка выхода за границы поля (змейка появляется с противоположной стороны)
        if new_x_pos < 0:
            new_x_pos = SCREEN_WIDTH - GRID_SIZE
        elif new_x_pos >= SCREEN_WIDTH:
            new_x_pos = 0

        if new_y_pos < 0:
            new_y_pos = SCREEN_HEIGHT - GRID_SIZE
        elif new_y_pos >= SCREEN_HEIGHT:
            new_y_pos = 0

        # Проверка столкновения с телом змейки
        if (new_x_pos, new_y_pos) in self.positions[2:]:
            self.reset()
        else:
            self.positions.insert(0, (new_x_pos, new_y_pos))
            if len(self.positions) > self.length:
                self.positions.pop(-1)

    def draw(self):
        """
        Отрисовка змейки на экране.
        """
        for position in self.positions:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def get_head_pos(self):
        """
        Возвращает позицию головы змейки.
        :return: tuple - координаты головы
        """
        return self.positions[0]

    def reset(self):
        """
        Сброс состояния змейки (возвращение в начальное состояние).
        """
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = (randint(-1, 1), randint(-1, 1))

    def cut(self):
        """
        Уменьшение размеров змейки на 1 клетку, либо игра начинается сначала.
        """
        if self.length > 1:
            self.length -= 1
            self.positions.pop(-1)
        else:
            self.reset()   


class Apple(GameObject):
    """
    Класс, описывающий яблоко в игре.
    """
    def __init__(self):
        super().__init__()
        self.body_color = APPLE_COLOR
        self.position = self.randomize_position()

    def randomize_position(self):
        """
        Случайным образом задает новую позицию яблока на поле.
        :return: tuple - координаты новой позиции
        """
        return randint(0, GRID_WIDTH - 1) * GRID_SIZE, randint(0, GRID_HEIGHT - 1) * GRID_SIZE

    def draw(self):
        """
        Отрисовка яблока на экране.
        """
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

class Rotten(Apple):
    """
    Класс, описывающий гнилое яблоко в игре - наследник класса Apple.
    """
    def __init__(self):
        super().__init__()
        self.body_color = ROTTEN_COLOR

def handle_keys(snake):
    """
    Обработка ввода от пользователя и изменение направления движения змейки.
    :param snake: объект класса Snake
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake.direction != DOWN:
                snake.next_direction = UP
            elif event.key == pygame.K_DOWN and snake.direction != UP:
                snake.next_direction = DOWN
            elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                snake.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                snake.next_direction = RIGHT


def main():
    """
    Главная функция игры.
    Запускает игровой цикл, создавая объекты змейки и яблока.
    """
    pygame.init()
    snake = Snake()
    apple = Apple()
    rotten = Rotten()

    while True:
        clock.tick(SPEED)
        screen.fill(BOARD_BACKGROUND_COLOR)

        handle_keys(snake)
        snake.update_direction()
        snake.move()

        # Проверка на поедание яблока
        if apple.position in snake.positions:
            snake.length += 1
            apple.position = apple.randomize_position()

        # Проверка на поедание гнилого яблока
        if rotten.position in snake.positions:
            snake.cut()
            rotten.position = rotten.randomize_position()

        snake.draw()
        apple.draw()
        rotten.draw()

        pygame.display.update()


if __name__ == '__main__':
    main()