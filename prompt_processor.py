import re

class PromptProcessor:
    """
    Um nó para limpar, substituir e adicionar tags a um prompt de texto ou a uma lista de prompts.
    Ele processa cada prompt tratando-o como uma lista de tags separadas por vírgula.
    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "text": ("STRING", {"forceInput": True}),
                "tags_to_remove": ("STRING", {
                    "multiline": True,
                    "default": "# Tags para remover (uma por linha)\nbad_hands\nworst_quality"
                }),
                "tags_to_replace": ("STRING", {
                    "multiline": True,
                    "default": "# Tags para substituir (formato: old > new)\nholding_phone > holding_cellphone\n1boy > 1girl, solo"
                }),
                "tags_to_append": ("STRING", {
                    "multiline": True,
                    "default": "# Tags para sempre adicionar (uma por linha)\nmasterpiece\nbest_quality"
                }),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("processed_text",)
    FUNCTION = "process"
    CATEGORY = "text/utils" # Categoria onde o nó aparecerá no menu

    def process(self, text, tags_to_remove, tags_to_replace, tags_to_append):
        # --- 1. Preparar as regras ---

        # Converte a string multilinha de remoção para uma lista de tags limpas
        remove_list = {tag.strip() for tag in tags_to_remove.splitlines() if tag.strip() and not tag.strip().startswith('#')}

        # Converte a string multilinha de substituição para um dicionário (old: new)
        replace_dict = {}
        for line in tags_to_replace.splitlines():
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if '>' in line:
                parts = [p.strip() for p in line.split('>', 1)]
                if len(parts) == 2 and parts[0]:
                    replace_dict[parts[0]] = parts[1]

        # Converte a string multilinha de adição para uma lista de tags limpas
        append_list = [tag.strip() for tag in tags_to_append.splitlines() if tag.strip() and not tag.strip().startswith('#')]

        # --- 2. Processar o texto de entrada ---

        # Verifica se a entrada é uma lista (para processamento em lote) ou uma string única
        is_list = isinstance(text, list)
        if not is_list:
            text = [text] # Transforma em lista para unificar o processamento

        processed_prompts = []

        for prompt in text:
            # Divide o prompt em tags individuais pela vírgula
            # Isso garante que só substituiremos tags exatas, e não partes de outras palavras
            tags = [tag.strip() for tag in prompt.split(',') if tag.strip()]
            
            # --- 3. Aplicar as regras em cada tag ---
            
            new_tags = []
            for tag in tags:
                # Primeiro, aplica a substituição. Se a tag não estiver no dicionário, usa a original.
                processed_tag = replace_dict.get(tag, tag)
                
                # Depois, verifica se a tag (original ou substituída) deve ser removida
                # A substituição pode resultar em múltiplas tags, então dividimos novamente
                sub_tags = [st.strip() for st in processed_tag.split(',') if st.strip()]
                
                for st in sub_tags:
                    if st not in remove_list:
                        new_tags.append(st)

            # Adiciona as tags da lista de "append"
            new_tags.extend(append_list)

            # --- 4. Limpeza final e montagem do prompt ---

            # Remove duplicatas mantendo a ordem (importante para prioridade de prompts)
            final_tags = []
            seen = set()
            for tag in new_tags:
                if tag not in seen:
                    final_tags.append(tag)
                    seen.add(tag)

            processed_prompt = ", ".join(final_tags)
            processed_prompts.append(processed_prompt)

        # --- 5. Retornar no mesmo formato da entrada ---
        
        if is_list:
            return (processed_prompts,)
        else:
            return (processed_prompts[0],)