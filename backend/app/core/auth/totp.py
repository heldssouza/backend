"""Time-based One-Time Password (TOTP) utilities."""
import base64
import secrets
import pyotp
import qrcode
import io


def generate_totp_secret() -> str:
    """
    Generate a random secret key for TOTP.
    """
    return base64.b32encode(secrets.token_bytes(20)).decode('utf-8')


def get_totp_uri(secret: str, username: str, issuer: str) -> str:
    """
    Generate a TOTP URI for QR code generation.
    """
    totp = pyotp.TOTP(secret)
    provisioning_uri = totp.provisioning_uri(
        name=username,
        issuer_name=issuer
    )

    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(provisioning_uri)
    qr.make(fit=True)

    # Create QR code image
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Convert image to base64
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    qr_code = base64.b64encode(buffer.getvalue()).decode()
    
    return f"data:image/png;base64,{qr_code}"


def verify_totp(secret: str, code: str) -> bool:
    """
    Verify a TOTP code.
    """
    totp = pyotp.TOTP(secret)
    return totp.verify(code)
