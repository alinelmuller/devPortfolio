# ...existing code...

# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST = 'smtp.example.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@example.com'
EMAIL_HOST_PASSWORD = 'your-email-password'

from django.core.mail import send_mail
send_mail(
    'Test Email',
    'This is a test email.',
    'alinelmuller@gmail.com',
    ['alinelmuller@gmail.com'],
    fail_silently=False,
)

# ...existing code...
