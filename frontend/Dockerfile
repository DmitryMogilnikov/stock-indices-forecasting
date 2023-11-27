FROM node:latest

WORKDIR frontend

ENV PATH /frontend/node_modules/.bin:$PATH


COPY . /frontend

RUN npm install --silent

CMD ["npm","run", "start"]