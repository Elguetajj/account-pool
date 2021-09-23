
CREATE DATABASE bitcoin;
USE bitcoin;

CREATE TABLE accounts (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	`name` VARCHAR(40), 
	`address` VARCHAR(40), 
    created TIMESTAMP,
	PRIMARY KEY (id)
);