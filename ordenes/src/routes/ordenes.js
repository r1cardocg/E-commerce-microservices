const express = require('express');
const router  = express.Router();
const Orden   = require('../models/Orden');

router.get('/ordenes', async (req, res) => {
  try {
    const filter = req.query.usuario_id
      ? { usuario_id: Number(req.query.usuario_id) }
      : {};
    const ordenes = await Orden.find(filter).sort({ creado_en: -1 });
    res.json({ ordenes });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

router.post('/ordenes', async (req, res) => {
  try {
    const { usuario_id, productos, direccion_envio } = req.body;

    const errors = {};
    if (!usuario_id)              errors.usuario_id   = 'El usuario_id es requerido';
    if (!productos || productos.length === 0)
      errors.productos = 'Se requiere al menos un producto';
    if (Object.keys(errors).length) return res.status(422).json({ errors });

    const total = productos.reduce(
      (sum, p) => sum + p.cantidad * p.precio_unitario, 0
    );

    const orden = await Orden.create({
      usuario_id,
      productos,
      total,
      direccion_envio: direccion_envio || '',
    });

    res.status(201).json(orden);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

router.get('/ordenes/:id', async (req, res) => {
  try {
    const orden = await Orden.findById(req.params.id);
    if (!orden) return res.status(404).json({ error: 'Orden no encontrada' });
    res.json(orden);
  } catch (err) {
    res.status(404).json({ error: 'Orden no encontrada' });
  }
});

router.put('/ordenes/:id', async (req, res) => {
  try {
    const { estado, direccion_envio } = req.body;
    const orden = await Orden.findByIdAndUpdate(
      req.params.id,
      { ...(estado && { estado }), ...(direccion_envio && { direccion_envio }) },
      { new: true, runValidators: true }
    );
    if (!orden) return res.status(404).json({ error: 'Orden no encontrada' });
    res.json(orden);
  } catch (err) {
    res.status(400).json({ error: err.message });
  }
});

router.delete('/ordenes/:id', async (req, res) => {
  try {
    const orden = await Orden.findByIdAndUpdate(
      req.params.id,
      { estado: 'cancelada' },
      { new: true }
    );
    if (!orden) return res.status(404).json({ error: 'Orden no encontrada' });
    res.json({ message: 'Orden cancelada', orden });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

module.exports = router;
