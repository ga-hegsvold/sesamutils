import os


class CertificateHandler:
    """Write a certificate to disk."""

    def __init__(self, certificate: str, file: str = "/usr/local/share/ca-certificates/ca.crt"):
        """Constructor.

        :param certificate: A string representation of the certificate.
        :type certificate: str
        :param file: File name for which to write the certificate into.
        :type file: str
        """
        self.certificate = certificate
        self.file = file

    def write(self):
        """Write certificate to disk."""
        with open(self.file, "wb") as file:
            file.write(bytes(self.certificate, "ascii"))

    @staticmethod
    def install():
        """Install CA certificate(s) by calling the shell command 'update-ca-certificates'.
        This will typically update /etc/ssl/certs/ with links to CA certificates in /usr/local/share/ca-certificates/.
        """
        os.system("update-ca-certificates")

    def __repr__(self):
        str_repr = \
                f"\nFile       : {self.file}" \
                f"\nCertificate: {self.certificate[-42:]}"  # last 42 chars

        return str_repr


if __name__ == "__main__":
    cert = CertificateHandler("foo-test", "bar.pem")
    print(cert.__doc__)
    print(cert)
    cert.write()
