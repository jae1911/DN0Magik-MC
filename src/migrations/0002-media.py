from yoyo import step

steps = [
    step(
        "CREATE TABLE Media (id INTEGER PRIMARY KEY AUTOINCREMENT, uuid VARCHAR(255) NOT NULL, hash VARCHAR(255) NOT NULL, type VARCHAR(255) NOT NULL, CONSTRAINT fk_uui_media FOREIGN KEY (uuid) REFERENCES Users(uuid))",
        "DROP TABLE Media",
    )
]
