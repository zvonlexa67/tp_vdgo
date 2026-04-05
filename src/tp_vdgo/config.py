from typing import List
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings

class PUser(BaseModel):
    puser: str
    passwd: str

class Settings(BaseSettings):
    model_config = {"env_file": ".env.example", "extra": "ignore"}

    debug: bool = False
    db_host: str = "localhost"
    db_port: str = "5432"
    db_name: str = "tp_vdgo"
    db_user: str = "admin"
    db_pass: str = "admin123poi"

    db_path_kladr: str = ""

    super_vdgo: PUser = Field(default_factory=lambda: PUser(puser="super_vdgo", passwd="dyOM+Xv#f51!HaTyXqCLkP+&Y%21(XUs6lULg1$#6NAYDt6%iS"))
    admin_vdgo: PUser = Field(default_factory=lambda: PUser(puser="admin_vdgo", passwd="#Z4eeAtMAIORYt9#8tDX0i*+K8z8Tbw81DoWOFL+^7Y*RF^iJO"))
    user_vdgo: PUser = Field(default_factory=lambda: PUser(puser="user_vdgo", passwd="i7oVuPlgsSqr0EDxJSc0^Vz8UEfhq_nEIaxPbACFLjRXgjvGfa"))
    guest_vdgo: PUser = Field(default_factory=lambda: PUser(puser="guest_vdgo", passwd="y5Xq46iu^PQuoEsJftZ^o5aS27KO@sU48BZPmnGOxeN5ouj%DM"))
    other_vdgo: PUser = Field(default_factory=lambda: PUser(puser="other_vdgo", passwd="ZV)qhvr6j#!lzGdA0^)KkCeYHT7^N9!5AsTd!QWmCStu%eFsk$"))

    @property
    def users(self) -> List[PUser]:
        return [
            self.super_vdgo,
            self.admin_vdgo,
            self.user_vdgo,
            self.guest_vdgo,
            self.other_vdgo
        ]
