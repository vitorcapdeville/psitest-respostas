from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy_utils import database_exists
from sqlmodel import Session, select

from app.database import criar_db_e_tabelas, engine, get_session
from app.models import QuestionariosBase, QuestionariosEnviados, QuestionarioPublic, QuestionariosEnviadosComStatus

if not database_exists(engine.url):
    criar_db_e_tabelas()


app = FastAPI()


@app.get("/respostas/{envio_id}")
def obter_respostas(envio_id: int, session: Annotated[Session, Depends(get_session)]) -> QuestionarioPublic:
    respostas = session.exec(select(QuestionariosEnviados).filter(QuestionariosEnviados.id == envio_id)).one()
    if not respostas:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Respostas não encontradas.")
    return respostas


@app.get("/respostas")
def obter_respostas_psicologo(
    email: str, session: Annotated[Session, Depends(get_session)]
) -> list[QuestionariosEnviadosComStatus]:
    questionarios_enviados = session.exec(
        select(QuestionariosEnviados).filter(QuestionariosEnviados.psicologo_email == email)
    ).all()
    if not questionarios_enviados:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Respostas não encontradas.")
    return [
        QuestionariosEnviadosComStatus(
            psicologo_email=questionario.psicologo_email,
            paciente_email=questionario.paciente_email,
            questionario_id=questionario.questionario_id,
            respondido=len(questionario.respostas) > 0,
        )
        for questionario in questionarios_enviados
    ]


@app.post("/envio")
def registrar_envio(info_envio: QuestionariosBase, session: Annotated[Session, Depends(get_session)]) -> None:
    session.add(QuestionariosEnviados(**info_envio.model_dump()))
    session.commit()
