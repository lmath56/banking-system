# Lucas Mathews - Fontys Student ID: 5023572
# Banking System Secret Key Generator
# Generates a secret key for the banking system API to manage user sessions

import secrets
secret_key = secrets.token_hex(16)  # Generates a 32-character hex string
print(secret_key)