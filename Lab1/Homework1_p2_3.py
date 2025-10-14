import tkinter as tk
from tkinter import messagebox, scrolledtext
from nltk.corpus import wordnet as wn


# ============================================
# WORDNET FUNCTIONS
# ============================================

def check_synonym(word1, word2):
    for synset in wn.synsets(word1):
        for lemma in synset.lemmas():
            if lemma.name().lower() == word2.lower():
                return True
    return False


def check_hypernym(word1, word2):
    for synset in wn.synsets(word1):
        for hyper in synset.hypernyms():
            for lemma in hyper.lemmas():
                if lemma.name().lower() == word2.lower():
                    return True
    return False


def check_hyponym(word1, word2):
    for synset in wn.synsets(word1):
        for hypo in synset.hyponyms():
            for lemma in hypo.lemmas():
                if lemma.name().lower() == word2.lower():
                    return True
    return False


def check_antonym(word1, word2):
    for synset in wn.synsets(word1):
        for lemma in synset.lemmas():
            for ant in lemma.antonyms():
                if ant.name().lower() == word2.lower():
                    return True
    return False


def calculate_similarity(word1, word2):
    synsets1 = wn.synsets(word1)
    synsets2 = wn.synsets(word2)

    if not synsets1 or not synsets2:
        return 0.0

    max_similarity = 0.0
    for s1 in synsets1:
        for s2 in synsets2:
            sim = s1.path_similarity(s2)
            if sim and sim > max_similarity:
                max_similarity = sim

    return max_similarity


def get_feedback(similarity):
    if similarity >= 0.9:
        return "🔥 Extremely good connection"
    elif similarity >= 0.7:
        return "🎯 Very good connection!"
    elif similarity >= 0.5:
        return "👍 Good connection!"
    elif similarity >= 0.3:
        return "🤔 Some connection"
    elif similarity >= 0.1:
        return "😐 Weak connection"
    else:
        return "❌ Very distant"


def calculate_points(similarity, relations):
    base_points = int(similarity * 100) - 25

    bonus = 0
    if relations['synonym']:
        bonus += 50
    if relations['hypernym']:
        bonus += 30
    if relations['hyponym']:
        bonus += 30
    if relations['antonym']:
        bonus += 20

    return base_points + bonus


# ============================================
# GUI CLASS
# ============================================

class WordAssociationGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Word Association Game")
        self.root.geometry("700x600")
        self.root.configure(bg="#1a1a1a")

        self.target_word = None
        self.total_score = 0
        self.guesses = 0
        self.guessed_words = set()

        self.create_widgets()

    def create_widgets(self):
        # Title
        title_frame = tk.Frame(self.root, bg="#0d0d0d", pady=15)
        title_frame.pack(fill=tk.X)

        title = tk.Label(title_frame, text="🎮 Word Association Game 🎮",
                         font=("Arial", 20, "bold"), bg="#0d0d0d", fg="#ff8c00")
        title.pack()

        # Instructions
        instructions = tk.Label(self.root,
                                text="Enter a target word and start guessing related words!",
                                font=("Arial", 11), bg="#1a1a1a", fg="#cccccc")
        instructions.pack(pady=10)

        # Target Word Frame
        target_frame = tk.Frame(self.root, bg="#1a1a1a")
        target_frame.pack(pady=10)

        tk.Label(target_frame, text="Target Word:", font=("Arial", 12, "bold"),
                 bg="#1a1a1a", fg="#ff8c00").grid(row=0, column=0, padx=5)

        self.target_entry = tk.Entry(target_frame, font=("Arial", 12), width=20,
                                     bg="#2d2d2d", fg="#ffffff", insertbackground="#ff8c00")
        self.target_entry.grid(row=0, column=1, padx=5)

        self.start_btn = tk.Button(target_frame, text="Start Game",
                                   command=self.start_game,
                                   font=("Arial", 11, "bold"),
                                   bg="#ff8c00", fg="#000000",
                                   padx=10, pady=5, cursor="hand2",
                                   activebackground="#ffa500")
        self.start_btn.grid(row=0, column=2, padx=5)

        # Score Frame
        score_frame = tk.Frame(self.root, bg="#2d2d2d", relief=tk.RAISED, borderwidth=2)
        score_frame.pack(pady=10, padx=20, fill=tk.X)

        self.score_label = tk.Label(score_frame, text="Score: 0 | Guesses: 0",
                                    font=("Arial", 14, "bold"), bg="#2d2d2d", fg="#ff8c00")
        self.score_label.pack(pady=10)

        # Guess Frame
        guess_frame = tk.Frame(self.root, bg="#1a1a1a")
        guess_frame.pack(pady=10)

        tk.Label(guess_frame, text="Your Guess:", font=("Arial", 12, "bold"),
                 bg="#1a1a1a", fg="#ff8c00").grid(row=0, column=0, padx=5)

        self.guess_entry = tk.Entry(guess_frame, font=("Arial", 12), width=20,
                                    bg="#2d2d2d", fg="#ffffff", insertbackground="#ff8c00",
                                    state=tk.DISABLED)
        self.guess_entry.grid(row=0, column=1, padx=5)
        self.guess_entry.bind('<Return>', lambda e: self.submit_guess())

        self.submit_btn = tk.Button(guess_frame, text="Submit",
                                    command=self.submit_guess,
                                    font=("Arial", 11, "bold"),
                                    bg="#ff6600", fg="#000000",
                                    padx=15, pady=5, state=tk.DISABLED,
                                    cursor="hand2", activebackground="#ff7700")
        self.submit_btn.grid(row=0, column=2, padx=5)

        # Feedback Area
        feedback_label = tk.Label(self.root, text="Feedback:",
                                  font=("Arial", 12, "bold"), bg="#1a1a1a", fg="#ff8c00")
        feedback_label.pack(pady=(15, 5))

        self.feedback_text = scrolledtext.ScrolledText(self.root,
                                                       font=("Courier", 10),
                                                       height=15, width=70,
                                                       bg="#0d0d0d", fg="#e0e0e0",
                                                       insertbackground="#ff8c00",
                                                       state=tk.DISABLED)
        self.feedback_text.pack(pady=5, padx=20)

        # Buttons Frame
        button_frame = tk.Frame(self.root, bg="#1a1a1a")
        button_frame.pack(pady=15)

        self.new_word_btn = tk.Button(button_frame, text="New Word",
                                      command=self.new_word,
                                      font=("Arial", 11),
                                      bg="#ff8c00", fg="#000000",
                                      padx=15, pady=5, state=tk.DISABLED,
                                      cursor="hand2", activebackground="#ffa500")
        self.new_word_btn.grid(row=0, column=0, padx=5)

        self.quit_btn = tk.Button(button_frame, text="Quit Game",
                                  command=self.quit_game,
                                  font=("Arial", 11),
                                  bg="#cc5500", fg="#ffffff",
                                  padx=15, pady=5, cursor="hand2",
                                  activebackground="#dd6600")
        self.quit_btn.grid(row=0, column=1, padx=5)

    def start_game(self):
        target = self.target_entry.get().strip().lower()

        if not target:
            messagebox.showwarning("Input Required", "Please enter a target word!")
            return

        if not wn.synsets(target):
            messagebox.showerror("Invalid Word",
                                 f"'{target}' not found in WordNet. Try another word.")
            return

        self.target_word = target
        self.total_score = 0
        self.guesses = 0
        self.guessed_words = set()

        self.target_entry.config(state=tk.DISABLED)
        self.start_btn.config(state=tk.DISABLED)
        self.guess_entry.config(state=tk.NORMAL)
        self.submit_btn.config(state=tk.NORMAL)
        self.new_word_btn.config(state=tk.NORMAL)

        self.update_score()
        self.add_feedback(f"🎯 TARGET WORD: {self.target_word.upper()}\n")
        self.add_feedback("=" * 60 + "\n")
        self.add_feedback("Start guessing related words!\n\n")

        self.guess_entry.focus()

    def submit_guess(self):
        if not self.target_word:
            return

        guess = self.guess_entry.get().strip().lower()
        self.guess_entry.delete(0, tk.END)

        if not guess:
            return

        if guess == self.target_word:
            messagebox.showinfo("Same Word",
                                "That's the target word itself! Try something related.")
            return

        if not wn.synsets(guess):
            messagebox.showwarning("Invalid Word",
                                   f"'{guess}' not found in WordNet. Try another word.")
            return

        if guess in self.guessed_words:
            messagebox.showinfo("Already Guessed",
                                f"'{guess}' already guessed. Try another word.")
            return

        self.guessed_words.add(guess)
        self.guesses += 1

        # Calculate
        similarity = calculate_similarity(self.target_word, guess)
        relations = {
            'synonym': check_synonym(self.target_word, guess),
            'hypernym': check_hypernym(self.target_word, guess),
            'hyponym': check_hyponym(self.target_word, guess),
            'antonym': check_antonym(self.target_word, guess)
        }
        points = calculate_points(similarity, relations)
        self.total_score += points

        # Display feedback
        self.add_feedback(f"Guess #{self.guesses}: {guess.upper()}\n", bold=True)
        self.add_feedback(f"  Similarity: {similarity:.3f} - {get_feedback(similarity)}\n")

        if relations['synonym']:
            self.add_feedback("  ✓ SYNONYM (+50 bonus)\n", color="green")
        if relations['hypernym']:
            self.add_feedback("  ✓ HYPERNYM (+30 bonus)\n", color="green")
        if relations['hyponym']:
            self.add_feedback("  ✓ HYPONYM (+30 bonus)\n", color="green")
        if relations['antonym']:
            self.add_feedback("  ✓ ANTONYM (+20 bonus)\n", color="green")

        if not any(relations.values()):
            self.add_feedback("  ⚬ No direct relation found\n")

        if points > 0:
            self.add_feedback(f"  Points earned: +{points}\n", color="blue")
        elif points < 0:
            self.add_feedback(f"  Points lost: {points}\n", color="red")
        else:
            self.add_feedback(f"  No points change\n")

        self.add_feedback("\n")
        self.update_score()

    def add_feedback(self, text, bold=False, color=None):
        self.feedback_text.config(state=tk.NORMAL)

        if bold:
            self.feedback_text.insert(tk.END, text, "bold")
            self.feedback_text.tag_config("bold", font=("Courier", 10, "bold"), foreground="#ff8c00")
        elif color:
            self.feedback_text.insert(tk.END, text, color)
            if color == "green":
                self.feedback_text.tag_config("green", foreground="#00ff7f")
            elif color == "blue":
                self.feedback_text.tag_config("blue", foreground="#00bfff")
            elif color == "red":
                self.feedback_text.tag_config("red", foreground="#ff6347")
        else:
            self.feedback_text.insert(tk.END, text)

        self.feedback_text.see(tk.END)
        self.feedback_text.config(state=tk.DISABLED)

    def update_score(self):
        self.score_label.config(text=f"Score: {self.total_score} | Guesses: {self.guesses}")

    def new_word(self):
        if messagebox.askyesno("New Word",
                               f"Start a new game?\nCurrent score: {self.total_score}"):
            self.target_entry.config(state=tk.NORMAL)
            self.target_entry.delete(0, tk.END)
            self.start_btn.config(state=tk.NORMAL)
            self.guess_entry.config(state=tk.DISABLED)
            self.submit_btn.config(state=tk.DISABLED)
            self.new_word_btn.config(state=tk.DISABLED)

            self.feedback_text.config(state=tk.NORMAL)
            self.feedback_text.delete(1.0, tk.END)
            self.feedback_text.config(state=tk.DISABLED)

            self.target_word = None
            self.total_score = 0
            self.guesses = 0
            self.guessed_words = set()
            self.update_score()

    def quit_game(self):
        if messagebox.askyesno("Quit", "Are you sure you want to quit?"):
            self.root.destroy()


# ============================================
# MAIN
# ============================================

if __name__ == "__main__":
    root = tk.Tk()
    app = WordAssociationGame(root)
    root.mainloop()