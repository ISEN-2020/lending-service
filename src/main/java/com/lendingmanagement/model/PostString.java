package com.lendingmanagement.model;


import javax.persistence.*;
import java.util.Date;

public class PostString {

	private String book;

	public PostString() {

	}

	public PostString(String book) {
		this.book=book;
	}
	


	public String getBook() {
		return this.book;
	}
}