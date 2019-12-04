"use strict"

const redis = require("redis");

module.exports = (body, callback) => {

    const currentStat = JSON.parse(body).current_stat;    
    const name = JSON.parse(body).name;


    const client = redis.createClient(6379, process.env.redis);

    client.set(name, currentStat, () => {
      client.quit();
      callback(null, { status: 'set done' });
    });
}
