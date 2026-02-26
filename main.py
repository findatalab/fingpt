from components.rag import pipeline

chat_history_id = "user_123_session_1"

while True:
    question = input("Enter your question or Q to exit.\n🧑 ")
    if question == "Q":
        break

    res = pipeline.run(
        data={
            "embedder": {"text": question},
            "prompt_builder": {"query": question},
            "message_retriever": {"chat_history_id": chat_history_id},
            "message_writer": {"chat_history_id": chat_history_id},
        },
        include_outputs_from={"llm"},
    )
   
    print(f'🤖 {res["llm"]["replies"][0].text}')
