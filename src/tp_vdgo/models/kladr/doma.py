from pydantic import BaseModel, Field


class Doma(BaseModel):
    name: str = Field(..., max_length=40, description="name")
    korp: str = Field(None, max_length=10, description="korp")
    socr: str = Field(..., max_length=10, description="socr")
    code: str = Field(..., max_length=19, description="code")
    index: str = Field(None, max_length=6, description="index")
    gninmb: str = Field(..., max_length=4, description="gninmb")
    uno: str = Field(None, max_length=4, description="uno")
    ocatd: str = Field(..., max_length=11, description="ocatd")

    @classmethod
    def get_pg_table_definition(cls) -> str:
        table = cls.__name__.lower()
        return f"""
            CREATE TABLE IF NOT EXISTS {table} (
                name CHAR(40) NOT NULL,
                korp CHAR(10),
                socr CHAR(10) NOT NULL,
                code CHAR(19) NOT NULL UNIQUE,
                index CHAR(6),
                gninmb CHAR(4) NOT NULL,
                uno CHAR(4),
                ocatd CHAR(11) NOT NULL
            );

            CREATE INDEX idx_doma_code ON {table}(code);

            GRANT SELECT ON TABLE {table} TO admin_vdgo;
            GRANT SELECT ON TABLE {table} TO user_vdgo;
            GRANT SELECT ON TABLE {table} TO guest_vdgo;
            GRANT SELECT ON TABLE {table} TO other_vdgo;
        """