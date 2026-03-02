package com.bharatmarwah.mail_tool_service;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.scheduling.annotation.EnableAsync;

@SpringBootApplication
@EnableAsync
public class MailToolServiceApplication {

	public static void main(String[] args) {
		SpringApplication.run(MailToolServiceApplication.class, args);
		System.out.println("Mail Tool Service started successfully");
		System.out.println("Swagger UI available at: http://localhost:8080/swagger-ui.html");
	}

}
