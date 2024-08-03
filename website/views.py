from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, logout_user, current_user
from .models import Note
from . import db
import json
from openai import OpenAI

cleint = OpenAI(
    api_key = "" #custom openai playground api key
)

views = Blueprint('views', __name__)


def chat_with_gpt(messages, prompt):
    messages.append({"role": "user", "content": prompt})
    new_note = Note(data=prompt, user_id=current_user.id, 
                    gptdata = json.dumps({"role": "user", "content": prompt}))
    db.session.add(new_note)
    response = cleint.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    return response.choices[0].message.content


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST': 
        prompt = request.form.get('note') #Gets the prompt from the HTML 

        if len(prompt) < 1:
            flash('Note is too short!', category='error') 
        else:
            messages = []
            for n in current_user.notes:
                message = json.loads(n.gptdata)
                messages.append(message)
            response = chat_with_gpt(messages, prompt)
            messages.append({"role": "system", "content": response})
            # current_user.messages = json.dumps(messages)
            new_note = Note(data=response, user_id=current_user.id, 
                            gptdata = json.dumps({"role": "system", "content": response}))  #providing the schema for the note 
            db.session.add(new_note) #adding the note to the database 
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("home.html", user=current_user)

@views.route('/delete-note', methods = ['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
    
    return jsonify({})
