FROM node:20-alpine

WORKDIR /app

# Copia o package.json e instala as dependências durante o build
COPY package*.json ./
RUN npm install

# Copia o resto dos arquivos do projeto
COPY . .

EXPOSE 3000

# Comando padrão para iniciar o Vite
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "3000"]