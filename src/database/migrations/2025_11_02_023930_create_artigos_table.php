<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

class CreateArtigosTable extends Migration
{
    /**
     * Run the migrations.
     *
     * @return void
     */
    public function up()
    {
        Schema::create('artigos', function (Blueprint $table) {
            $table->id();
            $table->string('titulo', 255); // O título do artigo
            $table->text('conteudo'); // O texto completo gerado pela IA "Key"
            $table->string('acao_ticker', 20); // O ticker da ação (ex: "PETR4.SA")
            $table->string('recomendacao', 50); // "Comprar", "Vender", "Manter"
            
            // Esta é a coluna do "Fator Humano"
            $table->string('status', 50)->default('rascunho'); // 'rascunho', 'aprovado', 'rejeitado'
            
            $table->timestamps(); // created_at e updated_at
        });
    }

    /**
     * Reverse the migrations.
     *
     */
    public function down()
    {
        Schema::dropIfExists('artigos');
    }
}
