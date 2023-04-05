// from https://github.com/Mido22/MediaRecorder-sample

'use strict'

// import { saveAs } from 'file-saver';

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
      type: 'audio/wav; codecs=opus',
      ext: '.wav',
      selector: {audio: true}
    };

  navigator.mediaDevices.getUserMedia(media.selector).then(_stream => {
    stream = _stream;
    id('selection_area').style.display = 'none';
    id('buttons_area').style.display = 'inherit';
    start.removeAttribute('disabled');
    const opt = {
      mimeType : "audio/wav; codecs=opus",
      // audioBitsPerSecond: 44100*1*1, // sample rate * bit depth * No. of channels
    };
    // recorder = new MediaRecorder(stream);
    recorder = new Recorder(stream)

    recorder.ondataavailable = e => {
      chunks.push(e.data);

      // save chunk
      // change to Blob.slice
      const full_blob = new Blob(chunks , {type: media.type});
      // saveAs(full_blob, "blob.wav");
      const small_blob = full_blob.slice(start=-10)
      // change filename
      const full_file = new File( [ full_blob ], "full_file.wav", { type: media.type} );
      const small_file = new File( [ small_blob ], "small_file.wav", { type: media.type} );

      // https://stackoverflow.com/questions/55202250/persisting-recorded-audio-from-browser-to-python-api-as-wav-file
      let reader = new FileReader();
      // reader.readAsDataURL(full_blob);
      // reader.onloadend = () => {
      //   let base64data = reader.result;

      let data = new FormData();
      data.append("csrfmiddlewaretoken", getCSRFToken())
      data.append("full_recorded_audio", full_file)
      data.append("small_recorded_audio", small_file)
      // data.append("base64data", base64data)

      // send request to python
      let xhr = new XMLHttpRequest()
      xhr.onreadystatechange = function() {
          if (this.readyState != 4) return
          updatePage(xhr) // create this function
      }
      xhr.open("POST", "get-pitch", true)
      xhr.send(data)
      // }

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
  recorder.start(1000);
}


stop.onclick = e => {
  stop.disabled = true;
  recorder.stop();
  recorder.exportWAV(createDownloadLink);

  // start.removeAttribute('disabled');
  start['disabled'] = false;
}

// https://blog.addpipe.com/using-recorder-js-to-capture-wav-audio-in-your-html5-web-site/
function createDownloadLink(blob) {
  Recorder.forceDownload(blob, "dummydummy.wav");
  return

  var url = URL.createObjectURL(blob);
  var au = document.createElement('audio');
  var li = document.createElement('li');
  var link = document.createElement('a');
  //add controls to the <audio> element 
  au.controls = true;
  au.src = url;
  //link the a element to the blob 
  link.href = url;
  link.download = new Date().toISOString() + '.wav';
  link.innerHTML = link.download;
  //add the new audio and a elements to the li element 
  li.appendChild(au);
  li.appendChild(link);
  //add the li element to the ordered list 
  
  var filename = new Date().toISOString();
  //filename to send to server without extension 
  //upload link 
  var upload = document.createElement('a');
  upload.href = "#";
  upload.innerHTML = "Upload";
  upload.addEventListener("click", function(event) {
      var xhr = new XMLHttpRequest();
      xhr.onload = function(e) {
          if (this.readyState === 4) {
              console.log("Server returned: ", e.target.responseText);
          }
      };
      var fd = new FormData();
      fd.append("audio_data", blob, filename);
      xhr.open("POST", "upload.php", true);
      xhr.send(fd);
  })
  li.appendChild(document.createTextNode(" ")) //add a space in between 
  li.appendChild(upload) //add the upload link to li

  recordingsList.appendChild(li);
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
