#!/bin/sh
echo "⏳ Aguardando o banco de dados iniciar na porta 5432..."
while ! nc -z db 5432; do
  sleep 1
done
echo "✅ Banco de dados disponível!"

echo "Aplicando migrations..."
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head

echo "Iniciando servidor..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
