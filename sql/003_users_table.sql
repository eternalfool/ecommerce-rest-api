use heroku_ec028af4a8b795d;

create table users
(
    id                 INT             NOT NULL AUTO_INCREMENT,
    role_type_id       INT             NOT NULL,
    username           VARCHAR(255)    NOT NULL,
    password_hash      TEXT            NOT NULL,
    is_active                 BOOLEAN NOT NULL DEFAULT true,
    PRIMARY KEY(id),
    UNIQUE(username),
    FOREIGN KEY (role_type_id) REFERENCES role_types(id)

) ENGINE = INNODB DEFAULT CHARSET = utf8;

ALTER TABLE users ADD COLUMN creation_date DATETIME;
ALTER TABLE users ADD COLUMN last_update DATETIME;
ALTER TABLE users ADD COLUMN last_updated_by VARCHAR(150);
/*delimiter //
CREATE TRIGGER users_insert_trigger BEFORE INSERT ON users
FOR EACH ROW BEGIN
    SET NEW.creation_date = NOW();
    SET NEW.last_updated_by = USER();
    SET NEW.last_update = NOW();
END;//
CREATE TRIGGER users_update_trigger BEFORE UPDATE ON users
FOR EACH ROW BEGIN
    SET NEW.last_updated_by = USER();
    SET NEW.last_update  =  NOW();
END;//
delimiter ;
