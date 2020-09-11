package com.lendingmanagement.controller;


import com.lendingmanagement.dao.LendBooksDao;
import com.lendingmanagement.model.LendBooks;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.ResponseBody;

import java.util.Arrays;
import java.util.List;

@Controller
public class LendBookManagementController {
	
	@Autowired
	LendBooksDao lendBooksDao;
	
	@RequestMapping(path = "/getBooks", method = RequestMethod.GET)
	public @ResponseBody List<LendBooks> getBook() {
		return lendBooksDao.getBook();
	}
	
	@RequestMapping(path = "/saveLend", method = RequestMethod.POST, produces=MediaType.APPLICATION_JSON_VALUE)
	public @ResponseBody LendBooks saveLend(@RequestBody LendBooks lb) {
		System.out.println("ON PASSE DANS CONTROLLER");
		return lendBooksDao.saveLend(lb);
	}
	
	@RequestMapping(path = "/deleteUser", method = RequestMethod.POST, produces=MediaType.APPLICATION_JSON_VALUE)
	public @ResponseBody LendBooks deleteUser(String title) {
		LendBooks bookToDelete = lendBooksDao.getBookByTitle(title);
		lendBooksDao.deleteInBatch(Arrays.asList(bookToDelete));
		return bookToDelete;
	}
}