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

	private static final String QUERY_GET_EXPIRED = "SELECT u.* FROM user.user AS u";
	private static final String QUERY_SAVE_LEND = "INSERT INTO user.user (name, email, password) VALUES ('%s','%s','%s')";
	
	@PersistenceContext
	EntityManager entityManager;
	
	@SuppressWarnings("unchecked")
	@Override
	public LendBooks getBook() {
		Query query = entityManager.createNativeQuery(QUERY_GET_EXPIRED, User.class);
		return query.getResultList();
	}

	@Override
	@Transactional
	public LendBooks saveLend(LendBooks lb) {
		Query query = entityManager.createNativeQuery(String.format(QUERY_SAVE_LEND, lb.getBookName(), lb.getName(), lb.getEmailAddress(), lb.getLendDate()), LendBooks.class);
		query.executeUpdate();
		return lb;
	}

}
