import librosa
from flask import *
import pyaudio
import wave
import numpy as np
import plotly.graph_objs as go
import plotly.io as pio
import os
from glob import glob
import threading

app = Flask(__name__)

@app.route('/')
def main():
	return render_template("index.html")



@app.route('/get_last_recorded_filename')
def get_last_recorded_filename():
    file_pattern = "record*.wav" # change this to match your file naming convention
    files = glob(file_pattern)
    if not files:
        return ""
    files = sorted(files, key=lambda f: int(os.path.splitext(f)[0][len("record"):]), reverse=True)
    return files[0]

FRAMES_PER_BUFFER = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 16000
@app.route('/mic_record/<action>')
def mic_record(action):
    is_recording = False
    global frames,stream
    print(action)
    if action == 'start':
        if not is_recording:
            
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
            is_recording = True
            frames = []

            # start a new thread to continuously read frames from the stream and append to the frames list
            def read_frames():
                while is_recording:
                    if stream.is_stopped():
                        break
                    data = stream.read(FRAMES_PER_BUFFER)
                    frames.append(data)

            threading.Thread(target=read_frames).start()

    elif action == 'stop':
            if is_recording:
                print("recording stopped")
                is_recording = False
            p = pyaudio.PyAudio()

            # stop the stream and terminate the PyAudio object
            stream.stop_stream()
            stream.close()
            p.terminate()

            # write the frames to a WAV file
            recfilename = "record" + str(len(os.listdir())) + ".wav"
            wf = wave.open(recfilename, 'wb')
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(p.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))
            wf.close()

    else:
        print("not recording")
    return ""

@app.route('/prediction', methods = ['POST'])
def success():
    if request.method == 'POST':
        data = request.form['audio_name']
        print(data)
        waveform_html, spectrogram_html = generate_plots(data)
        return render_template("prediction.html", name=data, waveform_html=waveform_html, spectrogram_html=spectrogram_html)


def generate_plots(filename):
    # Load audio file
    y, sr = librosa.load(filename)

    # Plot waveform
    waveform_fig = go.Figure()
    waveform_fig.add_trace(go.Scatter(x=np.arange(len(y))/sr, y=y))
    waveform_fig.update_layout(title="Waveform", xaxis_title="Time (seconds)", yaxis_title="Amplitude")
    waveform_html = pio.to_html(waveform_fig, full_html=False)

    # Plot spectrogram
    D = librosa.stft(y)
    DB = librosa.amplitude_to_db(abs(D))
    spectrogram_fig = go.Figure()
    spectrogram_fig.add_trace(go.Heatmap(x=np.arange(DB.shape[1])/sr, y=np.arange(DB.shape[0]), z=DB))
    spectrogram_fig.update_layout(title="Spectrogram", xaxis_title="Time (seconds)", yaxis_title="Frequency (Hz)")
    spectrogram_html = pio.to_html(spectrogram_fig, full_html=False)

    return waveform_html, spectrogram_html

if __name__ == '__main__':
	app.run(debug=True)
