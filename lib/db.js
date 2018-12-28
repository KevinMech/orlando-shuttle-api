const pgp = require('pg-promise')();

const db = pgp(process.env.DATABASE_URL || {
    host: 'localhost',
    port: 5432,
    database: 'busroutedb',
    user: 'postgres',
});

exports.testConnection = async () => {
    try {
        await db.connect();
        console.log('connected successfully!');
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
