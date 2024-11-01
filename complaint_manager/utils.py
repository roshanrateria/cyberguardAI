import http.client
import json
import base64
import functools
import moviepy.editor as mp
from .load_creds import load_creds
import os

import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

genai.configure(api_key="AIzaSyAxBnqVMdOQmeNiT2aLKd8ONcsEn83KMG8")
model = genai.GenerativeModel(model_name="gemini-1.5-pro")



auth="7aaU5Yo99_VFnL3KfRmNJxHGqCDMmx1Ab1CtEJwHwPAmDiwwRxFcb8hkxKZ3pgt_"

def split_and_encode_audio(video_path, segment_length=20):
  """Divides audio from a video into segments, returns base64 encoded strings in a list.
  Args:
      video_path: Path to the video file.
      segment_length: Duration in seconds for each segment (default: 20).
  Returns:
      A list of base64 encoded strings (one for each segment) or None on error.
  """

  try:
    from moviepy.editor import VideoFileClip
    clip = VideoFileClip(video_path)
    audio_clip = clip.audio

    # Get total audio duration
    total_duration = audio_clip.duration

    # Initialize list for storing base64 strings
    encoded_segments = []

    # Iterate through audio in segments
    start_time = 0
    while start_time < total_duration:
      # Calculate segment end time (ensure it doesn't exceed total duration)
      end_time = min(start_time + segment_length, total_duration)

      # Extract and trim the current segment
      segment_clip = audio_clip.subclip(start_time, end_time)

      # Write the segment audio to a temporary file
      segment_data = segment_clip.write_audiofile("temp.wav")

      # Read and encode the segment data to base64
      with open("temp.wav", "rb") as audio_file:
        audio_bytes = audio_file.read()
      base64_segment = base64.b64encode(audio_bytes).decode("utf-8")

      # Add the base64 encoded segment to the list
      encoded_segments.append(base64_segment)

      # Update start time for the next segment
      start_time = end_time

  except ImportError:
    print("Error: moviepy library not installed. Please install it using 'pip install moviepy'")
    return None

  return encoded_segments






# Function to generate interview question

@functools.cache
def extract_audio_to_text(response):
    conn = http.client.HTTPSConnection("dhruva-api.bhashini.gov.in")
    payload = json.dumps({
  "pipelineTasks": [
    {
      "taskType": "asr",
      "config": {
        "language": {
          "sourceLanguage": "hi"
        },
        "serviceId": "ai4bharat/conformer-hi-gpu--t4",
        "audioFormat": "flac",
        "samplingRate": 16000
      }
    },
    {
      "taskType": "translation",
      "config": {
        "language": {
          "sourceLanguage": "hi",
          "targetLanguage": "en"
        },
        "serviceId": "ai4bharat/indictrans-v2-all-gpu--t4"
      }
    }
  ],
  "inputData": {
    "audio": [
      {
        "audioContent": response
      }
    ]
  }
})
    headers = {
  'Accept': ' */*',
  'User-Agent': ' Thunder Client (https://www.thunderclient.com)',
  'Authorization': auth,
  'Content-Type': 'application/json'
}
    conn.request("POST", "/services/inference/pipeline", payload, headers)
    res = conn.getresponse()
    data = res.read()
    #print(data)
    return json.loads(data.decode("utf-8"))['pipelineResponse'][1]['output'][0]['target']

@functools.cache
def categorize(text):
    prompt=f"""Classify the below Text and provide Category,SubCategory,Priority(High/medium/low) and Confidence(0-1) in a JSON format:\n
Text: {text}

Categories : ['Online and Social Media Related Crime', 'Online Financial Fraud',
       'Online Gambling  Betting',
       'RapeGang Rape RGRSexually Abusive Content',
       'Any Other Cyber Crime', 'Cyber Attack/ Dependent Crimes',
       'Cryptocurrency Crime', 'Sexually Explicit Act',
       'Sexually Obscene material',
       'Hacking  Damage to computercomputer system etc',
       'Cyber Terrorism',
       'Child Pornography CPChild Sexual Abuse Material CSAM',
       'Online Cyber Trafficking', 'Ransomware',
       'Report Unlawful Content']

Sub Categories: ['Cyber Bullying  Stalking  Sexting', 'Fraud CallVishing',
       'Online Gambling  Betting', 'Online Job Fraud',
       'UPI Related Frauds', 'Internet Banking Related Fraud', nan,
       'Other', 'Profile Hacking Identity Theft',
       'DebitCredit Card FraudSim Swap Fraud', 'EWallet Related Fraud',
       'Data Breach/Theft', 'Cheating by Impersonation',
       'Denial of Service (DoS)/Distributed Denial of Service (DDOS) attacks',
       'FakeImpersonating Profile', 'Cryptocurrency Fraud',
       'Malware Attack', 'Business Email CompromiseEmail Takeover',
       'Email Hacking', 'Hacking/Defacement',
       'Unauthorised AccessData Breach', 'SQL Injection',
       'Provocative Speech for unlawful acts', 'Ransomware Attack',
       'Cyber Terrorism', 'Tampering with computer source documents',
       'DematDepository Fraud', 'Online Trafficking',
       'Online Matrimonial Fraud', 'Website DefacementHacking',
       'Damage to computer computer systems etc', 'Impersonating Email',
       'EMail Phishing', 'Ransomware', 'Intimidating Email',
       'Against Interest of sovereignty or integrity of India']

Format:{{
    "category":"",
    "subcategory":"",
    "Priority":"",
    "Confidence Score(Float)":""}}
"""

    response = model.generate_content(prompt,safety_settings={
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT:HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT:HarmBlockThreshold.BLOCK_NONE,
        
    })
    #print(response.text)
    p=response.text
    p=p.replace('`','')
    p=p.replace('json','')
    return p




def classify_complaint(video_file):
    text = split_and_encode_audio(video_file)
    t=''
    for i in text:
        t+= extract_audio_to_text(i)
    result = categorize(t)
    return result,t
def parse_response(response):
    
    # pairs = response.split(',')
    
    # # Create a dictionary to store the key-value pairs
    # result = {}
    
    # # Iterate over each pair and split by colon to get key and value
    # for pair in pairs:
    #     key, value = pair.split(':')
    #     result[key.strip()] = value.strip()  # Use strip() to remove extra spaces
    
    # # Convert the dictionary to JSON
   
    data = json.loads(response)
    category = data.get('category', 'Other')
    subcategory = data.get('subcategory', '')
    priority = data.get('Priority', 'Low')
    confidence_score = data.get('Confidence Score(Float)', 0.0)
    
    return {
        'category': category,
        'subcategory': subcategory,
        'priority': priority,
        'confidence_score': confidence_score
    }
