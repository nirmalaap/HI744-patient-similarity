# Patient Similarity Retrieval Assignment

This project implements the three required tasks in the HI 744 assignment using Pandas, TF-IDF, and BM25.

## Run on Windows

Create and activate a virtual environment, then install dependencies:

```bat
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

The dataset path is configured directly in `main.py`. Edit `input_folder` there to point to your unzipped patient JSON directory, then click **Run Python File** in VS Code.

## Required output files

The program generates only the three required assignment JSON files:

1. `outputs/tfidf_matrix.json` — Task 1. Direct lookup by patient UID and term, for example `tfidf_data["2569952-1"]["tumor"]`. Terms not stored have a weight of zero.
2. `outputs/top5_similar_patients.json` — Task 2. Each patient UID contains its `patient_id`, plus top-five patient UID lists for `tfidf` and `bm25`.
3. `outputs/evaluation_per_patient.json` — Task 3. Each patient UID contains Precision@5 and Recall@5 for both methods. Recall is `null` for patients without ground-truth similar patients.
4. `outputs/evaluation_summary.json` — Aggregate average Precision@5 and Recall@5 for each method, number of patients included in each average, patients excluded from average recall, and TF-IDF/BM25 top-five overlap.

The program also generates `reports/patient_similarity_report.pdf`, which contains the dataset description, preprocessing, method and parameter choices, evaluation results, overlap, interpretation, and limitations.

## Methods

- Pandas reads the JSON files recursively, combines records, and removes duplicate patient UIDs.
- Preprocessing standardizes text, removes URLs, numbers, punctuation, English stop words, and applies lemmatization.
- TF-IDF uses scikit-learn with smoothed IDF, sublinear term frequency, and L2 normalization. Cosine similarity ranks patients.
- BM25 uses `k1=1.5` and `b=0.75`; its own score ranks patients.
- The query patient is excluded from its own results.
- The `similar_patients` field is the ground truth; relevance values 1 and 2 both count as relevant.
- Patients without ground-truth similar patients are excluded from average recall, as required.

The report and result files are generated from the actual dataset when the program runs. Review and understand the code, and disclose AI assistance if required by course rules.
