FROM maven:3.6.3-openjdk-14-slim AS MAVEN_BUILD	

COPY lending_management/pom.xml /build/
COPY lending_management/src /build/src/
WORKDIR /build/						

RUN mvn package spring-boot:repackage

FROM gcr.io/distroless/java:11

WORKDIR /app

COPY --from=MAVEN_BUILD /build/target/lending_management-1.0.0.jar /app/

ENTRYPOINT ["java", "-jar", "lending_management-1.0.0.jar"]
