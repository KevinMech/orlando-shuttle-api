const express = require('express');
const app = express();
const port = 8080;

app.get('/', (req, res) =>{
    res.send('<h3>Welcome!</h3>' +
    '<p>This page is still under construction.</p>')
});

app.listen(port, (req, res)=>{
    console.log(`Successfully connected to port ${port}`)
});
