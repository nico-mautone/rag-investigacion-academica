def build_prompt_for_initial_message(query: str, documents: list[dict]) -> str:
    """
    Build a prompt that includes up to three context items (title, abstract, score),
    the user query, and the user context, in English.
    Emphasizes plain text, no LaTeX, no enumerations, minimal special characters.
    Also indicates that the final response must show a similarity score for each relevant document.
    """
    prompt_template = """
        You are a conversational assistant helping a researcher find relevant information for their investigation.
        You have to detect the lenguage of the query and answer in that lenguge. The researcher is asking the following question. 
        {query}
       

        Below are up to three articles that you found and might be relevant to this query, 
        each with a Score indicating similarity to the user's query:

        1) Title: "{title1}", Abstract: "{abstract1}, Score: {score1}"
        2) Title: "{title2}", Abstract: "{abstract2}, Score: {score2}"
        3) Title: "{title3}", Abstract: "{abstract3}, Score: {score3}"
        
        Your objectives are:
        - Analyze the researcher's query and determine if these articles are actually related to the new question or topic.
        - If any of them are directly related to the topic, simply state that no relevant articles are available.
          In this situation never include any differences or similarities. Just say that you could not find any relevant articles.
        - If they are related, briefly explain how these works differ from or resemble the researcher's line of inquiry or question,
          and mention each one's similarity score (Score).
        - Do not invent articles that are not listed above or information that was not provided.
        - Be concise when explaining the key differences between the researcher's question and what the articles present.
        - Always respond in the same language as the user question, preserving the articles' original titles.
        It is COMPULSORY to answer in the same language as the user question. If the user question is in English, answer in English.

        FORMAT INSTRUCTIONS:
        - Respond as if you were the conversational assistant and you found these articles.
        - Return the answer in plain text, without enumerations or LaTeX or special escape sequences.
        - Avoid using bullet points (e.g., "*", "1)") or symbols like "\\".
        - Structure your text into clear, simple paragraphs.
        - If any document is relevant, include its Score in the answer.
        
        Based on all the above, respond to the researcher in the best possible way in the same language as the user question:
    """

    titles = []
    abstracts = []
    scores = []
    for i in range(3):
        if i < len(documents):
            titles.append(documents[i].get("title", ""))
            abstracts.append(documents[i].get("abstract", ""))
            scores.append(documents[i].get("score", ""))
        else:
            titles.append("")
            abstracts.append("")
            scores.append("")

    return prompt_template.format(
        title1=titles[0],
        abstract1=abstracts[0],
        score1=scores[0],
        title2=titles[1],
        abstract2=abstracts[1],
        score2=scores[1],
        title3=titles[2],
        abstract3=abstracts[2],
        score3=scores[2],
        query=query,
    ).strip()


def build_prompt_to_check_necessity_of_retrieving_documents(
    user_context: list[dict], user_query: str
) -> str:
    """
    Build a prompt (string) to check if it is necessary to retrieve more documents 
    based on the user context, in English, returning exactly 'True' or 'False'.
    Only includes the last 10 messages from user_context.
    (No mention of scores here, as no documents are shown.)
    """
    prompt_template = """
        You are an assistant helping a researcher find relevant information for their investigation.
        In previous messages, you recommended some articles that might be relevant to their work.
        
        Conversation history:
        {previous_queries}
        
        This is the researcher latest message: "{last_query}"

        Your objectives are:
        1) Analyze their latest message.
        2) Review the rest of the conversation.
        3) Determine if the researcher is asking something about the previously recommended articles, 
           or if they want you to find new ones.
        
        For instance, if they ask about a new topic, you might need to retrieve new articles.
        But if they ask something about any of the articles you already provided, you might not need to retrieve new ones.

        Your response MUST be exactly one of the following tokens, with no quotes and no extra text:
        True (If you think the researcher wants you to find new articles)
        False (If you think the researcher is asking about the previously recommended articles)
    """
    
    conversation = get_recent_conversation(user_context)
        
    return prompt_template.format(
        last_query=user_query,
        previous_queries=conversation.strip()
    ).strip()


def build_prompt_for_intermediate_message_with_new_docs(
    user_context: list[dict], new_query: str, new_contexts: list[dict]
) -> str:
    """
    Build a prompt that references the conversation so far (user_context),
    plus up to 3 new documents (new_contexts) with their Score,
    and instructs the LLM to respond in plain text, no LaTeX, no enumerations, minimal special characters.
    Includes the condition: if none of the documents are relevant, simply say so
    and do not mention any differences or similarities.
    Only includes the last 10 messages from user_context.
    Also includes 'Score' for each retrieved document and instructs the assistant
    to mention the score for each relevant doc in the final answer.
    """
    prompt_template = """
        You are a conversational assistant helping a researcher find relevant information.
        Below is the previous conversation, followed by the new query
        and up to three newly articles that you found at the knowledge base, 
        each with a Score indicating similarity to the user's query.

        {conversation_history}

        You have to detect the lenguage of the new user question and answer 
        in the same lenguage. If the user question is in English, answer in English.
        New user question:
        {user_query}


        Potentially relevant articles (with their Score):
        1) Title: "{title1}", Abstract: "{abstract1}, Score: {score1}"
        2) Title: "{title2}", Abstract: "{abstract2}, Score: {score2}"
        3) Title: "{title3}", Abstract: "{abstract3}, Score: {score3}"

        Your objectives:
        - Review the previous conversation so you don't repeat unnecessary information.
        - Integrate the new user question with the additional articles.
        - Indicate whether these articles are really relevant to the new question and how they connect (if they do).
        
        - Always respond in the same language as the user question, preserving the articles' original titles.
        It is COMPULSORY to answer in the same language as the user question. If the user question is in English, answer in English.
        - If any of the articles are directly related to the topic, simply state that no relevant articles are available, 
          and do not include any differences or similarities. Just say that, anything else.
        - If they are relevant, mention their Score to show how similar they are to the user's query.
        - Do not invent information or use LaTeX or special characters.

        FORMAT INSTRUCTIONS:
        - Respond as if you were the conversational assistant and you found these articles.
        - Use plain text, no bullet points or enumerations.
        - Avoid escape sequences like "\\n" or "\\".
        - Structure your response in one or more paragraphs, but without lists or extra symbols.
        - If any document is relevant, include its Score in the answer.

        Based on this, provide the best possible answer to the researcher in the same language as the new user question:
    """

    # Use the auxiliary function
    conversation = get_recent_conversation(user_context)

    titles = []
    abstracts = []
    scores = []
    for i in range(3):
        if i < len(new_contexts):
            titles.append(new_contexts[i].get("title", ""))
            abstracts.append(new_contexts[i].get("abstract", ""))
            scores.append(new_contexts[i].get("score", ""))
        else:
            titles.append("")
            abstracts.append("")
            scores.append("")

    prompt_filled = prompt_template.format(
        conversation_history=conversation.strip(),
        user_query=new_query,
        title1=titles[0],
        abstract1=abstracts[0],
        score1=scores[0],
        title2=titles[1],
        abstract2=abstracts[1],
        score2=scores[1],
        title3=titles[2],
        abstract3=abstracts[2],
        score3=scores[2]
    ).strip()

    return prompt_filled


def build_prompt_for_intermediate_message_without_new_docs(
    user_context: list[dict], new_query: str
) -> str:
    """
    Build a prompt that references the conversation so far, but indicates
    that no new documents are needed.
    
    Also states that if the previous documents are not relevant, 
    it should simply say so and not discuss any differences or similarities.
    Only includes the last 10 messages from user_context.
    (No need to include scores because no new docs are provided here.)
    """
    prompt_template = """
        You are a conversational assistant helping a researcher with relevant information.
        Below is the previous conversation, followed by the new question.
        
        Previous conversation:
        {conversation_history}

        You have to detect the lenguage of the new user question and answer 
        in the same lenguage. If the user question is in English, answer in English:
        New user question: {user_query}

        It has been determined that no new documents are necessary for this query.
        But information about the previous articles can be found in the conversation history.
        
        Therefore, your objectives are:
        - Analyse conversation history.
        - Analyse the new question.
        - Always respond in the same language as the user question, preserving the articles' original titles.
        It is COMPULSORY to answer in the same language as the user question. If the user question is in English, answer in English.
        It is COMPULSORY to answer in the same language as the new user question.
        - Answer the new question as best as you can based on the previous conversation. Be concise.
        - If you consider that you do not have enough information in the conversation history
          to answer the question, just say that you can not answer and suggest broadening the search.
        - If you reference any previously mentioned articles, you may optionally note their 
          Score if relevant. Otherwise, no new docs are being introduced here.

        FORMAT INSTRUCTIONS:
        - Respond in plain text, without enumerations or LaTeX notation.
        - Respond as if you were the conversational assistant and you found these articles.
        - Do not use special characters like "\\" or "\\n".
        - Avoid bullet points or numbered lists.
        - Keep your answer concise, in the same language as the original question.
        - If you mention any previously mentioned document, you can include its Score if helpful.

        Provide the best possible answer to the researcher in the same language as the new user question:
    """

    conversation = get_recent_conversation(user_context)

    prompt_filled = prompt_template.format(
        conversation_history=conversation.strip(),
        user_query=new_query
    ).strip()

    return prompt_filled


def build_prompt_for_query_refinement(
    user_context: list[dict], 
    last_query: str
) -> str:
    """
    Build a prompt asking the LLM to refine or enrich the user's last query
    based on the overall conversation (user_context), so that we can use 
    the resulting query in a vector database for more accurate retrieval.
    Only includes the last 10 messages from user_context.
    (No mention of scores here, as this is just for refining the query.)
    """
    prompt_template = """
        You are a conversational assistant helping a researcher find relevant information in a vector database.
        Below is the recent conversation history, and the researcher's latest query.

        Conversation history:
        {conversation}

        Last user query:
        {last_query}

        Your goal:
        - Analyze the conversation and the user's latest question to create ONE single refined query 
        in ENGLISH that captures the essential details needed to search relevant documents in a vector database.
        - If the user's query already seems clear, you can simply restate it. 
        - Do not add extraneous text or disclaimers. Your output must be only the refined query.

        FORMAT INSTRUCTIONS:
        - Return only the final refined query, as a short plain-text string.
        - Do not include latex, bullet points, slash escape sequences, or any additional commentary.
        - Make sure the query is well-formed and directly usable as input to a vector database search.

        Based on all the above, produce the best possible refined query:
    """
    conversation = get_recent_conversation(user_context)
    prompt_filled = prompt_template.format(
        conversation=conversation.strip(),
        last_query=last_query
    ).strip()

    return prompt_filled

def get_recent_conversation(user_context: list[dict], limit: int = 10) -> str:
    """
    Extract the last `limit` messages from the user context and format them as a conversation string.
    """
    recent_context = user_context[-limit:]
    conversation = ""
    for idx, turn in enumerate(recent_context, start=1):
        conversation += (
            f"User message {idx}: {turn.get('query', '')}\n Assistant answer: {turn.get('response', '')}\n\n"
        )
    return conversation.strip()