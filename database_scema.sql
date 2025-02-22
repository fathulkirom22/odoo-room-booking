CREATE TABLE public.room_master (
	id serial4 NOT NULL,
	capacity int4 NOT NULL,
	"name" varchar NOT NULL,
	room_type varchar NOT NULL,
	"location" varchar NOT NULL,
	description text NULL,
	CONSTRAINT room_master_pkey PRIMARY KEY (id),
	CONSTRAINT room_master_unique_room_name UNIQUE (name),
);

CREATE TABLE public.room_booking (
	id serial4 NOT NULL,
	room_id int4 NOT NULL,
	"name" varchar NOT NULL,
	booking_name varchar NOT NULL,
	status varchar NULL,
	notes text NULL,
	booking_date date NOT NULL,
	status_order int4 NULL,
	CONSTRAINT room_booking_pkey PRIMARY KEY (id),
	CONSTRAINT room_booking_room_id_fkey FOREIGN KEY (room_id) REFERENCES public.room_master(id) ON DELETE RESTRICT,
);
