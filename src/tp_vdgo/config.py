from typing import List
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings

class PUser(BaseModel):
    puser: str
    passwd: str

class NameKladrDBF(BaseModel):
    path: str

class Settings(BaseSettings):
    model_config = {"env_file": ".env.example", "extra": "ignore"}

    debug: bool = False
    db_host: str = "localhost"
    db_port: str = "5432"
    db_name: str = "tp_vdgo"
    db_user: str = "admin"
    db_pass: str = "admin123poi"

    path_kladr: str = "kladr"

    altnames: NameKladrDBF = Field(default_factory=lambda: NameKladrDBF(path="ALTNAMES.DBF"))
    doma: NameKladrDBF = Field(default_factory=lambda: NameKladrDBF(path="DOMA.DBF"))
    flat: NameKladrDBF = Field(default_factory=lambda: NameKladrDBF(path="FLAT.DBF"))
    kladr: NameKladrDBF = Field(default_factory=lambda: NameKladrDBF(path="KLADR.DBF"))
    namemap: NameKladrDBF = Field(default_factory=lambda: NameKladrDBF(path="NAMEMAP.DBF"))
    socrbase: NameKladrDBF = Field(default_factory=lambda: NameKladrDBF(path="SOCRBASE.DBF"))
    street: NameKladrDBF = Field(default_factory=lambda: NameKladrDBF(path="STREET.DBF"))
    

    super_vdgo: PUser = Field(default_factory=lambda: PUser(puser="super_vdgo", passwd="dyOM!Xv*f51!HaTyXqCLkP*eY821*XUs6lULg1$*6NAYDt6MtS"))
    admin_vdgo: PUser = Field(default_factory=lambda: PUser(puser="admin_vdgo", passwd="!Z4eeAtMAIORYt9!8tDX0i*!K8z8Tbw81DoWOFL]^7Y*RF^iJO"))
    user_vdgo: PUser = Field(default_factory=lambda: PUser(puser="user_vdgo", passwd="i7oVuPlgsSqr0EDxJSc0^Vz8UEfhq_nEIaxPbACFLjRXgjvGfa"))
    guest_vdgo: PUser = Field(default_factory=lambda: PUser(puser="guest_vdgo", passwd="y5Xq46iu^PQuoEsJftZ^o5aS27KO@sU48BZPmnGOxeN5oujEDM"))
    other_vdgo: PUser = Field(default_factory=lambda: PUser(puser="other_vdgo", passwd="ZV)qhvr6j!!lzGdA0^)KkCeYHT7^N9!5AsTd!QWmCStuSeFsk$"))

    @property
    def users(self) -> List[PUser]:
        return [
            self.super_vdgo,
            self.admin_vdgo,
            self.user_vdgo,
            self.guest_vdgo,
            self.other_vdgo
        ]
