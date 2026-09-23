import urllib.request
import json

url = "https://fpuwuweqjcqycifjifsx.supabase.co/rest/v1/voluntarios?usuarios_idusuarios=eq.75"
req = urllib.request.Request(url, headers={
    "apikey": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZwdXd1d2VxamNxeWNpZmppZnN4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzQ2MTMzMTAsImV4cCI6MjA5MDE4OTMxMH0.gB65IWC3syw1QLsgNEv__l5IOoJidskCYiSV4-uMB8I",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZwdXd1d2VxamNxeWNpZmppZnN4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzQ2MTMzMTAsImV4cCI6MjA5MDE4OTMxMH0.gB65IWC3syw1QLsgNEv__l5IOoJidskCYiSV4-uMB8I"
})

try:
    with urllib.request.urlopen(req) as response:
        print("Select:", response.read().decode())
except Exception as e:
    print("Error:", e)
