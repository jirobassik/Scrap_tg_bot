import spacy
from spacy.matcher import Matcher
import time

nlp = spacy.load("ru_core_news_md")
matcher = Matcher(nlp.vocab, validate=True)


def fuzzy_search(text: str, *args) -> bool:
    start_time = time.time()
    doc = nlp(text.lower())
    for keyword in args:
        pattern = [{"TEXT": {"FUZZY": f"{keyword}"}}]
        matcher.add("TEXT", [pattern])
    matches = matcher(doc)
    end_time = time.time()
    print(f"Search time: {end_time - start_time}")
    return True if matches else False
