from yoyo import step

steps = [
    step(
        "CREATE TABLE Users (id INTEGER PRIMARY KEY AUTOINCREMENT, username VARCHAR(255) NOT NULL, password VARCHAR(255), uuid VARCHAR(255) NOT NULL, registered_on DATETIME NOT NULL)",
        "DROP TABLE Users",
    ),
    step(
        "CREATE TABLE UsernameHistory (id INTEGER PRIMARY KEY AUTOINCREMENT, username VARCHAR(255) NOT NULL, changed_on DATETIME NOT NULL, uuid VARCHAR(255) NOT NULL, CONSTRAINT fk_uui FOREIGN KEY (uuid) REFERENCES Users(uuid))",
        "DROP TABLE UsernameHistory",
    ),
]
