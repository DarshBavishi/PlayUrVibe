from music_player import app, db
from flask import render_template, redirect, request, url_for, flash, abort, Response
from flask_login import login_user, login_required, logout_user, current_user
from music_player.models import User, Feedback
from music_player.forms import LoginForm, RegistrationForm, MoodPicUpload, FeedbackForm
from werkzeug.security import generate_password_hash, check_password_hash
from music_player.picturehandler import detect_mood
import cv2
from deepface import DeepFace
import time

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/login',methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Grab the user from our User Models table
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if user.check_password(form.password.data) and user is not None:
                # Log in the user

                login_user(user)
                flash('Logged in successfully.')

                # If a user was trying to visit a page that requires a login
                # flask saves that URL as 'next'.
                next = request.args.get('next')

                # So let's now check if that next exists, otherwise we'll go to
                # the welcome page.
                if next == None or not next[0] == '/':
                    next = url_for('userhome')

                return redirect(next)
        else :
            flash('Incorrect Details')

    return render_template('login.html',form = form)

@app.route('/register',methods = ['GET','POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(email=form.email.data,username=form.username.data,password=form.password.data)

        db.session.add(user)
        db.session.commit()
        flash('Thanks for registering! Now you can login!')
        return redirect(url_for('login'))

    return render_template('register.html',form = form)

@app.route('/home')
@login_required
def userhome():
    return render_template('userhome.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You logged out!')
    return redirect(url_for('index'))

@app.route('/random')
@login_required
def randomsongs():
    return render_template('random.html')

@app.route('/randomEng')
@login_required
def randomEng():
    return render_template('ranenglish.html')

@app.route('/randomHin')
@login_required
def randomHin():
    return render_template('ranhindi.html')

@app.route('/emotion',methods=['GET','POST'])
@login_required
def emotion():
    form = MoodPicUpload()
    if form.validate_on_submit():
        if form.picture.data:
            username = current_user.username
            picture_file,mood = detect_mood(form.picture.data)
            print(mood)
            current_user.image_file=picture_file
            current_user.mood=mood[0]
            db.session.commit()
            return redirect(url_for('mood_player'))
        else:
            flash('Please upload a photo first for mood detection!')
    return render_template('emotion.html',form = form)

@app.route('/mood_player',methods=['GET','POST'])
@login_required
def mood_player():
    if current_user.image_file == 'default.png':
        flash('Please upload a photo first for mood detection!')
        return redirect(url_for('emotion'))

    image_file=url_for('static',filename='mood_uploads/'+ current_user.image_file)
    mood = current_user.mood
    return render_template('mood_player.html',mood = mood, img = image_file)

@app.route('/detect')
@login_required
def a():
    print('###########inside detect#############')
    """Video streaming home page."""
    return render_template('a.html')

captured_frames = []
def gen():
    """Video streaming generator function."""
    faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    cap = cv2.VideoCapture(0)

    fs = 1
    # Read until video is completed
    captured_frames.clear()
    while(cap.isOpened()):
      # Capture frame-by-frame
        ret, img = cap.read()
        if ret == True:
            captured_frames.append(img)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = faceCascade.detectMultiScale(gray,2,4)


            ##Draw a rectangle
            for(x , y , w , h) in faces:
                cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)
            img = cv2.resize(img, (0,0), fx=0.5, fy=0.5) 
            frame = cv2.imencode('.jpg', img)[1].tobytes()
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            time.sleep(0.1)
            fs+=1
            print(fs)
            if fs>=30:
                # cv2.destroyAllWindows()
                # return render_template('live_detect.html', mood = result['dominant_emotion'])
                break
        else: 
            break
        
            
@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/detect/play',methods=['GET','POST'])    
@login_required
def live_emotion():
    fin_emotion = ''
    emotions = {'sad': 0, 'angry': 0, 'disgust': 0, 'fear': 0, 'happy': 0, 'neutral': 0, 'surprise': 0}
    if len(captured_frames) > 0:
        for i in range(len(captured_frames) - 5,len(captured_frames)):
            try:
                print(i)
                result = DeepFace.analyze(captured_frames[i], actions = ['emotion'])
                print(result['dominant_emotion'])

                emotions[result['dominant_emotion']] += 1
            
            except:
                print('inside except')
                fin_emotion = ''
                
        fin_emotion = max(emotions, key=emotions.get)
        captured_frames.clear()
        print('----- fin emotion', fin_emotion)

    return render_template('live_detect.html',mood = fin_emotion )


@app.route("/contact",methods=['GET','POST'])
def contact():
    form = FeedbackForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        subject = form.subject.data

        f = Feedback(name = name,email = email,subject = subject)
        db.session.add(f)
        db.session.commit()
        print(f)

        flash('Your feedback has been submitted successfully')
        print('logged out contact')
        return redirect(url_for('index'))

    return render_template('contact.html',form = form)



    
    
@app.route("/feedback",methods=['GET','POST'])
@login_required
def feedback():
    form = FeedbackForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        subject = form.subject.data

        f = Feedback(name = name,email = email,subject = subject)
        db.session.add(f)
        db.session.commit()
        print(f)

        flash('Your feedback has been submitted successfully')
        print('logged out contact')
        return redirect(url_for('userhome'))

    return render_template('contact1.html',form = form)

if __name__ == '__main__':
    app.run(debug=True)
