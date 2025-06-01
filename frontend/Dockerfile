FROM node:22.8.0 AS base

WORKDIR /usr/src/app

COPY package*.json ./
RUN npm install

# Copy the rest of the application code
COPY . .

# Stage for tests
FROM base AS test
CMD ["npm", "test"]

# Stage for frontend
FROM base AS frontend
RUN npm run build
EXPOSE 3000
CMD ["node", "dist/index.js"]
