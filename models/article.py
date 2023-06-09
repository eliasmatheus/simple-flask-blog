"""Arquivo com a estrutura da classe Article."""

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union
from models import Base
from shared.utils import *


class Article(Base):
    """Define a estrutura da tabela de artigos.

    Args:
        Base (Type[_DeclarativeBase]): Classe base para a criação de novas
            tabelas.
    """

    __tablename__ = "articles"

    id = Column(String(50), primary_key=True)
    title = Column(String(90), unique=True)
    subtitle = Column(String(200), nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    content = Column(Text, nullable=False)

    # Definição do relacionamento entre o comentário e um produto.
    # Aqui está sendo definido a coluna 'produto' que vai guardar
    # a referencia ao produto, a chave estrangeira que relaciona
    # um produto ao comentário.
    author_id = Column(
        Integer, ForeignKey("authors.pk_author", ondelete="CASCADE")
    )
    author = relationship(
        "Author", foreign_keys="Article.author_id", back_populates="articles"
    )

    def __init__(
        self,
        title: str,
        subtitle: str,
        author_id: int,
        content: str,
        id: str = None,
        created_at: Union[DateTime, None] = None,
    ):
        """
        Cria um novo artigo.

        Args:
            id (str, optional): ID do artigo. Se não for especificado, será
                gerado um ID baseado no título do artigo.
            title (str): Título do artigo.
            subtitle (str): Subtítulo do artigo.
            author (str): Autor do artigo.
            content (str): Conteúdo do artigo.
            created_at (datetime, optional): Data de publicação do artigo. Se
                não for especificada, a data de publicação será a data atual.

        Returns:
            None
        """
        # Se não for informado um ID, será gerado um baseado no título
        if not id:
            id = self.generate_id(title)

        # Se o ID for informado, o valor não será alterado mesmo que o título
        # seja, para evitar problemas de integridade referencial
        self.id = id
        self.title = title
        self.subtitle = subtitle
        self.author_id = author_id
        self.content = content

        # se não for informada, será o data exata da inserção no banco
        if created_at:
            self.created_at = created_at

    def generate_id(self, title):
        """Gera um id para o artigo baseado no título."""
        id_string = remove_special_chars(title)
        id_string = replace_spaces(id_string)
        id_string = add_date_prefix(id_string)
        id_string = limit_length(id_string, 50)
        return id_string.lower()
