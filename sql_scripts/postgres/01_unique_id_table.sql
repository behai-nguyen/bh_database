-- Table: unique_id

DROP TABLE IF EXISTS unique_id;

CREATE TABLE IF NOT EXISTS unique_id
(
    tablename character varying(64) COLLATE pg_catalog."default" NOT NULL,
    columnname character varying(64) COLLATE pg_catalog."default" NOT NULL,
    id bigint NOT NULL,
    CONSTRAINT idx_18610_primary PRIMARY KEY (tablename, columnname)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS unique_id
    OWNER to postgres;