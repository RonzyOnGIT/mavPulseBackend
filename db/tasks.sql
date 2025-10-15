-- This file sets up the database tables for the mavpulse project

-- Create tables.
CREATE TABLE users
(
    id UUID PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE courses
(
    id SERIAL PRIMARY KEY,
    department VARCHAR(10) NOT NULL,
    code VARCHAR(10) NOT NULL,
    course_name VARCHAR(500) NOT NULL
);

CREATE TABLE notes
(
    id SERIAL PRIMARY KEY,
    title VARCHAR(50) NOT NULL,
    user_id UUID REFERENCES users(id),
    course_id INTEGER REFERENCES courses(id),
    created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE events
(
    id SERIAL PRIMARY KEY,
    title VARCHAR(50) NOT NULL,
    description TEXT,
    date TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT now()
);
    