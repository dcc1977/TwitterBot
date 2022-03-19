from requests_oauthlib import OAuth1Session
import config


# Amb això tinc el token de la Request
request_token_url = "https://api.twitter.com/oauth/request_token?oauth_callback=oob&x_auth_access_type=write"
oauth = OAuth1Session(config.API_KEY, client_secret=config.API_SECRET)

try:
    fetch_response = oauth.fetch_request_token(request_token_url)
except ValueError:
    print(
        "El consumer_key o consumer_secret no xuten."
    )

# Aqui ja tens les credencials que twitter t'ha validat com a teves.
resource_owner_key = fetch_response.get("oauth_token")
resource_owner_secret = fetch_response.get("oauth_token_secret")


# Aqui com a usuari del compte de twitter on s'ha de publicar, has de donar permisos lo típic. Vols donar accés a la applicació raspberry blah blah per que pugui publicar tweets?
base_authorization_url = "https://api.twitter.com/oauth/authorize"
authorization_url = oauth.authorization_url(base_authorization_url)
print("Ves aquí i et copies el codi que et mostra en pantalla: %s" % authorization_url)
verifier = input("Enganxa el teu codi PIN aqui: ")



# Obtenir el token d'accés
access_token_url = "https://api.twitter.com/oauth/access_token"
oauth = OAuth1Session(
    config.API_KEY,
    client_secret=config.API_SECRET,
    resource_owner_key=resource_owner_key,
    resource_owner_secret=resource_owner_secret,
    verifier=verifier,
)
oauth_tokens = oauth.fetch_access_token(access_token_url)

access_token = oauth_tokens["oauth_token"]
access_token_secret = oauth_tokens["oauth_token_secret"]


# Fem la petició d'autenticació final
oauth = OAuth1Session(
    config.API_KEY,
    client_secret=config.API_SECRET,
    resource_owner_key=access_token,
    resource_owner_secret=access_token_secret,
)


# Si tota la magia negra anterior funciona.... ara publicarem un tweet.
response = oauth.post(
    "https://api.twitter.com/2/tweets",
    json={"text": "Hola David"},
)

if response.status_code != 201:
    raise Exception(
        "Ha petao Paco: {} {}".format(response.status_code, response.text)
    )

print("Codi HTTP: {}".format(response.status_code))
