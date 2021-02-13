FROM node:15.1.0-slim

ARG PORT
ARG DB_HOST
ARG DB_PORT
ARG DB_NAME

ENV DEBUG server
ENV PORT ${PORT}
ENV DB_HOST ${DB_HOST}
ENV DB_PORT ${DB_PORT}
ENV DB_NAME ${DB_NAME}

WORKDIR /usr/src/app

COPY package.json ./

COPY tsconfig.json ./

RUN npm install

COPY server.ts ./

CMD ["npx", "ts-node", "./server.ts"]

