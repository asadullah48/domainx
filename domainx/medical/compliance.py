import re

class HIPAAComplianceScrubber:
    """
    HIPAA Safe Harbor De-identification Engine
    """

    @staticmethod
    def scrub_phi(text: str) -> str:
        scrubbed = text
        # 1. Names
        scrubbed = re.sub(r"(?i)(patient|pt|name):\s*[^,\r\n]+", "Patient: [REDACTED_NAME]", scrubbed)
        # 2. MRN
        scrubbed = re.sub(r"(?i)(mrn|record\s*#?):\s*[^,\r\n]+", "MRN: [REDACTED_MRN]", scrubbed)
        # 3. DOB
        scrubbed = re.sub(r"(?i)(dob|birthdate|date of birth):\s*[^,\r\n]+", "DOB: [REDACTED_DOB]", scrubbed)
        # 4. SSN
        scrubbed = re.sub(r"(?i)ssn:\s*[\d-]+", "SSN: [REDACTED_SSN]", scrubbed)
        scrubbed = re.sub(r"\b\d{3}-\d{2}-\d{4}\b", "[REDACTED_SSN]", scrubbed)
        # 5. Generic Dates
        scrubbed = re.sub(r"\b(0[1-9]|1[0-2])/(0[1-9]|[12]\d|3[01])/(19\d\d|20\d\d)\b", "[REDACTED_DATE]", scrubbed)
        # 6. Phone Numbers
        scrubbed = re.sub(r"\(?\b\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b", "[REDACTED_PHONE]", scrubbed)
        # 7. Emails
        scrubbed = re.sub(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", "[REDACTED_EMAIL]", scrubbed)
        # 8. Zip
        scrubbed = re.sub(r"\b\d{5}(-\d{4})?\b", "[REDACTED_ZIP]", scrubbed)
        return scrubbed
