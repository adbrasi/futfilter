# Importa a classe do nosso arquivo
from .prompt_processor import PromptProcessor

# Mapeia o nome da classe para um nome amigável que aparecerá na interface
NODE_CLASS_MAPPINGS = {
    "PromptProcessorNode": PromptProcessor
}

# Define o nome que será exibido no menu do ComfyUI
NODE_DISPLAY_NAME_MAPPINGS = {
    "PromptProcessorNode": "futa filter"
}

# Mensagem de confirmação que aparecerá no console ao iniciar o ComfyUI
print("✅ futa filter Node by bumbumzin sujo loaded")

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']