"""
Custom SMTP email backend that works around Python 3.14's stricter
X.509 certificate validation (VERIFY_X509_STRICT).

Gmail's intermediate CA certificates don't mark Basic Constraints as
critical, causing ssl.SSLCertVerificationError.  This backend provides
a relaxed ssl_context so the TLS handshake succeeds.
"""

import ssl
from django.core.mail.backends.smtp import EmailBackend


class GmailSMTPBackend(EmailBackend):
    def open(self):
        # Create a relaxed SSL context before Django calls starttls()
        if self.ssl_context is None:
            self.ssl_context = ssl.create_default_context()
        self.ssl_context.verify_flags &= ~ssl.VERIFY_X509_STRICT
        return super().open()
