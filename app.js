const express = require('express');
const db = require('./lib/db.js');
const buses = require('./routes/buses.js');

const app = express();
const port = process.env.PORT || 8080;

db.testConnection();

app.use('/api', buses);

app.get('/', (req, res) => {
    res.send('<h3>Welcome!</h3>'
    + '<p>This page is still under construction.</p>');
});

app.listen(port, () => {
    console.log(`Successfully connected to port ${port}`);
});
