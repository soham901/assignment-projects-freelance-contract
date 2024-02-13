FROM node:18-slim

WORKDIR /app

COPY package.json /app/package.json

RUN npm install

COPY . /app

CMD ["npm", "start"]

EXPOSE 5000