document.addEventListener("DOMContentLoaded", function () {
    const deviceSelect = document.getElementById("deviceSelect");
    const video = document.getElementById("video");
    const canvas = document.getElementById("canvas");
    const context = canvas.getContext("2d");

    async function listDevices() {
        try {
            const devices = await navigator.mediaDevices.enumerateDevices();
            const videoDevices = devices.filter(device => device.kind === "videoinput");
            deviceSelect.innerHTML = "";
            videoDevices.forEach(device => {
                const option = document.createElement("option");
                option.value = device.deviceId;
                option.text = device.label || `Camera ${deviceSelect.length + 1}`;
                deviceSelect.appendChild(option);
            });
        } catch (error) {
            console.error("Error listing devices:", error);
        }
    }

    async function startVideo(deviceId) {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ video: { deviceId: { exact: deviceId } } });
            video.srcObject = stream;
            video.play();
        } catch (error) {
            console.error("Error accessing webcam:", error);
        }
    }

    deviceSelect.addEventListener("change", function () {
        const selectedDeviceId = deviceSelect.value;
        startVideo(selectedDeviceId);
    });

    listDevices();
});
