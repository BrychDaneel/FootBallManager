CREATE OR REPLACE PACKAGE api IS

    TYPE match IS RECORD(
        home_name football.teams.name%TYPE,
        guest_name football.teams.name%TYPE,
        home_score NUMBER,
        guest_score NUMBER,
        match_id football.matchs.id%TYPE,
        home_id football.teams.id%TYPE,
        guest_id football.teams.id%TYPE
    );
    TYPE matchs IS TABLE OF match;

    FUNCTION match_list RETURN matchs PIPELINED;

END api;
/
SHOW ERRORS PACKAGE api;
/

CREATE OR REPLACE PACKAGE BODY api IS

    FUNCTION match_list RETURN matchs PIPELINED
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

END api;
/
SHOW ERRORS PACKAGE BODY api;
/
