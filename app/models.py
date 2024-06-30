from sqlmodel import Field, Relationship, SQLModel


class QuestionariosBase(SQLModel):
    psicologo_id: int
    paciente_id: int
    questionario_id: int


class QuestionariosEnviados(QuestionariosBase, table=True):
    id: int = Field(primary_key=True)
    psicologo_id: int
    paciente_id: int
    questionario_id: int

    respostas: list["Resposta"] = Relationship(back_populates="questionario")


class RespostaBase(SQLModel):
    pergunta_id: int
    alternativa_id: int


class Resposta(RespostaBase, table=True):
    id: int = Field(primary_key=True)
    envio_id: int = Field(foreign_key="questionariosenviados.id")

    questionario: QuestionariosEnviados = Relationship(back_populates="respostas")


class RespostaPublic(RespostaBase):
    pass


class QuestionarioPublic(QuestionariosBase):
    respostas: list[RespostaPublic]


class Correcao(SQLModel, table=True):
    correcao_id: int = Field(primary_key=True)
    envio_id: int = Field(foreign_key="questionariosenviados.id")
    score: int
    resultado: str
