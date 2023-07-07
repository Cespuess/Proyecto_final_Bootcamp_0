CREATE TABLE "movements" (
	"id"	INTEGER,
	"date"	TEXT NOT NULL,
	"hour"	TEXT NOT NULL,
	"from"	TEXT NOT NULL,
	"amount"	REAL NOT NULL,
	"to"	TEXT NOT NULL,
	"quantity"	REAL NOT NULL,
	"pu"	REAL NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
)