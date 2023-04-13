import spacy
from spacy.matcher import Matcher

nlp = spacy.load("ru_core_news_md")
matcher = Matcher(nlp.vocab, validate=True)


def fuzzy_search(text: str, *args) -> bool:
    doc = nlp(text.lower())
    for keyword in args:
        pattern = [{"TEXT": {"FUZZY": f"{keyword}"}}]
        matcher.add("TEXT", [pattern])
    matches = matcher(doc)
    return True if matches else False
