import sys
import pandas as pd
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from database import engine, SessionLocal
import models


def seed_snomed_filters(tsv_path: str):
    models.Base.metadata.create_all(bind=engine)

    db: Session = SessionLocal()
    skip_all_subsequent_repeats = False

    try:
        df = pd.read_csv(tsv_path, sep='\t')

        for index, row in df.iterrows():
            record_id = int(row['SNOMED code'])

            # 1. Quick initial check by ID
            exists = db.query(models.SnomedFilter).filter_by(id=record_id).first()
            if exists:
                if skip_all_subsequent_repeats:
                    continue

                print(f"\n[Duplicate ID Found] Row {index} matches an existing database ID: {record_id}")
                print(row.to_frame().T)

                choice = input("Skip this row and all subsequent repeats? (y/n): ").strip().lower()
                if choice == 'y':
                    skip_all_subsequent_repeats = True
                    continue
                else:
                    print("Execution stopped by user.")
                    sys.exit(0)

            # 2. Attempt insertion to catch other unique constraint failures
            new_filter = models.SnomedFilter(
                id=record_id,  # Explicitly setting your unique TSV IDs
                snomed_descriptor=str(row['SNOMED descriptor']),
                icdo_code=str(row['ICD-O code']),
                topography=str(row['topography']),
                filter_code=str(row['filter_code'])
            )

            try:
                db.add(new_filter)
                db.flush()  # Flush sends SQL to DB to trigger constraints without committing yet

            except IntegrityError as ie:
                db.rollback()  # Rollback the failed flush to keep the session clean

                if skip_all_subsequent_repeats:
                    continue

                print(f"\n[Unique Constraint Violation] Error at row {index}:")
                print(row.to_frame().T)
                print(f"Details: {ie.orig}")

                choice = input("Skip this row and all subsequent repeats? (y/n): ").strip().lower()
                if choice == 'y':
                    skip_all_subsequent_repeats = True
                    continue
                else:
                    print("Execution stopped by user.")
                    sys.exit(0)

        db.commit()
        print("\nDatabase seeding completed successfully.")

    except Exception as e:
        db.rollback()
        print(f"\nAn unexpected error occurred: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    seed_snomed_filters("snomed.tsv")