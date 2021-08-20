from music_player import db
from music_player.models import Feedback,User

print("---------All Registrations--------- ")
for user in User.query.all():
    print(f"ID : {user.id}")
    print(f"Username : {user.username}")
    print(f"Email : {user.email}")
    print(f"Image Filename : {user.image_file}")
    print()

print()
print("-----All Received Feedback -----------")
for feedback in Feedback.query.all():
    print(f"ID : {feedback.id}")
    print(f"Name : {feedback.name}")
    print(f"Email : {feedback.email}")
    print(f"Text : {feedback.subject}")
    print()