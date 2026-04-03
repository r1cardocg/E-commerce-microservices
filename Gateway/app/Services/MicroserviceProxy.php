<?php

namespace App\Services;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Http;

class MicroserviceProxy
{
    public function forward(string $baseUrl, string $path, Request $request)
    {
        $url = rtrim($baseUrl, '/') . '/' . ltrim($path, '/');

        $response = Http::withHeaders([
            'X-Internal-Key' => env('INTERNAL_KEY'),
            'Accept'         => 'application/json',
            'Content-Type'   => 'application/json',
        ])
        ->timeout(10)
        ->{strtolower($request->method())}($url, $request->all());

        return response($response->body(), $response->status())
            ->header('Content-Type', 'application/json');
    }
}