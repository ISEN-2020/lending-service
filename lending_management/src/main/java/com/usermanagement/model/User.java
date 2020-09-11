package com.usermanagement.model;


import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;

import com.fasterxml.jackson.annotation.JsonIgnore;

@Entity
public class User {
	
	@Id
	@GeneratedValue(strategy=GenerationType.AUTO)
	@Column(name="id", columnDefinition = "SMALLINT")
	private int id;
	
	@Column(name="name", columnDefinition = "VARCHAR(40)")
	private String name;
	
	@Column(name="email", columnDefinition = "VARCHAR(40)")
	private String emailAddress;
	
	@Column(name="password", columnDefinition = "VARCHAR(40)")
	private String password;
	
	@Column(name="enabled", columnDefinition = "TINYINT")
	private boolean enabled;
	
	public User() {
		
	}
	
	public User(String name, String emailAddress, String password) {
		this.name=name;
		this.emailAddress=emailAddress;
		this.password=password;
		this.enabled=true;
	}
	
	public int getId() {
		return this.id;
	}
	
	public String getName() {
		return this.name;
	}
	public String getEmailAddress() {
		return this.emailAddress;
	}
	
	public String getPassword() {
		return this.password;
	}
	
	public boolean getEnabled() {
		return this.enabled;
	}
}