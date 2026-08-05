# Build stage
FROM node:20-alpine AS builder

WORKDIR /app

# Copy package files
COPY package.json package-lock.json* ./

# Install dependencies
RUN npm install

# Copy source code
COPY . .

# Build the application
RUN npm run build

# Production stage - Static file server for Render
FROM node:20-alpine AS runner

WORKDIR /app

# Copy built files from builder stage
COPY --from=builder /app/dist ./dist

# Install serve for static file serving
RUN npm install -g serve

# Expose port (Render uses PORT env var)
EXPOSE $PORT

# Serve static files
CMD ["serve", "-s", "dist", "-l", "tcp://0.0.0.0:$PORT"]