<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Services\MicroserviceProxy;

class PagoController extends Controller
{
    private MicroserviceProxy $proxy;
    private string $baseUrl;

    public function __construct(MicroserviceProxy $proxy)
    {
        $this->proxy   = $proxy;
        $this->baseUrl = env('PAGOS_URL', 'http://localhost:8004');
    }

    public function index(Request $request)
    {
        return $this->proxy->forward($this->baseUrl, 'api/pagos', $request);
    }

    public function store(Request $request)
    {
        return $this->proxy->forward($this->baseUrl, 'api/pagos', $request);
    }

    public function show(Request $request, $id)
    {
        return $this->proxy->forward($this->baseUrl, "api/pagos/{$id}", $request);
    }
}