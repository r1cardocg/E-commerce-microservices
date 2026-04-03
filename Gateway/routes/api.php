<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\AuthController;
use App\Http\Controllers\UsuarioController;
use App\Http\Controllers\ProductoController;
use App\Http\Controllers\OrdenController;
use App\Http\Controllers\PagoController;
use App\Http\Controllers\NotificacionController;

Route::post('/register',        [AuthController::class, 'register']);
Route::post('/login',           [AuthController::class, 'login']);
Route::post('/forgot-password', [AuthController::class, 'forgotPassword']);
Route::post('/reset-password',  [AuthController::class, 'resetPassword']);

Route::middleware('auth:api')->group(function () {

    Route::post('/logout', [AuthController::class, 'logout']);
    Route::get('/me',      [AuthController::class, 'me']);

    Route::get('/usuarios',           [UsuarioController::class, 'index']);
    Route::get('/usuarios/{id}',      [UsuarioController::class, 'show']);
    Route::put('/usuarios/{id}',      [UsuarioController::class, 'update']);
    Route::delete('/usuarios/{id}',   [UsuarioController::class, 'destroy']);

    Route::get('/productos',          [ProductoController::class, 'index']);
    Route::post('/productos',         [ProductoController::class, 'store']);
    Route::get('/productos/{id}',     [ProductoController::class, 'show']);
    Route::put('/productos/{id}',     [ProductoController::class, 'update']);
    Route::delete('/productos/{id}',  [ProductoController::class, 'destroy']);

    Route::get('/ordenes',            [OrdenController::class, 'index']);
    Route::post('/ordenes',           [OrdenController::class, 'store']);
    Route::get('/ordenes/{id}',       [OrdenController::class, 'show']);
    Route::put('/ordenes/{id}',       [OrdenController::class, 'update']);
    Route::delete('/ordenes/{id}',    [OrdenController::class, 'destroy']);

    Route::get('/pagos',              [PagoController::class, 'index']);
    Route::post('/pagos',             [PagoController::class, 'store']);
    Route::get('/pagos/{id}',         [PagoController::class, 'show']);

    Route::get('/notificaciones',              [NotificacionController::class, 'index']);
    Route::post('/notificaciones',             [NotificacionController::class, 'store']);
    Route::patch('/notificaciones/{id}/leer',  [NotificacionController::class, 'marcarLeida']);
    Route::delete('/notificaciones/{id}',      [NotificacionController::class, 'destroy']);
});