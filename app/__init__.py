from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query, status
from sqlalchemy_utils import database_exists
from sqlmodel import Session, select

from app.database import criar_db_e_tabelas, engine, get_session
from app.models import QuestionariosEnviados, QuestionarioPublic

if not database_exists(engine.url):
    criar_db_e_tabelas()


app = FastAPI()


@app.get("/respostas/{envio_id}")
def obter_respostas(envio_id: int, session: Annotated[Session, Depends(get_session)]) -> QuestionarioPublic:
    respostas = session.exec(select(QuestionariosEnviados).filter(QuestionariosEnviados.id == envio_id)).one()
    if not respostas:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Respostas não encontradas.")
    return respostas
