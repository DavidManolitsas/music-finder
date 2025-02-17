// search bar
input = document.getElementById('search-bar');
baseUrl = "https://itunes.apple.com";


async function queryItunesApi(url) {
  const response = await fetch(url, {
    method: 'GET',
    mode: 'cors'
  })

  let data = await response.json();
  return data.results
}


async function getRelevantItunesArtists(searchTerm) {
  let url = baseUrl.concat("/search?term=").concat(searchTerm.replaceAll(" ", "+")).concat("&entity=musicArtist&limit=5")
  return await queryItunesApi(url)
}


async function getItunesArtist(searchTerm) {
  let url = baseUrl.concat("/search?term=").concat(searchTerm.replaceAll(" ", "+")).concat("&entity=musicArtist")
  let artists = await queryItunesApi(url)

  if (artists.length > 1) {
    for (const artist of artists) {
      if (artist.artistName === searchTerm) {
        return artist
      }
    }
  }

  return artists[0]
}


async function getArtistsSongs(artist) {
  // get artists itunes id
  let artistId;
  if ("amgArtistId" in artist) {
    artistId = "amgArtistId=" + artist.amgArtistId;
  } else {
    artistId = "id=" + artist.artistId;
  }

  let songUrl = baseUrl.concat("/lookup?").concat(artistId).concat("&entity=song")
  let songs = await queryItunesApi(songUrl)
  songs.shift()

  let albumUrl = baseUrl.concat("/lookup?").concat(artistId).concat("&entity=album")
  let albums = await queryItunesApi(albumUrl)
  albums.shift()

  return songs.concat(albums)
}


async function setSongGrid(artist, newReleases) {
  if (newReleases.length > 0) {
    let songCardHtml = ""
    newReleases.forEach(release => {
      let songImageUrl = release.artworkUrl100
      songImageUrl = songImageUrl.replaceAll("100x100", "600x600")

      let songName
      if ("trackCensoredName" in release) {
        songName = release.trackCensoredName
      } else {
        songName = release.collectionName
      }

      songName = songName.replace(" - Single", "").replace(" (Extended Mix)", "")

      songCardHtml += "<div class=\"song-card\">\n"
      songCardHtml += "    <img class=\"song-image\" src=\"" + songImageUrl + "\" width=\"300\" height=\"300\" alt=\"" + songName + "cover image\">\n"
      songCardHtml += "    <div class=\"card-container\">\n"
      songCardHtml += "        <div class=\"song-info\">\n"
      songCardHtml += "            <p class=\"song-title\">" + songName + "</p>\n"
      songCardHtml += "            <a href=\"" + artist.artistLinkUrl + "\"><p class=\"song-artist\">" + release.artistName + "</p></a>\n"
      songCardHtml += "        </div>\n"

      if (release.previewUrl != null) {
        songCardHtml += "        <div class=\"audio-controls\">\n"
        songCardHtml += "            <audio class=\"song-audio\" src=\"" + release.previewUrl + "\" type=\"audio/mpeg\">\n"
        songCardHtml += "            </audio>\n"
        songCardHtml += "            <button class=\"play-pause-btn\">\n"
        songCardHtml += "                <i class=\"fas fa-play\"></i><span class=\"play-pause-txt\" >Play</span>\n"
        songCardHtml += "            </button>\n"
        songCardHtml += "        </div>\n"
      }
      songCardHtml += "    </div>\n"
      songCardHtml += "</div>\n"
    })

    document.getElementById("song-grid").innerHTML = songCardHtml
    document.getElementById("search-results").innerHTML = ""
    document.querySelectorAll('.audio-controls').forEach(audioControl => {
      setAudioControls(audioControl)
    })
  } else {
    document.getElementById(
        "search-results").innerHTML = "No songs found for artist "
        + artist.artistName
    document.getElementById("song-grid").innerHTML = ""
  }
}


function filterSongs(releases) {
  let filteredReleases = []

  for (let newRelease1 in releases){
    for (let newRelease2 in releases) {
      if (newRelease1.song === newRelease2.song) {
        if ("preview" in newRelease2) {
          filteredReleases.push(newRelease2)
        } else {
          filteredReleases.push(newRelease1)
        }
        break
      }
    }
  }

  return filteredReleases
}


async function setSearchResults(searchTerm) {
  let artists = await getRelevantItunesArtists(searchTerm)
  const artistIds = []
  artistListHtml = "<ul>\n"
  for (const artist of artists) {
    artistListHtml += "    <li id=\"" + artist.artistId + "\">" + artist.artistName + "</li>\n"
    artistIds.push(artist.artistId.toString())
  }
  artistListHtml += "</ul>\n"
  document.getElementById('search-results').innerHTML = artistListHtml

  if (artistIds.length < 1) {
    document.getElementById('search-results').innerHTML = "No results found for " + searchTerm
  }

  for (const id of artistIds) {
    document.getElementById(id).addEventListener('click', event => {
      search(id).catch(function() {
        document.getElementById('search-results').innerHTML = "iTunes API call failed";
      });
    })
  }
}


async function search(searchTerm) {
  let artist = await getItunesArtist(searchTerm)

  if (artist) {
    console.log(artist)
    let songs = await getArtistsSongs(artist)

    let today = new Date()
    let startDate = today.setDate(today.getDate() - 93)
    let cutOffDate = today.setDate(today.getDate() + 365)

    const newReleases = []

    for (const song of songs) {
      let releaseDate = new Date(song.releaseDate)
      if (startDate < releaseDate) {
        if (releaseDate < cutOffDate) {
          newReleases.push(song)
        }
      }
    }

    // TODO: filter song releases to remove duplicates in search results
    // let filteredReleases = filterSongs(newReleases)
    await setSongGrid(artist, newReleases)
  }
}


function setAudioControls(audioControl) {
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
}


// Play song
function playSong(audio, audioControl, playBtn) {
  audioControl.classList.add('play');
  playBtn.querySelector('i.fas').classList.remove('fa-play');
  playBtn.querySelector('i.fas').classList.add('fa-pause');
  playBtn.querySelector('.play-pause-txt').innerText = "Pause";

  audio.play();
}


// Pause song
function pauseSong(audio, audioControl, playBtn) {
  audioControl.classList.remove('play');
  playBtn.querySelector('i.fas').classList.add('fa-play');
  playBtn.querySelector('i.fas').classList.remove('fa-pause');
  playBtn.querySelector('.play-pause-txt').innerText = "Play";

  audio.pause();
}


// play music
document.querySelectorAll('.audio-controls').forEach(audioControl => {
  setAudioControls(audioControl)
})


// search bar event
input.addEventListener("keyup", async function searchEvent(event) {
  if (event.key === "Enter") {
    let searchTerm = input.value
    if (searchTerm) {
      await setSearchResults(searchTerm).catch(function() {
        document.getElementById('search-results').innerHTML = "iTunes API call failed with search \"" + searchTerm + "\"";
      });
      input.value = ''
    }
  }
});

// navigation menu for record labels
function openNav() {
  document.getElementById("record-label-nav").style.width = "100%";
}

// Close when someone clicks on the "x" symbol inside the overlay
function closeNav() {
  document.getElementById("record-label-nav").style.width = "0%";
}
