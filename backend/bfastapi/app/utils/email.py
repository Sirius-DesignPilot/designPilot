from pydantic import BaseModel


class EmailSchema(BaseModel):
    subject: str
    html_content: str


def generate_reset_password_email(email_to: str, email: str, token: str) -> EmailSchema:
    reset_link = f"https://your-frontend-domain/reset-password?token={token}"

    html = f"""
    <h2>Password Reset Request</h2>
    <p>Hello {email},</p>
    <p>Click the link below to reset your password:</p>
    <a href="{reset_link}">Reset Password</a>
    """

    return EmailSchema(subject="Password Reset", html_content=html)


def send_email(email_to: str, subject: str, html_content: str):
    # Eğer gerçek e-posta atmak istersen SMTP eklenir
    print("=== EMAIL SENT ===")
    print("To:", email_to)
    print("Subject:", subject)
    print("HTML:", html_content)
