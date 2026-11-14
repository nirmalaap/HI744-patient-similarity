from pathlib import Path
from patient_similarity.pipeline import run_pipeline

if __name__ == "__main__":
    # Change this to the location of your patient JSON directory.
    input_folder = Path(
        r"C:\Users\Admin\Downloads\PMC-Patients-full"
    )

    run_pipeline(
        input_folder=input_folder,
        output_folder=Path("outputs"),
        report_folder=Path("reports"),
        top_k=5,
        max_features=None,
    )
