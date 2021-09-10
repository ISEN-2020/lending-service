package com.lendingmanagement.dao;

import java.util.List;

import javax.persistence.EntityManager;
import javax.persistence.NoResultException;
import javax.persistence.PersistenceContext;
import javax.persistence.Query;
import javax.transaction.Transactional;

import com.lendingmanagement.model.LendBooks;
import org.springframework.stereotype.Repository;

@Repository
public class CustomRepositoryImpl implements CustomRepository {

	private static final String QUERY_GET_ALL_BOOKS = "SELECT u.* FROM books_lend.books AS u";
	private static final String QUERY_COUNT_NAME = "Select case when count(case when u.name='%s' THEN 1 end) > %d then 1 else 0 end from books";	
	private static final String QUERY_SAVE_LEND = "INSERT INTO books_lend.books (id,book, name, email, date) VALUES (%d,'%s','%s','%s',NOW())";// CHANGE _ Ajout id 
	private static final String QUERY_GET_BOOK_BY_TITLE = "SELECT u.* FROM books_lend.books AS u WHERE u.book = ?1" ;
	private static final String QUERY_DELETE_BOOK = "DELETE FROM books_lend.books AS u WHERE u.book='%s' AND u.name='%s'";//delete with argument name of book and name of customer
	private static final String QUERY_GET_BOOK_EXPIRED = "SELECT u.* FROM books_lend.books AS u WHERE  NOW() > DATE_ADD(u.date , INTERVAL 30 DAY)" ;
	
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
        Query query = entityManager.createNativeQuery(String.format(QUERY_COUNT_NAME,lb.getName(),lb.getQuantitites()), LendBooks.class);
        if(query.getSingleResult() == null)
			return null;	

		query = null;
		query = entityManager.createNativeQuery(String.format(QUERY_SAVE_LEND,lb.getId(), lb.getBook(), lb.getName(), lb.getEmailAddress()), LendBooks.class);
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

	@Override
	@Transactional    // represente reutnBook _ ajout d'une requete vers book management pour set available book by ID
	public LendBooks returnBook(LendBooks lb) {  
		Query query = entityManager.createNativeQuery(String.format(QUERY_DELETE_BOOK, lb.getBook() , lb.getName(), LendBooks.class));
		query.executeUpdate();
		// Send set available to book management DB 
		return null;
	}

	@Override
	public List <LendBooks> getBookExpired() {
		Query query = entityManager.createNativeQuery(QUERY_GET_BOOK_EXPIRED, LendBooks.class);
		return query.getResultList();
	}

	
}
