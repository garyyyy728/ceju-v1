document.addEventListener("DOMContentLoaded", function () {
    const video = document.getElementById("video");
    const canvas = document.getElementById("canvas");
    const context = canvas.getContext("2d");
    const resultsElement = document.getElementById("results");
    const startButton = document.getElementById("startButton");
    const stopButton = document.getElementById("stopButton");

    let stream = null;
    let animationFrameId = null;

    async function startVideo() {
        try {
            stream = await navigator.mediaDevices.getUserMedia({ video: true });
            video.srcObject = stream;
            video.play();
            detectObjects();
        } catch (error) {
            console.error("Error accessing webcam:", error);
        }
    }

    function stopVideo() {
        if (stream) {
            stream.getTracks().forEach(track => track.stop());
            stream = null;
        }
        if (animationFrameId) {
            cancelAnimationFrame(animationFrameId);
            animationFrameId = null;
        }
        context.clearRect(0, 0, canvas.width, canvas.height);
        resultsElement.textContent = "";
    }

    async function detectObjects() {
        if (!stream) return;

        context.drawImage(video, 0, 0, canvas.width, canvas.height);
        const imageData = canvas.toDataURL("image/jpeg");

        try {
            const response = await fetch("/detect", {
                method: "POST",
                body: JSON.stringify({ image: imageData }),
                headers: { "Content-Type": "application/json" }
            });
            const detections = await response.json();
            displayDetections(detections);
        } catch (error) {
            console.error("Error detecting objects:", error);
        }

        animationFrameId = requestAnimationFrame(detectObjects);
    }

    function displayDetections(detections) {
        context.clearRect(0, 0, canvas.width, canvas.height);
        context.drawImage(video, 0, 0, canvas.width, canvas.height);

        detections.forEach(detection => {
            const { xmin, ymin, xmax, ymax, name, confidence } = detection;
            context.strokeStyle = "red";
            context.lineWidth = 2;
            context.strokeRect(xmin, ymin, xmax - xmin, ymax - ymin);
            context.fillStyle = "red";
            context.font = "16px Arial";
            context.fillText(`${name} (${(confidence * 100).toFixed(2)}%)`, xmin, ymin - 5);
        });

        resultsElement.textContent = JSON.stringify(detections, null, 2);
    }

    startButton.addEventListener("click", startVideo);
    stopButton.addEventListener("click", stopVideo);
});
