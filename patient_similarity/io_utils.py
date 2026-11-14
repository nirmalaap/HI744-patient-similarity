import json
from pathlib import Path

def save_json(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def save_tfidf_json(path, matrix, patient_uids, vectorizer):
    """
    Save TF-IDF weights as:
    patient_uid -> term -> weight.
    Zero-weight terms are omitted; an absent term has weight 0.
    """
    terms = vectorizer.get_feature_names_out()
    matrix = matrix.tocsr()
    result = {}

    for row_index, patient_uid in enumerate(patient_uids):
        row = matrix.getrow(row_index)
        result[patient_uid] = {
            str(terms[column_index]): round(float(weight), 8)
            for column_index, weight in zip(row.indices, row.data)
        }

    save_json(path, result)
