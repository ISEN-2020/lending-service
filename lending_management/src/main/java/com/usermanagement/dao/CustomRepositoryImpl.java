package com.usermanagement.dao;

import java.util.List;

import javax.persistence.EntityManager;
import javax.persistence.NoResultException;
import javax.persistence.PersistenceContext;
import javax.persistence.Query;
import javax.transaction.Transactional;

import org.springframework.stereotype.Repository;

import com.usermanagement.model.User;

@Repository
public class CustomRepositoryImpl implements CustomRepository {

	private static final String QUERY_GET_USER_BY_ID = "SELECT u.* FROM user.user AS u WHERE u.id = ?1" ;
	private static final String QUERY_GET_USERS = "SELECT u.* FROM user.user AS u";
	private static final String QUERY_SAVE_USER = "INSERT INTO user.user (name, email, password) VALUES ('%s','%s','%s')";
	
	@PersistenceContext
	EntityManager entityManager;
	
	@SuppressWarnings("unchecked")
	@Override
	public List<User> getUsers() {
		Query query = entityManager.createNativeQuery(QUERY_GET_USERS, User.class);
		return query.getResultList();
	}

	@Override
	@Transactional
	public User saveUser(User user) {
		Query query = entityManager.createNativeQuery(String.format(QUERY_SAVE_USER, user.getName(), user.getEmailAddress(), user.getPassword()), User.class);
		query.executeUpdate();
		System.out.println(user.getPassword());
		return this.getUserById(user.getId());
	}

	@Override
	public User getUserById(int id) {
		Query query = entityManager.createNativeQuery(QUERY_GET_USER_BY_ID, User.class);
		query.setParameter(1, id);
		try{
		return (User) query.getSingleResult();
		}catch (NoResultException nre){
			//Ignore this because as per your logic this is ok!
			}
		return null;
	}
}
