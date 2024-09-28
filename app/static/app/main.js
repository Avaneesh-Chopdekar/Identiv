const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;
const video = document.getElementById("video");
if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
  navigator.mediaDevices.getUserMedia({ video: true }).then(function (stream) {
    video.srcObject = stream;
  });
}

const dialog = document.getElementById("notification-dialog");
const dialogMessageBox = document.querySelector(".message");
const dialogMessageBody = document.querySelector(".message-body");
const closeNotificationBtn = document.getElementById("close-notification");

document.getElementById("loginBtn").addEventListener("click", function () {
  const canvas = document.createElement("canvas");
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  const ctx = canvas.getContext("2d");
  ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
  const imageData = canvas.toDataURL("image/jpeg");

  // Send the captured image to the server
  fetch(`${window.location.href}face-login/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
      "X-CSRFToken": csrfToken,
    },
    body: new URLSearchParams({
      image_data: imageData,
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      if (!dialog.open) {
        if (data.status === "error") {
          dialogMessageBox.classList.add("is-danger");
          dialogMessageBox.classList.remove("is-success");
        } else {
          dialogMessageBox.classList.add("is-success");
          dialogMessageBox.classList.remove("is-danger");
        }
        dialogMessageBody.textContent = data.message;
        dialog.showModal();
        setTimeout(() => {
          dialog.close();
        }, 5000);
      }
    });
});

closeNotificationBtn.addEventListener("click", () => {
  dialog.close();
});
