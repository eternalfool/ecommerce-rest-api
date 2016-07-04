use heroku_ec028af4a8b795d;

create table role_types
(
    id                 INT             NOT NULL AUTO_INCREMENT,
    role               VARCHAR(255)    NOT NULL,
    is_active                 BOOLEAN NOT NULL DEFAULT true,
    PRIMARY KEY(id)
) ENGINE = INNODB DEFAULT CHARSET = utf8;

ALTER TABLE role_types ADD COLUMN creation_date DATETIME;
ALTER TABLE role_types ADD COLUMN last_update DATETIME;
ALTER TABLE role_types ADD COLUMN last_updated_by VARCHAR(150);
delimiter //
CREATE TRIGGER role_types_insert_trigger BEFORE INSERT ON role_types
FOR EACH ROW BEGIN
    SET NEW.creation_date = NOW();
    SET NEW.last_updated_by = USER();
    SET NEW.last_update = NOW();
END;//
CREATE TRIGGER role_types_update_trigger BEFORE UPDATE ON role_types
FOR EACH ROW BEGIN
    SET NEW.last_updated_by = USER();
    SET NEW.last_update  =  NOW();
END;//
delimiter ;

