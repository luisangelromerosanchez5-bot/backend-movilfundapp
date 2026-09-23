import urllib.request
import json
from jose import jwt
from datetime import datetime, timedelta

secret = "fundapp-secret-jwt-key-for-fundacion-biosferas-2026"
to_encode = {"sub": "75", "rol": "voluntario", "email": "jpmercado@gmail.com"}
to_encode.update({"exp": datetime.utcnow() + timedelta(minutes=15)})
encoded_jwt = jwt.encode(to_encode, secret, algorithm="HS256")

url = "https://backend-movilfundapp.onrender.com/api/v1/postulaciones"
req = urllib.request.Request(url, headers={
    "accept": "application/json",
    "Authorization": f"Bearer {encoded_jwt}"
})

try:
    with urllib.request.urlopen(req) as response:
        print("Success:", response.read().decode())
except urllib.error.HTTPError as e:
    print("HTTP Error:", e.code)
    print("Response body:", e.read().decode())
except Exception as e:
    print("Error:", e)
