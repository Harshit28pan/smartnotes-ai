from datetime import datetime
import pandas as pd
import numpy as np
from pandas.errors import EmptyDataError
import os
import groq
from ai_helper import generate_note , summarize_note , generate_quiz


class NotesManager:
    
    def __init__(self):
        
        self.notes = []
        self.load_notes()
        print("Notes Manager started successully")
        
    def add_note(self):
        print("\n-----ADD NEW NOTE-----")
        title = input("Enter Note Title:")
        category = input("Enter Category:")
        priority = input("Enter Priority (High/Medium/low):")
        content = input("Enter Note Content:")
            
        note = {
            "id" : max(note["id"] for note in self.notes) + 1,
            "title": title,
            "category": category,
            "priority":priority,
            "content":content,
            "date_created":datetime.now().strftime("%d-%m-%Y"),
            "last_modified":datetime.now().strftime("%d-%m-%Y"),
            "status":"Active",
            "source":"Manual"
            }
        
        self.notes.append(note)
        
        try:
            
           self.save_notes()
           print("\n Note added successfully")
        
        except Exception as e:
            print("error",e)
        
    
    def save_notes(self):
        df= pd.DataFrame(self.notes)
        df.to_csv("notes.csv", index=False)
        
    def load_notes(self):

        if os.path.exists("notes.csv"):

            try:
                df = pd.read_csv("notes.csv")

                self.notes = []

                for i in range(len(df)):
                    
                    note = {
                    "id": df.loc[i, "id"],
                    "title": df.loc[i, "title"],
                    "category": df.loc[i, "category"],
                    "priority": df.loc[i, "priority"],
                    "content": df.loc[i, "content"],
                    "date_created": df.loc[i, "date_created"],
                    "last_modified": df.loc[i, "last_modified"],
                    "status": df.loc[i, "status"],
                    "source": df.loc[i, "source"]
                }

                    self.notes.append(note)

            except EmptyDataError:
                self.notes = []

        else:
            self.notes = []
    
    
    def display_note(self, note):

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
        
        if len(self.notes) == 0:
            print("No notes available")
            return
        
        for note in self.notes:
            self.display_note(note)
    
        
    
    def search_note(self):
        
        print("\n========== SEARCH NOTE ==========")

        print("1. Search by ID")
        print("2. Search by Title")
        print("3. Search by Category")
        print("4. Search by Priority")

        choice = input("\nEnter your choice: ")

        found = False

        if choice == "1":
            search_id = int(input("Enter Note ID: "))

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

        if found == False:
            print("\nNo Note Found.")
            
    
    def update_note(self):

        print("\n========== UPDATE NOTE ==========")

        update_id = int(input("Enter Note ID : "))

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

        if found == False:
             print("\n❌ Note Not Found.")
             

    def delete_note(self):

        print("\n========== DELETE NOTE ==========")

        delete_id = int(input("Enter Note ID : "))

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

        if found == False:

            print("\n❌ Note Not Found.")
            

    def filter_notes(self):

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

        if found == False:

             print("\nNo Notes Found")
             
    def change_status(self):
        
        notes_id= int(input("enter note id:"))
        
        found = False
        
        for note in self.notes:
            if note['id'] == notes_id:
                
                found = True
                print("\nCurrent status",note['status']) 
                
                print("1. active")
                print("2.completed")
                
                choice = int(input("Enter choice for status:"))
                
                if choice == 1:
                    note['status'] = "active"
                    
                    
                elif choice == 2:
                    note['status'] = "completed"
                    
                    
                else:
                    print("Invalid input")
                    return
                
                self.save_notes()
                print("\nStatus updated successfully")
                return
                    
                
        if not found:
            print("Invalid")
            
                
        
    def analysis_report(self):
        
        try:
            df = pd.read_csv("notes.csv")
        except:
            print("No notes found.")
            return
        

        print("\n------NOTES ANALYSIS REPORT------")

        print("Total Notes :", len(df))

        active = len(df[df["status"] == "Active"])
        print("Active Notes :", active)

        completed = len(df[df["status"] == "Completed"])
        print("Completed Notes :", completed)

        manual = len(df[df["source"] == "Manual"])
        print("Manual Notes :", manual)

        ai = len(df[df["source"] == "AI"])
        print("AI Notes :", ai)

        print("\nCategory Report")

        categories = df["category"].unique()

        for cat in categories:
            count = len(df[df["category"] == cat])
            print(cat, ":", count)

        high = len(df[df["priority"] == "High"])
        medium = len(df[df["priority"] == "Medium"])
        low = len(df[df["priority"] == "Low"])

        print("\nPriority Report")
        print("High :", high)
        print("Medium :", medium)
        print("Low :", low)
        
        print("\n------NUMPY ANALYSIS------")

        lengths = []

        for content in df["content"]:
            lengths.append(len(content))

        lengths = np.array(lengths)

        print("Average Note Length :", np.mean(lengths))
        print("Longest Note Length :", np.max(lengths))
        print("Shortest Note Length :", np.min(lengths))
        print("Total Characters :", np.sum(lengths))
        
        report = {
    "Total Notes": [len(df)],
    "Active Notes": [active],
    "Completed Notes": [completed],
    "Manual Notes": [manual],
    "AI Notes": [ai],
    "High Priority": [high],
    "Medium Priority": [medium],
    "Low Priority": [low]
        }

        report_df = pd.DataFrame(report)

        report_df.to_csv("analysis_report.csv", index=False)

        print("\nAnalysis Report Saved Successfully.")
        

    def ai_generate_note(self):

        topic = input("Enter Topic : ")

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

        else:

            print("\nNote Not Saved.")
            

    def ai_summarize_note(self):

        note_id = int(input("Enter Note ID : "))

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
            

    def ai_generate_quiz(self):

        note_id = int(input("Enter Note ID : "))

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
            
    
    def ai_menu(self):

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
        
        