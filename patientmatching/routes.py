from flask import  render_template, url_for, redirect, flash, session
from patientmatching import app
from patientmatching.forms import CreateProfileForm, EditProfileForm, DiagnosisForm
from patientmatching.algorithm import people_like_me, convert_phenotypes
import pandas as pd

df = pd.read_csv("patientmatching/data/peerMatchingDf.csv")
phenotypes = pd.read_csv("patientmatching/data/list_of_phenotypes.csv")
df = df.fillna('') #replacing all NaNs with empty strings

@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
def home():
    form = CreateProfileForm()
    edit_form = EditProfileForm()
    diagnosis_form = DiagnosisForm()
    if form.validate_on_submit():
        # the diagnosis variable stores checkbox info for whether they want to 
        # only see macthes for people with a diagnosis
        session["diagnosis"] = list({form.diagnosis.data})[0]
        symptoms = list({form.symptoms.data})[0]
        session["symptoms"] = symptoms.split(", ")
        session["symptoms"] = convert_phenotypes(session.get("symptoms"))
        session["name"] = list({form.username.data})[0]
        session["matches"] = list({form.number.data})[0]
        # we find the top k matches for a user
        matches = people_like_me(session.get("symptoms"),
                                 session.get("matches"),
                                 session.get("diagnosis"),
                                  df)
        return render_template('patient_matching.html',
                               matches=matches,
                               k=session.get("matches"),
                               diagnosis=session.get("diagnosis"),
                               name=session.get("name"),
                               symptoms=session.get("symptoms"),
                               edit_form=edit_form,
                               diagnosis_form=diagnosis_form)
    if edit_form.validate_on_submit() and edit_form.submit_edit_form.data:
        new_symptoms = list({edit_form.newSymptoms.data})[0]
        new_symptoms = new_symptoms.split(", ")
        session.get("symptoms").extend(new_symptoms)
        session["symptoms"] = convert_phenotypes(session.get("symptoms"))
        matches = people_like_me(session.get("symptoms"),
                                 session.get("matches"),
                                 session.get("diagnosis"),
                                 df)
        return render_template('patient_matching.html',
                               matches=matches,
                               k=session.get("matches"),
                               diagnosis=session.get("diagnosis"),
                               name=session.get("name"),
                               symptoms=session.get("symptoms"),
                               edit_form=edit_form,
                               diagnosis_form=diagnosis_form)
    if diagnosis_form.validate_on_submit():
        session["diagnosis"] = not session.get("diagnosis")
        matches = people_like_me(session.get("symptoms"),
                                 session.get("matches"),
                                 session.get("diagnosis"),
                                 df)
        return render_template('patient_matching.html',
                               matches=matches,
                               k=session.get("matches"),
                               diagnosis=session.get("diagnosis"),
                               name=session.get("name"),
                               symptoms=session.get("symptoms"),
                               edit_form=edit_form,
                               diagnosis_form=diagnosis_form)
    form = CreateProfileForm(formdata=None)
    return render_template('home.html', title='Find Matches', form=form)
