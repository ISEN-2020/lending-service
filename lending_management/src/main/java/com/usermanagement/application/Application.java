package com.usermanagement.application;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.autoconfigure.domain.EntityScan;
import org.springframework.data.jpa.repository.config.EnableJpaRepositories;

@SpringBootApplication(scanBasePackages = {"com.usermanagement"})
@EnableJpaRepositories("com.usermanagement.dao")
@EntityScan("com.usermanagement.model")
public class Application {
	
	public static void  main(String[] args) {
		SpringApplication.run(Application.class, args);
	}
}