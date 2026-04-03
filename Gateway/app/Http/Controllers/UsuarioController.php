<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Services\MicroserviceProxy;

class UsuarioController extends Controller
{
    private MicroserviceProxy $proxy;
    private string $baseUrl;

    public function __construct(MicroserviceProxy $proxy)
    {
        $this->proxy   = $proxy;
        $this->baseUrl = env('USUARIOS_URL', 'http://localhost:8001');
    }

    public function index(Request $request)
    {
        return $this->proxy->forward($this->baseUrl, 'usuarios', $request);
    }

    public function show(Request $request, $id)
    {
        return $this->proxy->forward($this->baseUrl, "usuarios/{$id}", $request);
    }

    public function update(Request $request, $id)
    {
        return $this->proxy->forward($this->baseUrl, "usuarios/{$id}", $request);
    }

    public function destroy(Request $request, $id)
    {
        return $this->proxy->forward($this->baseUrl, "usuarios/{$id}", $request);
    }
}