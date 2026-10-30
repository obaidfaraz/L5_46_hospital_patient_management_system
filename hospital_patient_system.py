"""Hospital patient records and admission management system."""

import hashlib
import secrets
from pathlib import Path
from typing import Dict, List, Optional, TypedDict


class PatientRecord(TypedDict):
    """Structure representing a patient's hospital record."""

    name: str
    ward: str
    is_admitted: bool
    bill: float


patient_records: Dict[str, PatientRecord] = {
    "P101": {
        "name": "John Doe",
        "ward": "ICU",
        "is_admitted": True,
        "bill": 2400.0,
    },
    "P102": {
        "name": "Jane Smith",
        "ward": "General",
        "is_admitted": False,
        "bill": 450.0,
    },
    "P103": {
        "name": "Robert Brown",
        "ward": "Private",
        "is_admitted": True,
        "bill": 1200.0,
    },
}


def admit_patient(
    patient_id: str,
    name: str,
    ward: str,
    intake_log: Optional[List[str]] = None,
) -> bool:
    """Admit a new patient and optionally record the admission event."""
    if patient_id in patient_records:
        return False

    patient_records[patient_id] = {
        "name": name,
        "ward": ward,
        "is_admitted": True,
        "bill": 0.0,
    }

    if intake_log is not None:
        intake_log.append(
            f"Admitted patient {patient_id} into ward {ward}"
        )

    return True


def discharge_patient(patient_id: str) -> bool:
    """Discharge a patient, returning False if the patient does not exist."""
    patient = patient_records.get(patient_id)
    if patient is None or not patient["is_admitted"]:
        return False

    patient["is_admitted"] = False
    return True


def verify_admission_status(patient_id: str) -> bool:
    """Return whether the specified patient currently has an admission."""
    patient = patient_records.get(patient_id)
    return patient is not None and patient["is_admitted"]


def calculate_treatment_cost(
    patient_id: str,
    multiplier: float = 1.12,
) -> float:
    """Calculate a patient's bill using a validated numeric multiplier."""
    if multiplier < 0:
        raise ValueError("The treatment-cost multiplier cannot be negative.")

    patient = patient_records.get(patient_id)
    if patient is None:
        raise KeyError(f"Unknown patient ID: {patient_id}")

    return patient["bill"] * multiplier


def generate_patient_hash(patient_id: str) -> str:
    """Generate a SHA-256 digest for a patient identifier."""
    return hashlib.sha256(patient_id.encode("utf-8")).hexdigest()


def generate_ward_token() -> int:
    """Generate a cryptographically secure four-digit ward token."""
    return secrets.randbelow(9000) + 1000


def export_patient_ledger(
    filename: str = "patient_records.txt",
) -> Path:
    """Write the patient ledger to a file and return its path."""
    output_path = Path(filename)
    with output_path.open("w", encoding="utf-8") as ledger_file:
        for patient_id, details in patient_records.items():
            ledger_file.write(
                f"{patient_id}: {details['name']}, "
                f"Ward: {details['ward']}, "
                f"Admitted: {details['is_admitted']}, "
                f"Bill: {details['bill']:.2f}\n"
            )

    print(f"Patient ledger exported to: {output_path}")
    return output_path


def get_ward_summary(
    records: Dict[str, PatientRecord],
) -> int:
    """Return the number of patients currently admitted."""
    return sum(
        1 for details in records.values() if details["is_admitted"]
    )


def main() -> None:
    """Run a short demonstration of the hospital patient system."""
    admit_patient("P104", "Alice Walker", "General")
    discharge_patient("P101")

    print(
        "Is P103 admitted:",
        verify_admission_status("P103"),
    )
    print(
        "Cost calculated:",
        calculate_treatment_cost("P103"),
    )
    print("Patient Hash:", generate_patient_hash("P103"))
    print("Ward Token:", generate_ward_token())
    export_patient_ledger()
    print("Active admits:", get_ward_summary(patient_records))


if __name__ == "__main__":
    main()
