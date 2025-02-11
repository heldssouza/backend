# Build stage
FROM node:18-alpine as build-stage

WORKDIR /app

# Instala as dependências
COPY package*.json ./
RUN npm install

# Copia o código fonte
COPY . .

# Compila a aplicação
RUN npm run build

# Production stage
FROM nginx:stable-alpine as production-stage

# Remove a configuração padrão do nginx
RUN rm -rf /etc/nginx/conf.d/*

# Copia a configuração personalizada do nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copia os arquivos compilados do estágio anterior
COPY --from=build-stage /app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
