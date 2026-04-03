<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;

class InternalKeyMiddleware
{
    public function handle(Request $request, Closure $next)
    {
        $key = $request->header('X-Internal-Key');
        if ($key !== env('INTERNAL_KEY')) {
            return response()->json(['error' => 'Acceso no autorizado'], 403);
        }
        return $next($request);
    }
}