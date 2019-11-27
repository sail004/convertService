CREATE TABLE "Good" (
	"Id"	INTEGER NOT NULL,
	"Name"	TEXT NOT NULL,
	"Description"	TEXT,
	"IsWeight"	INTEGER NOT NULL DEFAULT 0,
	PRIMARY KEY("Id")
);
CREATE TABLE "Receipt_head" (
	"Id"	INTEGER NOT NULL,
	"DateTime"	TEXT NOT NULL,
	"Sum"	NUMERIC,
	"DiscounCard"	TEXT,
	"Number"	TEXT,
	PRIMARY KEY("Id")
);
CREATE TABLE "Receipt_pos" (
	"IdCheck"	INTEGER NOT NULL,
	"NumPos"	INTEGER NOT NULL,
	"IdGood"	INTEGER NOT NULL,
	"Price"	NUMERIC NOT NULL,
	"Quantity"	NUMERIC NOT NULL,
	PRIMARY KEY("IdCheck","NumPos")
);
