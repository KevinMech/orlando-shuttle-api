const pgp = require('pg-promise')();

const db = pgp(process.env.DATABASE_URL || {
    host: 'localhost',
    port: 5432,
    database: 'busroutedb',
    user: 'postgres',
});

exports.testConnection = async () => {
    try {
        console.log('Connecting to database...');
        await db.connect();
        console.log('Connected to database successfully!');
    } catch (err) {
        console.log('Error connecting to database!');
        console.log(err);
        process.exit();
    }
};

exports.getAvailableRoutes = () => new Promise(async (resolve, reject) => {
    let buses = null;
    try {
        buses = await db.many('SELECT * FROM buses');
        resolve(buses);
    } catch (err) {
        reject(err);
    }
});

exports.getStops = id => new Promise(async (resolve, reject) => {
    try {
        const stops = await db.many('SELECT longitude, latitude FROM buses INNER JOIN stops ON buses.id = stops.id WHERE buses.id = $1', [id]);
        resolve(stops);
    } catch (err) {
        reject(err);
    }
});

exports.getRoutes = id => new Promise(async (resolve, reject) => {
    try {
        const routes = await db.many('SELECT longitude, latitude FROM buses INNER JOIN routes ON buses.id = routes.id WHERE buses.id = $1', [id]);
        resolve(routes);
    } catch (err) {
        reject(err);
    }
});
