package com.lendingmanagement.controller;


import com.lendingmanagement.dao.LendBooksDao;
import com.lendingmanagement.model.LendBooks;
import com.lendingmanagement.model.PostString;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.*;

import java.util.*;
import java.text.SimpleDateFormat;

@Controller
@CrossOrigin
public class LendBookManagementController {
	
	@Autowired
	LendBooksDao lendBooksDao;
	
	@RequestMapping(path = "/getBooks", method = RequestMethod.GET)
	public @ResponseBody List<LendBooks> getBook() {
		return lendBooksDao.getBook();
	}
	//lendbook
	@RequestMapping(path = "/saveLend", method = RequestMethod.POST, produces=MediaType.APPLICATION_JSON_VALUE)
	public @ResponseBody LendBooks saveLend(@RequestBody LendBooks lb) {
		return lendBooksDao.saveLend(lb);
	}
	//returnbook
	@RequestMapping(path = "/deleteBook", method = RequestMethod.POST, produces=MediaType.APPLICATION_JSON_VALUE)
	public @ResponseBody LendBooks returnBooks(@RequestBody LendBooks lb) {
		//LendBooks bookToDelete = lendBooksDao.getBookByTitle(poststring.getBook());
		//System.out.println(bookToDelete.getBook());
		//lendBooksDao.delete(bookToDelete);//.deleteInBatch(Arrays.asList(bookToDelete));
		//lendBooksDao.flush();
		//return bookToDelete;

		return lendBooksDao.returnBook(lb);
	}

	@RequestMapping(path = "/getBookExpired", method = RequestMethod.GET)
	public @ResponseBody List<LendBooks> getBookExpired() { return lendBooksDao.getBookExpired(); }

}