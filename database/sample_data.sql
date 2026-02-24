USE nfc_event_management;

-- Sample Events
INSERT INTO events (title, description, location, start_date, end_date, creator_id, max_attendees, category, status) VALUES
('Tech Conference 2026', 'Annual technology conference featuring the latest innovations', 'Convention Center Hall A', '2026-03-15 09:00:00', '2026-03-15 18:00:00', 1, 500, 'Technology', 'published'),
('Business Networking Mixer', 'Connect with industry professionals', 'Downtown Business Hub', '2026-03-20 18:00:00', '2026-03-20 21:00:00', 1, 100, 'Business', 'published');
