// from https://github.com/Mido22/MediaRecorder-sample

'use strict'

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
  media = {
      tag: 'audio',
      type: 'audio/ogg',
      ext: '.ogg',
      selector: {audio: true}
    };

  navigator.mediaDevices.getUserMedia(media.selector).then(_stream => {
    stream = _stream;
    id('selection_area').style.display = 'none';
    id('buttons_area').style.display = 'inherit';
    start.removeAttribute('disabled');
    recorder = new MediaRecorder(stream);
    console.log(recorder);
    recorder.ondataavailable = e => {
      chunks.push(e.data);
      if(recorder.state == 'inactive')  makeLink();
    };
    log('got media successfully');
  }).catch(log);

}

start.onclick = e => {
  start.disabled = true;
  stop.removeAttribute('disabled');
  chunks=[];
  recorder.start();
}


stop.onclick = e => {
  console.log("stopped")
  stop.disabled = true;
  recorder.stop();
  console.log("stopped2");
  start.removeAttribute('disabled');
}

function makeLink(){
  console.log("making link");
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
}
