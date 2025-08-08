const recButton = document.getElementById("recButton");
const status = document.getElementById("status");
const responseArea = document.getElementById("responseArea");

let mediaRecorder;
let audioChunks = [];

recButton.addEventListener("mousedown", startRecording);
recButton.addEventListener("mouseup", stopRecording);

function startRecording() {
    status.innerText = "録音中...";
    recButton.classList.add("recording");

    navigator.mediaDevices.getUserMedia({ audio: true })
        .then(stream => {
            mediaRecorder = new MediaRecorder(stream);
            audioChunks = [];
            mediaRecorder.ondataavailable = event => audioChunks.push(event.data);
            mediaRecorder.onstop = () => {
                const blob = new Blob(audioChunks, { type: "audio/webm" });
                const formData = new FormData();
                formData.append("audio", blob, "recording.webm");

                fetch("/transcribe", {
                    method: "POST",
                    body: formData
                })
                .then(res => res.json())
                .then(data => displayResponse(data.text))
                .catch(err => displayResponse("エラーが発生しました: " + err));
            };
            mediaRecorder.start();
        });
}

function stopRecording() {
    status.innerText = "処理中...";
    recButton.classList.remove("recording");
    if (mediaRecorder && mediaRecorder.state !== "inactive") {
        mediaRecorder.stop();
    }
}

function sendText() {
    const text = document.getElementById("textInput").value;
    if (!text) return;
    status.innerText = "送信中...";
    fetch("/textquery", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: text })
    })
    .then(res => res.json())
    .then(data => displayResponse(data.text))
    .catch(err => displayResponse("エラーが発生しました: " + err));
}

function displayResponse(text) {
    status.innerText = "完了";
    responseArea.innerText = text;
    const utterance = new SpeechSynthesisUtterance(text);
    speechSynthesis.speak(utterance);
}