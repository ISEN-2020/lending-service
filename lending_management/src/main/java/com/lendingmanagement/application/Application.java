package com.lendingmanagement.application;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.autoconfigure.domain.EntityScan;
import org.springframework.data.jpa.repository.config.EnableJpaRepositories;

@SpringBootApplication(scanBasePackages = {"com.lendingmanagement"})
@EnableJpaRepositories("com.lendingmanagement.dao")
@EntityScan("com.lendingmanagement.model")
public class Application {
	
	public static void  main(String[] args) {
		SpringApplication.run(Application.class, args);
	}
}