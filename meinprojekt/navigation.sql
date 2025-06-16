
CREATE TABLE djange.navigation (
	id int4 NOT NULL,
	parent int4 NOT NULL,
	nav_name varchar(255) NOT NULL,
	url varchar(255) DEFAULT '#'::character varying NOT NULL,
	start_page int2 DEFAULT 1 NOT NULL,
	CONSTRAINT navigation_pk PRIMARY KEY (id)
);

INSERT INTO djange.navigation (id,parent,nav_name,url) VALUES
	 (1,0,'Start-Seite','/',0),
	 (2,0,'Meine Test','#',1),
	 (3,2,'Eingabe','/eingabe',1),
	 (4,2,'Planung','/planung',1),
	 (5,0,'Sales','#',1),
	 (6,5,'Formular','#',1),
	 (7,6,'Objekte','/sales/objekte',1),
	 (8,6,'Prognose','/sales/prognose',1),
	 (9,5,'Report','#',1),
	 (10,9,'Report 1','#',1);
INSERT INTO djange.navigation (id,parent,nav_name,url) VALUES
	 (11,9,'Report 2','#',1);
