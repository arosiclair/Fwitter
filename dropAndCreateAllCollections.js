conn = new Mongo();
db = conn.getDB("Fwitter");
// db.auth("arosiclair", "cse356");

db.Users.drop();
db.Tweets.drop();
db.django_session.drop();

db.createCollection("Users");
db.createCollection("Tweets");
db.createCollection("django_session");

sh.shardCollection("Fwitter.Users", { "_id" : "hashed" } );
sh.shardCollection("Fwitter.Tweets", { "_id" : "hashed" } );
sh.shardCollection("Fwitter.django_session", { "_id" : "hashed" } );

db.Tweets.createIndex({ "timestamp": -1 });
db.Tweets.createIndex({ "likes": -1 });
db.Tweets.createIndex({ "parent": 1 });
db.Tweets.createIndex({ "content": "text"});