CREATE OR REPLACE PACKAGE api IS

    TYPE match IS RECORD(
        match_id football.matchs.id%TYPE,
        home_name football.teams.name%TYPE,
        guest_name football.teams.name%TYPE,
        home_id football.teams.id%TYPE,
        guest_id football.teams.id%TYPE,
        home_country football.countrys.name%TYPE,
        guest_country football.countrys.name%TYPE,
        home_score NUMBER,
        guest_score NUMBER,
        home_image football.emblems.image%TYPE,
        guest_image football.emblems.image%TYPE
    );
    TYPE match_table IS TABLE OF match;

    TYPE goal IS RECORD(
        home football.team_state.playHomeTeam%TYPE,
        time football.goals.time%TYPE,
        first_name football.personal_info.first_name%TYPE,
        last_name football.personal_info.last_name%TYPE,
        id football.goals.id%TYPE
    );
    TYPE goal_table IS TABLE OF goal;

    TYPE card IS RECORD(
        home football.team_state.playHomeTeam%TYPE,
        time football.cards.time%TYPE,
        color football.card_types.color%TYPE,
        first_name football.personal_info.first_name%TYPE,
        last_name football.personal_info.last_name%TYPE,
        id football.cards.id%TYPE
    );
    TYPE card_table IS TABLE OF card;

    TYPE arena IS RECORD(
        id football.arena.id%TYPE,
        name football.arena.name%TYPE,
        sity football.sitys.name%TYPE,
        country football.countrys.name%TYPE
    );
    TYPE arena_table IS TABLE OF arena;

    TYPE player IS RECORD(
        id football.players.id%TYPE,
        team_id football.teams.id%TYPE,
        first_name football.personal_info.first_name%TYPE,
        last_name football.personal_info.last_name%TYPE,
        team_name football.teams.name%TYPE
    );
    TYPE player_table IS TABLE OF player;

    TYPE team IS RECORD(
        id football.teams.id%TYPE,
        name football.teams.name%TYPE,
        sity football.sitys.name%TYPE,
        country football.countrys.name%TYPE,
        image football.emblems.image%TYPE
    );
    TYPE team_table IS TABLE OF team;

    FUNCTION get_match_list RETURN match_table PIPELINED;
    FUNCTION get_match_info(id NUMBER) RETURN match_table PIPELINED;
    FUNCTION get_goals(id NUMBER) RETURN goal_table PIPELINED;
    FUNCTION get_cards(id NUMBER) RETURN card_table PIPELINED;
    FUNCTION get_arena_list RETURN arena_table PIPELINED;
    FUNCTION get_player_list RETURN player_table PIPELINED;
    FUNCTION get_player_info(id NUMBER) RETURN player_table PIPELINED;
    FUNCTION count_player_goals(id NUMBER) RETURN NUMBER;
    FUNCTION get_player_matchs(id NUMBER) RETURN match_table PIPELINED;
    FUNCTION get_team_list RETURN team_table PIPELINED;
    FUNCTION get_team_info(id NUMBER) RETURN team_table PIPELINED;
    FUNCTION get_team_players(id NUMBER) RETURN player_table PIPELINED;

    PROCEDURE add_arena(
        name football.arena.name%TYPE,
        city football.sitys.name%TYPE,
        country football.countrys.name%TYPE
    );

    FUNCTION get_match_players(id NUMBER) RETURN player_table PIPELINED;

    PROCEDURE add_foul(
        type football.cards.type%TYPE,
        match football.cards.match%TYPE,
        time football.cards.time%TYPE,
        player football.cards.player%TYPE
    );

    PROCEDURE add_goal(
        match football.cards.match%TYPE,
        time football.cards.time%TYPE,
        player football.cards.player%TYPE
    );

    PROCEDURE add_player(
        first_name football.personal_info.first_name%TYPE,
        last_name football.personal_info.last_name%TYPE,
        birthday  football.personal_info.birthday%TYPE,
        team football.players.team%TYPE,
        role football.players.role%TYPE,
        playerNumber football.players.playerNumber%TYPE
    );
END api;
/
SHOW ERRORS PACKAGE api;
/

CREATE OR REPLACE PACKAGE BODY api IS

    FUNCTION get_match_list RETURN match_table PIPELINED
    IS
    BEGIN
        FOR curr IN (
            SELECT
                mt.id as match_id,
                home.name as home_name,
                guest.name as guest_name,
                home.id as home_id,
                guest.id as guest_id,
                hc.name as home_country,
                gc.name as guest_country,
                (
                    SELECT COUNT(*) FROM goals gl
                    INNER JOIN team_state ts ON gl.player = ts.playerId
                    WHERE gl.match = mt.id
                    AND ts.playHomeTeam = 1
                ) as home_score,
                (
                    SELECT COUNT(*) FROM goals gl
                    INNER JOIN team_state ts ON gl.player = ts.playerId
                    WHERE gl.match = mt.id
                    AND ts.playHomeTeam = 0
                ) as guest_score,
                em1.image as home_image,
                em2.image as guest_image
            FROM matchs mt
            INNER JOIN teams home ON home.id = mt.home_team
            INNER JOIN teams guest ON guest.id = mt.guest_team
            INNER JOIN sitys hs ON hs.id = home.city
            INNER JOIN sitys gs ON gs.id = guest.city
            INNER JOIN countrys hc ON hs.country = hc.id
            INNER JOIN countrys gc ON gs.country = gc.id
            LEFT JOIN emblems em1 ON em1.id = home.emblem
            LEFT JOIN emblems em2 ON em2.id = guest.emblem
        )
        LOOP
            PIPE ROW (curr);
        END LOOP;
    END;

    FUNCTION get_match_info(id NUMBER) RETURN match_table PIPELINED IS
    BEGIN
        FOR curr IN (
            SELECT * FROM TABLE(SELECT get_match_list() FROM DUAL)
            WHERE match_id = get_match_info.id
        )
        LOOP
            PIPE ROW (curr);
        END LOOP;
    END;

    FUNCTION get_goals(id NUMBER) RETURN goal_table PIPELINED IS
    BEGIN
        FOR curr IN (
            SELECT
                ts.playHomeTeam,
                gl.time,
                pi.first_name,
                pi.last_name,
                gl.id
            FROM goals gl
            INNER JOIN matchs mt ON mt.id = gl.match
            INNER JOIN players pl ON pl.id = gl.player
            INNER JOIN personal_info pi ON pi.id = pl.personal_info
            INNER JOIN team_state ts
                ON ts.matchId = mt.id AND ts.playerId = pl.id
            WHERE mt.id = get_goals.id
            ORDER BY gl.time
        )
        LOOP
            PIPE ROW (curr);
        END LOOP;
    END;


    FUNCTION get_cards(id NUMBER) RETURN card_table PIPELINED IS
    BEGIN
        FOR curr IN (
            SELECT
                ts.playHomeTeam as home,
                cr.time as time,
                ct.color as color,
                pi.first_name as first_name,
                pi.last_name as last_name,
                cr.id as id
            FROM cards cr
            INNER JOIN matchs mt ON mt.id = cr.match
            INNER JOIN players pl ON pl.id = cr.player
            INNER JOIN personal_info pi ON pi.id = pl.personal_info
            INNER JOIN card_types ct ON ct.id = cr.type
            INNER JOIN team_state ts
                ON ts.matchId = mt.id AND ts.playerId = pl.id
            WHERE mt.id = get_cards.id
            ORDER BY cr.time
        )
        LOOP
            PIPE ROW (curr);
        END LOOP;
    END;


    FUNCTION get_arena_list RETURN arena_table PIPELINED IS
    BEGIN
        FOR curr IN (
            SELECT
                ar.id as id,
                ar.name as name,
                st.name as sity,
                ct.name as country
            FROM arena ar
            INNER JOIN sitys st ON st.id = ar.sity
            INNER JOIN countrys ct ON ct.id = st.country
        )
        LOOP
            PIPE ROW (curr);
        END LOOP;
    END;


    FUNCTION get_player_list RETURN player_table PIPELINED IS
    BEGIN
        FOR curr IN (
            SELECT
                pl.id as id,
                tm.id as team_id,
                pi.first_name as first_name,
                pi.last_name as last_name,
                tm.name as team_name
                FROM players pl
                LEFT JOIN teams tm ON pl.team = tm.id
                INNER JOIN personal_info pi on pi.id = pl.personal_info
        )
        LOOP
            PIPE ROW (curr);
        END LOOP;
    END;

    FUNCTION get_player_info(id NUMBER) RETURN player_table PIPELINED IS
    BEGIN
        FOR curr IN (
            SELECT
                pl.id as id,
                tm.id as team_id,
                pi.first_name as first_name,
                pi.last_name as last_name,
                tm.name as team_name
                FROM players pl
                LEFT JOIN teams tm ON pl.team = tm.id
                INNER JOIN personal_info pi on pi.id = pl.personal_info
                WHERE pl.id = get_player_info.id
        )
        LOOP
            PIPE ROW (curr);
        END LOOP;
    END;

    FUNCTION count_player_goals(id NUMBER) RETURN NUMBER IS
        res NUMBER;
    BEGIN
        SELECT COUNT(*) INTO res
            FROM goals gl
            INNER JOIN players pl ON pl.id = gl.player
            WHERE pl.id = count_player_goals.id;
        RETURN res;
    END;

    FUNCTION get_player_matchs(id NUMBER) RETURN match_table PIPELINED IS
    BEGIN
        FOR curr IN (
            SELECT
                match_id,
                home_name,
                guest_name,
                home_id,
                guest_id,
                home_country,
                guest_country,
                home_score,
                guest_score,
                home_image,
                guest_image
            FROM TABLE(SELECT get_match_list FROM DUAL)
            INNER JOIN team_state ts ON ts.matchId = match_id
            INNER JOIN players pl ON ts.playerId = pl.id
            WHERE pl.id = get_player_matchs.id
        )
        LOOP
            PIPE ROW (curr);
        END LOOP;
    END;

    FUNCTION get_team_list RETURN team_table PIPELINED IS
    BEGIN
        FOR curr IN (
            SELECT
                tm.id as id,
                tm.name as name,
                st.name as sity,
                ct.name as county,
                em.image as image
            FROM teams tm
            INNER JOIN sitys st ON tm.city = st.id
            INNER JOIN countrys ct ON ct.id = st.country
            LEFT JOIN emblems em ON em.id = tm.emblem
        )
        LOOP
            PIPE ROW (curr);
        END LOOP;
    END;

    FUNCTION get_team_info(id NUMBER) RETURN team_table PIPELINED IS
    BEGIN
        FOR curr IN (
            SELECT *
            FROM TABLE(get_team_list)
            WHERE id = get_team_info.id
        )
        LOOP
            PIPE ROW (curr);
        END LOOP;
    END;

    FUNCTION get_team_players(id NUMBER) RETURN player_table PIPELINED IS
    BEGIN
        FOR curr IN (
            SELECT *
            FROM TABLE(get_player_list)
            WHERE team_id = get_team_players.id
        )
        LOOP
            PIPE ROW (curr);
        END LOOP;
    END;


    PROCEDURE add_arena(
        name football.arena.name%TYPE,
        city football.sitys.name%TYPE,
        country football.countrys.name%TYPE
    ) IS
    country_id NUMBER;
    city_id NUMBER;
    country_exist NUMBER;
    city_exist NUMBER;
    BEGIN

        SELECT COUNT(*) INTO country_exist
            FROM countrys WHERE name = add_arena.country;

        IF country_exist = 0 THEN
            INSERT INTO countrys(name) VALUES (add_arena.country);
        END IF;

        SELECT id INTO country_id FROM countrys
            WHERE name = add_arena.country;

        SELECT COUNT(*) INTO city_exist
            FROM sitys WHERE name = add_arena.city;

        IF city_exist = 0 THEN
            INSERT INTO sitys(name, country)
                VALUES (add_arena.city, add_arena.country_id);
        END IF;

        SELECT id INTO city_id FROM sitys WHERE name = add_arena.city;

        INSERT INTO arena(name, sity) VALUES (name, city_id);

    END;


    FUNCTION get_match_players(id NUMBER) RETURN player_table PIPELINED IS
    BEGIN
        FOR curr IN (
            SELECT
                pl.id,
                pl.team_id,
                pl.first_name,
                pl.last_name,
                pl.team_name
            FROM TABLE(get_player_list) pl
            INNER JOIN team_state ts
                ON ts.playerId = pl.id
            WHERE ts.matchId = get_match_players.id
        )
        LOOP
            PIPE ROW (curr);
        END LOOP;
    END;

    PROCEDURE add_foul(
        type football.cards.type%TYPE,
        match football.cards.match%TYPE,
        time football.cards.time%TYPE,
        player football.cards.player%TYPE
    )
    IS
    BEGIN
        INSERT INTO cards(type, match, time, player)
            VALUES (
                add_foul.type, add_foul.match,
                add_foul.time, add_foul.player
            );
    END;

    PROCEDURE add_goal(
        match football.cards.match%TYPE,
        time football.cards.time%TYPE,
        player football.cards.player%TYPE
    )
    IS
    BEGIN
        INSERT INTO goals(match, time, player)
            VALUES (add_goal.match, add_goal.time, add_goal.player);
    END;

    PROCEDURE add_player(
        first_name football.personal_info.first_name%TYPE,
        last_name football.personal_info.last_name%TYPE,
        birthday  football.personal_info.birthday%TYPE,
        team football.players.team%TYPE,
        role football.players.role%TYPE,
        playerNumber football.players.playerNumber%TYPE
    )
    IS
    BEGIN
        INSERT INTO personal_info(first_name, last_name, birthday)
            VALUES (
                add_player.first_name,
                add_player.last_name,
                add_player.birthday
            );
        INSERT INTO players(personal_info, team, playerNumber, role)
            VALUES (
                (SELECT MAX(id) FROM personal_info),
                add_player.team,
                add_player.playerNumber,
                add_player.role
            );
    END;

END api;
/
SHOW ERRORS PACKAGE BODY api;
/
