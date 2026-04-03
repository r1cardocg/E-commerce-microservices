<?php

namespace App\Http\Controllers;

use App\Models\Pago;
use Illuminate\Http\Request;
use Illuminate\Support\Str;

class PagoController extends Controller
{
    private array $metodosValidos = [
        'tarjeta_credito',
        'tarjeta_debito',
        'pse',
        'transferencia',
    ];

    public function index(Request $request)
    {
        $pagos = $request->query('usuario_id')
            ? Pago::where('usuario_id', $request->query('usuario_id'))->get()
            : Pago::all();

        return response()->json(['pagos' => $pagos]);
    }

    public function store(Request $request)
    {
        $errors = [];

        if (!$request->usuario_id)
            $errors['usuario_id'] = 'El usuario_id es requerido';
        if (!$request->orden_id)
            $errors['orden_id'] = 'El orden_id es requerido';
        if (!$request->monto || floatval($request->monto) <= 0)
            $errors['monto'] = 'El monto debe ser mayor a 0';
        if (!in_array($request->metodo_pago, $this->metodosValidos))
            $errors['metodo_pago'] = 'Método inválido. Use: ' . implode(', ', $this->metodosValidos);

        if (!empty($errors))
            return response()->json(['errors' => $errors], 422);

        $pago = Pago::create([
            'usuario_id'  => $request->usuario_id,
            'orden_id'    => $request->orden_id,
            'monto'       => $request->monto,
            'metodo_pago' => $request->metodo_pago,
            'estado'      => 'completado',
            'referencia'  => Str::uuid(),
        ]);

        return response()->json($pago, 201);
    }

    public function show($id)
    {
        $pago = Pago::find($id);
        if (!$pago)
            return response()->json(['error' => 'Pago no encontrado'], 404);
        return response()->json($pago);
    }
}