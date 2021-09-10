package com.lendingmanagement.dao;

import java.util.List;

import com.lendingmanagement.model.LendBooks;
import com.lendingmanagement.model.PostString;

public interface CustomRepository {

	public List<LendBooks> getBook();
	public LendBooks saveLend(LendBooks lb);
	public LendBooks getBookByTitle(String title);
	public LendBooks deleteBookByTitle(String title);
	public List<LendBooks> getBookExpired();
}
