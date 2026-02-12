docker-compose down
docker-compose up -d
timeout /t 5
docker logs ai-chatbot-backend
