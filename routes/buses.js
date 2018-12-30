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

router.get('/shuttle/name/:name', async (req, res) => {
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
    res.status(404).send('404 resource not found');
});

router.get('/shuttle/id/:id', async (req, res) => {
    let stops;
    let routes;
    const id = Number(req.params.id);
    if (!Number.isNaN(id)) {
        for (const shuttle of availableshuttles) {
            if (id === shuttle.id) {
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
        res.status(404).send('404 resource not found');
    } else {
        res.status(400).send('400 bad request');
    }
});

module.exports = router;
