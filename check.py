from database import SessionLocal
import models


def check_first_filter():
    # Open a database session
    db = SessionLocal()
    try:
        # Query the SnomedFilter table for the first record
        first_record = db.query(models.SnomedFilter).first()

        if first_record:
            print("First filter found:")
            print(f"id:                {first_record.id}")
            print(f"snomed_descriptor: {first_record.snomed_descriptor}")
            print(f"icdo_code:         {first_record.icdo_code}")
            print(f"topography:         {first_record.topography}")
            print(f"filter_code:       {first_record.filter_code}")
        else:
            print("The snomed_filters table is currently empty.")

    except Exception as e:
        print(f"An error occurred while querying the database: {e}")
    finally:
        # Ensure the session is closed
        db.close()


if __name__ == "__main__":
    check_first_filter()