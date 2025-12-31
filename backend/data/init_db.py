from .db import engine, Base
from .models import User, EnergyRecord
from .carbon_models import CarbonCredit, CarbonTransaction

# Cria as tabelas no banco de dados
if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    print("Tabelas criadas com sucesso!")
