<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Pago extends Model
{
    protected $table = 'pagos';

    protected $fillable = [
        'usuario_id',
        'orden_id',
        'monto',
        'metodo_pago',
        'estado',
        'referencia',
    ];

    protected $casts = [
        'monto' => 'decimal:2',
    ];
}