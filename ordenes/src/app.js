const express    = require('express');
const mongoose   = require('mongoose');
const ordenRoutes = require('./routes/ordenes');
const { internalKeyMiddleware } = require('./middlewares/internalKey');

const app = express();
app.use(express.json());

mongoose.connect(process.env.MONGO_URI || 'mongodb://localhost:27017/ordenes_db')
  .then(() => console.log('MongoDB conectado'))
  .catch(err => console.error('Error MongoDB:', err));

app.use(internalKeyMiddleware);

app.use('/', ordenRoutes);

app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({ error: 'Error interno del servidor' });
});

module.exports = app;
