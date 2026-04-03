const request = require('supertest');

// Mock mongoose ANTES de cargar la app
jest.mock('mongoose', () => ({
  connect:   jest.fn().mockResolvedValue(true),
  Schema:    jest.requireActual('mongoose').Schema,
  model:     jest.requireActual('mongoose').model,
  connect:   jest.fn().mockResolvedValue(true),
}));

// Setear variable de entorno ANTES de cargar la app
process.env.INTERNAL_KEY = 'ecommerce_internal_key_2026';
process.env.MONGO_URI    = 'mongodb://127.0.0.1:27017/test';

const app = require('../src/app');

const HEADERS = { 'x-internal-key': 'ecommerce_internal_key_2026' };

// Mock del modelo Orden
jest.mock('../src/models/Orden', () => ({
  find:        jest.fn(),
  findById:    jest.fn(),
  findByIdAndUpdate: jest.fn(),
  create:      jest.fn(),
}));

const Orden = require('../src/models/Orden');

describe('Órdenes API', () => {

  test('GET /ordenes sin internal key retorna 403', async () => {
    const res = await request(app).get('/ordenes');
    expect(res.status).toBe(403);
  });

  test('GET /ordenes retorna 200', async () => {
    Orden.find.mockReturnValue({
      sort: jest.fn().mockResolvedValue([])
    });
    const res = await request(app).get('/ordenes').set(HEADERS);
    expect(res.status).toBe(200);
    expect(Array.isArray(res.body.ordenes)).toBe(true);
  });

  test('POST /ordenes sin usuario_id retorna 422', async () => {
    const res = await request(app)
      .post('/ordenes')
      .set(HEADERS)
      .send({ productos: [{ producto_id: '1', nombre: 'X', cantidad: 1, precio_unitario: 10 }] });
    expect(res.status).toBe(422);
    expect(res.body.errors).toHaveProperty('usuario_id');
  });

  test('POST /ordenes sin productos retorna 422', async () => {
    const res = await request(app)
      .post('/ordenes')
      .set(HEADERS)
      .send({ usuario_id: 1, productos: [] });
    expect(res.status).toBe(422);
  });

  test('GET /ordenes/:id inexistente retorna 404', async () => {
    Orden.findById.mockResolvedValue(null);
    const res = await request(app)
      .get('/ordenes/507f1f77bcf86cd799439011')
      .set(HEADERS);
    expect(res.status).toBe(404);
  });

});