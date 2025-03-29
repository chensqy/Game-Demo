import tkinter as tk
import random


class SnakeGame:
    def __init__(self, master):
        self.master = master
        self.master.title("贪吃蛇游戏")
        self.master.resizable(False, False)

        # 游戏参数
        self.cell_size = 20
        self.width = 30
        self.height = 20
        self.canvas_width = self.width * self.cell_size
        self.canvas_height = self.height * self.cell_size

        # 创建画布
        self.canvas = tk.Canvas(master,
                                width=self.canvas_width,
                                height=self.canvas_height,
                                bg="white")
        self.canvas.pack()

        # 分数显示
        self.score_label = tk.Label(master, text="分数: 0", font=('Arial', 12))
        self.score_label.pack()

        # 初始化游戏
        self.reset_game()

        # 绑定键盘事件
        self.master.bind("<KeyPress>", self.on_key_press)

        # 开始游戏循环
        self.update()

    def reset_game(self):
        """重置游戏状态"""
        self.snake = [(10, 10), (9, 10), (8, 10)]  # 初始蛇身
        self.direction = (1, 0)  # 初始方向向右
        self.score = 0
        self.game_over = False
        self.place_food()
        self.update_score()

    def place_food(self):
        """随机放置食物"""
        while True:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            if (x, y) not in self.snake:
                self.food = (x, y)
                break

    def update_score(self):
        """更新分数显示"""
        self.score_label.config(text=f"分数: {self.score}")

    def on_key_press(self, event):
        """处理键盘输入"""
        key = event.keysym.lower()
        if key == 'w' and self.direction != (0, 1):
            self.direction = (0, -1)
        elif key == 's' and self.direction != (0, -1):
            self.direction = (0, 1)
        elif key == 'a' and self.direction != (1, 0):
            self.direction = (-1, 0)
        elif key == 'd' and self.direction != (-1, 0):
            self.direction = (1, 0)
        elif key == 'r' and self.game_over:
            self.reset_game()

    def move_snake(self):
        """移动蛇"""
        if self.game_over:
            return

        # 计算新头部位置
        head_x, head_y = self.snake[0]
        dir_x, dir_y = self.direction
        new_head = ((head_x + dir_x) % self.width, (head_y + dir_y) % self.height)

        # 检查是否撞到自己
        if new_head in self.snake:
            self.game_over = True
            return

        # 添加新头部
        self.snake.insert(0, new_head)

        # 检查是否吃到食物
        if new_head == self.food:
            self.score += 1
            self.update_score()
            self.place_food()
        else:
            # 如果没有吃到食物，移除尾部
            self.snake.pop()

    def draw(self):
        """绘制游戏画面"""
        self.canvas.delete("all")

        # 绘制网格
        for x in range(0, self.canvas_width, self.cell_size):
            self.canvas.create_line(x, 0, x, self.canvas_height, fill="lightgray")
        for y in range(0, self.canvas_height, self.cell_size):
            self.canvas.create_line(0, y, self.canvas_width, y, fill="lightgray")

        # 绘制蛇
        for segment in self.snake:
            x, y = segment
            self.canvas.create_rectangle(
                x * self.cell_size, y * self.cell_size,
                (x + 1) * self.cell_size, (y + 1) * self.cell_size,
                fill="green", outline="black"
            )

        # 绘制食物
        food_x, food_y = self.food
        self.canvas.create_oval(
            food_x * self.cell_size, food_y * self.cell_size,
            (food_x + 1) * self.cell_size, (food_y + 1) * self.cell_size,
            fill="red", outline="black"
        )

        # 游戏结束显示
        if self.game_over:
            self.canvas.create_text(
                self.canvas_width // 2, self.canvas_height // 2,
                text="游戏结束! 按R键重新开始",
                font=('Arial', 16), fill="red"
            )

    def update(self):
        """游戏更新循环"""
        self.move_snake()
        self.draw()

        # 设置下一次更新
        if not self.game_over:
            self.master.after(200, self.update)  # 每200毫秒更新一次


if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()