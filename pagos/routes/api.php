<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\PagoController;

Route::middleware('internal.key')->group(function () {
    Route::get('/pagos',       [PagoController::class, 'index']);
    Route::post('/pagos',      [PagoController::class, 'store']);
    Route::get('/pagos/{id}',  [PagoController::class, 'show']);
});