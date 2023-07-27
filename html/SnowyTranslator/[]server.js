const express = require('express');
const cors = require('cors');
const app = express();
const port = 3000;

app.use(cors()); // Enable CORS for all routes

app.get('/audio', async (req, res) => {
  const { text } = req.query;

  // Your audio handling logic here
  // Replace this with your actual audio fetching logic
  const fetch = require('node-fetch');
  const sourceLanguage = 'en'; // Set your desired source language code (e.g., 'en' for English)
  const audioUrl = `https://translate.google.com/translate_tts?ie=UTF-8&tl=${sourceLanguage}&client=tw-ob&q=${encodeURIComponent(text)}`;

  try {
    const response = await fetch(audioUrl);
    const audioBuffer = await response.buffer();

    // Set the response headers for the audio file
    res.set({
      'Content-Type': 'audio/mpeg', // Assuming the audio file is in MP3 format
      'Content-Length': audioBuffer.length,
    });

    // Send the audio data to the client
    res.send(audioBuffer);
  } catch (error) {
    console.error('Error fetching audio:', error);
    res.status(500).send('Error fetching audio');
  }
});

// Start the server
app.listen(port, () => {
  console.log(`Server is listening on port ${port}`);
});

