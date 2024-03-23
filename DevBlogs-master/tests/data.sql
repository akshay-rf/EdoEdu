INSERT INTO user (username, password) VALUES
('test', 'pbkdf2:sha256:150000$Gnq6iMfB$f9847f7e4e977a3b1eb7b35aa6e0c46f7316a76477fddfa1028efec7ebc9039e'),
('other', 'pbkdf2:sha256:150000$Gnq6iMfB$f9847f7e4e977a3b1eb7b35aa6e0c46f7316a76477fddfa1028efec7ebc9039e');

INSERT INTO post (title, body, author_id, created)
VALUES
('test title', 'test body', 1, '2018-01-01 00:00:00');
