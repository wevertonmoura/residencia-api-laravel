<?php

return [
    /*
    |--------------------------------------------------------------------------
    | Cross-Origin Resource Sharing (CORS) Configuration
    |--------------------------------------------------------------------------
    */

    'paths' => ['api/*', 'sanctum/csrf-cookie'],

    'allowed_methods' => ['*'], // Permite todos os métodos (GET, POST, PATCH, etc.)

    'allowed_origins' => [
        // O '*' (wildcard) diz ao Laravel para aceitar pedidos de QUALQUER 
        // origem. Isto irá resolver o nosso problema de CORS local.
        '*', 
    ],

    'allowed_origins_patterns' => [],

    'allowed_headers' => ['*'], // Permite todos os cabeçalhos

    'exposed_headers' => [],

    'max_age' => 0,

    'supports_credentials' => false,

];