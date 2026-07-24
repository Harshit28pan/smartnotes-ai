from datetime import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from ai_helper import generate_note , summarize_note , generate_quiz


class NotesManager:
    
    """
    A menu-driven application used to create, manage,
    search, update and analyze notes.
    """
    
    def __init__(self):
        
        """
    Initialize the Notes Manager and load all existing notes.
        """
        
        self.notes = []
        self.load_notes()
        print("Notes Manager started successully")
        
        if self.notes:

            print("\nPreviously Saved Notes\n")
 
            for note in self.notes:
                self.display_note(note)
  
        else:
           print("No saved notes available.")
        
    def add_note(self):
        """
    Collect note details from the user and save the note.
        """
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
           if self.notes:
               new_id = max(note["id"] for note in self.notes) + 1
           else:
               new_id = 1

           note = {
            "id": new_id,
            "title": title,
            "category": category,
            "priority": priority,
            "content": content,
            "date_created": datetime.now().strftime("%d-%m-%Y"),
            "last_modified": datetime.now().strftime("%d-%m-%Y"),
            "status": "Active",
            "source": "Manual"
              }
           self.notes.append(note)
           self.save_notes()
           print("\nNote added successfully.")
        except Exception as e:
            print("Error:", e)
        
    
    def save_notes(self):
        
        """
     Save all notes into the CSV file.
        """
        df= pd.DataFrame(self.notes)
        
        try:
            df.to_csv("notes.csv",index=False)
        except PermissionError:
            print("Please close notes.csv and try again.")
        except Exception as e:
            print(e)
        
    def load_notes(self):
        
        """
     Load notes from the CSV file when the application starts.
        """

        if os.path.exists("notes.csv"):

            try:
                df = pd.read_csv("notes.csv")
                self.notes = df.to_dict("records") 

            except Exception:
                self.notes = []

        else:
            self.notes = []
    
    
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
        
        """
      Display all available notes.
        """
        
        print("\n-----ALL NOTES-----\n")
        
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
       Update an existing note based on its ID.
         """

        print("\n========== UPDATE NOTE ==========")

        try:
            update_id = int(input("Enter Note ID : "))
        except ValueError:
            print("Please enter a valid ID.")
            return

        found = False

        for note in self.notes:

            if note["id"] == update_id:

                print("\nCurrent Note Details")
                self.display_note(note)

                note["title"] = input("Enter New Title : ")
                note["category"] = input("Enter New Category : ")
                note["priority"] = input("Enter New Priority : ")
                note["content"] = input("Enter New Content : ")

                note["last_modified"] = datetime.now().strftime("%d-%m-%Y")

                self.save_notes()

                print("\n✅ Note Updated Successfully!")

                found = True

                break

        if not found:
             print("\n❌ Note Not Found.")
             

    def delete_note(self):
        
        """
       Delete a note permanently from the records.
         """

        print("\n========== DELETE NOTE ==========")

        try:
            delete_id = int(input("Enter Note ID : "))
        except ValueError:
            print("Please enter a valid ID.")
            return

        found = False

        for note in self.notes:

            if note["id"] == delete_id:

                self.display_note(note)

                confirm = input("\nAre you sure? (yes/no) : ").lower()

                if confirm == "yes":
                    
                    found = True

                    self.notes.remove(note)
                    self.save_notes()

                    print("\n✅ Note Deleted Successfully!")

                else:

                    print("\nDeletion Cancelled.")

                    found = True
                    break

        if not found:

            print("\n❌ Note Not Found.")
            

    def filter_notes(self):
        
        """
      Display notes based on selected filters.
        """

        print("\n========== FILTER NOTES ==========")

        print("1. Filter by Category")
        print("2. Filter by Priority")
        print("3. Filter by Status")

        choice = input("\nEnter your choice : ")
 
        found = False

        if choice == "1":

            category = input("Enter Category : ").lower()

            for note in self.notes:

                if note["category"].lower() == category:

                    self.display_note(note)
                    found = True

        elif choice == "2":

            priority = input("Enter Priority (High/Medium/Low) : ").lower()

            for note in self.notes:

                if note["priority"].lower() == priority:

                    self.display_note(note)
                    found = True

        elif choice == "3":

            status = input("Enter Status (Active/Completed) : ").lower()

            for note in self.notes:

                if note["status"].lower() == status:

                    self.display_note(note)
                    found = True

        else:

            print("\nInvalid Choice!")
            return

        if not found:

             print("\nNo Notes Found")
             
    def change_status(self):
        
        """
      Change the status of a note.
        """
        try:
            notes_id= int(input("enter note id:"))
        except ValueError:
            print("Please enter a valid ID.")
            return
        
        found = False
        
        for note in self.notes:
            if note['id'] == notes_id:
                
                found = True
                print("\nCurrent status",note['status']) 
                
                print("1. Active")
                print("2.Completed")
                
                choice = int(input("Enter choice for status:"))
                
                if choice == 1:
                    note['status'] = "Active"
                    
                    
                elif choice == 2:
                    note['status'] = "Completed"
                    
                    
                else:
                    print("Invalid input")
                    return
                
                self.save_notes()
                print("\nStatus updated successfully")
                return
                    
                
        if not found:
            print("Invalid")
            
                
        
    def analysis_report(self):

        """
    Generate a detailed statistical report of stored notes.
        """

        try:
            df = pd.read_csv("notes.csv")

        except FileNotFoundError:
            print("notes.csv file not found.")
            return

        except pd.errors.EmptyDataError:
            print("notes.csv is empty.")
            return

        if df.empty:
            print("No notes available.")
            return

        print("\n========== NOTES ANALYTICS REPORT ==========\n")

    # ---------------- BASIC STATISTICS ---------------- #

        total_notes = len(df)

        active = len(df[df["status"] == "Active"])
        completed = len(df[df["status"] == "Completed"])

        manual = len(df[df["source"] == "Manual"])
        ai = len(df[df["source"] == "AI"])

        completion_rate = (completed / total_notes) * 100
        ai_usage_rate = (ai / total_notes) * 100
  
        print(f"Total Notes          : {total_notes}")
        print(f"Active Notes         : {active}")
        print(f"Completed Notes      : {completed}")
        print(f"Completion Rate      : {completion_rate:.2f}%")

        print(f"\nManual Notes         : {manual}")
        print(f"AI Generated Notes   : {ai}")
        print(f"AI Usage Rate        : {ai_usage_rate:.2f}%")

    # ---------------- CATEGORY REPORT ---------------- #

        print("\n========== CATEGORY RANKING ==========")

        category_counts = df["category"].value_counts()
  
        for category, count in category_counts.items():
            print(f"{category:<20}: {count}")

    # ---------------- PRIORITY REPORT ---------------- #

        print("\n========== PRIORITY REPORT ==========")

        high = len(df[df["priority"] == "High"])
        medium = len(df[df["priority"] == "Medium"])
        low = len(df[df["priority"] == "Low"])

        high_percent = (high / total_notes) * 100
        medium_percent = (medium / total_notes) * 100
        low_percent = (low / total_notes) * 100

        print(f"High Priority        : {high} ({high_percent:.2f}%)")
        print(f"Medium Priority      : {medium} ({medium_percent:.2f}%)")
        print(f"Low Priority         : {low} ({low_percent:.2f}%)")

    # ---------------- NUMPY ANALYSIS ---------------- #

        character_lengths = []
        word_counts = []
  
        for content in df["content"]:

            character_lengths.append(len(content))

            words = len(content.split())
            word_counts.append(words)

        character_lengths = np.array(character_lengths)
        word_counts = np.array(word_counts)

        average_characters = np.mean(character_lengths)
        average_words = np.mean(word_counts)

        longest_index = np.argmax(character_lengths)
        shortest_index = np.argmin(character_lengths)

        longest_note = df.iloc[longest_index]
        shortest_note = df.iloc[shortest_index]

        print("\n========== CONTENT ANALYSIS ==========")

        print(f"Average Characters   : {average_characters:.2f}")
        print(f"Average Words        : {average_words:.2f}")

        print("\nLongest Note")

        print(f"ID                   : {longest_note['id']}")
        print(f"Title                : {longest_note['title']}")
        print(f"Characters           : {character_lengths[longest_index]}")

        print("\nShortest Note")

        print(f"ID                   : {shortest_note['id']}")
        print(f"Title                : {shortest_note['title']}")
        print(f"Characters           : {character_lengths[shortest_index]}")

        print(f"\nTotal Characters     : {np.sum(character_lengths)}")

    # ---------------- EXPORT REPORT ---------------- #

        report = {
        "Total Notes": [total_notes],
        "Active Notes": [active],
        "Completed Notes": [completed],
        "Completion Rate (%)": [round(completion_rate, 2)],
        "Manual Notes": [manual],
        "AI Notes": [ai],
        "AI Usage Rate (%)": [round(ai_usage_rate, 2)],
        "High Priority": [high],
        "Medium Priority": [medium],
        "Low Priority": [low],
        "Average Characters": [round(average_characters, 2)],
        "Average Words": [round(average_words, 2)],
        "Longest Note Characters": [np.max(character_lengths)],
        "Shortest Note Characters": [np.min(character_lengths)],
        "Total Characters": [np.sum(character_lengths)]
        }

        report_df = pd.DataFrame(report)

        report_df.to_csv("analysis_report.csv", index=False)

        print("\nAnalysis Report Saved Successfully.")
        
        
    def visualization_report(self):

            try:
                df = pd.read_csv("notes.csv")

            except FileNotFoundError:
                print("notes.csv file not found.")
                return

            except pd.errors.EmptyDataError:
                print("notes.csv is empty.")
                return

            if df.empty:
                print("No notes available.")
                return
            
            # category pie chart
            category_counts = df["category"].value_counts()

            plt.figure(figsize=(7, 7))

            plt.pie(
                category_counts.values,
                labels=category_counts.index,
                autopct="%1.1f%%",
                startangle=90
               )

            plt.title("Notes Distribution by Category")

            plt.axis("equal")

            plt.savefig(
                "reports/charts/category_pie.png",
                 dpi=300,
                 bbox_inches="tight"
             )

            plt.close()
            
            # Priority bar chart
            priority_counts = df["priority"].value_counts()
            
            plt.figure(figsize=(8,5))
            
            plt.bar(
                priority_counts.index,
                priority_counts.values
               )
            plt.title("Priority Distribution")
            plt.xlabel("Priority")
            plt.ylabel("Notes")
            
            plt.savefig(
                 "reports/charts/priority_bar.png",
                  dpi=300,
                  bbox_inches="tight"
                    )
            
            # ---------------- STATUS PIE CHART ---------------- #

            status_counts = df["status"].value_counts()

            plt.figure(figsize=(7,7))

            plt.pie(
               status_counts.values,
               labels=status_counts.index,
               autopct="%1.1f%%",
               startangle=90
                )

            plt.title("Status Distribution")

            plt.axis("equal")

            plt.savefig(
                "reports/charts/status_pie.png",
                 dpi=300,
                 bbox_inches="tight"
                   )

            plt.close()

            print("Status Pie Chart Generated Successfully.")
            
            # ---------------- AI VS MANUAL BAR CHART ---------------- #

            source_counts = df["source"].value_counts()

            plt.figure(figsize=(8,5))

            plt.bar(
               source_counts.index,
               source_counts.values
             )

            plt.title("AI vs Manual Notes")

            plt.xlabel("Source")

            plt.ylabel("Number of Notes")

            plt.savefig(
                "reports/charts/source_bar.png",
                 dpi=300,
                 bbox_inches="tight"
               )

            plt.close()

            print("AI vs Manual Chart Generated Successfully.")
        
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

            if len(self.notes) == 0:
                new_id = 1
            else:
                new_id = max(note["id"] for note in self.notes) + 1

            new_note = {
                "id": new_id,
                "title": title,
                "category": category,
                "priority": priority,
                "status": "Active",
                "source": "AI",
                "content": note_content,
                "date_created": datetime.now().strftime("%d-%m-%Y"),
                "last_modified": datetime.now().strftime("%d-%m-%Y")
            }

            self.notes.append(new_note)

            self.save_notes()

            print("\nAI Note Saved Successfully!")

        # else:
        #     print("\nNote Not Saved.")

    except Exception as e:
        print("Unable to generate note.")
        print("Error:", e)    
    

    def ai_summarize_note(self):
        """
    Generate AI summary of a note and optionally save it.
        """

        try:
            note_id = int(input("Enter Note ID: "))

            found = False

            for note in self.notes:

                if note["id"] == note_id:

                    found = True

                    summary = summarize_note(note["content"])

                    print("\n========== SUMMARY ==========\n")
                    print(summary)

                    choice = input("\nSave Summary as New Note? (yes/no): ")

                if choice.lower() == "yes":

                    if len(self.notes) == 0:
                        new_id = 1
                    else:
                        new_id = max(note["id"] for note in self.notes) + 1

                    new_note = {
                        "id": new_id,
                        "title": note["title"],
                        "category": note["category"],
                        "priority": note["priority"],
                        "status": "Active",
                        "source": "AI",
                        "content": summary,
                        "date_created": datetime.now().strftime("%d-%m-%Y"),
                        "last_modified": datetime.now().strftime("%d-%m-%Y")
                    }

                    self.notes.append(new_note)
                    self.save_notes()

                    print("\nSummary Saved Successfully.")

                break

            if not found:
               print("\nNote ID Not Found.")

        except ValueError:
            print("Invalid Note ID. Please enter a number.")

        except PermissionError:
            print("Please close notes.csv and try again.")

        except Exception as e:
            print("Unable to generate summary.")
            print("Error:", e)

    def ai_generate_quiz(self):
        """
    Generate an AI quiz from a note and optionally save it as a text file.
        """

        try:
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
        
        