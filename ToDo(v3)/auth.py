from pymstodo import ToDoConnection
from dotenv import load_dotenv, set_key
import os

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

auth_url = ToDoConnection.get_auth_url(client_id)
redirect_resp = input(f'Go here and authorize:\n{auth_url}\n\nPaste the full redirect URL below:\n')
token = ToDoConnection.get_token(client_id, client_secret, redirect_resp)

set_key('.env', "TOKEN", str(token))
