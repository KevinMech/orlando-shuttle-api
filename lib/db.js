const pgp = require('pg-promise')();

exports.testConnection = async () => {
    const db = pgp(process.env.DATABASE_URL || {
        host: 'localhost',
        port: 5432,
        database: 'busroutedb',
        user: 'postgress',
    });
    try {
        await db.connect();
        console.log('connected successfully!');
    } catch (err) {
        console.log('Error connecting to database!');
        console.log(err);
        process.exit();
    }
};
