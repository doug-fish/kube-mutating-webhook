docker build -t webhook . && \
docker tag webhook dougfish1/internal-service-webhook:latest && \
docker push dougfish1/internal-service-webhook:latest
