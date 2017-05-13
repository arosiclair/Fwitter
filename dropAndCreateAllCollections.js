conn = new Mongo();
db = conn.getDB("Fwitter");
// db.auth("arosiclair", "cse356");

db.Users.drop();
db.Tweets.drop();
db.django_session.drop();

db.createCollection("Users");
db.createCollection("Tweets");
db.createCollection("django_session");

sh.shardCollection("Fwitter.Users", { "_id" : 1 } );
sh.shardCollection("Fwitter.Tweets", { "_id" : 1 } );
sh.shardCollection("Fwitter.django_session", { "_id" : 1 } );

//TODO: Recreate indexes