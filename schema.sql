DROP TABLE IF EXISTS deviceSummary;
DROP TABLE IF EXISTS dhcpService;
DROP TABLE IF EXISTS device;
DROP TABLE IF EXISTS dnsServer;
DROP TABLE IF EXISTS wifi;
CREATE TABLE deviceSummary (
    ds_id INTEGER PRIMARY KEY AUTOINCREMENT,
    interfaceName TEXT NOT NULL,
    ipv4Address TEXT NOT NULL,
    macAddress TEXT NOT NULL
);

CREATE TABLE dhcpService (
    dh_id INTEGER PRIMARY KEY AUTOINCREMENT,
    adressRange INTEGER NOT NULL,
    reservations INTEGER NOT NULL
);

CREATE TABLE device (
    de_id INTEGER PRIMARY KEY AUTOINCREMENT,
    whiteList TEXT NOT NULL,
    blackList TEXT NOT NULL
);

CREATE TABLE dnsServer (
    servers TEXT NOT NULL
);

CREATE TABLE wifi (
    essidName TEXT NOT NULL,
    wifiPasword TEXT NOT NULL,
);
