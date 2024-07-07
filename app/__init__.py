from typing import Annotated
from urllib.parse import quote_plus

import httpx
from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy_utils import database_exists
from sqlmodel import Session, select

from app.database import criar_db_e_tabelas, engine, get_session
from app.models import (
    QuestionarioPublic,
    QuestionariosBase,
    QuestionariosEnviados,
    QuestionariosEnviadosComStatus,
    Resposta,
)
from app.settings import Settings, get_settings

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
        return []
    return [
        QuestionariosEnviadosComStatus(
            id=questionario.id,
            psicologo_email=questionario.psicologo_email,
            paciente_email=questionario.paciente_email,
            questionario_id=questionario.questionario_id,
            respondido=len(questionario.respostas) > 0,
        )
        for questionario in questionarios_enviados
    ]


@app.get("/envios")
def obter_envios_por_email(email: str, session: Annotated[Session, Depends(get_session)]) -> QuestionariosEnviados:
    questionarios = session.exec(
        select(QuestionariosEnviados).filter(QuestionariosEnviados.paciente_email == email)
    ).all()
    for questionario in questionarios:
        if len(questionario.respostas) == 0:
            return questionario
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Envios não encontrados.")


@app.post("/envio")
async def registrar_envio(
    info_envio: QuestionariosBase,
    session: Annotated[Session, Depends(get_session)],
    settings: Annotated[Settings, Depends(get_settings)],
) -> None:
    session.add(QuestionariosEnviados(**info_envio.model_dump()))
    session.commit()

    data = {
        "email": quote_plus(info_envio.paciente_email),
        "subject": "Novo questionário atribuido a você",
        "message": f"Olá, você recebeu um novo questionário de {info_envio.psicologo_email}. Acesse este link para respondê-lo: {settings.FRONT_END_URL}/responder/{info_envio.paciente_email}",
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(f"{settings.PSITEST_EMAILS}/send-email", json=data)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)


@app.post("/responder")
def gravar_respostas(info_respostas: list[Resposta], session: Annotated[Session, Depends(get_session)]) -> None:
    session.add_all(info_respostas)
    session.commit()
