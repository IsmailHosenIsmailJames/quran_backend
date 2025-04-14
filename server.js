const express = require('express');
const path = require('path');
const app = express();
const port = 3000; // or any port you prefer

// Serve static files from the "public" directory
app.use(express.static(path.join(__dirname, 'public')));

// Health check endpoint
app.get('/health', (req, res) => {
   res.status(200).send('OK');
});

// Start the server
app.listen(port, '0.0.0.0', () => {
   console.log(`Server is running on http://localhost:${port}`);
});