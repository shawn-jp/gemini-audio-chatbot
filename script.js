let mediaRecorder;
let audioChunks = [];

const button = document.getElementById("recordButton");
const responseDiv = document.getElementById("response");

button.addEventListener("mousedown", async () => {
  const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
  mediaRecorder = new MediaRecorder(stream);
  audioChunks = [];

  mediaRecorder.addEventListener("dataavailable", event => {
    audioChunks.push(event.data);
  });

  mediaRecorder.addEventListener("stop", async () => {
    const audioBlob = new Blob(audioChunks, { type: "audio/webm" });
    const formData = new FormData();
    formData.append("audio", audioBlob);

    responseDiv.textContent = "🕒 応答中...";

    const res = await fetch("/transcribe", {
      method: "POST",
      body: formData,
    });

    const data = await res.json();
    responseDiv.textContent = data.reply;
  });

  mediaRecorder.start();
  responseDiv.textContent = "🎙️ 録音中…";
});

button.addEventListener("mouseup", () => {
  mediaRecorder.stop();
});