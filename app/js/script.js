document.querySelectorAll('.audio-controls').forEach(audioControl => {
  let playBtn = audioControl.querySelector('.play-pause-btn')
  let audio = audioControl.querySelector('.song-audio')

  playBtn.addEventListener('click', event => {
    const isPlaying = audioControl.classList.contains('play');

    if (isPlaying) {
      pauseSong(audio, audioControl, playBtn);
    } else {
      playSong(audio, audioControl, playBtn);
    }
  })
})

// Play song
function playSong(audio, audioControl, playBtn) {
  audioControl.classList.add('play');
  playBtn.querySelector('i.fas').classList.remove('fa-play');
  playBtn.querySelector('i.fas').classList.add('fa-pause');

  audio.play();
}

// Pause song
function pauseSong(audio, audioControl, playBtn) {
  audioControl.classList.remove('play');
  playBtn.querySelector('i.fas').classList.add('fa-play');
  playBtn.querySelector('i.fas').classList.remove('fa-pause');

  audio.pause();
}
