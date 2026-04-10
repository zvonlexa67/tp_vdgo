from pydantic import BaseModel, Field

class NameMap(BaseModel):
    code: str = Field(..., max_length=17, description="code")
    name: str = Field(..., max_length=250, description="name")
    shname: str = Field(..., max_length=40, description="shname")
    scname: str = Field(..., max_length=10, description="scname")

    @classmethod
    def get_pg_table_definition(cls) -> str:
        table = cls.__name__.lower()
        return f"""
            CREATE TABLE IF NOT EXISTS {table} (
                code CHAR(17) NOT NULL UNIQUE,
                name CHAR(250) NOT NULL,
                shname CHAR(40) NOT NULL,
                scname CHAR(10) NOT NULL
            );

            CREATE INDEX idx_namemap_code ON {table}(code);

            GRANT SELECT ON TABLE {table} TO admin_vdgo;
            GRANT SELECT ON TABLE {table} TO user_vdgo;
            GRANT SELECT ON TABLE {table} TO guest_vdgo;
            GRANT SELECT ON TABLE {table} TO other_vdgo;
        """