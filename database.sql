-- Create ENUM types for gender, status, and applicantType
CREATE TYPE gender_enum AS ENUM ('Male', 'Female', 'Other');
CREATE TYPE status_enum AS ENUM ('Single', 'Married', 'Student', 'Employed', 'Other');
CREATE TYPE applicant_type_enum AS ENUM ('Partner', 'Child', 'Single', 'Married', 'Divorced', 'Widowed', 'Other');

-- Users Table for Signup/Login
CREATE TABLE Users (
    id SERIAL PRIMARY KEY,
    firstName VARCHAR(50) NOT NULL,
    middleName VARCHAR(50),
    lastName VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL, -- Store hashed passwords
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- InsuranceForms Table for Form Data
CREATE TABLE InsuranceForms (
    id SERIAL PRIMARY KEY,
    firstName VARCHAR(50) NOT NULL,
    middleName VARCHAR(50),
    lastName VARCHAR(50) NOT NULL,
    gender gender_enum NOT NULL,
    age INT CHECK (age >= 0), -- Ensure age is non-negative
    status status_enum NOT NULL,
    dob DATE NOT NULL,
    streetAddress VARCHAR(255) NOT NULL,
    city VARCHAR(100) NOT NULL,
    stateProvince VARCHAR(100) NOT NULL,
    zipCode VARCHAR(20) NOT NULL,
    email VARCHAR(100) NOT NULL,
    phoneNumber VARCHAR(20) NOT NULL,
    applicantType applicant_type_enum, -- Extended ENUM options
    applicantFullName VARCHAR(150),
    applicantGender gender_enum,
    applicantDob DATE,
    digitalSignature BYTEA, -- Store binary data (PDF or signature)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);