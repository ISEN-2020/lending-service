package com.lendingmanagement.dao;

import java.util.List;

import javax.persistence.EntityManager;
import javax.persistence.NoResultException;
import javax.persistence.PersistenceContext;
import javax.persistence.Query;
import javax.transaction.Transactional;

import com.lendingmanagement.dao.CustomRepository;
import com.lendingmanagement.model.LendBooks;
import org.springframework.stereotype.Repository;

@Repository
public class CustomRepositoryImpl implements CustomRepository {

	private static final String QUERY_GET_ALL_BOOKS = "SELECT u.* FROM books_lend.books AS u";
	private static final String QUERY_SAVE_LEND = "INSERT INTO books_lend.books (book, name, email, date) VALUES ('%s','%s','%s','%tF')";
	private static final String QUERY_GET_BOOK_BY_TITLE = "SELECT u.* FROM books_lend.books AS u WHERE u.book = ?1" ;

	
	@PersistenceContext
	EntityManager entityManager;
	
	@SuppressWarnings("unchecked")
	@Override
	public List<LendBooks> getBook() {
		Query query = entityManager.createNativeQuery(QUERY_GET_ALL_BOOKS, LendBooks.class);
		return query.getResultList();
	}

	@Override
	@Transactional
	public LendBooks saveLend(LendBooks lb) {
		Query query = entityManager.createNativeQuery(String.format(QUERY_SAVE_LEND, lb.getBookName(), lb.getName(), lb.getEmailAddress(), lb.getLendDate()), LendBooks.class);
		query.executeUpdate();
		return lb;
	}

	@Override
	public LendBooks getBookByTitle(String title) {
		Query query = entityManager.createNativeQuery(QUERY_GET_BOOK_BY_TITLE, LendBooks.class);
		query.setParameter(1, title);
		try{
			return (LendBooks) query.getSingleResult();
		}catch (NoResultException nre){
			//Ignore this because as per your logic this is ok!
		}
		return null;
	}

}
