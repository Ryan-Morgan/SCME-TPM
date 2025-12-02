-- Ensure we are in the correct database
USE my_application_db;

-- 2. Create the USERS table with a UNIQUE constraint on userId
CREATE TABLE IF NOT EXISTS users (
    fName   VARCHAR(50) NOT NULL,
    lName   VARCHAR(50) NOT NULL,
    userId  INT(8) UNSIGNED NOT NULL
);
