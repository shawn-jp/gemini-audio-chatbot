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
  navigator.mediaDevices.getUserMedia({ audio: true }).then(stream => {
    mediaRecorder = new MediaRecorder(stream);
    mediaRecorder.start();
    chunks = [];

    mediaRecorder.ondataavailable = e => chunks.push(e.data);
    mediaRecorder.onstop = () => {
      const blob = new Blob(chunks, { type: 'audio/webm' });
      const formData = new FormData();
      formData.append('audio', blob);

      fetch('/transcribe', {
        method: 'POST',
        body: formData
      })
      .then(res => res.json())
      .then(data => {
        document.getElementById("result").innerText = data.response || "エラー";
      });
    };
  });
}

function stopRec() {
  if (mediaRecorder && mediaRecorder.state !== "inactive") {
    mediaRecorder.stop();
  }
}