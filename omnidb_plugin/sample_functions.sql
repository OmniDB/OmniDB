-- SIMPLE
CREATE OR REPLACE FUNCTION omnidb.function_01(text, text)
RETURNS text AS $$
BEGIN
    RETURN $1 || ' ' || $2;
END;
$$ LANGUAGE plpgsql;

-- SELECT omnidb.function_01('hello', 'world');
-- --> 'hello world'

---

-- PARAMETER ALIAS
CREATE OR REPLACE FUNCTION omnidb.function_02(int, int)
RETURNS int AS $$
DECLARE
    i ALIAS FOR $1;
    j ALIAS FOR $2;
    sum int;
BEGIN
    sum := i + j;
    RETURN sum;
END;
$$ LANGUAGE plpgsql;

-- SELECT omnidb.function_02(41, 1);
-- --> 42

---

-- NAMED PARAMETERS
CREATE OR REPLACE FUNCTION omnidb.function_03(i int, j int)
RETURNS int AS $$
DECLARE
    sum int;
BEGIN
    sum := i + j;
    RETURN sum;
END;
$$ LANGUAGE plpgsql;

-- SELECT omnidb.function_03(41, 1);
-- --> 42

---

-- CONTROL STRUCTURES: IF
CREATE OR REPLACE FUNCTION omnidb.function_04(i int)
RETURNS boolean AS $$
DECLARE
    tmp int;
BEGIN
    tmp := i % 2;
    IF tmp = 0 THEN
        RETURN true;
    ELSE
        RETURN false;
    END IF;
END;
$$ LANGUAGE plpgsql;

-- SELECT omnidb.function_04(3);
-- --> f
-- SELECT omnidb.function_04(32);
-- --> t

---

-- CONTROL STRUCTURES: FOR ... LOOP
CREATE OR REPLACE FUNCTION omnidb.function_05(i numeric)
RETURNS numeric AS $$
DECLARE
    tmp numeric; result numeric;
BEGIN
    result := 1;
    FOR tmp IN 1 .. i LOOP
        result := result * tmp;
    END LOOP;
    RETURN result;
END;
$$ LANGUAGE plpgsql;

-- SELECT omnidb.function_05(42::numeric);
-- --> 1405006117752879898543142606244511569936384000000000

---

-- CONTROL STRUCTURES: WHILE ... LOOP
CREATE OR REPLACE FUNCTION omnidb.function_06(i numeric)
RETURNS numeric AS $$
DECLARE tmp numeric; result numeric;
BEGIN
    result := 1; tmp := 1;
    WHILE tmp <= i LOOP
        result := result * tmp;
        tmp := tmp + 1;
    END LOOP;
    RETURN result;
END;
$$ LANGUAGE plpgsql;

-- SELECT omnidb.function_06(42::numeric);
-- --> 1405006117752879898543142606244511569936384000000000

---

-- RECURSIVE
CREATE OR REPLACE FUNCTION omnidb.function_07(i numeric)
RETURNS numeric AS $$
BEGIN
    IF i = 0 THEN
        RETURN 1;
    ELSIF i = 1 THEN
        RETURN 1;
    ELSE
        RETURN i * omnidb.function_07(i - 1);
    END IF;
END;
$$ LANGUAGE plpgsql;

-- SELECT omnidb.function_07(42::numeric);
-- --> 1405006117752879898543142606244511569936384000000000

---

-- RECORD TYPES
CREATE OR REPLACE FUNCTION omnidb.function_08()
RETURNS text AS $$
DECLARE
    tmp RECORD;
BEGIN
    SELECT INTO tmp 1 + 1 AS a, 2 + 2 AS b;
    RETURN 'a = ' || tmp.a || '; b = ' || tmp.b;
END;
$$ LANGUAGE plpgsql;

-- SELECT omnidb.function_08();
-- --> 'a = 2; b = 4'

---

-- PERFORM
CREATE TABLE omnidb.foo(x integer);

CREATE OR REPLACE FUNCTION omnidb.function_09_aux() RETURNS void AS
$$ INSERT INTO omnidb.foo VALUES (41),(42) $$ LANGUAGE sql;

CREATE OR REPLACE FUNCTION omnidb.function_09()
RETURNS text AS $$
BEGIN
    PERFORM omnidb.function_09_aux();
    RETURN 'OK';
END;
$$ LANGUAGE plpgsql;

-- SELECT omnidb.function_09();
-- --> 'OK'
-- SELECT * FROM omnidb.foo;
-- --> 41, 42

---

-- DYNAMIC SQL
CREATE OR REPLACE FUNCTION omnidb.function_10(i int)
RETURNS omnidb.foo AS $$
DECLARE
    rec RECORD;
BEGIN
    EXECUTE 'SELECT * FROM omnidb.foo WHERE x = ' || i INTO rec;
    RETURN rec;
END;
$$ LANGUAGE plpgsql;

-- SELECT * FROM omnidb.function_10(42);
-- --> 42

---

-- CURSORS
CREATE OR REPLACE FUNCTION omnidb.function_11()
RETURNS numeric AS $$
DECLARE
    tmp RECORD; result numeric;
BEGIN
    result := 0.00;
    FOR tmp IN SELECT * FROM omnidb.foo LOOP
        result := result + tmp.x;
    END LOOP;
    RETURN result;
END;
$$ LANGUAGE plpgsql;

-- SELECT omnidb.function_11();
-- --> 83

---

-- ALTERNATIVE FUNCTION TERMINATOR
CREATE FUNCTION omnidb.function_12(text)
RETURNS text
AS 'DECLARE
        str text;
        ret text;
        i   integer;
        len integer;

    BEGIN
        str := upper($1);
        ret := '''';
        i   := 1;
        len := length(str);
        WHILE i <= len LOOP
            ret := ret || substr(str, i, 1) || '' '';
            i := i + 1;
        END LOOP;
        RETURN ret;
    END;'
LANGUAGE 'plpgsql';

-- SELECT omnidb.function_12('Hello World');
-- --> 'H E L L O W O R L D'

---

-- ERROR HANDLING
CREATE OR REPLACE FUNCTION omnidb.function_13(a integer, b integer)
RETURNS integer AS $$
BEGIN
    RETURN a + b;
EXCEPTION
    WHEN numeric_value_out_of_range THEN
    -- do some important stuff
    RETURN -1;
WHEN OTHERS THEN
    -- do some other important stuff
    RETURN -1;
END;
$$ LANGUAGE plpgsql;

---

-- NESTED EXCEPTION BLOCKS
CREATE TABLE omnidb.bar(a integer, b text);

CREATE FUNCTION omnidb.function_14(key integer, data text)
RETURNS void AS $$
BEGIN
    LOOP
        UPDATE omnidb.bar SET b = data WHERE a = key;
        IF found THEN RETURN;
        END IF;
        BEGIN
            INSERT INTO omnidb.bar (a, b) VALUES (key, data);
            RETURN;
        EXCEPTION WHEN unique_violation THEN
        -- do nothing
        END;
    END LOOP;
EXCEPTION WHEN OTHERS THEN
-- do something else
END;
$$ LANGUAGE plpgsql;
