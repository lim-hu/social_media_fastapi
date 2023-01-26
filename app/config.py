from pydantic import BaseSettings

class Settings(BaseSettings):
    db_host: str
    db_port: str
    db_user: str
    db_pass: str
    db_name: str
    secret_key: str
    algorithm: str
    access_token_exp: int
    reset_token_exp: int
    
    from_email: str
    email_pass: str
    
    class Config:
        env_file = '.env'
    
settings = Settings()
    