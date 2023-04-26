const recordBtn = document.querySelector(".record");



let recording = false;

function ExecPythonCommand(pythonCommand){
  var request = new XMLHttpRequest()
  request.open("GET", "/" + pythonCommand, true)
  request.send()
}

function startRecording() {
  ExecPythonCommand('mic_record/start');
  recordBtn.classList.add("recording");
  recordBtn.querySelector("p").innerHTML = "Listening...";
  recording = true;
}

function stopRecording() {
  ExecPythonCommand('mic_record/stop');
  recordBtn.querySelector("p").innerHTML = "Start Listening";
  recordBtn.classList.remove("recording");
  recording = false;
  var checkInterval = setInterval(function() {
    var request = new XMLHttpRequest();
    request.open("GET", "/get_last_recorded_filename", true);
    request.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
        var fileName = this.responseText;
        if (fileName) {
          fileNameDisplay.textContent = "File: " + fileName;
          clearInterval(checkInterval);
        }
      }
    };
    request.send();
  }, 500);
}


const fileInput = document.getElementById('file-input');
const fileNameDisplay = document.getElementById('audioname');

recordBtn.addEventListener("click", () => {
  if (!recording) {
    startRecording();
  } else {
    stopRecording();
  }
});


  fileInput.addEventListener('change', function() {
    fileNameDisplay.textContent = 'File: ' + this.files[0].name;
  });


function download() {
  const text = result.innerText;
  const filename = "speech.txt";
  const audioBlob = new Blob(chunks, { type: "audio/mpeg" }); // değişiklik yapıldı
  const audioUrl = window.URL.createObjectURL(new Blob(chunks, {type: 'audio/mpeg'}));
  const audioFilename = "speech.mp3"; // uzantı .mp3 olarak değiştirildi

  const element = document.createElement("a");
  element.setAttribute(
    "href",
    "data:text/plain;charset=utf-8," + encodeURIComponent(text)
  );
  element.setAttribute("download", filename);
  element.style.display = "none";
  document.body.appendChild(element);
  element.click();
  document.body.removeChild(element);

  const audioElement = document.createElement("a");
  audioElement.setAttribute("href", audioUrl);
  audioElement.setAttribute("download", audioFilename);
  audioElement.style.display = "none";
  document.body.appendChild(audioElement);
  audioElement.click();
  document.body.removeChild(audioElement);
}



downloadBtn.addEventListener("click", download);

clearBtn.addEventListener("click", () => {
  result.innerHTML = "";
  downloadBtn.disabled = true;
});
