const mongoose = require('mongoose');

const connect = async () => {
  const uri = process.env.MONGO_URI || 'mongodb://localhost:27017/ordenes_db';
  await mongoose.connect(uri);
  console.log('MongoDB Atlas conectado');
};

module.exports = { connect };
