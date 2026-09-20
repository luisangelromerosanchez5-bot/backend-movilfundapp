import urllib.request
import json
from uuid import uuid4

url = "https://fpuwuweqjcqycifjifsx.supabase.co/rest/v1/personas"

data = {
    "nombrecompleto": "Paola Gomez",
    "correo": "paola@gmail.com",
    "contrasena": "ef797c8118f02dfb649607dd5d3f8c7623048c9c063d532cc95c5ed7a898a64f",
    "telefono": 3000000000,
}

req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers={
    "apikey": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZwdXd1d2VxamNxeWNpZmppZnN4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzQ2MTMzMTAsImV4cCI6MjA5MDE4OTMxMH0.gB65IWC3syw1QLsgNEv__l5IOoJidskCYiSV4-uMB8I",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZwdXd1d2VxamNxeWNpZmppZnN4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzQ2MTMzMTAsImV4cCI6MjA5MDE4OTMxMH0.gB65IWC3syw1QLsgNEv__l5IOoJidskCYiSV4-uMB8I",
    "Content-Type": "application/json",
    "Prefer": "return=representation"
})

try:
    with urllib.request.urlopen(req) as response:
        print("Success:", response.read().decode())
except urllib.error.HTTPError as e:
    print("HTTP Error:", e.code)
    print("Response body:", e.read().decode())
except Exception as e:
    print("Error:", e)
