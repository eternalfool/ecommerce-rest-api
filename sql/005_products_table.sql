use ecommerce_db;

create table products
(
    id                 INT             NOT NULL AUTO_INCREMENT,
    name               VARCHAR(255)    NOT NULL,
    seller_id          INT             NOT NULL,
    description1       TEXT            		   ,
    description2       TEXT            		   ,
    sku_id             VARCHAR(255)            ,
    price              VARCHAR(255)            ,
    image_urls         TEXT    		           ,
    video_urls         TEXT    		           ,
    discount           VARCHAR(10)             ,
    coupons            VARCHAR(100)            ,
    available_colors   TEXT                    ,
    weight             VARCHAR(10)             ,
    is_active                 BOOLEAN NOT NULL DEFAULT true,
    PRIMARY KEY(id),
    FOREIGN KEY (seller_id) REFERENCES sellers(id)

) ENGINE = INNODB DEFAULT CHARSET = utf8;

ALTER TABLE products ADD COLUMN creation_date DATETIME;
ALTER TABLE products ADD COLUMN last_update DATETIME;
ALTER TABLE products ADD COLUMN last_updated_by VARCHAR(150);
delimiter //
CREATE TRIGGER products_insert_trigger BEFORE INSERT ON products
FOR EACH ROW BEGIN
    SET NEW.creation_date = NOW();
    SET NEW.last_updated_by = USER();
    SET NEW.last_update = NOW();
END;//
CREATE TRIGGER products_update_trigger BEFORE UPDATE ON products
FOR EACH ROW BEGIN
    SET NEW.last_updated_by = USER();
    SET NEW.last_update  =  NOW();
END;//
delimiter ;
