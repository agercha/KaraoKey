// from https://github.com/Mido22/MediaRecorder-sample

'use strict'

function sendData() {
  // blank, for now!
}

function getCSRFToken() {
  let cookies = document.cookie.split(";")
  for (let i = 0; i < cookies.length; i++) {
      let c = cookies[i].trim()
      if (c.startsWith("csrftoken=")) {
          return c.substring("csrftoken=".length, c.length)
      }
  }
  return "unknown"
}

let log = console.log.bind(console),
  id = val => document.getElementById(val),
  ul = id('ul'),
  request_button = id('request_button'),
  start = id('start'),
  stop = id('stop'),
  stream,
  recorder,
  counter=1,
  chunks,
  media;

request_button.onclick = e => {
// body.onload = e => {
  media = {
      tag: 'audio',
      type: 'audio/wav',
      ext: '.wav',
      selector: {audio: true}
    };

  navigator.mediaDevices.getUserMedia(media.selector).then(_stream => {
    stream = _stream;
    id('selection_area').style.display = 'none';
    id('buttons_area').style.display = 'inherit';
    start.removeAttribute('disabled');
    recorder = new MediaRecorder(stream);

    recorder.ondataavailable = e => {
      chunks.push(e.data);

      // save chunk
      // change to Blob.slice
      const full_blob = new Blob(chunks , {type: "audio/wav"});
      const small_blob = full_blob.slice(start=-10)
      // change filename
      const full_file = new File( [ full_blob ], "full_file.wav", { type: "audio/wav"} );
      const small_file = new File( [ small_blob ], "small_file.wav", { type: "audio/wav"} );

      let data = new FormData();
      data.append("csrfmiddlewaretoken", getCSRFToken())
      data.append("full_recorded_audio", full_file)
      data.append("small_recorded_audio", small_file)

      // send request to python
      let xhr = new XMLHttpRequest()
      xhr.onreadystatechange = function() {
          if (this.readyState != 4) return
          updatePage(xhr) // create this function
      }
      xhr.open("POST", "get-pitch", true)
      xhr.send(data)

      if(recorder.state == 'inactive')  makeLink();
    };

  }).catch(log);

}

function updatePage(xhr) {
  if (xhr.status == 200) {
    let response = JSON.parse(xhr.responseText)
    processResponse(response)
    return
  }
}

function processResponse(response) {
  document.getElementById("result").innerHTML = response[0]['curr_pitch']
}

start.onclick = e => {
  start.disabled = true;
  stop.removeAttribute('disabled');
  chunks=[];
  recorder.start(2000);
}


stop.onclick = e => {
  stop.disabled = true;
  recorder.stop();
  start.removeAttribute('disabled');
}

function makeLink(){
  let blob = new Blob(chunks, {type: media.type })
    , url = URL.createObjectURL(blob)
    , li = document.createElement('li')
    , mt = document.createElement(media.tag)
  ;
  mt.controls = true;
  mt.src = url;
  li.appendChild(mt);
  ul.innerHTML = "";
  ul.appendChild(li);
  document.getElementById("result").innerHTML = "";
}
