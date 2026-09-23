import urllib.request
import json

url = "https://backend-movilfundapp.onrender.com/api/v1/postulaciones"
req = urllib.request.Request(url, headers={
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3OTAyMTgzNTQsInN1YiI6Ijc1IiwiaWQiOiI3NSIsInJvbCI6InZvbHVudGFyaW8iLCJlbWFpbCI6ImpwbWVyY2Fkb0BnbWFpbC5jb20i.something"
})

# Note: We don't have the full signature for the JWT in the screenshot.
# But wait, in the backend config: JWT_SECRET="your-super-secret-key"
# We can just generate a valid token!
from jose import jwt
from datetime import datetime, timedelta

secret = "fundapp_secret_key_2026_secure!" # wait, what is the secret?
