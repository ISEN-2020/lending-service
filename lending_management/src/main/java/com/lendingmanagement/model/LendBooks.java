package com.lendingmanagement.model;


import javax.persistence.*;
import java.util.Date;

@Entity
public class LendBooks {

	@Id
	@GeneratedValue(strategy=GenerationType.AUTO)
	@Column(name="id", columnDefinition = "SMALLINT")
	private int id;

	@Column(name="book", columnDefinition = "VARCHAR(100)")
	private String bookname;

	@Column(name="name", columnDefinition = "VARCHAR(40)")
	private String name;

	@Column(name="email", columnDefinition = "VARCHAR(40)")
	private String emailAddress;

	@Column(name="date", columnDefinition = "DATE")
	private Date lendDate;



	public LendBooks() {

	}

	public LendBooks(String name, String emailAddress, String password) {
		this.name=name;
		this.emailAddress=emailAddress;
	}
	
	public int getId() {
		return this.id;
	}

	public String getBookName() {
		return this.bookname;
	}
	public String getName() {
		return this.name;
	}
	public String getEmailAddress() {
		return this.emailAddress;
	}
	public Date getLendDate() {
		return this.lendDate;
	}

}