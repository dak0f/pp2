import psycopg2
from psycopg2 import Error
import csv

class PhoneBook:
    def __init__(self):
        try:
            self.connection = psycopg2.connect(
                user="postgres",
                password="add20070701",
                host="localhost",
                port="5432",
                database="phonebook"
            )
            self.cursor = self.connection.cursor()
            self.create_table()
            self.drop_and_create_functions_and_procedures()
        except Error as e:
            print(f"Error connecting to PostgreSQL: {e}")

    def __del__(self):
        if self.connection:
            self.cursor.close()
            self.connection.close()

    def create_table(self):
        try:
            create_table_query = '''
            CREATE TABLE IF NOT EXISTS phonebook (
                id SERIAL PRIMARY KEY,
                first_name VARCHAR(50) NOT NULL,
                last_name VARCHAR(50),
                phone VARCHAR(20) NOT NULL UNIQUE,
                email VARCHAR(100)
            );
            '''
            self.cursor.execute(create_table_query)
            self.connection.commit()
        except Error as e:
            print(f"Error creating table: {e}")

    def drop_and_create_functions_and_procedures(self):
        try:
            self.cursor.execute("DROP FUNCTION IF EXISTS search_by_pattern(TEXT);")
            self.cursor.execute("DROP PROCEDURE IF EXISTS insert_or_update_user(TEXT, TEXT);")
            self.cursor.execute("DROP PROCEDURE IF EXISTS insert_many_users(TEXT[][]);")
            self.cursor.execute("DROP FUNCTION IF EXISTS get_contacts_paginated(INTEGER, INTEGER);")
            self.cursor.execute("DROP PROCEDURE IF EXISTS delete_by_name_or_phone(TEXT);")

            # Search by pattern
            self.cursor.execute('''
            CREATE OR REPLACE FUNCTION search_by_pattern(pattern TEXT)
            RETURNS SETOF phonebook AS $$
            BEGIN
                RETURN QUERY
                SELECT * FROM phonebook
                WHERE first_name ILIKE '%' || pattern || '%'
                   OR last_name ILIKE '%' || pattern || '%'
                   OR phone LIKE '%' || pattern || '%'
                   OR email ILIKE '%' || pattern || '%';
            END;
            $$ LANGUAGE plpgsql;
            ''')

            # Insert or update user
            self.cursor.execute('''
            CREATE OR REPLACE PROCEDURE insert_or_update_user(
                p_name TEXT, p_phone TEXT
            )
            AS $$
            BEGIN
                IF EXISTS (SELECT 1 FROM phonebook WHERE phone = p_phone) THEN
                    UPDATE phonebook
                    SET first_name = p_name
                    WHERE phone = p_phone;
                ELSE
                    INSERT INTO phonebook (first_name, phone)
                    VALUES (p_name, p_phone);
                END IF;
            END;
            $$ LANGUAGE plpgsql;
            ''')

            # Insert many users
            self.cursor.execute('''
            CREATE OR REPLACE PROCEDURE insert_many_users(
                IN p_users TEXT[][],
                OUT incorrect_data TEXT[]
            )
            AS $$
            DECLARE
                user_record TEXT[];
                phone_text TEXT;
            BEGIN
                incorrect_data := '{}';
                FOREACH user_record SLICE 1 IN ARRAY p_users
                LOOP
                    phone_text := user_record[2];
                    IF phone_text ~ '^[0-9]+$' THEN
                        CALL insert_or_update_user(user_record[1], phone_text);
                    ELSE
                        incorrect_data := array_append(
                            incorrect_data,
                            user_record[1] || ';' || phone_text
                        );
                    END IF;
                END LOOP;
            END;
            $$ LANGUAGE plpgsql;
            ''')

            # Pagination
            self.cursor.execute('''
            CREATE OR REPLACE FUNCTION get_contacts_paginated(
                lim INTEGER, offs INTEGER
            )
            RETURNS SETOF phonebook AS $$
            BEGIN
                RETURN QUERY
                SELECT * FROM phonebook
                ORDER BY first_name, last_name
                LIMIT lim OFFSET offs;
            END;
            $$ LANGUAGE plpgsql;
            ''')

            # Delete by name or phone
            self.cursor.execute('''
            CREATE OR REPLACE PROCEDURE delete_by_name_or_phone(
                search_term TEXT
            )
            AS $$
            BEGIN
                DELETE FROM phonebook
                WHERE first_name = search_term OR phone = search_term;
            END;
            $$ LANGUAGE plpgsql;
            ''')

            self.connection.commit()
        except Error as e:
            print(f"Error creating functions and procedures: {e}")

    def insert_from_csv(self, filename):
        try:
            with open(filename, 'r') as f:
                reader = csv.reader(f)
                next(reader)
                for row in reader:
                    if len(row) >= 3:
                        first_name, last_name, phone = row[0], row[1], row[2]
                        email = row[3] if len(row) > 3 else None
                        insert_query = """
                        INSERT INTO phonebook (first_name, last_name, phone, email)
                        VALUES (%s, %s, %s, %s)
                        ON CONFLICT (phone) DO NOTHING
                        """
                        self.cursor.execute(insert_query, (first_name, last_name, phone, email))
            self.connection.commit()
            print("CSV data imported successfully")
        except (Error, FileNotFoundError) as e:
            print(f"Error importing from CSV: {e}")

    def insert_from_console(self):
        print("\nAdd a new contact:")
        first_name = input("First name: ")
        last_name = input("Last name (optional): ")
        phone = input("Phone: ")
        email = input("Email (optional): ")
        try:
            insert_query = """
            INSERT INTO phonebook (first_name, last_name, phone, email)
            VALUES (%s, %s, %s, %s)
            """
            self.cursor.execute(insert_query, (first_name, last_name, phone, email))
            self.connection.commit()
            print("Contact added successfully")
        except Error as e:
            self.connection.rollback()
            print(f"Error adding contact: {e}")

    def update_contact(self):
        search_term = input("Enter first name or phone to update: ")
        try:
            search_query = """
            SELECT * FROM phonebook
            WHERE first_name = %s OR phone = %s
            """
            self.cursor.execute(search_query, (search_term, search_term))
            contact = self.cursor.fetchone()
            if not contact:
                print("Contact not found")
                return
            print(f"\nFound contact: {contact[1]} {contact[2]}, phone: {contact[3]}, email: {contact[4]}")
            print("Enter new values (press Enter to keep current):")
            new_first_name = input(f"New first name [{contact[1]}]: ") or contact[1]
            new_last_name = input(f"New last name [{contact[2]}]: ") or contact[2]
            new_phone = input(f"New phone [{contact[3]}]: ") or contact[3]
            new_email = input(f"New email [{contact[4]}]: ") or contact[4]
            update_query = """
            UPDATE phonebook
            SET first_name = %s, last_name = %s, phone = %s, email = %s
            WHERE id = %s
            """
            self.cursor.execute(update_query, (new_first_name, new_last_name, new_phone, new_email, contact[0]))
            self.connection.commit()
            print("Contact updated successfully")
        except Error as e:
            print(f"Error updating contact: {e}")

    def query_contacts(self):
        print("\nSearch options:")
        print("1. By first name")
        print("2. By last name")
        print("3. By phone")
        print("4. By email")
        print("5. Show all")
        print("6. Pattern search")
        print("7. Pagination")
        choice = input("Choose an option (1-7): ")
        try:
            if choice == '1':
                name = input("Enter first name: ")
                query = "SELECT * FROM phonebook WHERE first_name = %s"
                self.cursor.execute(query, (name,))
            elif choice == '2':
                last_name = input("Enter last name: ")
                query = "SELECT * FROM phonebook WHERE last_name = %s"
                self.cursor.execute(query, (last_name,))
            elif choice == '3':
                phone = input("Enter phone: ")
                query = "SELECT * FROM phonebook WHERE phone = %s"
                self.cursor.execute(query, (phone,))
            elif choice == '4':
                email = input("Enter email: ")
                query = "SELECT * FROM phonebook WHERE email = %s"
                self.cursor.execute(query, (email,))
            elif choice == '5':
                query = "SELECT * FROM phonebook"
                self.cursor.execute(query)
            elif choice == '6':
                pattern = input("Enter search pattern: ")
                self.cursor.execute("SELECT * FROM search_by_pattern(%s)", (pattern,))
            elif choice == '7':
                limit = int(input("Records per page: "))
                offset = int(input("Page number (starting from 0): ")) * limit
                self.cursor.execute("SELECT * FROM get_contacts_paginated(%s, %s)", (limit, offset))
            else:
                print("Invalid option")
                return
            contacts = self.cursor.fetchall()
            if not contacts:
                print("No contacts found")
                return
            print("\nFound contacts:")
            print("-" * 50)
            for contact in contacts:
                print(f"ID: {contact[0]}")
                print(f"Name: {contact[1]} {contact[2]}")
                print(f"Phone: {contact[3]}")
                print(f"Email: {contact[4]}")
                print("-" * 50)
        except Error as e:
            print(f"Error during search: {e}")

    def delete_contact(self):
        search_term = input("Enter first name or phone to delete: ")
        try:
            self.cursor.callproc("delete_by_name_or_phone", (search_term,))
            self.connection.commit()
            print("Contact(s) deleted")
        except Error as e:
            print(f"Error deleting contact: {e}")

    def insert_or_update_user(self):
        print("\nInsert/update contact:")
        first_name = input("First name: ")
        phone = input("Phone: ")
        try:
            self.cursor.callproc("insert_or_update_user", (first_name, phone))
            self.connection.commit()
            print("Operation completed successfully")
        except Error as e:
            print(f"Error: {e}")

    def insert_many_users(self):
        print("\nInsert multiple contacts (format: name;phone)")
        print("Enter 'done' to finish")
        users = []
        while True:
            user_input = input("Enter name and phone: ")
            if user_input.lower() == 'done':
                break
            if ';' not in user_input:
                print("Invalid format. Use: name;phone")
                continue
            users.append(user_input.split(';', 1))

        if not users:
            print("No data entered")
            return

        try:
            users_array = [[str(i + 1), u[0], u[1]] for i, u in enumerate(users)]
            self.cursor.callproc("insert_many_users", (users_array,))
            incorrect_data = self.cursor.fetchone()[0]
            self.connection.commit()

            if incorrect_data:
                print("\nInvalid data (phone must contain only digits):")
                for data in incorrect_data:
                    print(data)
            else:
                print("All contacts inserted/updated successfully")
        except Error as e:
            print(f"Error: {e}")

def main():
    phonebook = PhoneBook()
    while True:
        print("\nPhoneBook Menu")
        print("1. Add from CSV")
        print("2. Add contact manually")
        print("3. Update contact")
        print("4. Search contacts")
        print("5. Delete contact")
        print("6. Insert/update contact (procedure)")
        print("7. Insert multiple contacts (procedure)")
        print("8. Exit")
        choice = input("Choose an option (1-8): ")
        if choice == '1':
            filename = input("Enter CSV file name: ")
            phonebook.insert_from_csv(filename)
        elif choice == '2':
            phonebook.insert_from_console()
        elif choice == '3':
            phonebook.update_contact()
        elif choice == '4':
            phonebook.query_contacts()
        elif choice == '5':
            phonebook.delete_contact()
        elif choice == '6':
            phonebook.insert_or_update_user()
        elif choice == '7':
            phonebook.insert_many_users()
        elif choice == '8':
            break
        else:
            print("Invalid option, try again")

if __name__ == "__main__":
    main()
