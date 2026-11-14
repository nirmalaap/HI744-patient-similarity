import re, string
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

_LEMMA = None
_MODE = "rule-based fallback"
_INITIALIZED = False

def _init():
    global _LEMMA, _MODE, _INITIALIZED
    if _INITIALIZED: return
    _INITIALIZED = True
    try:
        import nltk
        from nltk.stem import WordNetLemmatizer
        try: nltk.data.find("corpora/wordnet")
        except LookupError:
            nltk.download("wordnet", quiet=True)
            nltk.download("omw-1.4", quiet=True)
        test = WordNetLemmatizer()
        test.lemmatize("patients")
        _LEMMA, _MODE = test, "NLTK WordNetLemmatizer"
    except Exception:
        _LEMMA, _MODE = None, "rule-based fallback"

def lemmatization_mode():
    return _MODE

def _fallback(w):
    if len(w)>5 and w.endswith("ies"): return w[:-3]+"y"
    if len(w)>4 and w.endswith("sses"): return w[:-2]
    if len(w)>4 and w.endswith("s") and not w.endswith(("ss","us","is")): return w[:-1]
    if len(w)>5 and w.endswith("ing"):
        s=w[:-3]
        return s[:-1] if len(s)>2 and s[-1]==s[-2] else s
    if len(w)>4 and w.endswith("ed"): return w[:-2]
    return w

def preprocess_text(value):
    global _LEMMA
    if not _INITIALIZED: _init()
    s=str(value).lower()
    s=re.sub(r"https?://\S+|www\.\S+", " ", s)
    s=re.sub(r"\b\d+(?:\.\d+)?\b", " ", s)
    s=s.translate(str.maketrans({c:" " for c in string.punctuation}))
    words=re.findall(r"[a-z]+", s)
    out=[]
    for w in words:
        if w in ENGLISH_STOP_WORDS or len(w)<2: continue
        w=_LEMMA.lemmatize(w) if _LEMMA else _fallback(w)
        if w and w not in ENGLISH_STOP_WORDS: out.append(w)
    return " ".join(out)
