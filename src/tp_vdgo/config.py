from typing import List
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings

class PUser(BaseModel):
    puser: str
    passwd: str

class NameKladrDBF(BaseModel):
    file: str
    table: str
    path: str

class Settings(BaseSettings):
    model_config = {"env_file": ".env", "extra": "ignore"}

    debug: bool = False
    
    # Database
    db_host: str = "localhost"
    db_port: str = "5432"
    db_name: str = "tp_vdgo"
    db_user: str = "admin"
    db_pass: str = "admin123poi"

    # KLADR paths
    path_kladr: str = "kladr"
    
    altnames_file: str = "ALTNAMES.DBF"
    doma_file: str = "DOMA.DBF"
    flat_file: str = "FLAT.DBF"
    kladr_file: str = "KLADR.DBF"
    namemap_file: str = "NAMEMAP.DBF"
    socrbase_file: str = "SOCRBASE.DBF"
    street_file: str = "STREET.DBF"

    altnames_table: str = "altnames"
    doma_table: str = "doma"
    flat_table: str = "flat"
    kladr_table: str = "kladr"
    namemap_table: str = "namemap"
    socrbase_table: str = "socrbase"
    street_table: str = "street"

    # Users credentials
    super_user: str = "super_vdgo"
    super_passwd: str = "dyOM!Xv*f51!HaTyXqCLkP*eY821*XUs6lULg1$*6NAYDt6MtS"
    admin_user: str = "admin_vdgo"
    admin_passwd: str = "!Z4eeAtMAIORYt9!8tDX0i*!K8z8Tbw81DoWOFL]^7Y*RF^iJO"
    user_user: str = "user_vdgo"
    user_passwd: str = "i7oVuPlgsSqr0EDxJSc0^Vz8UEfhq_nEIaxPbACFLjRXgjvGfa"
    guest_user: str = "guest_vdgo"
    guest_passwd: str = "y5Xq46iu^PQuoEsJftZ^o5aS27KO@sU48BZPmnGOxeN5oujEDM"
    other_user: str = "other_vdgo"
    other_passwd: str = "ZV)qhvr6j!!lzGdA0^)KkCeYHT7^N9!5AsTd!QWmCStuSeFsk$"

    @property
    def altnames(self) -> NameKladrDBF:
        return NameKladrDBF(file=self.altnames_file, table=self.altnames_table, path=f"{self.path_kladr}/{self.altnames_file}")
    
    @property
    def doma(self) -> NameKladrDBF:
        return NameKladrDBF(file=self.doma_file, table=self.doma_table, path=f"{self.path_kladr}/{self.doma_file}")
    
    @property
    def flat(self) -> NameKladrDBF:
        return NameKladrDBF(file=self.flat_file, table=self.flat_table, path=f"{self.path_kladr}/{self.flat_file}")
    
    @property
    def kladr(self) -> NameKladrDBF:
        return NameKladrDBF(file=self.kladr_file, table=self.kladr_table, path=f"{self.path_kladr}/{self.kladr_file}")
    
    @property
    def namemap(self) -> NameKladrDBF:
        return NameKladrDBF(file=self.namemap_file, table=self.namemap_table, path=f"{self.path_kladr}/{self.namemap_file}")
    
    @property
    def socrbase(self) -> NameKladrDBF:
        return NameKladrDBF(file=self.socrbase_file, table=self.socrbase_table, path=f"{self.path_kladr}/{self.socrbase_file}")
    
    @property
    def street(self) -> NameKladrDBF:
        return NameKladrDBF(file=self.street_file, table=self.street_table, path=f"{self.path_kladr}/{self.street_file}")

    @property
    def super_vdgo(self) -> PUser:
        return PUser(puser=self.super_user, passwd=self.super_passwd)
    
    @property
    def admin_vdgo(self) -> PUser:
        return PUser(puser=self.admin_user, passwd=self.admin_passwd)
    
    @property
    def user_vdgo(self) -> PUser:
        return PUser(puser=self.user_user, passwd=self.user_passwd)
    
    @property
    def guest_vdgo(self) -> PUser:
        return PUser(puser=self.guest_user, passwd=self.guest_passwd)
    
    @property
    def other_vdgo(self) -> PUser:
        return PUser(puser=self.other_user, passwd=self.other_passwd)

    @property
    def users(self) -> List[PUser]:
        return [
            self.super_vdgo,
            self.admin_vdgo,
            self.user_vdgo,
            self.guest_vdgo,
            self.other_vdgo
        ]
