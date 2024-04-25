document.addEventListener('DOMContentLoaded', function() {
  const audioPlayer = document.getElementById('audioPlayer');
  const playPauseBtn = document.getElementById('playPauseBtn');
  const muteBtn = document.getElementById('muteBtn');
  const progressBar = document.querySelector('.audio-progress-bar');
  const currentTimeDisplay = document.getElementById('currentTime');
  const totalTimeDisplay = document.getElementById('totalTime');

  playPauseBtn.addEventListener('click', () => {
      if (audioPlayer.paused || audioPlayer.ended) {
          audioPlayer.play();
          playPauseBtn.innerHTML = '<i class="fas fa-pause"></i>';
      } else {
          audioPlayer.pause();
          playPauseBtn.innerHTML = '<i class="fas fa-play"></i>';
      }
  });

  muteBtn.addEventListener('click', () => {
      if (audioPlayer.muted) {
          audioPlayer.muted = false;
          muteBtn.innerHTML = '<i class="fas fa-volume-up"></i>';
      } else {
          audioPlayer.muted = true;
          muteBtn.innerHTML = '<i class="fas fa-volume-off"></i>';
      }
  });

  audioPlayer.addEventListener('timeupdate', () => {
      const currentTime = formatTime(audioPlayer.currentTime);
      const totalTime = formatTime(audioPlayer.duration);
      currentTimeDisplay.textContent = currentTime;
      totalTimeDisplay.textContent = totalTime;
      const progress = (audioPlayer.currentTime / audioPlayer.duration) * 100;
      progressBar.style.width = `${progress}%`;
  });

  function formatTime(time) {
      const minutes = Math.floor(time / 60);
      let seconds = Math.floor(time % 60);
      seconds = (seconds < 10) ? `0${seconds}` : seconds;
      return `${minutes}:${seconds}`;
  }
});
