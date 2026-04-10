from pydantic import BaseModel, Field

class Flat(BaseModel):
    code: str = Field(..., max_length=23, description="code")
    np: str = Field(..., max_length=4, description="np")
    gninmb: str = Field(..., max_length=4, description="gninmb")
    name: str = Field(..., max_length=40, description="name")
    index: str = Field(None, max_length=6, description="index")
    uno: str = Field(..., max_length=4, description="uno")

    @classmethod
    def get_pg_table_definition(cls) -> str:
        table = cls.__name__.lower()
        return f"""
            CREATE TABLE IF NOT EXISTS {table} (
                code CHAR(23) NOT NULL UNIQUE,
                np CHAR(4) NOT NULL,
                gninmb CHAR(4) NOT NULL,
                name CHAR(40) NOT NULL,
                index CHAR(6),
                uno CHAR(4) NOT NULL
            );

            CREATE INDEX idx_flat_code ON {table}(code);

            GRANT SELECT ON TABLE {table} TO admin_vdgo;
            GRANT SELECT ON TABLE {table} TO user_vdgo;
            GRANT SELECT ON TABLE {table} TO guest_vdgo;
            GRANT SELECT ON TABLE {table} TO other_vdgo;
        """