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

router.get('/shuttle', async (req, res) => {
    let stops;
    let routes;
    let promises = [];
    let shuttles = [];
    for (const shuttle of availableshuttles) {
        try {
            stops = await db.getStops(shuttle.id);
            routes = await db.getRoutes(shuttle.id);
        } catch (err) {
            console.log(`Error: Failed to fetch JSON for shuttle ${shuttle.name}`);
            console.log(err);
        }
        let shuttleJSON = new Shuttle(shuttle.id, shuttle.name, stops, routes);
        shuttles.push(shuttleJSON);
    }
    res.send(shuttles);
});

router.get('/shuttle/:name', async (req, res) => {
    let stops;
    let routes;
    for (const shuttle of availableshuttles) {
        if (req.params.name.toLowerCase().trim() === shuttle.name.toLowerCase().trim()) {
            try {
                stops = await db.getStops(shuttle.id);
                routes = await db.getRoutes(shuttle.id);
            } catch (err) {
                console.log(`Error: Failed to fetch JSON for shuttle ${shuttle.name}`);
                console.log(err);
            }
            const shuttleJSON = new Shuttle(shuttle.id, shuttle.name, stops, routes);
            res.send(shuttleJSON);
            return;
        }
    }
});

module.exports = router;
