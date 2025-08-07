
const recordButton = document.getElementById("recordButton");
const resultDiv = document.getElementById("result");

let mediaRecorder;
let chunks = [];

recordButton.addEventListener("mousedown", startRecording);
recordButton.addEventListener("touchstart", startRecording);
recordButton.addEventListener("mouseup", stopRecording);
recordButton.addEventListener("mouseleave", stopRecording);
recordButton.addEventListener("touchend", stopRecording);

function startRecording() {
  navigator.mediaDevices.getUserMedia({ audio: true }).then(stream => {
    mediaRecorder = new MediaRecorder(stream);
    mediaRecorder.start();

    chunks = [];
    mediaRecorder.ondataavailable = e => chunks.push(e.data);

    mediaRecorder.onstop = () => {
      const blob = new Blob(chunks, { type: "audio/webm" });
      const formData = new FormData();
      formData.append("audio_data", blob);

      fetch("/transcribe", { method: "POST", body: formData })
        .then(res => res.json())
        .then(data => {
          if (data.text) {
            resultDiv.textContent = data.text;
            speak(data.text);
          } else {
            resultDiv.textContent = "エラー: " + data.error;
          }
        });
    };
  });
}

function stopRecording() {
  if (mediaRecorder && mediaRecorder.state !== "inactive") {
    mediaRecorder.stop();
  }
}

function speak(text) {
  const utterance = new SpeechSynthesisUtterance(text);
  utterance.lang = "ja-JP";
  speechSynthesis.speak(utterance);
}
