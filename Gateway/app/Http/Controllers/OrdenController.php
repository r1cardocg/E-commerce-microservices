<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Services\MicroserviceProxy;

class OrdenController extends Controller
{
    private MicroserviceProxy $proxy;
    private string $baseUrl;

    public function __construct(MicroserviceProxy $proxy)
    {
        $this->proxy   = $proxy;
        $this->baseUrl = env('ORDENES_URL', 'http://localhost:8003');
    }

    public function index(Request $request)
    {
        return $this->proxy->forward($this->baseUrl, 'ordenes', $request);
    }

    public function store(Request $request)
    {
        return $this->proxy->forward($this->baseUrl, 'ordenes', $request);
    }

    public function show(Request $request, $id)
    {
        return $this->proxy->forward($this->baseUrl, "ordenes/{$id}", $request);
    }

    public function update(Request $request, $id)
    {
        return $this->proxy->forward($this->baseUrl, "ordenes/{$id}", $request);
    }

    public function destroy(Request $request, $id)
    {
        return $this->proxy->forward($this->baseUrl, "ordenes/{$id}", $request);
    }
}