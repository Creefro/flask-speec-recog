from distutils.log import debug
from fileinput import filename
import os
import sounddevice as sd
import soundfile as sf
from flask import *
import pyaudio
import wave

app = Flask(__name__)

@app.route('/')
def main():
	return render_template("upload.html")

@app.route('/success', methods = ['POST'])
def success():
	if request.method == 'POST':
		f = request.files['file']
		f.save(f.filename)
		return render_template("Acknowledgement.html", name = f.filename)
        

# Specify the upload folder for the recorded audio files
app.config['UPLOAD_FOLDER'] = 'uploads'

# Function to start recording audio from the user's microphone
def start_recording():
    duration = 5  # Record for 5 seconds
    fs = 44100  # Sample rate
    myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()  # Wait for the recording to finish
    return myrecording, fs

@app.route('/mic_record')
def mic_record():
        FRAMES_PER_BUFFER = 3200
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 16000
        p = pyaudio.PyAudio()
        
        # starts recording
        stream = p.open(
                format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=FRAMES_PER_BUFFER
        )

        print("start recording...")

        frames = []
        seconds = 5
        for i in range(0, int(RATE / FRAMES_PER_BUFFER * seconds)):
                data = stream.read(FRAMES_PER_BUFFER)
                frames.append(data)

        print("recording stopped")

        stream.stop_stream()
        stream.close()
        p.terminate()


        wf = wave.open("asdqwe.wav", 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()
        return render_template('upload.html')


# Route to handle the record button
@app.route('/record', methods=['POST'])
def record():
    # Start recording
    recording, fs = start_recording()

    # Save the recording to a .wav file
    filename = 'recording.wav'
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    sf.write(filepath, recording, fs)

    # Redirect to the file download page
    return redirect(url_for('download', filename=filename))

# Route to download the recorded audio file
@app.route('/download/<filename>')
def download(filename):
    return render_template('download.html', filename=filename)


if __name__ == '__main__':
	app.run(debug=True)
