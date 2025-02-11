import tkinter as tk
from tkinter import messagebox


class TicTacToeGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Крестики-нолики")
        self.master.geometry("350x450")
        self.master.resizable(False, False)

        # Инициализация игровых переменных
        self.player_choice = None  # Выбор игрока (X или 0)
        self.current_player = None  # Текущий ход
        self.move_count = 0  # Счётчик заполненных клеток в раунде
        self.score = {"X": 0, "0": 0}  # Счёт побед для каждого игрока
        self.buttons = []  # Список кнопок игрового поля

        # Создаём виджеты
        self.create_widgets()
        # Перед началом игры предлагаем выбрать, за кого играть
        self.ask_player_choice()
        # Начинаем первый раунд
        self.new_round()

    def create_widgets(self):
        # Фрейм для счётчика побед
        self.score_frame = tk.Frame(self.master)
        self.score_frame.pack(pady=10)
        self.label_score = tk.Label(
            self.score_frame,
            text="Score X: 0   Score 0: 0",
            font=("Arial", 14)
        )
        self.label_score.pack()

        # Метка для отображения, чей ход
        self.turn_label = tk.Label(
            self.master,
            text="Ход: ",
            font=("Arial", 14)
        )
        self.turn_label.pack(pady=5)

        # Фрейм для игрового поля
        self.board_frame = tk.Frame(self.master)
        self.board_frame.pack()
        for i in range(3):
            row_buttons = []
            for j in range(3):
                btn = tk.Button(
                    self.board_frame,
                    text="",
                    font=("Arial", 20),
                    width=5,
                    height=2,
                    command=lambda r=i, c=j: self.on_click(r, c)
                )
                btn.grid(row=i, column=j)
                row_buttons.append(btn)
            self.buttons.append(row_buttons)

        # Кнопка для сброса всей игры (сброс поля и счётчиков)
        self.reset_button = tk.Button(
            self.master,
            text="Сброс игры",
            font=("Arial", 14),
            command=self.reset_game
        )
        self.reset_button.pack(pady=10)

    def ask_player_choice(self):
        """
        Открываем небольшое окно, где игрок выбирает, чем играть:
        X или 0. Выбор определяет, кто ходит первым.
        """
        choice_window = tk.Toplevel(self.master)
        choice_window.title("Выбор игрока")
        tk.Label(
            choice_window,
            text="Выберите, чем вы будете играть:",
            font=("Arial", 12)
        ).pack(padx=20, pady=10)

        def choose_x():
            self.player_choice = "X"
            self.current_player = "X"  # Игрок, выбравший X, ходит первым
            self.turn_label.config(text="Ход: X")
            choice_window.destroy()

        def choose_o():
            self.player_choice = "0"
            self.current_player = "0"  # Если выбрали 0, то первый ход у 0
            self.turn_label.config(text="Ход: 0")
            choice_window.destroy()

        btn_x = tk.Button(choice_window, text="X", font=("Arial", 14), width=5, command=choose_x)
        btn_x.pack(side=tk.LEFT, padx=10, pady=10)
        btn_o = tk.Button(choice_window, text="0", font=("Arial", 14), width=5, command=choose_o)
        btn_o.pack(side=tk.RIGHT, padx=10, pady=10)

        # Ожидаем, пока окно выбора не будет закрыто
        self.master.wait_window(choice_window)

    def on_click(self, row, col):
        """
        Обработка клика по кнопке игрового поля.
        Если клетка пуста, ставим символ текущего игрока, увеличиваем счётчик ходов,
        затем проверяем наличие победителя или ничьей.
        """
        if self.buttons[row][col]["text"] != "":
            return  # Клетка уже занята

        self.buttons[row][col]["text"] = self.current_player
        self.move_count += 1

        if self.check_winner():
            self.score[self.current_player] += 1
            self.update_score()
            messagebox.showinfo("Игра окончена", f"Игрок {self.current_player} победил!")
            if self.score[self.current_player] == 3:
                messagebox.showinfo("Игра окончена", f"Игрок {self.current_player} выиграл серию!")
                self.reset_game()  # Если один из игроков набрал 3 победы, сбрасываем игру
            else:
                self.new_round()
            return

        if self.move_count == 9:
            messagebox.showinfo("Игра окончена", "Ничья!")
            self.new_round()
            return

        # Переключаем ход
        self.current_player = "0" if self.current_player == "X" else "X"
        self.turn_label.config(text=f"Ход: {self.current_player}")

    def check_winner(self):
        """
        Проверяем строки, столбцы и диагонали на наличие трёх одинаковых символов (не пустых).
        """
        b = self.buttons
        # Проверка строк
        for i in range(3):
            if b[i][0]["text"] == b[i][1]["text"] == b[i][2]["text"] != "":
                return True
        # Проверка столбцов
        for j in range(3):
            if b[0][j]["text"] == b[1][j]["text"] == b[2][j]["text"] != "":
                return True
        # Проверка диагоналей
        if b[0][0]["text"] == b[1][1]["text"] == b[2][2]["text"] != "":
            return True
        if b[0][2]["text"] == b[1][1]["text"] == b[2][0]["text"] != "":
            return True
        return False

    def update_score(self):
        """Обновляем метку со счётчиком побед."""
        self.label_score.config(text=f"Score X: {self.score['X']}   Score 0: {self.score['0']}")

    def new_round(self):
        """
        Сбрасываем игровое поле (но не счётчики побед) и начинаем новый раунд.
        В данном примере для разнообразия очередность ходов меняется (альтернируется).
        """
        self.move_count = 0
        for row in self.buttons:
            for btn in row:
                btn.config(text="")
        # Меняем очередность: если предыдущий раунд завершился победой или ничьёй,
        # то в новом раунде начинает другой игрок.
        self.current_player = "0" if self.current_player == "X" else "X"
        self.turn_label.config(text=f"Ход: {self.current_player}")

    def reset_game(self):
        """
        Полный сброс игры: очищаем поле, сбрасываем счёт побед и начинаем новый раунд.
        """
        self.score = {"X": 0, "0": 0}
        self.update_score()
        self.new_round()


if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToeGame(root)
    root.mainloop()
