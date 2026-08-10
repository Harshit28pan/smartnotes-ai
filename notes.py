from datetime import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import seaborn as sns

from ai_helper import generate_note , summarize_note , generate_quiz

from database import (
    add_note as db_add_note,
    get_notes as db_get_notes,
    update_note as db_update_note,
    delete_note as db_delete_note
)


class NotesManager:
    
    """
    A menu-driven application used to create, manage,
    search, update and analyze notes.
    """
    
    def __init__(self):

        self.notes = []

        try:
            self.notes = db_get_notes()
        except Exception as e:
            print("❌ Unable to load notes from MySQL:", e)

        print("Notes Manager started successfully")

        if self.notes:

            print("\nPreviously Saved Notes\n")

        for note in self.notes:
            self.display_note(note)

        else:
            print("No saved notes available.")
        
    def add_note(self):

        print("\n------ ADD NEW NOTE ------")

        try:

            title = input("Enter Note Title: ")

            if not title.strip():
                print("Title cannot be empty.")
                return

            category = input("Enter Category: ")
            priority = input("Enter Priority (High/Medium/Low): ")
            content = input("Enter Note Content: ")

            if not content.strip():
                print("Content cannot be empty.")
                return

            today = datetime.now().strftime("%Y-%m-%d")

            note = {
            "title": title,
            "category": category,
            "priority": priority,
            "status": "Active",
            "source": "Manual",
            "content": content,
            "date_created": today,
            "last_modified": today
            }

            db_add_note(note)

            # Refresh self.notes from MySQL
            self.notes = db_get_notes()

            print("\n✅ Note added successfully.")

        except Exception as e:
                print("❌ Error:", e)
    
    
    
    def display_note(self, note):
        
        """
      Display the details of a single note.
         """

        print("\n------------------------------")

        print(f"ID : {note['id']}")
        print(f"Title : {note['title']}")
        print(f"Category : {note['category']}")
        print(f"Priority : {note['priority']}")
        print(f"Content : {note['content']}")
        print(f"Status : {note['status']}")
        print(f"Source : {note['source']}")
        print(f"Created : {note['date_created']}")
        print(f"Modified : {note['last_modified']}")

        print("------------------------------")
        
    def view_notes(self):

        print("\n-----ALL NOTES-----\n")

        self.notes = db_get_notes()

        if len(self.notes) == 0:
            print("No notes available")
            return

        for note in self.notes:
            self.display_note(note)
        
    
    def search_note(self):
        
        """
        Search notes using ID, title, category or priority.
        """
        
        
        
        print("\n========== SEARCH NOTE ==========")

        print("1. Search by ID")
        print("2. Search by Title")
        print("3. Search by Category")
        print("4. Search by Priority")

        choice = input("\nEnter your choice: ")
        
        # Get latest notes from MySQL
        self.notes = db_get_notes()

        found = False

        if choice == "1":
            
            try:
                search_id=int(input("ENTER NOTE ID:"))
            except ValueError:
                print("Please enter a valid ID.")
                return
            
            for note in self.notes:
                if note["id"] == search_id:
                    self.display_note(note)
                    found = True

        elif choice == "2":
            search_title = input("Enter Title: ").lower()

            for note in self.notes:
                if search_title in note["title"].lower():
                    self.display_note(note)
                    found = True

        elif choice == "3":
            search_category = input("Enter Category: ").lower()

            for note in self.notes:
                if note["category"].lower() == search_category:
                    self.display_note(note)
                    found = True

        elif choice == "4":
            search_priority = input("Enter Priority (High/Medium/Low): ").lower()

            for note in self.notes:
                if note["priority"].lower() == search_priority:
                    self.display_note(note)
                    found = True

        else:
            print("\nInvalid Choice!")
            return

        if not found:
            print("\nNo Note Found.")
            
    
    def update_note(self):

        """
    Update an existing note by ID.
        """

        print("\n========== UPDATE NOTE ==========")

        try:
            update_id = int(input("Enter Note ID : "))

        except ValueError:
            print("Please enter a valid ID.")
            return

        # Get latest notes from MySQL
        self.notes = db_get_notes()

        found = False

        for note in self.notes:

            if note["id"] == update_id:

                found = True

                print("\nCurrent Note Details:")
                self.display_note(note)

                print("\nEnter New Details:")

                title = input("Enter New Title : ")
                category = input("Enter New Category : ")
                priority = input("Enter New Priority : ")
                content = input("Enter New Content : ")

                # Keep existing values if user leaves field empty
                if not title.strip():
                    title = note["title"]

                if not category.strip():
                    category = note["category"]

                if not priority.strip():
                    priority = note["priority"]

                if not content.strip():
                    content = note["content"]

                # Update date
                last_modified = datetime.now().strftime("%Y-%m-%d")

                # Update MySQL
                db_update_note(
                update_id,
                title,
                category,
                priority,
                note["status"],
                note["source"],
                content
                )
 
                # Refresh notes from MySQL
                self.notes = db_get_notes()

                print("\n✅ Note Updated Successfully!")

                break

        if not found:

            print("\n❌ Note Not Found.")
             

    def delete_note(self):

        """
    Delete a note by ID.
        """

        print("\n========== DELETE NOTE ==========")

        try:
             delete_id = int(input("Enter Note ID : "))

        except ValueError:
             print("Please enter a valid ID.")
             return
  
        # Get latest notes from MySQL
        self.notes = db_get_notes()

        found = False

        for note in self.notes:

            if note["id"] == delete_id:

                found = True

                print("\nNote to be deleted:")
                self.display_note(note)

                confirm = input(
                "\nAre you sure you want to delete this note? (yes/no): "
                ).lower()

                if confirm == "yes":

                    result = db_delete_note(delete_id)

                    if result:

                        # Refresh notes from MySQL
                        self.notes = db_get_notes()

                        print("\n✅ Note Deleted Successfully!")

                    else:

                        print("\n❌ Note could not be deleted.")

                else:

                    print("\n❌ Deletion Cancelled.")
  
                break

        if not found:

            print("\n❌ Note Not Found.")


    def filter_notes(self):

        """
        Filter notes by category, priority or status.
        """

        print("\n========== FILTER NOTES ==========")

        print("1. Filter by Category")
        print("2. Filter by Priority")
        print("3. Filter by Status")

        choice = input("\nEnter your choice: ")

        # Get latest notes from MySQL
        self.notes = db_get_notes()

        filtered_notes = []

        if choice == "1":

            category = input("Enter Category: ").lower()

            for note in self.notes:

                if note["category"].lower() == category:
                    filtered_notes.append(note)

        elif choice == "2":

            priority = input(
            "Enter Priority (High/Medium/Low): "
            ).lower()

            for note in self.notes:

                if note["priority"].lower() == priority:
                    filtered_notes.append(note)

        elif choice == "3":

            status = input(
            "Enter Status (Active/Completed): "
            ).lower()

            for note in self.notes:

                if note["status"].lower() == status:
                    filtered_notes.append(note)

        else:

            print("\n❌ Invalid Choice!")
            return

        if not filtered_notes:

            print("\nNo matching notes found.")
            return

        print("\n========== FILTERED NOTES ==========")

        for note in filtered_notes:

             self.display_note(note)    

    def change_status(self):

        """
        Change the status of a note.
        """

        print("\n========== CHANGE STATUS ==========")

        try:
            note_id = int(input("Enter Note ID: "))

        except ValueError:
            print("Please enter a valid ID.")
            return

        # Get latest notes from MySQL
        self.notes = db_get_notes()

        found = False

        for note in self.notes:

            if note["id"] == note_id:

                found = True

                print("\nCurrent Status:", note["status"])

                print("\n1. Active")
                print("2. Completed")
 
                choice = input("\nEnter new status: ")

                if choice == "1":
                    new_status = "Active"

                elif choice == "2":
                    new_status = "Completed"

                else:
                    print("\n❌ Invalid choice.")
                    return

                # Update status in MySQL
                db_update_note(
                note_id,
                note["title"],
                note["category"],
                note["priority"],
                new_status,
                note["source"],
                note["content"]
                )

                # Refresh notes
                self.notes = db_get_notes()

                print(
                     f"\n✅ Status changed to {new_status} successfully!"
                )

                break

        if not found:

            print("\n❌ Note Not Found.")
        
    def analysis_report(self):

        """
         Generate analysis report using MySQL data.
        """

        print("\n========== ANALYSIS REPORT ==========\n")

        # Get latest data from MySQL
        self.notes = db_get_notes()

        if not self.notes:

            print("No notes available for analysis.")
            return

        # Convert MySQL data into DataFrame
        df = pd.DataFrame(self.notes)

        # ---------------- BASIC KPIs ---------------- #

        total_notes = len(df)

        active_notes = len(
        df[df["status"].str.lower() == "active"]
        )

        completed_notes = len(
        df[df["status"].str.lower() == "completed"]
        )

        manual_notes = len(
        df[df["source"].str.lower() == "manual"]
        )

        ai_notes = len(
        df[df["source"].str.lower() == "ai"]
        )

    # ---------------- CONTENT ANALYSIS ---------------- #

        df["word_count"] = (
        df["content"]
        .fillna("")
        .astype(str)
        .str.split()
        .str.len()
    )

        df["character_count"] = (
        df["content"]
        .fillna("")
        .astype(str)
        .str.len()
        )

        average_words = df["word_count"].mean()

        average_characters = df["character_count"].mean()

        longest_note = df["word_count"].max()

        shortest_note = df["word_count"].min()

    # ---------------- REPORT ---------------- #

        print("Total Notes       :", total_notes)
        print("Active Notes      :", active_notes)
        print("Completed Notes   :", completed_notes)

        print("Manual Notes      :", manual_notes)
        print("AI Notes          :", ai_notes)

        print(
        "Average Words     :",
        round(average_words, 2)
        )

        print(
        "Average Characters:",
        round(average_characters, 2)
        )

        print(
        "Longest Note      :",
        longest_note,
        "words"
    )

        print(
        "Shortest Note     :",
        shortest_note,
        "words"
        )

    # ---------------- CATEGORY REPORT ---------------- #

        print("\n----- CATEGORY REPORT -----")

        category_report = (
        df["category"]
        .value_counts()
        )

        print(category_report)

    # ---------------- PRIORITY REPORT ---------------- #

        print("\n----- PRIORITY REPORT -----")

        priority_report = (
        df["priority"]
        .value_counts()
        )

        print(priority_report)

        # ---------------- STATUS REPORT ---------------- #

        print("\n----- STATUS REPORT -----")

        status_report = (
        df["status"]
        .value_counts()
        )

        print(status_report)

    # ---------------- SOURCE REPORT ---------------- #

        print("\n----- SOURCE REPORT -----")

        source_report = (
        df["source"]
        .value_counts()
        )

        print(source_report)

        print("\n====================================")
    
    def visualization_report(self):

        """
        Generate visualization report using MySQL data.
        """

        print("\n========== VISUALIZATION REPORT ==========\n")

        # Get latest notes from MySQL
        self.notes = db_get_notes()

        if not self.notes:
            print("No notes available for visualization.")
            return

        # Convert MySQL data into DataFrame
        df = pd.DataFrame(self.notes)

        # Create folders
        os.makedirs("reports/charts", exist_ok=True)

        # --------------------------------------------------
        # 1. CATEGORY PIE CHART
        # --------------------------------------------------

        category_counts = df["category"].value_counts()

        plt.figure(figsize=(7, 7))

        plt.pie(
        category_counts,
        labels=category_counts.index,
        autopct="%1.1f%%",
        startangle=90
         )

        plt.title("Notes by Category")

        plt.tight_layout()

        plt.savefig(
        "reports/charts/category_pie.png",
        dpi=300,
        bbox_inches="tight"
        )

        plt.close()

        # --------------------------------------------------
        # 2. PRIORITY BAR CHART
        # --------------------------------------------------

        priority_counts = df["priority"].value_counts()

        plt.figure(figsize=(8, 5))

        bars = plt.bar(
        priority_counts.index,
        priority_counts.values
         )

        plt.title("Notes by Priority")
        plt.xlabel("Priority")
        plt.ylabel("Number of Notes")

        plt.grid(
        axis="y",
        linestyle="--",
        alpha=0.5
         )

        for bar in bars:

            plt.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height(),
            int(bar.get_height()),
            ha="center",
            va="bottom"
            )

            plt.tight_layout()

            plt.savefig(
        "reports/charts/priority_bar.png",
        dpi=300,
        bbox_inches="tight"
        )

        plt.close()

    # --------------------------------------------------
    # 3. STATUS PIE CHART
    # --------------------------------------------------

        status_counts = df["status"].value_counts()

        plt.figure(figsize=(7, 7))

        plt.pie(
        status_counts,
        labels=status_counts.index,
        autopct="%1.1f%%",
        startangle=90
         )

        plt.title("Notes by Status")

        plt.tight_layout()

        plt.savefig(
        "reports/charts/status_pie.png",
        dpi=300,
        bbox_inches="tight"
         )

        plt.close()

    # --------------------------------------------------
    # 4. AI VS MANUAL PIE CHART
    # --------------------------------------------------

        source_counts = df["source"].value_counts()

        plt.figure(figsize=(7, 7))

        plt.pie(
        source_counts,
        labels=source_counts.index,
        autopct="%1.1f%%",
        startangle=90
    )

        plt.title("AI vs Manual Notes")

        plt.tight_layout()

        plt.savefig(
        "reports/charts/ai_vs_manual_pie.png",
        dpi=300,
        bbox_inches="tight"
        )

        plt.close()

        print("✅ Visualization Report generated successfully!")

        print("\nCharts saved in:")
        print("reports/charts/")
    
    def ai_generate_note(self):
        """
         Generate notes using AI.
        """

        try:
            topic = input("Enter Topic: ")

            if not topic.strip():
                print("Topic cannot be empty.")
                return

            note_content = generate_note(topic)

            print("\n========== GENERATED NOTE ==========\n")
            print(note_content)

            choice = input("\nDo you want to save this note? (yes/no): ")

            if choice.lower() == "yes":

                title = input("Enter Title : ")
                category = input("Enter Category : ")
                priority = input("Enter Priority (High/Medium/Low): ")

                new_note = {
                "title": title,
                "category": category,
                "priority": priority,
                "status": "Active",
                "source": "AI",
                "content": note_content,
                "date_created": datetime.now().strftime("%Y-%m-%d"),
                "last_modified": datetime.now().strftime("%Y-%m-%d")
                }

                db_add_note(new_note)

                self.notes = db_get_notes()

                print("\nAI Note Saved Successfully!")

            else:
                print("\nNote Not Saved.")

        except Exception as e:
            print("Unable to generate note.")
            print("Error:", e)    
    

    def ai_summarize_note(self):
        """
        Generate AI summary of a note and optionally save it.
        """

        try:
            # Get latest notes from MySQL
            self.notes = db_get_notes()

            note_id = int(input("Enter Note ID: "))

            found = False

            for note in self.notes:

                if note["id"] == note_id:

                    found = True

                    summary = summarize_note(note["content"])

                    print("\n========== SUMMARY ==========\n")
                    print(summary)

                    choice = input(
                        "\nSave Summary as New Note? (yes/no): "
                    )

                    if choice.lower() == "yes":

                        # No ID required because MySQL AUTO_INCREMENT
                        new_note = {
                        "title": note["title"],
                        "category": note["category"],
                        "priority": note["priority"],
                        "status": "Active",
                        "source": "AI",
                        "content": summary,
                        "date_created": datetime.now().strftime("%Y-%m-%d"),
                        "last_modified": datetime.now().strftime("%Y-%m-%d")
                        }

                        # Save summary directly to MySQL
                        db_add_note(new_note)

                        # Refresh notes from MySQL
                        self.notes = db_get_notes()

                        print("\nSummary Saved Successfully.")

                    else:

                         print("\nSummary Not Saved.")

                    break

            if not found:

                print("\nNote ID Not Found.")

        except ValueError:

            print("Invalid Note ID. Please enter a number.")

        except Exception as e:

            print("Unable to generate summary.")
            print("Error:", e)

    def ai_generate_quiz(self):
        """
    Generate an AI quiz from a note and optionally save it as a text file.
        """

        try:
            
             self.notes = db_get_notes()
             
             note_id = int(input("Enter Note ID: "))

             found = False

             for note in self.notes:

                 if note["id"] == note_id:

                    found = True

                    quiz = generate_quiz(note["content"])

                    print("\n========== QUIZ ==========\n")
                    print(quiz)

                    choice = input("\nSave Quiz in Text File? (yes/no): ")

                    if choice.lower() == "yes":

                        file_name = f"Quiz_{note_id}.txt"

                        with open(file_name, "w", encoding="utf-8") as file:
                            file.write(quiz)

                            print("\nQuiz Saved Successfully.")

                        break

             if not found:
                     print("\nNote ID Not Found.")

        except ValueError:
            print("Invalid Note ID. Please enter a valid number.")

        except PermissionError:
            print("Permission denied while saving the quiz.")

        except Exception as e:
            print("Unable to generate quiz.")
            print("Error:", e)
            
    
    def ai_menu(self):
        
        """
        Display AI feature options for notes.
        """

        while True:

            print("\n========== AI FEATURES ==========")

            print("1. Generate Note")
            print("2. Summarize Note")
            print("3. Generate Quiz")
            print("4. Back")
            
            try:
                
                choice = input("\nEnter Choice : ")

                if choice == "1":

                    self.ai_generate_note()

                elif choice == "2":

                    self.ai_summarize_note()

                elif choice == "3":

                    self.ai_generate_quiz()

                elif choice == "4":

                    break

                else:

                    print("Invalid Choice.")
                    
            except ValueError:
                print("Enter valid no.")
        
        