from pydantic import BaseModel, Field

class Altnames(BaseModel):
    oldcode: str = Field(..., max_length=19, description="Старый код")
    newcode: str = Field(..., max_length=19, description="Новый код")
    level: str = Field(..., max_length=1, description="Уровень")

    @classmethod
    def get_pg_table_definition(cls) -> str:
        table = cls.__name__.lower()
        return f"""
                CREATE TABLE IF NOT EXISTS {table} (
                    oldcode CHAR(19) NOT NULL,
                    newcode CHAR(19) NOT NULL,
                    level CHAR(1) NOT NULL
                );

                GRANT SELECT ON TABLE {table} TO admin_vdgo;
                GRANT SELECT ON TABLE {table} TO user_vdgo;
                GRANT SELECT ON TABLE {table} TO guest_vdgo;
                GRANT SELECT ON TABLE {table} TO other_vdgo;
            """