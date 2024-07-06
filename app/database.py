from sqlmodel import Session, SQLModel, create_engine

from app.models import Resposta, QuestionariosEnviados, Correcao  # noqa: F401

sqlite_file_name = "database.sqlite"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


def criar_db_e_tabelas():
    SQLModel.metadata.create_all(engine)

    respostas = [
        Resposta(envio_id=1, pergunta_id=1, alternativa_id=1),
        Resposta(envio_id=1, pergunta_id=2, alternativa_id=3),
        Resposta(envio_id=1, pergunta_id=5, alternativa_id=2),
    ]
    questionario = QuestionariosEnviados(
        psicologo_email="vitor771@gmail.com", paciente_email="teste@email.com", questionario_id=1, respostas=respostas
    )
    with Session(engine) as session:
        session.add(questionario)
        session.commit()


def get_session():
    with Session(engine) as session:
        yield session
