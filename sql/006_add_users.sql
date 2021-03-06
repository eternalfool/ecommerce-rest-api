/* Adds two users with username:password as shashwat:shashwat and admin:admin, the second used admin:admin has admin privileges */
use heroku_ec028af4a8b795d;
INSERT INTO role_types(id, role) VALUES(1, "SELLER");
INSERT INTO role_types(id, role) VALUES(2, "ADMIN");
INSERT INTO users (role_type_id, username, password_hash) values((SELECT id from role_types where role="SELLER"), "shashwat", "$6$rounds=635119$1l2IvJl0lMKQeLJg$wdx0xgguNUZSB2Y31JyqZ2V4UvXbebndQdIz58fdTfr/aPHJl7ec5XDfwnauW1Gl3sUaPyCaUxdV/HlJqovpW/");
INSERT INTO sellers(user_id, name) values((select id from users where username="shashwat"), "shashwat");
INSERT INTO users (role_type_id, username, password_hash) values((SELECT id from role_types where role="ADMIN"), "admin", "$6$rounds=629854$J74EOWsR8mnkb51/$1SZ.DvxbVIupO0dEXcHBxLzB5Nz0BG0OBjU5oU4DCWNmbt0b57Ezs9qEivSY7mmO1gDcD/83irQE/Nc75lgcD0");
INSERT INTO sellers(user_id, name) values((select id from users where username="admin"), "admin");
