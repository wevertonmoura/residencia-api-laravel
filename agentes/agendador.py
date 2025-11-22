import time
import logging
from main import main # Importa a função main do seu script principal

# Configuração
INTERVALO_HORAS = 4 # Executa a cada 4 horas
INTERVALO_SEGUNDOS = INTERVALO_HORAS * 3600

logging.basicConfig(level=logging.INFO, format='%(asctime)s - AGENDADOR - %(message)s')
logger = logging.getLogger("Agendador")

if __name__ == "__main__":
    logger.info(f"=== INICIANDO AGENDADOR DE TAREFAS (Intervalo: {INTERVALO_HORAS}h) ===")
    
    while True:
        try:
            logger.info("⏰ Hora de trabalhar! Iniciando execução dos agentes...")
            main() # Chama o seu script principal
            logger.info("💤 Trabalho concluído. Dormindo...")
        except Exception as e:
            logger.error(f"❌ Erro durante a execução: {e}")
        
        # Espera o tempo definido
        time.sleep(INTERVALO_SEGUNDOS)