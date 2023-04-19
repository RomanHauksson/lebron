const voice = "VOICE_ID"

async function fetchAudio(text) {
    return fetch(
        `https://api.elevenlabs.io/v1/text-to-speech/${voice}`,
        {
            method: "POST",
            headers: {
                accept: "audio/mpeg",
                "Content-Type": "application/json",
                "xi-api-key": "XI_API_KEY",
            },
            body: JSON.stringify({
                text: text,
                voice_setings: {
                    stability: .75,
                    similarity_boost: .75,
                },
            }),
        }
    ).then(res => {
        if (!res.ok)
          throw new Error(`${res.status} = ${res.statusText}`);      // response.body is a readable stream.
        // Calling getReader() gives us exclusive access to
        // the stream's content
        let reader = res.body.getReader();
        // read() returns a promise that resolves
        // when a value has been received
        return reader
          .read()
          .then((result) => {
            return result;
          });
      })
  }

export async function lebronSays(text) {
    fetchAudio(text).then((response) => {
        // response.value for fetch streams is a Uint8Array
        var blob = new Blob([response.value], { type: 'audio/mp3' });
        var url = window.URL.createObjectURL(blob)
        window.audio = new Audio();
        window.audio.src = url;
        window.audio.play();
    }).catch((error) => {
        console.log(error.message);
    });
}