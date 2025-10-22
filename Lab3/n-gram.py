import requests
from bs4 import BeautifulSoup
import re
from collections import defaultdict
import math

WIKIPEDIA_URLS = [
    "https://ro.wikipedia.org/wiki/România",
    "https://ro.wikipedia.org/wiki/Inteligență_artificială",
    "https://ro.wikipedia.org/wiki/Limba_română",
    "https://ro.wikipedia.org/wiki/București",
    "https://ro.wikipedia.org/wiki/Programare",
]


class RomanianNGramModel:
    def __init__(self, n=3, k=0.1):
        self.n = n
        self.k = k
        # Need 3 levels: ngram_size -> context -> word -> count
        self.ngrams = defaultdict(lambda: defaultdict(lambda: defaultdict(int))) # {n: {context: total_count}}
        self.context_counts = defaultdict(lambda: defaultdict(int))
        self.vocabulary = set()
        self.corpus_size = 0

    def extract_text_from_wikipedia(self, url):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')
            content = soup.find('div', {'id': 'mw-content-text'})

            if not content:
                print(f"WARNING: Could not find 'mw-content-text' div in {url}")
                print(f"Page title: {soup.find('title').get_text() if soup.find('title') else 'No title'}")
                return ""

            paragraphs = content.find_all('p')
            if not paragraphs:
                print(f"WARNING: Found content div but no paragraphs in {url}")
                return ""

            text_parts = []
            for p in paragraphs:
                p_text = p.get_text()
                p_text = ' '.join(p_text.split())
                if p_text:
                    text_parts.append(p_text)

            text = ' '.join(text_parts)

            # DEBUG: Show how much text we got
            print(f"  Extracted {len(text)} characters, {len(text.split())} words")

            return text
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return ""

    def tokenize(self, text):
        text = text.lower()
        # Get rid of any citations
        text = re.sub(r'\[\d+\]', '', text)
        sentences = re.split(r'[.!?]+', text)

        tokens = []
        for sentence in sentences:
            words = re.findall(r'[a-zăâîșțĂÂÎȘȚ]+', sentence)
            if words:
                tokens.append('<START>')
                tokens.extend(words)
                tokens.append('<END>')

        return tokens

    def train(self, urls):
        print("Fetching and processing Wikipedia articles...")
        all_tokens = []

        for url in urls:
            print(f"Processing: {url}")
            text = self.extract_text_from_wikipedia(url)
            tokens = self.tokenize(text)
            all_tokens.extend(tokens)

        self.corpus_size = len(all_tokens)
        self.vocabulary = set(all_tokens)
        print(f"\nCorpus statistics:")
        print(f"  Total tokens: {self.corpus_size}")
        print(f"  Vocabulary size: {len(self.vocabulary)}")

        for ngram_size in range(1, self.n + 1):
            print(f"Building {ngram_size}-grams...")
            for i in range(len(all_tokens) - ngram_size + 1):
                ngram = tuple(all_tokens[i:i + ngram_size])

                if ngram_size == 1:
                    context = ()
                    word = ngram[0]
                else:
                    context = ngram[:-1]
                    word = ngram[-1]

                self.ngrams[ngram_size][context][word] += 1
                self.context_counts[ngram_size][context] += 1

        print("Training complete!\n")

    def get_probability(self, word, context, ngram_size):
        # Try current n-gram size
        if context in self.context_counts[ngram_size]:
            word_count = self.ngrams[ngram_size][context].get(word, 0)
            context_total = self.context_counts[ngram_size][context]
            vocab_size = len(self.vocabulary)

            # Add-k smoothing
            if word_count > 0:
                # Use actual probability with minimal smoothing
                probability = (word_count + 0.001) / (context_total + 0.001 * vocab_size)
            else:
                # Only smooth for unseen words
                probability = 1 / (context_total + vocab_size)
            return probability

        # Backoff to lower-order n-gram
        if ngram_size > 1 and len(context) > 0:
            # Use shorter context
            shorter_context = context[1:]  # Remove first word
            return self.get_probability(word, shorter_context, ngram_size - 1)

        # Fallback to unigram probability
        if ngram_size == 1 or len(context) == 0:
            word_count = self.ngrams[1][()].get(word, 0)
            total_count = self.context_counts[1][()]
            vocab_size = len(self.vocabulary)
            return (word_count + self.k) / (total_count + self.k * vocab_size)

        return self.k / (self.k * len(self.vocabulary))  # Unknown word

    def sentence_probability(self, sentence):
        tokens = self.tokenize(sentence)

        # Remove START and END tokens for processing
        tokens = [t for t in tokens if t not in ['<START>', '<END>']]

        if not tokens:
            return 0.0

        log_prob = 0.0
        print(f"\nCalculating probability for: '{sentence}'")
        print(f"Tokens: {tokens}\n")

        # Add START token at beginning
        tokens = ['<START>'] + tokens

        for i in range(1, len(tokens)):
            # Get context (up to n-1 previous words)
            context_start = max(0, i - (self.n - 1))
            context = tuple(tokens[context_start:i])
            word = tokens[i]

            # Calculate probability
            prob = self.get_probability(word, context, len(context) + 1)
            log_prob += math.log(prob)

            print(f"  P({word} | {' '.join(context)}) = {prob:.6f}")

        print(f"\nLog probability: {log_prob:.4f}")
        print(f"Probability: {math.exp(log_prob):.2e}")

        return log_prob


if __name__ == "__main__":
    print("Initializing the Romanian 4-gram Language Model")

    model = RomanianNGramModel(n=4, k=0.1)
    model.train(WIKIPEDIA_URLS)

    test_sentences = [
        "România este o țară frumoasă",
        "Inteligența artificială este fascinantă",
        "Limba română este vorbită în România",
        "Bucureștiul este capitala României"
    ]

    print("=" * 60)
    print("Testing sentence probabilities:")
    print("=" * 60)

    for sentence in test_sentences:
        model.sentence_probability(sentence)
        print("\n" + "-" * 60)

    # Interactive mode
    print("\n" + "=" * 60)
    print(" Enter Romanian sentences to calculate probability")
    print("(Press Ctrl+C or type 'quit' to exit)")
    print("=" * 60)

    try:
        while True:
            user_sentence = input("\nEnter a Romanian sentence: ").strip()
            if user_sentence.lower() in ['quit', 'exit', 'q']:
                break
            if user_sentence:
                model.sentence_probability(user_sentence)
    except KeyboardInterrupt:
        print("\n\nExiting...")
