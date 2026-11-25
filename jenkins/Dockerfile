FROM jenkins/jenkins:lts-jdk17
USER root
# CLI de Docker (para que Jenkins use el Docker del host)
COPY --from=docker:cli /usr/local/bin/docker /usr/local/bin/docker
USER root
