from pydantic import BaseModel, Field

class Kladr(BaseModel):
    name: str = Field(..., max_length=40, description="name")
    socr: str = Field(..., max_length=10, description="socr")
    code: str = Field(..., max_length=13, description="code")
    index: str = Field(None, max_length=6, description="index")
    gninmb: str = Field(..., max_length=4, description="gninmb")
    uno: str = Field(None, max_length=4, description="uno")
    ocatd: str = Field(..., max_length=11, description="ocatd")
    status: str = Field(None, max_length=1, description="status")

    @classmethod
    def get_pg_table_definition(cls) -> str:
        table = cls.__name__.lower()
        return f"""
            CREATE TABLE IF NOT EXISTS {table} (
                name CHAR(40) NOT NULL,
                socr CHAR(10) NOT NULL,
                code CHAR(13) NOT NULL UNIQUE,
                index CHAR(6),
                gninmb CHAR(4) NOT NULL,
                uno CHAR(4),
                ocatd CHAR(11) NOT NULL,
                status CHAR(1)
            );

            CREATE INDEX idx_kladr_code ON {table}(code);

            GRANT SELECT ON TABLE {table} TO admin_vdgo;
            GRANT SELECT ON TABLE {table} TO user_vdgo;
            GRANT SELECT ON TABLE {table} TO guest_vdgo;
            GRANT SELECT ON TABLE {table} TO other_vdgo;
        """