from flask import Flask, request, jsonify
from jose import jwt

app = Flask(__name__)
@app.route('/dummy', methods=['GET'])
def dummy():
    return {"dummy":"ok"}

def verify_jwt_token(token, public_key):
    try:
        # Vérification de la signature du token JWT en utilisant la clé publique
        decoded_token = jwt.decode(token, public_key, algorithms=['HS256'])
        return decoded_token
    except jwt.ExpiredSignatureError:
        return {"valid":False,"error": "Le token JWT a expiré."}
    except jwt.JWTError:
        return {"valid":False,"error": "Le token JWT est invalide."}

@app.route('/verify', methods=['POST'])
def verify_token():
    token = request.json.get('token')
    public_key = "mspr_dolib@arr_edgar_edgar_lynda_pierre_alexandre"

    if not token:
        return {"valid":False,"error": "Token manquant dans la requête."}

    decoded_payload = verify_jwt_token(token, public_key)
    if decoded_payload:
        return {"valid":True,"message": "Le token JWT est valide.", "payload": decoded_payload}
    else:
        return {"valid":False,"error": "Le token JWT n'est pas valide."}

if __name__ == '__main__':
    app.run()
