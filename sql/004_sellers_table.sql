use ecommerce_db;

create table sellers
(
    id                 INT             NOT NULL AUTO_INCREMENT,
    user_id            INT             NOT NULL,
    name               TEXT            NOT NULL,
    contact_name       VARCHAR(255)            ,
    contact_number     VARCHAR(30)             ,
    email_id           VARCHAR(255)            ,
    is_active                 BOOLEAN NOT NULL DEFAULT true,
    PRIMARY KEY(id),
    UNIQUE(user_id),
    FOREIGN KEY (user_id) REFERENCES users(id)
) ENGINE = INNODB DEFAULT CHARSET = utf8;

ALTER TABLE sellers ADD COLUMN creation_date DATETIME;
ALTER TABLE sellers ADD COLUMN last_update DATETIME;
ALTER TABLE sellers ADD COLUMN last_updated_by VARCHAR(150);
delimiter //
CREATE TRIGGER sellers_insert_trigger BEFORE INSERT ON sellers
FOR EACH ROW BEGIN
    SET NEW.creation_date = NOW();
    SET NEW.last_updated_by = USER();
    SET NEW.last_update = NOW();
END;//
CREATE TRIGGER sellers_update_trigger BEFORE UPDATE ON sellers
FOR EACH ROW BEGIN
    SET NEW.last_updated_by = USER();
    SET NEW.last_update  =  NOW();
END;//
delimiter ;
