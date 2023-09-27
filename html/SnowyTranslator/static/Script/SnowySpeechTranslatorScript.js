  async function ggSpeakUrlGet(text, sourceLanguage) {
    if (window.location.protocol === "file:") {
      var ggTranslateUrl = "https://translate.google.com/translate_tts?ie=UTF-8&tl=" +
        sourceLanguage +  "&client=tw-ob&q=" + encodeURIComponent(text);
      return ggTranslateUrl;
    }
    else {
      try {
        var baseUrl;
        if (window.location.protocol === 'file:') {
            baseUrl = 'https://snsmile.site:3000';
        } else {
            baseUrl = '';
        }
        const response = await fetch('${baseUrl}/text-to-speech', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            sourceLanguage: sourceLanguage,
            text: text
          })
        });
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        const audioData = await response.arrayBuffer();
        const audioBlob = new Blob([audioData], { type: 'audio/mpeg' });
        return URL.createObjectURL(audioBlob);
      } catch (error) {
        console.error('Error:', error);
        return null; // or handle the error in a way appropriate for your application
      }
    }
  }
