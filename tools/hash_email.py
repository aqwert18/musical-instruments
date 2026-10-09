"""Print the SHA-256 of a Google account e-mail for the ALLOWED_SHA256 list.

The site is public, so the authorised accounts are stored as hashes instead of
plain e-mail addresses. Usage:  python tools/hash_email.py someone@gmail.com
"""
import hashlib, sys

for email in sys.argv[1:]:
    print(hashlib.sha256(email.strip().lower().encode()).hexdigest(), '#', email.split('@')[0][:2] + '…')
