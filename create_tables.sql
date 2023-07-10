-- Table: public.client

-- DROP TABLE IF EXISTS public.client;

CREATE TABLE IF NOT EXISTS public.client
(
    id integer NOT NULL DEFAULT nextval('client_id_seq'::regclass),
    external_id character varying COLLATE pg_catalog."default",
    name character varying COLLATE pg_catalog."default",
    is_active boolean,
    create_date timestamp without time zone,
    activate_date timestamp without time zone,
    deactivate_date timestamp without time zone,
    cashbox_connection_key character varying COLLATE pg_catalog."default",
    CONSTRAINT client_pkey PRIMARY KEY (id),
    CONSTRAINT client_cashbox_connection_key_key UNIQUE (cashbox_connection_key),
    CONSTRAINT client_external_id_key UNIQUE (external_id)
);

-- Table: public.task

-- DROP TABLE IF EXISTS public.task;

CREATE TABLE IF NOT EXISTS public.task
(
    id bigint NOT NULL DEFAULT nextval('task_id_seq'::regclass),
    "number" character varying COLLATE pg_catalog."default",
    client_id integer,
    data text COLLATE pg_catalog."default",
    create_date timestamp without time zone,
    status character varying COLLATE pg_catalog."default",
    status_message text COLLATE pg_catalog."default",
    CONSTRAINT task_pkey PRIMARY KEY (id),
    CONSTRAINT task_number_key UNIQUE ("number")
)
