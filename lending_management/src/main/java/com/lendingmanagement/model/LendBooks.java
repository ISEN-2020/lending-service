package com.lendingmanagement.model;


import javax.persistence.*;
import java.text.SimpleDateFormat;
import java.util.Date;

@Entity
public class LendBooks {

	@Id
	@GeneratedValue(strategy=GenerationType.AUTO)
	@Column(name="id", columnDefinition = "SMALLINT")
	private int id;

	@Column(name="book", columnDefinition = "VARCHAR(100)")
	private String book;

	@Column(name="name", columnDefinition = "VARCHAR(40)")
	private String name;

	@Column(name="email", columnDefinition = "VARCHAR(40)")
	private String emailAddress;

	@Column(name="date", columnDefinition = "DATE")
	private Date lendDate;



	public LendBooks() {
	}

	public LendBooks( String book, String name, String emailAddress) {
		this.name=name;
		this.emailAddress=emailAddress;
		this.book=book;
	}
	
	public int getId() {
		return this.id;
	}

	public String getBook() {
		return this.book;
	}
	public String getName() {
		return this.name;
	}
	public String getEmailAddress() {
		return this.emailAddress;
	}
	public Date getDate(){
		return this.lendDate;
	}

}