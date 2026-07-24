from notes import NotesManager

"""
Run the main menu of the Notes Manager application.
"""

def __main__():
    
    manager = NotesManager()
   
    while True:
    
        print("\n-----Notes Manager-----\n")
        
        print("1. Add Note")
        print("2.View Note")
        print("3.Search Note")
        print("4. Update Note")
        print("5. Delete Note")
        print("6. filter_notes")
        print("7.Change_status")
        print("8.Analysis Report")
        print("9. AI feature")
        print("10. Exit")
    
        try:
        
            choice = int(input("Enter Your choice:"))
    
            if choice == 1 :
                manager.add_note()
        
            elif choice == 2:
                manager.view_notes()
        
            elif choice == 3:
                manager.search_note()
    
            elif choice == 4:
                manager.update_note()
    
            elif choice == 5:
                manager.delete_note()
    
            elif choice == 6:
                manager.filter_notes()
            
            elif choice == 7:
                manager.change_status()
        
            elif choice == 8:
                manager.analysis_report()
        
            elif choice == 9:
                manager.ai_menu()
                
    
            elif choice == 10:
                print("\n Thank You for using Notes Manager!")
                break
    
            else:
                print("\nInvalid choice ! please try again")
            
    
        except ValueError:
            print("\nPlease enter a valid number.")
            
if __name__ == "__main__":
    __main__()
        
    
    
    