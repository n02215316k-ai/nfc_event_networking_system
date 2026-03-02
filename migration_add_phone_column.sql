-- Optional: Add phone column to users table
-- Run this if you want to add phone functionality

ALTER TABLE users 
ADD COLUMN phone VARCHAR(20) AFTER email;

-- Add index for phone lookups
CREATE INDEX idx_phone ON users(phone);
