-- Drop tables if they already exist
DROP TABLE IF EXISTS UserTable CASCADE;
DROP TABLE IF EXISTS SessionStorage CASCADE;
DROP TABLE IF EXISTS EventData CASCADE;

-- Create the User table
CREATE TABLE UserTable (
    id SERIAL PRIMARY KEY,
    student_email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    major VARCHAR(10) CHECK (major IN ('UG', 'G')),
    role VARCHAR(10) CHECK (role IN ('Admin', 'Student')),
    session_key VARCHAR(255)
);

-- Create the Session Storage table
CREATE TABLE SessionStorage (
    session_id SERIAL PRIMARY KEY,
    session_key VARCHAR(255) UNIQUE NOT NULL,
    data TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create the EventData table
CREATE TABLE EventData (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    description TEXT NOT NULL,
    title VARCHAR(255) NOT NULL,
    location VARCHAR(255),
    time TIME NOT NULL,
    organizer VARCHAR(255) NOT NULL
);

INSERT INTO UserTable (student_email, username, password, role, major)
VALUES ('admin@example.com', 'admin', '$2b$12$U2zmQiz7mk61pVLjJRV2h.vPOPQ.vtOMvLfqmRJ8AHnD5ZWkR/2h.', 'Admin', NULL);