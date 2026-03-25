from flask import Flask, render_template, request, jsonify
from components.rag import pipeline
from .models import db, ChatHistory


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
    db.init_app(app)
    with app.app_context():
        db.create_all()
    # Идентификатор для хранения истории чата в рамках одного сеанса. В реальном приложении это  связано с сессией пользователя.
    chat_history_id = "default_chat_history"

    @app.route("/")
    def home():
        return render_template("index.html")

    @app.route("/chatbot")
    @app.route("/fingpt")
    def chatbot_page():
        chat_history = ChatHistory.query.order_by(ChatHistory.timestamp.asc()).all()
        return render_template("fingpt.html", chat_history=chat_history)

    @app.route("/chat", methods=["POST"])
    def chat():
        data = request.get_json()
        user_message = data.get("message", "")

        reply_dict = pipeline.run(
            data={
                "embedder": {"text": user_message},
                "prompt_builder": {"query": user_message},
                "message_retriever": {"chat_history_id": chat_history_id},
                "message_writer": {"chat_history_id": chat_history_id},
            },
            include_outputs_from={"llm"},
        )
        llm_reply = str(
            reply_dict["llm"]["replies"][0].text
        )  # Извлекаем ответ LLM из словаря
        print(
            "Pipeline outputs:", llm_reply
        )  

        # Save to chat history
        new_entry = ChatHistory(user_message=user_message, llm_reply=llm_reply)
        db.session.add(new_entry)
        db.session.commit()
        return jsonify({"reply": llm_reply})

    return app
