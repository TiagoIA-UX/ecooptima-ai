# EcoOptima AI

Plataforma SaaS para otimização energética e rastreamento de carbono com IA.

## Setup rápido

1. Instale dependências do backend:
   ```bash
   pip install -r backend/requirements.txt
   ```
2. Instale dependências do frontend:
   ```bash
   cd frontend && npm install
   ```
3. Execute o backend:
   ```bash
   uvicorn backend.api.main:app --reload
   ```
4. Execute o frontend:
   ```bash
   npm start
   ```

## Testando a integração

1. Acesse o frontend em http://localhost:3000
2. Digite valores (ex: 6,7,8) e clique em "Prever Consumo".
3. O resultado será exibido com base no modelo de IA do backend.
