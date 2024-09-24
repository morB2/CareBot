const express = require('express');
const axios = require('axios');
const app = express();
const port = 5000;

app.use(express.json());

app.post('/api/messages', (req, res) => {
  const { text, user } = req.body;
  const message = { text, user, timestamp: new Date() };
  // שמור את ההודעה
  res.status(200).json(message);
});

app.post('/api/python-function', async (req, res) => {
  try {
    const { text } = req.body;
    const pythonResponse = await axios.post('http://localhost:5001/python-endpoint', { text });
    res.status(200).json(pythonResponse.data);
  } catch (error) {
    res.status(500).json({ error: 'Failed to communicate with Python service' });
  }
});

app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
