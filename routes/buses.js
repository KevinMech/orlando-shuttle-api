const express = require('express');
const db = require('../lib/db.js');

const router = express.Router();
let buses = [];

router.use(async (req, res, next) => {
    buses = await db.getAvailableRoutes();
    next();
});

router.get('/', () => {
    buses.forEach((bus) => {
        console.log(bus);
    });
});

module.exports = router;
