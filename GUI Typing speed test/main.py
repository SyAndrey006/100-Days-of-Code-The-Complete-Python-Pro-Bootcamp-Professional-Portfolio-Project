import tkinter as tk
import time
import random

word_list = ["cat", "dog", "car", "sun", "pen", "hat", "box", "red", "blue", "tree","book", "fish", "milk", "egg", "cup", "ball", "house", "rain", "run", "bird"]

def generate_text(num_words=20):
    return random.sample(word_list, num_words) if num_words <= len(word_list) else \
           [random.choice(word_list) for _ in range(num_words)]

class TypingSpeedTest:
    def __init__(self, root):
        self.root = root
        self.root.title("Typing Speed Test")
        self.root.geometry("500x250")

        self.words = generate_text()
        self.word_index = 0
        self.correct = 0
        self.start_time = None

        self.label_instructions = tk.Label(root, text="Type the words below (press SPACE after each word):",font=("Arial", 14))
        self.label_instructions.pack(pady=10)

        self.text_display = tk.Text( root, width=30, height=3, font=("Arial", 16), wrap="word", bg=self.root.cget("bg"), bd=0, highlightthickness=0)
        self.text_display.pack(pady=10)
        self.text_display.tag_configure("center", justify="center")
        self.text_display.config(state="disabled", cursor="arrow")

        self.entry = tk.Entry(root, width=20, font=("Arial", 14))
        self.entry.pack(pady=10)
        self.entry.bind("<space>", self.check_word)

        self.result_label = tk.Label(root, text="", font=("Arial", 14))
        self.result_label.pack(pady=10)

        self.update_highlight()

    def update_highlight(self):
        self.text_display.config(state="normal")
        self.text_display.delete("1.0", tk.END)

        for i, word in enumerate(self.words):
            if i == self.word_index:
                self.text_display.insert(tk.END, word + " ", "highlight")
            else:
                self.text_display.insert(tk.END, word + " ")

        self.text_display.tag_config("highlight", foreground="green", font=("Arial", 16, "bold"))
        self.text_display.tag_add("center", "1.0", "end")
        self.text_display.config(state="disabled")

    def check_word(self, event=None):
        if self.start_time is None:
            self.start_time = time.time()

        typed_word = self.entry.get().strip()
        self.entry.delete(0, tk.END)

        if typed_word == self.words[self.word_index]:
            self.correct += 1

        self.word_index += 1

        if self.word_index >= len(self.words):
            self.show_result()
        else:
            self.update_highlight()

    def show_result(self):
        end_time = time.time()
        time_taken = end_time - self.start_time
        words_per_minute = round((self.word_index / time_taken) * 60)
        accuracy = round((self.correct / self.word_index) * 100)

        self.result_label.config(text=f"Speed: {words_per_minute} WPM | Accuracy: {accuracy}%")

        self.entry.config(state="disabled")


if __name__ == "__main__":
    root = tk.Tk()
    app = TypingSpeedTest(root)
    root.mainloop()
