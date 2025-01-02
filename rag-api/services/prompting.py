def build_prompt(query: str, contexts: list[dict]) -> str:
    """
    Build a prompt that includes up to three context items (title, abstract) and the user query.
    """
    prompt_template = """
    You are an assistant helping a researcher find relevant academic papers.

    You have these top-3 relevant papers with titles and abstracts:
    1) Title: {title1}
       Abstract: {abstract1}
    2) Title: {title2}
       Abstract: {abstract2}
    3) Title: {title3}
       Abstract: {abstract3}

    The researcher asks: "{query}"

    Your tasks:
    - Analyze the abstracts and see how they relate to the research topic.
    - Summarize the key similarities or differences to the topic.
    - If none are relevant, say "I didn't find any relevant information to this topic".

    If any are relevant, respond with:
    "I have found relevant information about your research topic in the following papers:
        - Title: ...
        - Similarities: ...
        - Differences: ...
    "
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

    return prompt_template.format(
        title1=titles[0],
        abstract1=abstracts[0],
        title2=titles[1],
        abstract2=abstracts[1],
        title3=titles[2],
        abstract3=abstracts[2],
        query=query
    ).strip()