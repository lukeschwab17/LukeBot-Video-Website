from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    session,
    abort,
    jsonify,
)
from zenora import APIClient
from werkzeug.exceptions import BadRequest
import os
from databaseWeb import Database
from config import *
import random

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

    # build votes for each video
    all_votes = []
    for video in video_data:
        all_votes.append(Database.get_votes(video[0]))
    return render_template(
        "videos.html",
        current_user=current_user,
        video_data=video_data,
        all_votes=all_votes,
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


@app.route("/toggle_button", methods=["POST"])
def toggle_button():
    bearer_client = APIClient(session.get("token"), bearer=True)
    current_user = bearer_client.users.get_current_user()
    discord_id = str(current_user.id)

    # Example: Check if the button is already pressed for the given video ID
    video_id = str(request.json.get("videoId"))

    # Perform database check here to determine button state
    # For demonstration, let's assume the state is toggled in memory
    button_state = toggle_button_state(discord_id, video_id)

    # Return JSON response indicating button state
    return jsonify({"exists": button_state})


def toggle_button_state(discord_id, video_id):
    # Toggle the button state in the database or in memory
    if not is_button_pressed(discord_id, video_id):
        Database.vote_update("add", video_id, discord_id)
        print("add")
    else:
        Database.vote_update("remove", video_id, discord_id)
        print("remove")
    # Here, we just simulate the toggling behavior
    return is_button_pressed(discord_id, video_id)


def is_button_pressed(discord_id, video_id):
    # Check if the button is pressed in the database or in memory
    # Here, we just simulate the state being randomly true or false
    return Database.did_user_vote(discord_id, video_id)


if __name__ == "__main__":
    app.run(debug=True)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
