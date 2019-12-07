"use strict"

const redis = require("redis");

module.exports = (body, callback) => {

    const name = JSON.parse(body).player_name;
    const action = JSON.parse(body).action;

    const client = redis.createClient(6379, process.env.redis);

    if(action=='save'){
    const currentStat = JSON.parse(body).current_stat;    
    client.set(name, currentStat, () => {
      client.quit();
      callback(null, { 'status': action+' done', "name":name,"saved status":currentStat });
    });
    }else if(action=='load'){
    const stat = client.get(name, (err, replies) => {
      client.quit();
      callback(null, { 'status': action+' done', "name":name,"saved status":replies });
    });
    }
}
