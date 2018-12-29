const express = require('express');
const db = require('../lib/db.js');

const router = express.Router();
let availableshuttles = [];

function Shuttle(id, name, stops, routes) {
    this.id = id;
    this.name = name;
    this.stops = stops;
    this.routes = routes;
}

router.use(async (req, res, next) => {
    try {
        availableshuttles = await db.getAvailableRoutes();
    } catch (err) {
        console.log(err);
    }
    next();
});

router.get('/', async (req, res) => {
    let stops;
    let routes;
    let promises = [];
    let shuttles = [];
    for (const shuttle of availableshuttles) {
        try {
            stops = await db.getStops(shuttle.id);
            routes = await db.getRoutes(shuttle.id);
            let shuttleJSON = new Shuttle(shuttle.id, shuttle.name, stops, routes);
            shuttles.push(shuttleJSON);
        } catch (err) {
            console.log(`Error: Failed to fetch JSON for shuttle ${shuttle.name}`);
            console.log(err);
        }
    }
    res.send(shuttles);
});

module.exports = router;
