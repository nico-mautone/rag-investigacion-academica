def build_prompt(query: str, contexts: list[dict], user_context: list[dict]) -> str:
    """
    Build a prompt that includes up to three context items (title, abstract), the user query, and the user context.
    """
    prompt_template = """
        Lee con atención la siguiente conversación previa:
        {user_context}

        El usuario realiza la siguiente consulta (puede ser una segunda pregunta que solo hace referencia a los artículos que ya le fueron proporcionados y no busca nuevos):
        {query}

        A continuación, se presentan los artículos disponibles que podrían ser relevantes para esta consulta:

        1) Título: "{title1}", Resumen: "{abstract1}"
        2) Título: "{title2}", Resumen: "{abstract2}"
        3) Título: "{title3}", Resumen: "{abstract3}"
        
        Tu objetivo es:

        - Analizar la consulta del usuario y determinar si los artículos anteriores están realmente relacionados con la nueva pregunta o tema planteado.
        - Si lo están, explica brevemente cómo estos trabajos difieren o se asemejan a la línea de investigación o pregunta del usuario.
        - Si no hay relación, indica de manera clara que no dispones de artículos relevantes para esa consulta y sugiere al usuario ampliar la búsqueda.
        - Responde siempre en el mismo idioma de la pregunta original, conservando los nombres de los artículos en su idioma original.
        - No inventes artículos que no aparezcan en la lista anterior ni información que no se haya proporcionado.
        - Sé breve al exponer las diferencias clave entre lo que pregunta el usuario y lo que presentan los artículos.
        - Con esta información, genera la mejor respuesta posible de acuerdo con las instrucciones anteriores.
    """

    # Extract up to 3 results
    titles = []
    abstracts = []
    for i in range(3):
        if i < len(contexts):
            titles.append(contexts[i].get("title", ""))
            abstracts.append(contexts[i].get("abstract", ""))
        else:
            titles.append("")
            abstracts.append("")

    # Format user context
    user_context_str = ""
    for item in user_context:
        user_context_str += f"Query: {item.get('query', '')}\nAnswer: {item.get('answer', '')}\n\n"

    return prompt_template.format(
        title1=titles[0],
        abstract1=abstracts[0],
        title2=titles[1],
        abstract2=abstracts[1],
        title3=titles[2],
        abstract3=abstracts[2],
        query=query,
        user_context=user_context_str.strip()
    ).strip()