from pydantic import BaseModel, Field

class SocrBase(BaseModel):
    level: str = Field(..., max_length=5, description="level")
    scname: str = Field(..., max_length=10, description="scname")
    socrname: str = Field(..., max_length=29, description="socrname")
    kod_t_st: str = Field(..., max_length=3, description="kod_t_st")

    @classmethod
    def get_pg_table_definition(cls) -> str:
        table = cls.__name__.lower()
        return f"""
            CREATE TABLE IF NOT EXISTS {table} (
                level CHAR(5) NOT NULL,
                scname CHAR(10) NOT NULL,
                socrname CHAR(29) NOT NULL,
                kod_t_st CHAR(3) NOT NULL
            );

            GRANT SELECT ON TABLE {table} TO admin_vdgo;
            GRANT SELECT ON TABLE {table} TO user_vdgo;
            GRANT SELECT ON TABLE {table} TO guest_vdgo;
            GRANT SELECT ON TABLE {table} TO other_vdgo;
        """