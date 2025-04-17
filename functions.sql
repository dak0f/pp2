-- 1. Функция поиска по шаблону (имя, фамилия или номер)
CREATE OR REPLACE FUNCTION search_contacts(pattern TEXT)
RETURNS TABLE(name TEXT, phone TEXT) AS $$
BEGIN
    RETURN QUERY
    SELECT name, phone FROM phonebook
    WHERE name ILIKE '%' || pattern || '%'
       OR phone ILIKE '%' || pattern || '%';
END;
$$ LANGUAGE plpgsql;

-- 2. Процедура: вставка или обновление одного пользователя
CREATE OR REPLACE PROCEDURE insert_or_update_user(p_name TEXT, p_phone TEXT)
LANGUAGE plpgsql AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM phonebook WHERE name = p_name) THEN
        UPDATE phonebook SET phone = p_phone WHERE name = p_name;
    ELSE
        INSERT INTO phonebook(name, phone) VALUES(p_name, p_phone);
    END IF;
END;
$$;

-- 3. Процедура: массовая вставка пользователей с проверкой
CREATE OR REPLACE PROCEDURE insert_many_users(
    names TEXT[],
    phones TEXT[],
    OUT invalid_entries TEXT[]
)
LANGUAGE plpgsql AS $$
DECLARE
    i INT := 1;
BEGIN
    invalid_entries := ARRAY[]::TEXT[];
    WHILE i <= array_length(names, 1) LOOP
        IF phones[i] ~ '^\+?[0-9]{10,15}$' THEN
            CALL insert_or_update_user(names[i], phones[i]);
        ELSE
            invalid_entries := array_append(invalid_entries, names[i] || ':' || phones[i]);
        END IF;
        i := i + 1;
    END LOOP;
END;
$$;

-- 4. Функция с пагинацией
CREATE OR REPLACE FUNCTION get_contacts_paginated(p_limit INT, p_offset INT)
RETURNS TABLE(name TEXT, phone TEXT) AS $$
BEGIN
    RETURN QUERY
    SELECT name, phone FROM phonebook
    ORDER BY name
    LIMIT p_limit OFFSET p_offset;
END;
$$ LANGUAGE plpgsql;

-- 5. Процедура удаления по имени или телефону
CREATE OR REPLACE PROCEDURE delete_by_name_or_phone(p_value TEXT)
LANGUAGE plpgsql AS $$
BEGIN
    DELETE FROM phonebook
    WHERE name = p_value OR phone = p_value;
END;
$$;
