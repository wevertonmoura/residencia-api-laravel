<?php

return [

    /*
    |--------------------------------------------------------------------------
    | Configuração CORS (Versão Específica para VS Code)
    |--------------------------------------------------------------------------
    */

    // Permite acesso a qualquer rota
    'paths' => ['*', 'api/*'],

    // Permite todos os métodos (GET, POST, etc)
    'allowed_methods' => ['*'],

    // AQUI ESTÁ A MUDANÇA: 
    // Adicionamos explicitamente o endereço do seu Front-end
    'allowed_origins' => [
        '*',                      // Tenta liberar geral
        'http://127.0.0.1:5500',  // Libera seu VS Code (IP)
        'http://localhost:5500',  // Libera seu VS Code (Nome)
    ],

    'allowed_origins_patterns' => [],

    'allowed_headers' => ['*'],

    'exposed_headers' => [],

    'max_age' => 0,

    'supports_credentials' => false,

];