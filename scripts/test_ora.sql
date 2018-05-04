alter SESSION set NLS_DATE_FORMAT = 'yyyy-mm-dd hh24:mi:ss';
alter SESSION set NLS_TIMESTAMP_FORMAT = 'hh24:mi:ss';


INSERT INTO countrys(name)  SELECT 'Russian' FROM dual UNION ALL   SELECT 'Belarus' FROM dual UNION ALL   SELECT 'USA' FROM dual UNION ALL   SELECT 'China' FROM dual;


INSERT INTO sitys(country, name) 
     SELECT (SELECT id FROM countrys WHERE NAME = 'Russian'), 'Moskov' FROM dual UNION ALL 
     SELECT (SELECT id FROM countrys WHERE NAME = 'Belarus'), 'Minsk' FROM dual UNION ALL 
     SELECT (SELECT id FROM countrys WHERE NAME = 'USA'), 'New-York' FROM dual UNION ALL 
     SELECT (SELECT id FROM countrys WHERE NAME = 'China'), 'Pekin' FROM dual;

INSERT INTO arena(sity, name) 
     SELECT (SELECT id FROM sitys WHERE name = 'Moskov'), 'Arena1' FROM dual UNION ALL 
     SELECT (SELECT id FROM sitys WHERE name= 'Minsk'), 'Arena2' FROM dual UNION ALL 
     SELECT (SELECT id FROM sitys WHERE name= 'New-York'), 'Arena3' FROM dual UNION ALL 
     SELECT (SELECT id FROM sitys WHERE name= 'Pekin'), 'Arena4' FROM dual;


INSERT INTO personal_info(first_name, last_name, birthday)
     SELECT 'Иван', 'Иванов', '1997-07-20' FROM dual UNION ALL   SELECT 'Петр', 'Петров', '1996-05-22' FROM dual UNION ALL 
     SELECT 'Олег', 'Смирнов', '1994-04-25' FROM dual UNION ALL   SELECT 'Петя', 'Петечки', '1995-06-20' FROM dual UNION ALL 
     SELECT 'Джон', 'Смит', '1996-04-26' FROM dual UNION ALL   SELECT 'Джорж', 'Кэмерон', '1996-03-24' FROM dual UNION ALL 
     SELECT 'Ли', 'Сау', '1993-08-24' FROM dual UNION ALL   SELECT 'Пунь', 'Ю', '1999-09-07' FROM dual UNION ALL   SELECT 'Сунь', 'Хау', '1997-03-05' FROM dual;


INSERT INTO team_roles(name)  SELECT 'Нападающий' FROM dual UNION ALL   SELECT 'Вратарь' FROM dual;


INSERT INTO teams(name, city)
     SELECT 'Moskov1', (SELECT id FROM sitys WHERE name = 'Moskov') FROM dual UNION ALL 
     SELECT 'Minsk1', (SELECT id FROM sitys WHERE name = 'Minsk') FROM dual UNION ALL 
     SELECT 'New-York1', (SELECT id FROM sitys WHERE name = 'New-York') FROM dual UNION ALL 
     SELECT 'Pekin1', (SELECT id FROM sitys WHERE name = 'Pekin') FROM dual;


INSERT INTO players(personal_info, team, playerNumber, role)
     SELECT 
        (SELECT id FROM personal_info WHERE last_name='Иванов'),
        (SELECT id FROM teams WHERE name = 'Moskov1'),
        1,
        (SELECT id FROM team_roles WHERE name = 'Нападающий')
     FROM dual UNION ALL 
     SELECT 
        (SELECT id FROM personal_info WHERE last_name='Петров'),
        (SELECT id FROM teams WHERE name = 'Moskov1'),
        2,
        (SELECT id FROM team_roles WHERE name = 'Вратарь')
     FROM dual UNION ALL 
     SELECT 
        (SELECT id FROM personal_info WHERE last_name='Смирнов'),
        (SELECT id FROM teams WHERE name = 'Minsk1'),
        1,
        (SELECT id FROM team_roles WHERE name = 'Нападающий')
     FROM dual UNION ALL 
     SELECT 
        (SELECT id FROM personal_info WHERE last_name='Петечки'),
        (SELECT id FROM teams WHERE name = 'Minsk1'),
        2,
        (SELECT id FROM team_roles WHERE name = 'Вратарь')
     FROM dual UNION ALL 
     SELECT 
        (SELECT id FROM personal_info WHERE last_name='Смит'),
        (SELECT id FROM teams WHERE name = 'New-York1'),
        1,
        (SELECT id FROM team_roles WHERE name = 'Нападающий')
     FROM dual UNION ALL 
     SELECT 
        (SELECT id FROM personal_info WHERE last_name='Кэмерон'),
        (SELECT id FROM teams WHERE name = 'New-York1'),
        2,
        (SELECT id FROM team_roles WHERE name = 'Вратарь')
     FROM dual UNION ALL 
     SELECT 
        (SELECT id FROM personal_info WHERE last_name='Сау'),
        (SELECT id FROM teams WHERE name = 'Pekin1'),
        1,
        (SELECT id FROM team_roles WHERE name = 'Нападающий')
     FROM dual UNION ALL 
     SELECT 
        (SELECT id FROM personal_info WHERE last_name='Ю'),
        (SELECT id FROM teams WHERE name = 'Pekin1'),
        2,
        (SELECT id FROM team_roles WHERE name = 'Вратарь')
     FROM dual UNION ALL 
     SELECT 
        (SELECT id FROM personal_info WHERE last_name='Хау'),
        (SELECT id FROM teams WHERE name = 'Pekin1'),
        3,
        (SELECT id FROM team_roles WHERE name = 'Нападающий')
     FROM dual;


INSERT INTO matchs(home_team, guest_team, matchStart, arena) VALUES
    (
        (SELECT id FROM teams WHERE name = 'Moskov1'),
        (SELECT id FROM teams WHERE name = 'Minsk1'),
        '2018-05-04 23:00:00',
        (SELECT id FROM arena WHERE name = 'Arena1')
    );




INSERT INTO team_state(matchId, playerId, playerNumber, playHomeTeam)
     SELECT 
        (SELECT MAX(id) from matchs),
        (SELECT id FROM players WHERE personal_info =
            (SELECT id FROM personal_info WHERE last_name='Иванов')),
        1,
        1
     FROM dual UNION ALL 
     SELECT 
        (SELECT MAX(id) from matchs),
        (SELECT id FROM players WHERE personal_info =
            (SELECT id FROM personal_info WHERE last_name='Петров')),
        2,
        1
     FROM dual UNION ALL 
     SELECT 
        (SELECT MAX(id) from matchs),
        (SELECT id FROM players WHERE personal_info =
            (SELECT id FROM personal_info WHERE last_name='Смирнов')),
        1,
        0
     FROM dual UNION ALL 
     SELECT 
        (SELECT MAX(id) from matchs),
        (SELECT id FROM players WHERE personal_info =
            (SELECT id FROM personal_info WHERE last_name='Петечки')),
        2,
        0
     FROM dual;



INSERT INTO matchs(home_team, guest_team, matchStart, arena) VALUES
    (
        (SELECT id FROM teams WHERE name = 'New-York1'),
        (SELECT id FROM teams WHERE name = 'Pekin1'),
        '2018-05-06 12:00:00',
        (SELECT id FROM arena WHERE name = 'Arena3')
    );




INSERT INTO team_state(matchId, playerId, playerNumber, playHomeTeam)
     SELECT 
        (SELECT MAX(id) from matchs),
        (SELECT id FROM players WHERE personal_info =
            (SELECT id FROM personal_info WHERE last_name='Смит')),
        1,
        1
     FROM dual UNION ALL 
     SELECT 
        (SELECT MAX(id) from matchs),
        (SELECT id FROM players WHERE personal_info = 
            (SELECT id FROM personal_info WHERE last_name='Кэмерон')),
        2,
        1
     FROM dual UNION ALL 
     SELECT 
        (SELECT MAX(id) from matchs),
        (SELECT id FROM players WHERE personal_info = 
            (SELECT id FROM personal_info WHERE last_name='Сау')),
        1,
        0
     FROM dual UNION ALL 
     SELECT 
        (SELECT MAX(id) from matchs),
        (SELECT id FROM players WHERE personal_info = 
            (SELECT id FROM personal_info WHERE last_name='Ю')),
        2,
        0
     FROM dual UNION ALL 
     SELECT 
        (SELECT MAX(id) from matchs),
        (SELECT id FROM players WHERE personal_info = 
            (SELECT id FROM personal_info WHERE last_name='Хау')),
        3,
        0
     FROM dual;


INSERT INTO goals(match, time, player) VALUES
    (
        (SELECT id FROM matchs WHERE guest_team = (SELECT id FROM teams WHERE name = 'Pekin1')),
        '1:03:01',
        (SELECT players.id FROM players
            INNER JOIN personal_info
            ON players.personal_info = personal_info.id
        WHERE personal_info.last_name='Сау')
    );



INSERT INTO card_types(color)  SELECT 'red' FROM dual UNION ALL   SELECT 'yellow' FROM dual;

INSERT INTO cards(type, match, time, player) VALUES
    (
        (SELECT id FROM card_types WHERE color='red'),
        (SELECT id FROM matchs WHERE guest_team = (SELECT id FROM teams WHERE name = 'Pekin1')),
        '00:30:54',
        (SELECT players.id FROM players
            INNER JOIN personal_info
            ON players.personal_info = personal_info.id
        WHERE personal_info.last_name='Ю')
    );

INSERT INTO users(login, password) VALUES ('1234', '1234');
INSERT INTO admins(userId) SELECT id FROM users WHERE login='1234';
