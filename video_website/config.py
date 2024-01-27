from urllib import parse

with open("LukeBot/LukeBot/keys/bot_token.txt", "r") as token:
    BOT_TOKEN = token.read().rstrip()

with open(
    "LukeBot/LukeBot/keys/client_secret.txt",
    "r",
) as client_secret:
    CLIENT_SECRET = client_secret.read().rstrip()

with open("LukeBot/LukeBot/keys/secret_key.txt", "r") as secret_key:
    SECRET_KEY = secret_key.read().rstrip()

REDIRECT_URI = "http://127.0.0.1:5000/oauth/callback"
OAUTH_URL = f"https://discord.com/api/oauth2/authorize?client_id=1188696002476126290&response_type=code&redirect_uri={parse.quote(REDIRECT_URI)}&scope=identify"
