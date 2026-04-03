<?php

namespace App\Services;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Http;

class MicroserviceProxy
{
    public function forward(string $baseUrl, string $path, Request $request)
    {
        $url = rtrim($baseUrl, '/') . '/' . ltrim($path, '/');

        $headers = [
            'X-Internal-Key' => env('INTERNAL_KEY'),
            'Accept'         => 'application/json',
            'Content-Type'   => 'application/json',
        ];

        $method   = strtolower($request->method());
        $body     = $request->all();

        $response = Http::withHeaders($headers)
            ->timeout(10)
            ->{$method}($url, $body);

        return response($response->body(), $response->status())
            ->header('Content-Type', 'application/json');
    }
}