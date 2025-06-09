from flask import redirect, url_for, request, jsonify, make_response, current_app
from config import GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET
from utils.security import generate_jwt
from repositories.user_repository import UserRepository
from database import SessionLocal
import os, requests, jwt
from datetime import datetime, timedelta
from config import GOOGLE_CLIENT_ID,GOOGLE_CLIENT_SECRET,GOOGLE_REDIRECT_URI,FRONTEND_REDIRECT_URI


class GoogleAuthService:
    def __init__(self,db_session):
        self.client_id = GOOGLE_CLIENT_ID
        self.client_secret = GOOGLE_CLIENT_SECRET
        self.redirect_uri = GOOGLE_REDIRECT_URI
        self.frontend_redirect = FRONTEND_REDIRECT_URI
        self.user_repo = UserRepository(db_session)

    def get_google_auth_url(self):
        return (
            "https://accounts.google.com/o/oauth2/v2/auth?"
            f"client_id={self.client_id}&"
            f"redirect_uri={self.redirect_uri}&"
            "response_type=code&"
            "scope=openid%20email%20profile"
        )

    def handle_google_callback(self, code):
        # Step 1: Exchange code for token
        token_res = requests.post("https://oauth2.googleapis.com/token", data={
            "code": code,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "redirect_uri": self.redirect_uri,
            "grant_type": "authorization_code"
        }).json()

        if "error" in token_res:
            return {"success": False, "message": "Token exchange failed"}, 400

        # Step 2: Use access token to get user info
        user_info = requests.get(
            "https://www.googleapis.com/oauth2/v2/userinfo",
            headers={"Authorization": f"Bearer {token_res['access_token']}"}
        ).json()

        # Step 3: Store or retrieve user
        user = self.user_repo.get_or_create_google_user(user_info)
         # Step 4: Generate JWT token
        token = generate_jwt(user.email, user.role.name)
        print ("Generating JWT token", token)

        return token, user
