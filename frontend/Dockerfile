# Use a imagem oficial do Node
FROM node:16-alpine

# Definir diretório de trabalho
WORKDIR /app

# Copiar arquivos de dependências
COPY package.json yarn.lock* ./

# Instalar dependências
RUN npm install

# Copiar o resto dos arquivos
COPY . .

# Construir a aplicação
RUN npm run build

# Instalar serve para servir os arquivos estáticos
RUN npm install -g serve

# Porta que o React usa
EXPOSE 3000

# Comando para rodar a aplicação
CMD ["serve", "-s", "build", "-l", "3000"]
