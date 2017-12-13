INSERT INTO countrys(name) VALUES ('Russian'), ('Belarus'), ('USA'), ('China');


INSERT INTO sitys(country, name) VALUES 
    ((SELECT id FROM countrys WHERE NAME = 'Russian'), 'Moskov'),
    ((SELECT id FROM countrys WHERE NAME = 'Belarus'), 'Minsk'),
    ((SELECT id FROM countrys WHERE NAME = 'USA'), 'New-York'),
    ((SELECT id FROM countrys WHERE NAME = 'China'), 'Pekin');

INSERT INTO arena(sity, name) VALUES 
    ((SELECT id FROM sitys WHERE name = 'Moskov'), 'Arena1'),
    ((SELECT id FROM sitys WHERE name= 'Minsk'), 'Arena2'),
    ((SELECT id FROM sitys WHERE name= 'New-York'), 'Arena3'),
    ((SELECT id FROM sitys WHERE name= 'Pekin'), 'Arena4');


INSERT INTO personal_info(first_name, last_name, birthday) VALUES
    ('Иван', 'Иванов', '1997-07-20'), ('Петр', 'Петров', '1996-05-22'),
    ('Олег', 'Смирнов', '1994-04-25'), ('Петя', 'Петечки', '1995-06-20'),
    ('Джон', 'Смит', '1996-04-26'), ('Джорж', 'Кэмерон', '1996-03-24'),
    ('Ли', 'Сау', '1993-08-24'), ('Пунь', 'Ю', '1999-09-07'), ('Сунь', 'Хау', '1997-03-05');


INSERT INTO team_roles(name) VALUES ('Нападающий'), ('Вратарь');


INSERT INTO teams(name, city) VALUES 
    ('Moskov1', (SELECT id FROM sitys WHERE name = 'Moskov')),
    ('Minsk1', (SELECT id FROM sitys WHERE name = 'Minsk')),
    ('New-York1', (SELECT id FROM sitys WHERE name = 'New-York')),
    ('Pekin1', (SELECT id FROM sitys WHERE name = 'Pekin'));


INSERT INTO players(personal_info, team, `number`, role) VALUES
    (
        (SELECT id FROM personal_info WHERE last_name='Иванов'),
        (SELECT id FROM teams WHERE name = 'Moskov1'),
        1,
        (SELECT id FROM team_roles WHERE name = 'Нападающий')
    ),
    (
        (SELECT id FROM personal_info WHERE last_name='Петров'),
        (SELECT id FROM teams WHERE name = 'Moskov1'),
        2,
        (SELECT id FROM team_roles WHERE name = 'Вратарь')
    ),


    (
        (SELECT id FROM personal_info WHERE last_name='Смирнов'),
        (SELECT id FROM teams WHERE name = 'Minsk1'),
        1,
        (SELECT id FROM team_roles WHERE name = 'Нападающий')
    ),
    (
        (SELECT id FROM personal_info WHERE last_name='Петечки'),
        (SELECT id FROM teams WHERE name = 'Minsk1'),
        2,
        (SELECT id FROM team_roles WHERE name = 'Вратарь')
    ),



    (
        (SELECT id FROM personal_info WHERE last_name='Смит'),
        (SELECT id FROM teams WHERE name = 'New-York1'),
        1,
        (SELECT id FROM team_roles WHERE name = 'Нападающий')
    ),
    (
        (SELECT id FROM personal_info WHERE last_name='Кэмерон'),
        (SELECT id FROM teams WHERE name = 'New-York1'),
        2,
        (SELECT id FROM team_roles WHERE name = 'Вратарь')
    ),


    (
        (SELECT id FROM personal_info WHERE last_name='Сау'),
        (SELECT id FROM teams WHERE name = 'Pekin1'),
        1,
        (SELECT id FROM team_roles WHERE name = 'Нападающий')
    ),
    (
        (SELECT id FROM personal_info WHERE last_name='Ю'),
        (SELECT id FROM teams WHERE name = 'Pekin1'),
        2,
        (SELECT id FROM team_roles WHERE name = 'Вратарь')
    ),
    (
        (SELECT id FROM personal_info WHERE last_name='Хау'),
        (SELECT id FROM teams WHERE name = 'Pekin1'),
        3,
        (SELECT id FROM team_roles WHERE name = 'Нападающий')
    );


INSERT INTO matchs(home_team, guest_team, start, arena) VALUES
    (
        (SELECT id FROM teams WHERE name = 'Moskov1'),
        (SELECT id FROM teams WHERE name = 'Minsk1'),
        "2017-12-25 23:00:00",
        (SELECT id FROM arena WHERE name = 'Arena1')
    );




INSERT INTO team_state(matchId, playerId, `number`, playHomeTeam) VALUES
    (
        (SELECT MAX(id) from matchs),
        (SELECT `id` FROM players WHERE `id` =
            (SELECT id FROM personal_info WHERE last_name='Иванов')),
        1,
        TRUE
    ),
    (
        (SELECT MAX(id) from matchs),
        (SELECT `id` FROM players WHERE `id` = 
            (SELECT id FROM personal_info WHERE last_name='Петров')),
        2,
        TRUE
    ),
    (
        (SELECT MAX(id) from matchs),
        (SELECT `id` FROM players WHERE `id` = 
            (SELECT id FROM personal_info WHERE last_name='Смирнов')),
        1,
        FALSE
    ),
    (
        (SELECT MAX(id) from matchs),
        (SELECT `id` FROM players WHERE `id` = 
            (SELECT id FROM personal_info WHERE last_name='Петечки')),
        2,
        FALSE
    );



INSERT INTO matchs(home_team, guest_team, start, arena) VALUES
    (
        (SELECT id FROM teams WHERE name = 'New-York1'),
        (SELECT id FROM teams WHERE name = 'Pekin1'),
        "2017-12-9 12:00:00",
        (SELECT id FROM arena WHERE name = 'Arena3')
    );




INSERT INTO team_state(matchId, playerId, `number`, playHomeTeam) VALUES
    (
        (SELECT MAX(id) from matchs),
        (SELECT `id` FROM players WHERE `id` =
            (SELECT id FROM personal_info WHERE last_name='Смит')),
        1,
        TRUE
    ),
    (
        (SELECT MAX(id) from matchs),
        (SELECT `id` FROM players WHERE `id` = 
            (SELECT id FROM personal_info WHERE last_name='Кэмерон')),
        2,
        TRUE
    ),
    (
        (SELECT MAX(id) from matchs),
        (SELECT `id` FROM players WHERE `id` = 
            (SELECT id FROM personal_info WHERE last_name='Сау')),
        1,
        FALSE
    ),
    (
        (SELECT MAX(id) from matchs),
        (SELECT `id` FROM players WHERE `id` = 
            (SELECT id FROM personal_info WHERE last_name='Ю')),
        2,
        FALSE
    ),
    (
        (SELECT MAX(id) from matchs),
        (SELECT `id` FROM players WHERE `id` = 
            (SELECT id FROM personal_info WHERE last_name='Хау')),
        3,
        FALSE
    );



INSERT INTO match_results(length, home_team_score, guest_team_score) VALUES
    ("2:10:23", 4, 0);

UPDATE matchs SET
    result = (SELECT MAX(id) FROM match_results)
WHERE
    guest_team = (SELECT id FROM teams WHERE name = 'Pekin1');


INSERT INTO `goals`(`match`, `time`, `player`) VALUES
    (
        (SELECT id FROM matchs WHERE guest_team = (SELECT id FROM teams WHERE name = 'Pekin1')),
        "1:03:01",
        (SELECT pl.id FROM players as pl
            INNER JOIN personal_info as pi
            ON pl.personal_info = pi.id
        WHERE pi.last_name='Сау')
    );



INSERT INTO card_types(color) VALUES ("red"), ("yellow");

INSERT INTO `cards`(`type`, `match`, `time`, `player`) VALUES
    (
        (SELECT id FROM card_types WHERE color="red"),
        (SELECT id FROM matchs WHERE guest_team = (SELECT id FROM teams WHERE name = 'Pekin1')),
        "00:30:54",
        (SELECT pl.id FROM players as pl
            INNER JOIN personal_info as pi
            ON pl.personal_info = pi.id
        WHERE pi.last_name='Ю')
    );



INSERT INTO `replaces`(`match`, `replaced_player`, `player`, `time`) VALUES
    (
        (SELECT id FROM matchs WHERE guest_team = (SELECT id FROM teams WHERE name = 'Pekin1')),
        (SELECT pl.id FROM players as pl
            INNER JOIN personal_info as pi
            ON pl.personal_info = pi.id
        WHERE pi.last_name='Ю'),
        (SELECT pl.id FROM players as pl
            INNER JOIN personal_info as pi
            ON pl.personal_info = pi.id
        WHERE pi.last_name='Хау'),
        "00:40:00"
    );

INSERT INTO users(`login`, `password`) VALUES ('1234', '1234');
INSERT INTO admins(`user`) VALUES (1);
