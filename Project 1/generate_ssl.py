#!/usr/bin/env python3
"""
Simple SSL Certificate Generator
Creates self-signed certificates for HTTPS development
"""

import subprocess
import sys
import os

def generate_ssl_certificate():
    """Generate self-signed SSL certificate using OpenSSL"""
    try:
        # Create a simple config file for OpenSSL
        config_content = """
[req]
distinguished_name = req_distinguished_name
x509_extensions = v3_req
prompt = no

[req_distinguished_name]
C = US
ST = Kentucky
L = Williamsburg
O = University of the Cumberlands
CN = localhost

[v3_req]
keyUsage = keyEncipherment, dataEncipherment
extendedKeyUsage = serverAuth
subjectAltName = @alt_names

[alt_names]
DNS.1 = localhost
DNS.2 = 127.0.0.1
IP.1 = 127.0.0.1
"""
        
        # Write config to temporary file
        with open('openssl.conf', 'w') as f:
            f.write(config_content)
        
        # Generate private key and certificate
        cmd = [
            'openssl', 'req', '-x509', '-newkey', 'rsa:2048',
            '-keyout', 'key.pem', '-out', 'cert.pem',
            '-days', '365', '-nodes',
            '-config', 'openssl.conf'
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ SSL certificates generated successfully!")
            print("📄 cert.pem - Certificate file")
            print("🔑 key.pem - Private key file")
            print("")
            print("⚠️  Note: These are self-signed certificates for development only.")
            print("🌐 Browsers will show a security warning - this is normal for self-signed certificates.")
            
            # Clean up config file
            if os.path.exists('openssl.conf'):
                os.remove('openssl.conf')
            
            return True
        else:
            print("❌ Error generating certificates:")
            print(result.stderr)
            return False
            
    except FileNotFoundError:
        print("❌ OpenSSL not found. Please install OpenSSL:")
        print("🔗 Windows: Download from https://slproweb.com/products/Win32OpenSSL.html")
        print("🔗 macOS: brew install openssl")
        print("🔗 Linux: apt-get install openssl (Ubuntu/Debian) or yum install openssl (RHEL/CentOS)")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def create_simple_certificates():
    """Fallback method using Python only (less secure but works)"""
    try:
        from cryptography import x509
        from cryptography.x509.oid import NameOID
        from cryptography.hazmat.primitives import hashes, serialization
        from cryptography.hazmat.backends import default_backend
        from cryptography.hazmat.primitives.asymmetric import rsa
        import datetime
        import ipaddress
        
        # Generate private key
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        
        # Create certificate
        subject = issuer = x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, "US"),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "Kentucky"),
            x509.NameAttribute(NameOID.LOCALITY_NAME, "Williamsburg"),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, "University of the Cumberlands"),
            x509.NameAttribute(NameOID.COMMON_NAME, "localhost"),
        ])
        
        cert = x509.CertificateBuilder().subject_name(
            subject
        ).issuer_name(
            issuer
        ).public_key(
            private_key.public_key()
        ).serial_number(
            x509.random_serial_number()
        ).not_valid_before(
            datetime.datetime.utcnow()
        ).not_valid_after(
            datetime.datetime.utcnow() + datetime.timedelta(days=365)
        ).add_extension(
            x509.SubjectAlternativeName([
                x509.DNSName("localhost"),
                x509.IPAddress(ipaddress.IPv4Address("127.0.0.1")),
            ]),
            critical=False,
        ).sign(private_key, hashes.SHA256(), default_backend())
        
        # Save certificate
        with open("cert.pem", "wb") as f:
            f.write(cert.public_bytes(serialization.Encoding.PEM))
        
        # Save private key
        with open("key.pem", "wb") as f:
            f.write(private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            ))
        
        print("✅ SSL certificates generated using Python cryptography!")
        print("📄 cert.pem - Certificate file")
        print("🔑 key.pem - Private key file")
        return True
        
    except ImportError:
        print("❌ Python cryptography library not available.")
        print("💡 Install with: pip install cryptography")
        return False

if __name__ == "__main__":
    print("🔐 SSL Certificate Generator")
    print("=" * 30)
    
    # Try OpenSSL first, then fallback to Python cryptography
    if not generate_ssl_certificate():
        print("\n🔄 Trying alternative method...")
        if not create_simple_certificates():
            print("\n❌ Could not generate SSL certificates.")
            print("💡 You can still run the application with HTTP (without SSL).")
            sys.exit(1)
    
    print("\n🚀 Certificates ready! You can now run 'python app.py' with HTTPS support.")