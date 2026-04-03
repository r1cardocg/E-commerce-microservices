<?php

namespace Tests\Feature;

use Tests\TestCase;
use Illuminate\Foundation\Testing\RefreshDatabase;
use App\Models\Pago;

class PagoTest extends TestCase
{
    use RefreshDatabase;

    private array $headers = [
        'X-Internal-Key' => 'EcommerceSecretKey',
        'Accept'         => 'application/json',
        'Content-Type'   => 'application/json',
    ];

    public function test_sin_internal_key_retorna_403(): void
    {
        $response = $this->getJson('/api/pagos');
        $response->assertStatus(403);
    }

    public function test_key_incorrecta_retorna_403(): void
    {
        $response = $this->withHeaders(['X-Internal-Key' => 'incorrecta'])
                         ->getJson('/api/pagos');
        $response->assertStatus(403);
    }

    public function test_listar_pagos_vacio(): void
    {
        $response = $this->withHeaders($this->headers)->getJson('/api/pagos');
        $response->assertStatus(200)
                 ->assertJsonStructure(['pagos']);
    }

    public function test_crear_pago_exitoso(): void
    {
        $response = $this->withHeaders($this->headers)->postJson('/api/pagos', [
            'usuario_id'  => 1,
            'orden_id'    => 'orden-abc-123',
            'monto'       => 250.00,
            'metodo_pago' => 'tarjeta_credito',
        ]);

        $response->assertStatus(201)
                 ->assertJsonFragment(['estado' => 'completado'])
                 ->assertJsonStructure(['id', 'referencia', 'estado']);
    }

    public function test_crear_sin_usuario_id_retorna_422(): void
    {
        $response = $this->withHeaders($this->headers)->postJson('/api/pagos', [
            'orden_id'    => 'orden-123',
            'monto'       => 100.00,
            'metodo_pago' => 'paypal',
        ]);

        $response->assertStatus(422)
                 ->assertJsonStructure(['errors' => ['usuario_id']]);
    }

    public function test_crear_monto_negativo_retorna_422(): void
    {
        $response = $this->withHeaders($this->headers)->postJson('/api/pagos', [
            'usuario_id'  => 1,
            'orden_id'    => 'orden-123',
            'monto'       => -50,
            'metodo_pago' => 'paypal',
        ]);

        $response->assertStatus(422)
                 ->assertJsonStructure(['errors' => ['monto']]);
    }

    public function test_crear_metodo_invalido_retorna_422(): void
    {
        $response = $this->withHeaders($this->headers)->postJson('/api/pagos', [
            'usuario_id'  => 1,
            'orden_id'    => 'orden-123',
            'monto'       => 100,
            'metodo_pago' => 'bitcoin',
        ]);

        $response->assertStatus(422)
                 ->assertJsonStructure(['errors' => ['metodo_pago']]);
    }

    public function test_crear_body_vacio_retorna_422(): void
    {
        $response = $this->withHeaders($this->headers)->postJson('/api/pagos', []);
        $response->assertStatus(422);
    }

    public function test_obtener_pago_existente(): void
    {
        $pago = Pago::create([
            'usuario_id'  => 1,
            'orden_id'    => 'orden-xyz',
            'monto'       => 500.00,
            'metodo_pago' => 'transferencia',
            'estado'      => 'completado',
            'referencia'  => 'ref-test-001',
        ]);

        $response = $this->withHeaders($this->headers)->getJson("/api/pagos/{$pago->id}");
        $response->assertStatus(200)
                 ->assertJsonFragment(['id' => $pago->id]);
    }

    public function test_obtener_pago_no_existe_retorna_404(): void
    {
        $response = $this->withHeaders($this->headers)->getJson('/api/pagos/9999');
        $response->assertStatus(404);
    }
}