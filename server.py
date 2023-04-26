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
        

@app.route('/mic_record')
def mic_record():
        FRAMES_PER_BUFFER = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 2
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
        seconds = 10
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

if __name__ == '__main__':
	app.run(debug=True)
