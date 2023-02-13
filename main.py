from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import FileResponse
import uvicorn
import tempfile
import json
import os
import fakeyou
from model import load_json

fy = fakeyou.FakeYou()
fy.login( os.environ['USERNAME'], os.environ['PASSWORD'])

app = FastAPI()
list_person = load_json('person.json') 
model_token = load_json('model_token.json') 

@app.get('/')
def main():
  return {'status' : True,
         '/speak' : {
           'text' : 'string',
           'person' : list_person 
         }}

@app.get('/speak')
async def textToSpeech(text: str = Query(..., min_length=1),
                       person: int = Query(...)):
  try:
    person_found = False
    
    for name, id in list_person.items():
      
      if person == int(id):
        person_found = True
        
        token = model_token[name]
        with tempfile.NamedTemporaryFile() as tf:
          file_name = tf.name + '.mp3'
          fy.say(text=text, ttsModelToken=token, filename=file_name)
          return FileResponse(file_name)
          
    if not person_found:
        return { "status": False, "message": "id person tidak ditemukan"}
    
  except fakeyou.exception.TooManyRequests:
        return { "status": False, "message": "terlalu banyak permintaan, coba beberapa saat lagi"}
    
  except fakeyou.exception.TtsAttemptFailed:
        return { "status": False, "message": "mungkin textnya tidak mendukung"}

@app.get('/get-person')
def get_person():
  return list_person
  

if __name__ == "__main__":

    uvicorn.run(app, host="0.0.0.0", port=8000)