FROM node:22.8.0

WORKDIR /usr/src/app

COPY package*.json ./
RUN npm install

# Copy the rest of the application code
COPY . .

# Compile the TypeScript code
RUN npm run build

EXPOSE 3000

CMD ["node", "dist/index.js"]
