CREATE OR REPLACE PACKAGE api IS

    TYPE match_short IS RECORD(
        home_name football.teams.name%TYPE,
        guest_name football.teams.name%TYPE,
        home_score NUMBER,
        guest_score NUMBER,
        match_id football.matchs.id%TYPE,
        home_id football.teams.id%TYPE,
        guest_id football.teams.id%TYPE
    );
    TYPE matchs IS TABLE OF match_short;

    TYPE match_info IS RECORD(
        home_name football.teams.name%TYPE,
        guest_name football.teams.name%TYPE,
        home_country football.countrys.name%TYPE,
        guest_country football.countrys.name%TYPE,
        home_score NUMBER,
        guest_score NUMBER,
        home_image emblems.image%TYPE,
        guest_image emblems.image%TYPE
    );
    TYPE match_info_table IS TABLE OF match_info;

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

    FUNCTION get_match_list RETURN matchs PIPELINED;
    FUNCTION get_match_info(id NUMBER) RETURN match_info_table PIPELINED;
    FUNCTION get_goals(id NUMBER) RETURN goal_table PIPELINED;
    FUNCTION get_cards(id NUMBER) RETURN card_table PIPELINED;
    FUNCTION get_arena_list RETURN arena_table PIPELINED;

END api;
/
SHOW ERRORS PACKAGE api;
/

CREATE OR REPLACE PACKAGE BODY api IS

    FUNCTION get_match_list RETURN matchs PIPELINED
    IS
        CURSOR match_list_cursor IS
                SELECT
                    home.name as home_name,
                    guest.name as guest_name,
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
                    mt.id as match_id,
                    home.id as home_id,
                    guest.id as guest_id
                FROM matchs mt
                INNER JOIN teams home ON home.id = mt.home_team
                INNER JOIN teams guest ON guest.id = mt.guest_team;
    BEGIN
        FOR curr IN match_list_cursor LOOP
            PIPE ROW (curr);
        END LOOP;
    END;



    FUNCTION get_match_info(id NUMBER) RETURN match_info_table PIPELINED
    IS
        CURSOR match_info_cursor IS
        SELECT
                home.name as home_name,
                guest.name as guest_name,
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
            WHERE mt.id = get_match_info.id;

        info match_info;
    BEGIN
        OPEN match_info_cursor;
        FETCH match_info_cursor INTO info;
        PIPE ROW(info);
        CLOSE match_info_cursor;
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

END api;
/
SHOW ERRORS PACKAGE BODY api;
/
