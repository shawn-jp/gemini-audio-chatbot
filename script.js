let btn = document.getElementById("recordButton");
let mediaRecorder;
let chunks = [];

btn.addEventListener("mousedown", startRec);
btn.addEventListener("mouseup", stopRec);
btn.addEventListener("touchstart", function(e) {
  e.preventDefault();
  startRec();
});
btn.addEventListener("touchend", stopRec);

function startRec() {
  btn.src = "rec_button_active.png";
  navigator.mediaDevices.getUserMedia({ audio: true }).then(stream => {
    mediaRecorder = new MediaRecorder(stream);
    mediaRecorder.start();
    chunks = [];

    mediaRecorder.ondataavailable = e => chunks.push(e.data);
    mediaRecorder.onstop = () => {
      btn.src = "rec_button.png";
      const blob = new Blob(chunks, { type: 'audio/webm' });
      const formData = new FormData();
      formData.append('audio', blob);

      fetch('/transcribe', {
        method: 'POST',
        body: formData
      })
      .then(res => res.json())
      .then(data => showResponse(data.response || "エラー"));
    };
  }).catch(err => {
    btn.src = "rec_button.png";
    alert("録音に失敗しました");
  });
}

function stopRec() {
  if (mediaRecorder && mediaRecorder.state !== "inactive") {
    mediaRecorder.stop();
  }
}

document.getElementById("textForm").addEventListener("submit", function(e) {
  e.preventDefault();
  const text = document.getElementById("textInput").value;
  fetch("/transcribe", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({ text })
  })
  .then(res => res.json())
  .then(data => showResponse(data.response || "エラー"));
});

function showResponse(text) {
  document.getElementById("result").innerText = text;
  const utter = new SpeechSynthesisUtterance(text);
  speechSynthesis.speak(utter);
}