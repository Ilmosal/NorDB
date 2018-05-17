/*
CREATE ROLES
------------
This file has all commands for creating all the roles required by the database if they already don't exist.
*/

--Guest user role for people that can only read data in the database and nothing else
DO $$BEGIN
IF ('guests' NOT IN (SELECT rolname FROM pg_roles)) THEN 
    CREATE ROLE guests;
END IF;
END$$;

--Default role for most of the users. Can read and insert data in the database but cannot modify and remove anything other than their additions
DO $$BEGIN
IF ('default_users' NOT IN (SELECT rolname FROM pg_roles)) THEN 
    CREATE ROLE default_users;
END IF;
END$$;

--Station Manager role for the database. Can do everything a default user can, but also can insert and modify station data in database.
DO $$BEGIN
IF ('station_managers' NOT IN (SELECT rolname FROM pg_roles)) THEN 
    CREATE ROLE station_managers;
    GRANT default_users TO station_managers;
END IF;
END$$;

--Admin role for the database. Can access and modify database
DO $$BEGIN
IF ('admins' NOT IN (SELECT rolname FROM pg_roles)) THEN 
    CREATE ROLE admins;
END IF;
END$$;


