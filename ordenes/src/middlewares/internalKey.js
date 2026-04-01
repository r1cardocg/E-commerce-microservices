const internalKeyMiddleware = (req, res, next) => {
  const key = req.headers['x-internal-key'];
  if (key !== process.env.INTERNAL_KEY) {
    return res.status(403).json({ error: 'Acceso no autorizado' });
  }
  next();
};

module.exports = { internalKeyMiddleware };
