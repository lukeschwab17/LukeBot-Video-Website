from flask import Flask, flash, redirect, render_template, request, session, abort
from zenora import APIClient
from werkzeug.exceptions import BadRequest
import os
from databaseWeb import Database
from config import *

# zenora library and usage:
# https://github.com/ahnaf-zamil/zenora
app = Flask(__name__)
app.secret_key = SECRET_KEY
client = APIClient(BOT_TOKEN, client_secret=CLIENT_SECRET)


# home page
@app.route("/")
def home():
    if not "token" in session:
        return render_template("oauth2_login.html", oauth_url=OAUTH_URL)

    bearer_client = APIClient(session.get("token"), bearer=True)
    current_user = bearer_client.users.get_current_user()
    current_user_id = str(current_user.id)
    video_data = Database.get_all_videos(current_user_id)

    return render_template(
        "videos.html", current_user=current_user, video_data=video_data
    )


# video search
@app.route(f"/search", methods=["POST"])
def search():
    search_query = request.form.get("searchbar")
    filtered_videos = Database.check_search(search_query)

    bearer_client = APIClient(session.get("token"), bearer=True)
    current_user = bearer_client.users.get_current_user()
    current_user_id = str(current_user.id)
    video_data = Database.get_all_videos(current_user_id)

    return render_template(
        "videos.html", current_user=current_user, video_data=filtered_videos
    )


# oauth
@app.route("/oauth/callback")
def callback():
    try:
        code = request.args["code"]
    except BadRequest:
        return redirect("/")

    access_token = client.oauth.get_access_token(code, REDIRECT_URI).access_token
    session["token"] = access_token
    return redirect("/")


# logout
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True, port=5000)
