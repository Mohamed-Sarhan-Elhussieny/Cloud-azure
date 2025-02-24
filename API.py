from fastapi import FastAPI, File, UploadFile, HTTPException, Response
from fastapi.staticfiles import StaticFiles
import random
import io
import speech_recognition as sr
import os
import arabic_reshaper
from bidi.algorithm import get_display
import uuid
import pyttsx3
from last_script import Patient, PatientQA
import azure.cognitiveservices.speech as speechsdk
import pandas as pd
import json
from fastapi.responses import JSONResponse


app = FastAPI()

# تحميل ملف Excel عند تشغيل السيرفر
from fastapi import FastAPI, HTTPException
import os
import json
import pandas as pd

app = FastAPI()

# تحديد مسار ملف Excel داخل نفس المجلد
file_name = "MED_VR_cases_final.xlsx"
file_path = os.path.abspath(file_name)  # تأكد من تحديد المسار الكامل للملف

# التحقق من وجود الملف
if not os.path.exists(file_path):
    raise FileNotFoundError(f"⚠️ File '{file_name}' not found in the current directory.")

# تحميل بيانات ملف Excel عند تشغيل السيرفر
df = pd.read_excel(file_path)

# متغير لتخزين الحالة الحالية
current_case = {}

@app.get("/get_cases")
def get_cases():
    """إرجاع قائمة بالحالات المتاحة من ملف Excel."""
    cases = df[["id", "description"]].to_dict(orient="records")
    return {"cases": cases}

@app.get("/select_case/{case_id}")
def get_case(case_id: int):
    """إرجاع بيانات الحالة المختارة بناءً على ID."""
    global current_case  
    case_row = df[df["id"] == case_id]
    
    if case_row.empty:
        raise HTTPException(status_code=404, detail="⚠️ Case not found")
    
    case_data = case_row.iloc[0].to_dict()
    


    for key in ["personal_data", "examination_data", "model_data", "investigations_data","Presenting_Complaint","hpi","medical_history","family_history"]:
        if key in case_data and isinstance(case_data[key], str):  # التأكد من أنها ليست `NaN`
            try:
                print(f"تحليل {key}: {case_data[key]}")  # طباعة البيانات لفحصها
                case_data[key] = json.loads(case_data[key])
            except json.JSONDecodeError as e:
                raise HTTPException(status_code=500, detail=f"خطأ في تحليل JSON في {key}: {str(e)}")

    current_case = case_data  # تخزين الحالة المختارة

    return case_data

@app.get("/get_selected_case")
def get_selected_case():
    """إرجاع الحالة المختارة حاليًا."""
    if not current_case:
        raise HTTPException(status_code=404, detail="⚠️ No case selected")
    return current_case









def extract_patient_data_from_case(current_case):
    if not current_case or 'personal_data' not in current_case:
        raise HTTPException(status_code=400, detail="No personal data available")

    personal_data = current_case['personal_data']
    Presenting_Complaint = current_case['Presenting_Complaint']

    # استخراج القيم من personal_data (يجب أن يكون لديك الحقول المناسبة في current_case)
    patient = Patient(
        name=personal_data.get("name", "غير محدد"),
        age=personal_data.get("age", 0),
        sex=personal_data.get("sex", "غير محدد"),
        address=personal_data.get("address", "غير محدد"),
        occupation=personal_data.get("occupation", "غير محدد"),
        marital_status=personal_data.get("marital_status", False),
        children=personal_data.get("children", False),
        is_smoker=personal_data.get("is_smoker", False),
        parent_is_smoker=personal_data.get("parent_is_smoker", False),
        num_of_cigrates=personal_data.get("num_of_cigrates", 0),
        duration_of_smoking=personal_data.get("duration_of_smoking", 0),
        alcohol_user=personal_data.get("alcohol_user"),
        Tea_addict=personal_data.get("Tea_addict"),
        Pet_owner=personal_data.get("Pet_owner"),
        is_eating=personal_data.get("is_eating"),
        Polyuria=personal_data.get("Polyuria"),
        Polyuria_colour = personal_data.get("Polyuria_colour"),

        Dysuria=Presenting_Complaint.get("Dysuria", False),
        breathe_odor=Presenting_Complaint.get("breathe_odor", False),
        vomiting=Presenting_Complaint.get("vomiting", False),
        constipation=Presenting_Complaint.get("constipation", False),
        Diarrhea=Presenting_Complaint.get("Diarrhea", False),
        Jaundice=Presenting_Complaint.get("Jaundice", False),
        blotting=Presenting_Complaint.get("blotting", False),
        chest_pain=Presenting_Complaint.get("chest_pain", False),
        cough=Presenting_Complaint.get("cough", False),
        fever=Presenting_Complaint.get("fever", False),
        vomiting_blood=Presenting_Complaint.get("vomiting_blood", False),
        conscious_level=Presenting_Complaint.get("conscious_level", False),
        hemopt=Presenting_Complaint.get("hemopt", False),
        cyanosis=Presenting_Complaint.get("cyanosis", False),
        edema=Presenting_Complaint.get("edema", False),
        heart=Presenting_Complaint.get("heart", False),
        last_reading=Presenting_Complaint.get("last_reading", False),
        infaction=Presenting_Complaint.get("infaction", False),
        mou=Presenting_Complaint.get("mou", False)
    )
    
    return patient

# استخرج patient من current_case
def extract_chief_complaint(current_case):
    Presenting_Complaint = current_case['Presenting_Complaint']
    
    complaint = Presenting_Complaint.get("Complaint")
    Duration= Presenting_Complaint.get("Duration")
    Onset  = Presenting_Complaint.get("Onset")
    Severity= Presenting_Complaint.get("Severity")
    releaving_factor = Presenting_Complaint.get("releaving_factor")
    full_complaint = (complaint,Duration,Onset,Severity,releaving_factor)
    return full_complaint

####################################################################


@app.get("/audio/{filename}")
async def get_audio(filename: str):
    file_path = os.path.join("uploads", filename)
    if os.path.exists(file_path):
        with open(file_path, "rb") as audio_file:
            return Response(content=audio_file.read(), media_type="audio/wav")
    return Response(content="File not found", status_code=404)


#####################################################

# Speech-to-Text: Convert user question audio to text
def transcribe_audio_to_text(file: UploadFile) -> str:
    recognizer = sr.Recognizer()
    try:
        # Load audio data from the uploaded file
        audio_data = io.BytesIO(file.file.read())
        with sr.AudioFile(audio_data) as source:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.record(source)
            # Transcribe audio to text in Arabic
            text = recognizer.recognize_google(audio, language="ar-EG")
            print("Transcription:", text)
            return text
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
        return "عذراً، لم أتمكن من فهم السؤال."
    except sr.RequestError as e:
        print(f"Request error from Google Speech Recognition: {e}")
        raise HTTPException(status_code=500, detail=f"Speech-to-Text Error: {e}")
    


#####################################################
def generate_arabic_audio(text: str, patient_sex: str = "male") -> str:
    # Generate a unique filename using UUID
    audio_path_wav = f"uploads/output.wav"
    
    # Configure the Azure Speech service
    speech_key = "57a2148c429940abb027514632f82fac"  
    service_region = "westeurope"  

    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    
    # Select voice based on patient sex
    if patient_sex.lower() == "female":
        speech_config.speech_synthesis_voice_name = "ar-EG-SalmaNeural"  # Female Arabic voice
    else:
        speech_config.speech_synthesis_voice_name = "ar-EG-ShakirNeural"  # Male Arabic voice

    audio_config = speechsdk.audio.AudioOutputConfig(filename=audio_path_wav)

    # Create a synthesizer
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

    # Speak the text
    result = synthesizer.speak_text(text)

    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("Speech synthesized for text: [{}]".format(text))
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Speech synthesis canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))

    return f"output.wav"


######################################################


# تحويل النص العربي إلى صيغة قابلة للعرض
def reshape_arabic_text(text):
    reshaped_text = arabic_reshaper.reshape(text)  # Reshape the text
    bidi_text = get_display(reshaped_text)  # Apply the bidi algorithm
    return bidi_text


  
@app.post("/ask-audio/")
async def ask_audio(file: UploadFile):
    if not file.filename.endswith(".wav"):
        raise HTTPException(status_code=400, detail="Only .wav files are supported.")
    
    # Step 1: Convert audio to text (question)
    question_text = transcribe_audio_to_text(file)
    print(f"Question: {question_text}")
    
    # Generate audio with neutral voice for errors
    if question_text == "عذراً، لم أتمكن من فهم السؤال.":
        audio_file_name = generate_arabic_audio(question_text)
        audio_file_url = f"http://localhost:8000/audio/{audio_file_name}"
        return {
            "question": question_text,
            "response_text": "عذراً، لم أتمكن من فهم السؤال.",
            "audio_file": audio_file_url
        }
    
    # Extract patient data
    patient = extract_patient_data_from_case(current_case)
    
    # Get patient sex
    patient_sex = patient.sex.lower() if hasattr(patient, 'sex') else "male"
    
##########################################################################
    Presenting_Complaint = current_case['Presenting_Complaint']
    complaint = Presenting_Complaint.get("Complaint", "لا يوجد")
    Duration= Presenting_Complaint.get("Duration",  "لا يوجد")
    Onset  = Presenting_Complaint.get("Onset",  "لا يوجد")
    Severity= Presenting_Complaint.get("Severity",  "لا يوجد")
    releaving_factor = Presenting_Complaint.get("releaving_factor",  "لا يوجد")
    patient.add_chief_complaint(complaint,Duration,Onset,Severity,releaving_factor)

##########################################################################
    hpi_data = current_case['hpi']
    patient.add_hpi(hpi_data)

###########################################################################
    medical_history = current_case['medical_history']
    patient.add_medical_history(
        condition = medical_history.get("condition", "غير محدد"),
        details = medical_history.get("details", "غير محدد"),
        last_time = medical_history.get("last_time", "غير محدد"),
        percentage = medical_history.get("percentage", "غير محدد"),
        other = medical_history.get("other", "غير محدد"),
        blood_transfusions=medical_history.get("blood_transfusions", "غير محدد"),
        operation=medical_history.get("operation", "غير محدد")
    )
############################################################################
    patient.add_medication(
        response = "اللّهُ يَسْلِمُكَ يَا دُكْتُورُ.")

############################################################################
    family_history = current_case['family_history']
    patient.add_family_history(
        family = family_history.get("family", "غير محدد"), 
        illness = family_history.get("illness", "غير محدد")
    )
    
############################################################################
    qa = PatientQA(patient)
    response_text = qa.match_question(question_text)
    if not response_text:
        response_text = "عذراً، لا يمكنني الإجابة على هذا السؤال الآن."

    # Step 3: Convert the response text to audio based on patient sex
    audio_file_name = generate_arabic_audio(response_text, patient_sex)
    audio_file_url = f"http://localhost:8000/audio/{audio_file_name}"
    
    return {
        "question": question_text,
        "response_text": response_text,
        "audio_file": audio_file_url
    }




@app.get("/")
def root():
    return {"message": "Welcome to the Patient Voice-to-Voice API!"}