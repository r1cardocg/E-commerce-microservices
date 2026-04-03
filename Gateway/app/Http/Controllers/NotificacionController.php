<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Services\MicroserviceProxy;

class NotificacionController extends Controller
{
    private MicroserviceProxy $proxy;
    private string $baseUrl;

    public function __construct(MicroserviceProxy $proxy)
    {
        $this->proxy   = $proxy;
        $this->baseUrl = env('NOTIFICACIONES_URL', 'http://localhost:8005');
    }

    public function index(Request $request)
    {
        return $this->proxy->forward($this->baseUrl, 'notificaciones', $request);
    }

    public function store(Request $request)
    {
        return $this->proxy->forward($this->baseUrl, 'notificaciones', $request);
    }

    public function marcarLeida(Request $request, $id)
    {
        return $this->proxy->forward($this->baseUrl, "notificaciones/{$id}/leer", $request);
    }

    public function destroy(Request $request, $id)
    {
        return $this->proxy->forward($this->baseUrl, "notificaciones/{$id}", $request);
    }
}