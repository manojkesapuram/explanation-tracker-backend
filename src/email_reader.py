import imaplib
import email
from email.utils import parseaddr


def fetch_emails():
    HOST = "imap.gmail.com"
    EMAIL = "columbuskvmk@gmail.com"
    PASSWORD = "fhbx giax klbb knhi"

    mail = imaplib.IMAP4_SSL(HOST)
    mail.login(EMAIL, PASSWORD)
    mail.select("inbox")

    # ✅ search emails
    status, messages = mail.search(None, '(SUBJECT "Explanation -")')

    if status != "OK":
        return []

    email_ids = messages[0].split()
    email_ids = email_ids[-10:]

    results = []

    for eid in email_ids:
        _, msg_data = mail.fetch(eid, "(RFC822)")
        raw_email = msg_data[0][1]
        msg = email.message_from_bytes(raw_email)

        subject = msg["Subject"]

        # ✅ strict filter
        if not subject or not subject.startswith("Explanation -"):
            continue

        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True).decode(errors="ignore")
        else:
            body = msg.get_payload(decode=True).decode(errors="ignore")

        name = subject.split("Explanation -")[1].strip()
        raw_from = msg.get("From")
        name_from, email_from = parseaddr(raw_from)

        results.append({
            "name": name,  # from subject
            "email": email_from,  # ✅ FIXED
            "explanation": body
        })

    return results