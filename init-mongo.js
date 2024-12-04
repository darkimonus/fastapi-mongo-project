db = db.getSiblingDB("fastapi_db");

db.createUser({
  user: 'admin',
  pwd: 'admin',
  roles: [
    {
      role: 'readWrite',
      db: 'fastapi_db',
    },
  ],
});
