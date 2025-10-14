from nltk.corpus import wordnet as wn

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


def play_game():
    print("=" * 60)
    print("WORD ASSOCIATION GAME")
    print("=" * 60)
    print("\nGuess words related to the target word!")
    print("Type 'quit' to exit or 'new' for a new word.\n")

    target_word = input("Enter the target word: ").strip().lower()

    if not wn.synsets(target_word):
        print(f"Word '{target_word}' not found in WordNet. Try another word.")
        return

    print(f"\nTarget word: {target_word.upper()}")
    print("Start guessing related words!\n")

    total_score = 0
    guesses = 0
    guessed_words = set()

    while True:
        guess = input("Your guess: ").strip().lower()

        if guess == 'quit':
            print(f"\nGame Over! Final Score: {total_score} points from {guesses} guesses")
            break

        if guess == 'new':
            print(f"\nFinal Score for '{target_word}': {total_score} points from {guesses} guesses\n")
            play_game()
            return

        if guess == target_word:
            print("That's the target word itself! Try something related.\n")
            continue

        if not wn.synsets(guess):
            print(f"Word '{guess}' not found in WordNet. Try another word.\n")
            continue

        if guess in guessed_words:
            print(f"Word '{guess}' is already guessed. Try another word.\n")
            continue

        guessed_words.add(guess)

        guesses += 1

        similarity = calculate_similarity(target_word, guess)

        relations = {
            'synonym': check_synonym(target_word, guess),
            'hypernym': check_hypernym(target_word, guess),
            'hyponym': check_hyponym(target_word, guess),
            'antonym': check_antonym(target_word, guess)
        }

        points = calculate_points(similarity, relations)
        total_score += points

        print(f"\n  Similarity Score: {similarity:.3f}")
        print(f"  {get_feedback(similarity)}")

        relation_found = False
        if relations['synonym']:
            print("  ✓ SYNONYM - Direct meaning match! (+50 bonus)")
            relation_found = True
        if relations['hypernym']:
            print("  ✓ HYPERNYM - More general category! (+30 bonus)")
            relation_found = True
        if relations['hyponym']:
            print("  ✓ HYPONYM - More specific type! (+30 bonus)")
            relation_found = True
        if relations['antonym']:
            print("  ✓ ANTONYM - Opposite meaning! (+20 bonus)")
            relation_found = True

        if not relation_found:
            print("  ⚬ No direct relation found")

        if points > 0:
            print(f"  Points earned: {points}")
        elif points < 0:
            print(f"  Points lost: {points}")
        else:
            print(f"  You did not lose or gain any points!")
        print(f"  Total Score: {total_score}\n")

play_game()