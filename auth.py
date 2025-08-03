import falcon
import firebase_admin
import firebase_admin.auth
import enum

from db import UserEntry


class Auth:
    __auth__ = True

    @staticmethod
    def set_auth(auth: bool):
        Auth.__auth__ = auth

    @staticmethod
    def init_firebase(firebase_cfg: str):
        cred = firebase_admin.credentials.Certificate(firebase_cfg)
        firebase_admin.initialize_app(cred)

    @staticmethod
    def validate_permission(req, resp, resource, params):
        if not Auth.__auth__:
            req.context.user = dict()
            return

        auth_header = req.auth
        if not auth_header:
            raise falcon.HTTPUnauthorized()

        if not auth_header.startswith("Bearer"):
            raise falcon.HTTPUnauthorized()

        token = auth_header.removeprefix("Bearer").strip()

        try:
            decoded_token = firebase_admin.auth.verify_id_token(token)
        except:
            raise falcon.HTTPUnauthorized(description="Invalid token")

        email_address = decoded_token["email"]
        session = req.context.db_session

        user = session.query(UserEntry).filter(UserEntry.email_address == email_address).first()

        if not user:
            raise falcon.HTTPUnauthorized(description=f"User {email_address} not found in local db.")

        req.context.user = user
