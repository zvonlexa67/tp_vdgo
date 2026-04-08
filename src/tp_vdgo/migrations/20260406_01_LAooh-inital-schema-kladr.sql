-- Inital schema KLADR
-- depends: 

CREATE TABLE IF NOT EXISTS altnames (
    oldcode CHAR(19) NOT NULL,
    newcode CHAR(19) NOT NULL,
    level CHAR(1) NOT NULL
);

GRANT SELECT ON TABLE altnames TO admin_vdgo;
GRANT SELECT ON TABLE altnames TO user_vdgo;
GRANT SELECT ON TABLE altnames TO guest_vdgo;
GRANT SELECT ON TABLE altnames TO other_vdgo;

--

CREATE TABLE IF NOT EXISTS doma (
    name CHAR(40) NOT NULL,
    korp CHAR(10),
    socr CHAR(10) NOT NULL,
    code CHAR(19) NOT NULL UNIQUE,
    index CHAR(6),
    gninmb CHAR(4) NOT NULL,
    uno CHAR(4),
    ocatd CHAR(11) NOT NULL
);

CREATE INDEX idx_doma_code ON doma(code);

GRANT SELECT ON TABLE doma TO admin_vdgo;
GRANT SELECT ON TABLE doma TO user_vdgo;
GRANT SELECT ON TABLE doma TO guest_vdgo;
GRANT SELECT ON TABLE doma TO other_vdgo;

--

CREATE TABLE IF NOT EXISTS kladr (
    name CHAR(40) NOT NULL,
    socr CHAR(10) NOT NULL,
    code CHAR(13) NOT NULL UNIQUE,
    index CHAR(6),
    gninmb CHAR(4) NOT NULL,
    uno CHAR(4),
    ocatd CHAR(11) NOT NULL,
    status CHAR(1)
);

CREATE INDEX idx_kladr_code ON kladr(code);

GRANT SELECT ON TABLE kladr TO admin_vdgo;
GRANT SELECT ON TABLE kladr TO user_vdgo;
GRANT SELECT ON TABLE kladr TO guest_vdgo;
GRANT SELECT ON TABLE kladr TO other_vdgo;

--

CREATE TABLE IF NOT EXISTS street (
    name CHAR(40) NOT NULL,
    socr CHAR(10) NOT NULL,
    code CHAR(13) NOT NULL UNIQUE,
    index CHAR(6),
    gninmb CHAR(4) NOT NULL,
    uno CHAR(4),
    ocatd CHAR(11) NOT NULL
);

CREATE INDEX idx_street_code ON street(code);

GRANT SELECT ON TABLE street TO admin_vdgo;
GRANT SELECT ON TABLE street TO user_vdgo;
GRANT SELECT ON TABLE street TO guest_vdgo;
GRANT SELECT ON TABLE street TO other_vdgo;

--

CREATE TABLE IF NOT EXISTS socrbase (
    level CHAR(5) NOT NULL,
    scname CHAR(10) NOT NULL,
    socrname CHAR(29) NOT NULL,
    kod_t_st CHAR(3) NOT NULL UNIQUE
);

CREATE INDEX idx_socrbase_kod_t_st ON socrbase(kod_t_st);

GRANT SELECT ON TABLE socrbase TO admin_vdgo;
GRANT SELECT ON TABLE socrbase TO user_vdgo;
GRANT SELECT ON TABLE socrbase TO guest_vdgo;
GRANT SELECT ON TABLE socrbase TO other_vdgo;

--

CREATE TABLE IF NOT EXISTS flat (
    code CHAR(23) NOT NULL UNIQUE,
    np CHAR(4) NOT NULL,
    gninmb CHAR(4) NOT NULL,
    name CHAR(40) NOT NULL,
    index CHAR(6),
    uno CHAR(4) NOT NULL
);

CREATE INDEX idx_flat_code ON flat(code);

GRANT SELECT ON TABLE flat TO admin_vdgo;
GRANT SELECT ON TABLE flat TO user_vdgo;
GRANT SELECT ON TABLE flat TO guest_vdgo;
GRANT SELECT ON TABLE flat TO other_vdgo;

--

CREATE TABLE IF NOT EXISTS namemap (
    code CHAR(17) NOT NULL UNIQUE,
    name CHAR(250) NOT NULL,
    shname CHAR(40) NOT NULL,
    scname CHAR(10) NOT NULL
);

CREATE INDEX idx_namemap_code ON namemap(code);

GRANT SELECT ON TABLE namemap TO admin_vdgo;
GRANT SELECT ON TABLE namemap TO user_vdgo;
GRANT SELECT ON TABLE namemap TO guest_vdgo;
GRANT SELECT ON TABLE namemap TO other_vdgo;

--
