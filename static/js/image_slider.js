document.addEventListener("DOMContentLoaded", function () {
  const imagPreview = document.getElementById("image-preview");
  const prevBtn = document.getElementById("prevBtn");
  const nextBtn = document.getElementById("nextBtn");

  const images = [
    "https://images.pexels.com/photos/2305761/pexels-photo-2305761.jpeg?auto=compress&cs=tinysrgb&w=600",
    "https://images.pexels.com/photos/811587/pexels-photo-811587.jpeg?auto=compress&cs=tinysrgb&w=600",
    "https://images.pexels.com/photos/1191403/pexels-photo-1191403.jpeg?auto=compress&cs=tinysrgb&w=600",
    "https://images.pexels.com/photos/1028708/pexels-photo-1028708.jpeg?auto=compress&cs=tinysrgb&w=600",
    "https://images.pexels.com/photos/2072867/pexels-photo-2072867.jpeg?auto=compress&cs=tinysrgb&w=600",
    "https://images.pexels.com/photos/2550703/pexels-photo-2550703.jpeg?auto=compress&cs=tinysrgb&w=600",
    "https://images.pexels.com/photos/6681862/pexels-photo-6681862.jpeg?auto=compress&cs=tinysrgb&w=600",
    "https://images.pexels.com/photos/2836945/pexels-photo-2836945.jpeg?auto=compress&cs=tinysrgb&w=600",
    "https://images.pexels.com/photos/461431/pexels-photo-461431.jpeg?auto=compress&cs=tinysrgb&w=600",
    "https://images.pexels.com/photos/5047013/pexels-photo-5047013.jpeg?auto=compress&cs=tinysrgb&w=600",
  ]

  let currentIdx = 0;

  function updateImage() {
    imagPreview.src = images[currentIdx];
  }

  function nextImage() {
    currentIdx = (currentIdx + 1) % images.length;
    updateImage();
  }

  function prevImage() {
    currentIdx = (currentIdx - 1 + images.length) % images.length;
    updateImage();
  }

  nextBtn.addEventListener("click", nextImage);
  prevBtn.addEventListener("click", prevImage);

  // Auto slide every 2 seconds
  const intervalId = setInterval(nextImage, 2000);

  // Stop auto slide when clicking on next or prev buttons
  nextBtn.addEventListener("click", () => clearInterval(intervalId));
  prevBtn.addEventListener("click", () => clearInterval(intervalId));
});

