// from https://github.com/Mido22/MediaRecorder-sample

'use strict'

function getJSON() {
  let xhr = new XMLHttpRequest()
  xhr.onreadystatechange = function() {
      if (this.readyState != 4) return
      logJSON(xhr)
  }

  xhr.open("GET", "get-json", true)
  xhr.send()
}

function logJSON(xhr) {
  if (xhr.status == 200) {
    let response = JSON.parse(xhr.responseText)
    JSONhandler(response)
    return
  }
}

function JSONhandler(vals) {
  console.log(vals)
  return
}