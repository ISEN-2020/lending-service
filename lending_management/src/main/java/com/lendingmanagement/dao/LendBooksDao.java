package com.lendingmanagement.dao;

import com.lendingmanagement.model.LendBooks;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import com.lendingmanagement.model.LendBooks;

@Repository
public interface LendBooksDao extends JpaRepository<LendBooks, Integer>, CustomRepository{

}
