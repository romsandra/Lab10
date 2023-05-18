import pyttsx3, pyaudio, vosk
import json, requests
import webbrowser

tts = pyttsx3.init('sapi5')

voices = tts.getProperty('voices')
tts.setProperty('voices', 'en')

for voice in voices:
    print(voice.name)
    if voice.name == 'Microsoft Zira Desktop - English (United States)':
        tts.setProperty('voice', voice.id)

model = vosk.Model('vosk-model-small-en-us-0.15')
record = vosk.KaldiRecognizer(model, 16000)
pa = pyaudio.PyAudio()
stream = pa.open(format=pyaudio.paInt16,
                 channels=1,
                 rate=16000,
                 input=True,
                 frames_per_buffer=8000)
stream.start_stream()


def listen():
    while True:
        data = stream.read(4000, exception_on_overflow=False)
        if record.AcceptWaveform(data) and len(data) > 0:
            answer = json.loads(record.Result())
            if answer['text']:
                yield answer['text']


def speak(say):
    tts.say(say)
    tts.runAndWait()

def meaning(word):
    try:
        response = requests.get(f'https://api.dictionaryapi.dev/api/v2/entries/en/{word}')
        data = response.json()
        print(data[0]['meanings'][0]['definitions'][0]['definition'])
        speak(data[0]['meanings'][0]['definitions'][0]['definition'])
    except Exception:
        print('Meaning not found')
        speak('Meaning not found')

def save(word):
    response = requests.get(f'https://api.dictionaryapi.dev/api/v2/entries/en/{word}')
    data = response.json()
    with open("word.txt", "w") as f:
        json.dump(data, f)
    print("The data is saved to a file word.txt")
    speak("The data is saved to a file word.txt")

def example(word):
    try:
        response = requests.get(f'https://api.dictionaryapi.dev/api/v2/entries/en/{word}')
        data = response.json()
        print(data[0]['meanings'][0]['definitions'][0]['example'])
        speak(data[0]['meanings'][0]['definitions'][0]['example'])
    except Exception:
        print('Example not found')
        speak('Example not found')

def link(word):
    try:
        speak('I open the link in the browser')
        webbrowser.open_new(f'https://api.dictionaryapi.dev/api/v2/entries/en/{word}')
    except Exception:
        print('Link not found')
        speak('Link not found')


for speech in listen():
    if 'find' in speech:
        text = speech.split("find ")[1]
        try:
            response = requests.get(f'https://api.dictionaryapi.dev/api/v2/entries/en/{text}')
            data = response.json()
            print(data['message'])
        except Exception:
            print('The word', text, 'was found')
            speak(f'The word {text} was found')
    elif 'meaning' in speech:
        meaning(text)
    elif 'example' in speech:
        example(text)
    elif 'save' in speech:
        save(text)
    elif 'link' in speech:
        link(text)
    elif 'exit' or 'bye' in speech:
        speak('bye')
        exit()
    else:
        print('The command is not recognized')
        speak('error')