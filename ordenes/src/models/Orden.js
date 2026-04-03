const mongoose = require('mongoose');

const productoOrdenSchema = new mongoose.Schema({
  producto_id:     { type: String, required: true },
  nombre:          { type: String, required: true },
  cantidad:        { type: Number, required: true, min: 1 },
  precio_unitario: { type: Number, required: true, min: 0 },
});

const ordenSchema = new mongoose.Schema({
  usuario_id: { type: Number, required: true },
  productos:  { type: [productoOrdenSchema], required: true },
  total:      { type: Number, required: true },
  estado:     {
    type:    String,
    enum:    ['pendiente', 'confirmada', 'enviada', 'entregada', 'cancelada'],
    default: 'pendiente',
  },
  direccion_envio: { type: String, default: '' },
}, { timestamps: { createdAt: 'creado_en', updatedAt: 'actualizado_en' } });

module.exports = mongoose.model('Orden', ordenSchema);
