<?php

return [

    /*
    |--------------------------------------------------------------------------
    | Configurações de CORS (Cross-Origin Resource Sharing)
    |--------------------------------------------------------------------------
    |
    | Configure aqui as permissões de acesso da sua API.
    | O 'fruitcake/laravel-cors' usa estas configurações.
    |
    */

    'paths' => ['api/*'], // Aplica o CORS a todas as rotas da sua API

    'allowed_methods' => ['*'], // Permite todos os métodos (GET, POST, PUT, DELETE)

    'allowed_origins' => ['*'], // <-- ESTA É A LINHA MAIS IMPORTANTE
                              // Permite que QUALQUER site (incluindo o seu painel)
                              // faça pedidos à sua API.

    'allowed_origins_patterns' => [],

    'allowed_headers' => ['*'], // Permite todos os cabeçalhos

    'exposed_headers' => [],

    'max_age' => 0,

    'supports_credentials' => false,

];