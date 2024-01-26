from flask import Flask, Flask, flash, redirect, render_template, request, session, abort
import os
from databaseWeb import Database

app = Flask(__name__)

@app.route('/')
def allvideos(username: str = None):

    if not username or not session.get('logged_in'):
        return render_template('login.html')
    video_data_all = Database.get_all_videos(username) # list of tuples. tuples -> rowid, user_id, number_of_clips, recording_name, file_path, guilds
    return render_template('videos.html', all_video_data=video_data_all)

@app.route(f'/search', methods=['POST'])
def search():
    search_query = request.form.get('searchbar')
    filtered_videos = Database.check_search(search_query)
    return render_template('videos.html', all_video_data=filtered_videos)

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username-submission']
        password = request.form['password-submission']
    #PLACEHOLDERS UNTIL DATABASE RUNNING
    for login in Database.get_logins():
        if username.lower() == login[0].lower() and password == login[1]:
            session['logged_in'] = True
            break
        else:
            flash('wrong password!')
    return allvideos(username)

if __name__ == "__main__":

    app.run(debug=True, port=5000)
    
