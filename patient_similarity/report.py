from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

def create_report(path,stats,docstats,lemma,summary):
    Path(path).parent.mkdir(parents=True,exist_ok=True)
    styles=getSampleStyleSheet()
    styles.add(ParagraphStyle(name="SmallBody",parent=styles["BodyText"],fontSize=9,leading=12))
    story=[Paragraph("Patient Similarity Retrieval: Methods and Results",styles["Title"]),Spacer(1,10),
      Paragraph("1. Dataset and goal",styles["Heading2"]),
      Paragraph(f"The program found {stats['json_files_found']} JSON files and loaded "
        f"{stats['unique_patients_loaded']} unique patient records; {stats['invalid_records_or_files']} "
        f"invalid files or records were skipped. Each document combines the title and clinical case "
        f"description. The goal is to retrieve the five most similar other patients and compare "
        f"TF-IDF with BM25.",styles["SmallBody"]),
      Paragraph(f"Average processed document length: {docstats['average']:.1f} tokens; "
        f"median: {docstats['median']:.1f}; empty documents: {docstats['empty']}.",styles["SmallBody"]),
      Paragraph("2. Methods",styles["Heading2"]),
      Paragraph(f"Preprocessing lowercases and standardizes text, removes URLs, numeric tokens, "
        f"punctuation, English stop words and short tokens, and applies {lemma}.",styles["SmallBody"]),
      Paragraph("Task 1 — TF-IDF: scikit-learn TfidfVectorizer uses smoothed IDF, sublinear term "
        "frequency (1 + log(tf)) and L2 normalization. Smoothing stabilizes IDF; sublinear TF limits "
        "the effect of repeated terms; L2 normalization supports cosine comparison. The UID-keyed "
        "JSON stores non-zero weights, so a missing term has weight zero.",styles["SmallBody"]),
      Paragraph("Task 2 — BM25: BM25 is a term-based ranking method using term frequency, inverse "
        "document frequency and document-length normalization. Settings are k1=1.5 and b=0.75. "
        "TF-IDF uses cosine similarity; BM25 uses its own ranking score. A patient is excluded from "
        "its own results. Both methods are lexical and may miss synonym-based clinical similarity.",
        styles["SmallBody"]),
      Paragraph("Task 3 — Evaluation: Precision@5 is relevant retrieved patients divided by five. "
        "Recall@5 is relevant retrieved patients divided by the number of ground-truth similar "
        "patients. Ground-truth labels 1 and 2 are both relevant. Patients without similar_patients "
        "are excluded from average recall, as required.",styles["SmallBody"]),
      Paragraph("3. Results",styles["Heading2"])]
    rows=[["Method","Average P@5","Average R@5","Recall N"]]
    for m,v in summary["metrics"].items():
        rows.append([m.upper(),f"{v['average_precision_5']:.4f}",
                     f"{v['average_recall_5']:.4f}" if v["average_recall_5"] is not None else "N/A",
                     str(v["recall_patients_count"])])
    t=Table(rows,colWidths=[1.2*inch,1.35*inch,1.35*inch,1.1*inch])
    t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),colors.lightblue),
      ("GRID",(0,0),(-1,-1),0.5,colors.grey),("FONTSIZE",(0,0),(-1,-1),8),
      ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),("PADDING",(0,0),(-1,-1),6)]))
    story += [t,Spacer(1,8),
      Paragraph(f"{summary['patients_with_no_ground_truth_excluded_from_average_recall']} patients "
        f"had no ground-truth links and were excluded from average recall. Precision is averaged "
        f"over all {stats['unique_patients_loaded']} patients. Average top-five Jaccard overlap "
        f"between TF-IDF and BM25: {summary['average_top5_jaccard_overlap_tfidf_bm25']}.",
        styles["SmallBody"]),
      Paragraph("Interpretation and limitations",styles["Heading2"]),
      Paragraph("Precision indicates how many of the five suggestions are known relevant patients. "
        "Recall indicates how much of the known relevant-patient set appears in the five suggestions. "
        "The provided ground truth may be incomplete; an absent link does not prove clinical "
        "dissimilarity. The lexical methods do not understand clinical meaning beyond word overlap.",
        styles["SmallBody"]),
      Paragraph("Reproducibility",styles["Heading2"]),
      Paragraph("Run: python main.py PATH_TO_INPUT_DATA_FOLDER. All reported counts and metrics "
        "are generated from the dataset at run time.",styles["SmallBody"])]
    SimpleDocTemplate(str(path),pagesize=letter,rightMargin=.6*inch,leftMargin=.6*inch,
                      topMargin=.55*inch,bottomMargin=.55*inch).build(story)
