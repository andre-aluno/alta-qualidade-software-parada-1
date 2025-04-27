FROM python:3.10-slim

# Define o diretório de trabalho
WORKDIR /app

# Copia todo o contexto do projeto para dentro do container
COPY . .

# (Opcional) Instala dependências, se houver requirements.txt
# RUN pip install --no-cache-dir -r requirements.txt

# Garante permissão de execução para o script
RUN chmod +x converter.py

# Ao iniciar, abre um shell interativo para permitir uso do CLI e execução de testes
CMD ["sh"]
