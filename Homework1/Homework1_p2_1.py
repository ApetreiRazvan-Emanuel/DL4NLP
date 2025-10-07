from nltk.corpus import wordnet as wn
import nltk
nltk.download('wordnet')

def get_synonyms(word):
    synonyms = set()
    for synset in wn.synsets(word):
        for lemma in synset.lemmas():
            synonyms.add(lemma.name())
    synonyms.discard(word)
    return synonyms


def get_antonyms(word):
    antonyms = set()
    for synset in wn.synsets(word):
        for lemma in synset.lemmas():
            if lemma.antonyms():
                for ant in lemma.antonyms():
                    antonyms.add(ant.name())
    return antonyms


def get_hypernyms(word):
    """Get hypernyms (more general terms)"""
    hypernyms = set()
    for synset in wn.synsets(word):
        for hyper in synset.hypernyms():
            for lemma in hyper.lemmas():
                hypernyms.add(lemma.name())
    return hypernyms


def get_hyponyms(word):
    """Get hyponyms (more specific terms)"""
    hyponyms = set()
    for synset in wn.synsets(word):
        for hypo in synset.hyponyms():
            for lemma in hypo.lemmas():
                hyponyms.add(lemma.name())
    return hyponyms


def get_meronyms(word):
    meronyms = set()
    for synset in wn.synsets(word):
        # Part meronyms (has parts)
        for mero in synset.part_meronyms():
            for lemma in mero.lemmas():
                meronyms.add(lemma.name())
        # Substance meronyms (made of)
        for mero in synset.substance_meronyms():
            for lemma in mero.lemmas():
                meronyms.add(lemma.name())
        # Member meronyms (has members)
        for mero in synset.member_meronyms():
            for lemma in mero.lemmas():
                meronyms.add(lemma.name())
    return meronyms


def get_definitions(word):
    definitions = []
    for synset in wn.synsets(word):
        definitions.append(f"{synset.name()}: {synset.definition()}")
    return definitions


def explore_word(word):
    print(f"Exploring word: '{word}'")
    print("=" * 60)

    synsets = wn.synsets(word)
    if not synsets:
        print(f"Word '{word}' not found in WordNet.")
        return

    print(f"\nFound {len(synsets)} synset(s)\n")

    synonyms = get_synonyms(word)
    antonyms = get_antonyms(word)
    hypernyms = get_hypernyms(word)
    hyponyms = get_hyponyms(word)
    meronyms = get_meronyms(word)
    definitions = get_definitions(word)

    print("DEFINITIONS:")
    for definition in definitions:
        print(f"  - {definition}")

    print(f"\nSYNONYMS ({len(synonyms)}):")
    print(f"  {sorted(synonyms)}")

    print(f"\nANTONYMS ({len(antonyms)}):")
    print(f"  {sorted(antonyms)}")

    print(f"\nHYPERNYMS ({len(hypernyms)}) - more general:")
    print(f"  {sorted(hypernyms)}")

    print(f"\nHYPONYMS ({len(hyponyms)}) - more specific:")
    print(f"  {sorted(hyponyms)}")

    print(f"\nMERONYMS ({len(meronyms)}) - parts/members:")
    print(f"  {sorted(meronyms)}")

    total = len(synonyms) + len(antonyms) + len(hypernyms) + len(hyponyms) + len(meronyms)
    print(f"\nTotal related words collected: {total}")


word = input("Enter a word to explore: ")
explore_word(word)