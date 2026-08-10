import mysql.connector

from config import HOST, PORT, USER, PASSWORD, DATABASE


# --------------------------------------------------
# 1. DATABASE CONNECTION
# --------------------------------------------------

def get_connection():
    try:
        conn = mysql.connector.connect(
            host=HOST,
            port=PORT,
            user=USER,
            password=PASSWORD,
            database=DATABASE
        )

        return conn

    except mysql.connector.Error as e:
        print("❌ Database connection failed:", e)
        return None


# --------------------------------------------------
# 2. ADD NOTE - CREATE
# --------------------------------------------------

def add_note(note):
    conn = get_connection()

    if conn is None:
        return

    cursor = conn.cursor()

    query = """
        INSERT INTO notes
        (
            title,
            category,
            priority,
            status,
            source,
            content,
            date_created,
            last_modified
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """

    values = (
        note["title"],
        note["category"],
        note["priority"],
        note["status"],
        note["source"],
        note["content"],
        note["date_created"],
        note["last_modified"]
    )

    try:
        cursor.execute(query, values)
        conn.commit()

        print("✅ Note added successfully!")

    except mysql.connector.Error as e:
        print("❌ Failed to add note:", e)

    finally:
        cursor.close()
        conn.close()


# --------------------------------------------------
# 3. VIEW NOTES - READ
# --------------------------------------------------

def get_notes():
    conn = get_connection()

    if conn is None:
        return []

    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT
            id,
            title,
            category,
            priority,
            status,
            source,
            content,
            date_created,
            last_modified
        FROM notes
        ORDER BY id
    """

    try:
        cursor.execute(query)

        notes = cursor.fetchall()

        return notes

    except mysql.connector.Error as e:
        print("❌ Failed to fetch notes:", e)
        return []

    finally:
        cursor.close()
        conn.close()


# --------------------------------------------------
# 4. UPDATE NOTE - UPDATE
# --------------------------------------------------

def update_note(
    note_id,
    title,
    category,
    priority,
    status,
    source,
    content
):

    conn = get_connection()

    if conn is None:
        return

    cursor = conn.cursor()

    query = """
        UPDATE notes
        SET
            title = %s,
            category = %s,
            priority = %s,
            status = %s,
            source = %s,
            content = %s,
            last_modified = CURDATE()
        WHERE id = %s
    """

    values = (
        title,
        category,
        priority,
        status,
        source,
        content,
        note_id
    )

    try:
        cursor.execute(query, values)

        conn.commit()

        if cursor.rowcount > 0:
            print("✅ Note updated successfully!")
        else:
            print("⚠️ Note ID not found.")

    except mysql.connector.Error as e:
        print("❌ Failed to update note:", e)

    finally:
        cursor.close()
        conn.close()


# --------------------------------------------------
# 5. DELETE NOTE - DELETE
# --------------------------------------------------

def delete_note(note_id):

    conn = get_connection()

    if conn is None:
        return

    cursor = conn.cursor()

    query = """
        DELETE FROM notes
        WHERE id = %s
    """

    try:
        cursor.execute(query, (note_id,))

        conn.commit()

        if cursor.rowcount > 0:
            print("✅ Note deleted successfully!")
        else:
            print("⚠️ Note ID not found.")

    except mysql.connector.Error as e:
        print("❌ Failed to delete note:", e)

    finally:
        cursor.close()
        conn.close()


# --------------------------------------------------
# 6. TEST
# --------------------------------------------------

if __name__ == "__main__":

    print("Testing MySQL connection...\n")

    conn = get_connection()

    if conn:
        print("✅ MySQL Connection Successful!")
        conn.close()

    # Show current notes
    print("\nCurrent Notes:\n")

    notes = get_notes()

    for note in notes:

        print("----------------------------------")
        print("ID:", note["id"])
        print("Title:", note["title"])
        print("Category:", note["category"])
        print("Priority:", note["priority"])
        print("Status:", note["status"])

    # Test DELETE
    # delete_note(1)

    # Show notes after deletion
    print("\nNotes after deletion:\n")

    notes = get_notes()

    for note in notes:

        print("----------------------------------")
        print("ID:", note["id"])
        print("Title:", note["title"])
        print("Category:", note["category"])
        print("Priority:", note["priority"])
        print("Status:", note["status"])