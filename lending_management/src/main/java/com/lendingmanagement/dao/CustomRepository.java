package com.lendingmanagement.dao;

import java.util.List;

import com.lendingmanagement.model.LendBooks;

public interface CustomRepository {

	public LendBooks getBook();
	public LendBooks saveLend(LendBooks lb);
}
