const express = require('express');
const https = require('https');
const path = require('path');
const fs = require('fs');
const cors = require('cors');
const app = express();
const port = 3000;

app.use(express.json());
app.use(cors());

// Add the paths to your SSL certificate and private key
const options = {
  key: fs.readFileSync(path.join(__dirname,'privkey.pem')),
  cert: fs.readFileSync(path.join(__dirname,'fullchain.pem')),
};

app.post('/text-to-speech', async (req, res) => {
  try {
    const { sourceLanguage, text } = req.body;
    const url =
      'https://translate.google.com/translate_tts?ie=UTF-8&tl=' +
      sourceLanguage +
      '&client=tw-ob&q=' +
      encodeURIComponent(text);

    // Make a GET request to Google's TTS API
    const response = await https.get(url, (googleRes) => {
      // Set the response headers for audio
      res.setHeader('Content-Type', 'audio/mpeg');
      res.setHeader('Content-Disposition', 'inline');

      // Pipe the Google TTS response to the client's response
      googleRes.pipe(res);
    });
  } catch (error) {
    console.error('Error:', error.message);
    res.status(500).send('Error generating speech.');
  }
});

// Create an HTTPS server using the 'https' module
const server = https.createServer(options, app);

server.listen(port, () => {
  console.log(`Server running on https://localhost:${port}`);
});
