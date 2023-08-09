from pymstodo import ToDoConnection


def get_tok():
    client_id = "64edb794-587d-49d4-9e6b-8180b3915886"
    client_secret = "0HF8Q~nKSYM05DGL9arjESEi214wmEujFPSe6drx"

    auth_url = ToDoConnection.get_auth_url(client_id)

    redirect_resp = input(f'Go here and authorize:\n{auth_url}\n\nPaste the full redirect URL below:\n')
    token = ToDoConnection.get_token(client_id, client_secret, redirect_resp)

    with open('references/token.txt', 'w') as f:
        s = client_id + "\n" + client_secret + "\n" + str(token) + "\n"
        f.write(s)


if __name__ == '__main__':
    get_tok()

