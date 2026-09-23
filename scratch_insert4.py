import urllib.request
import json

# Insert into voluntarios
url_vol = "https://fpuwuweqjcqycifjifsx.supabase.co/rest/v1/voluntarios"
data_vol = {
    "usuarios_idusuarios": 73,
    "usuarios_idusuarios_ref": 73
}
req_vol = urllib.request.Request(url_vol, data=json.dumps(data_vol).encode('utf-8'), headers={
    "apikey": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZwdXd1d2VxamNxeWNpZmppZnN4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzQ2MTMzMTAsImV4cCI6MjA5MDE4OTMxMH0.gB65IWC3syw1QLsgNEv__l5IOoJidskCYiSV4-uMB8I",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZwdXd1d2VxamNxeWNpZmppZnN4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzQ2MTMzMTAsImV4cCI6MjA5MDE4OTMxMH0.gB65IWC3syw1QLsgNEv__l5IOoJidskCYiSV4-uMB8I",
    "Content-Type": "application/json",
    "Prefer": "return=representation"
})

try:
    with urllib.request.urlopen(req_vol) as response:
        print("Voluntarios Insert:", response.read().decode())
except urllib.error.HTTPError as e:
    print("Voluntarios HTTP Error:", e.code)
    print("Response body:", e.read().decode())
except Exception as e:
    print("Error:", e)
