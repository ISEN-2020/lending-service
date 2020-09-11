package com.lendingmanagement.dao;

import java.util.List;

import com.lendingmanagement.model.LendBooks;

public interface CustomRepository {

	public List<LendBooks> getBook();
	public LendBooks saveLend(LendBooks lb);
	public LendBooks getBookByTitle(String title);
}
