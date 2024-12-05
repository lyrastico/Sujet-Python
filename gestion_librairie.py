# Sujet de Louis Barthes IPSSI MTP

# Je commente pour spécifier que je comprends bien ce que je fais , un peu de légitimité en ces temps de chat GPT
# dans ce projet, j'utiliserais try et exept, me permettant une gestion d'erreur approfondie, comme j'en ai l'habitude en javaScript
# avec try catch. Ma documentation pour leur utilisation : https://www.w3schools.com/python/python_try_except.asp

# Etape 1 : créer ma classe livre

class Book:
    def __init__(self, title: str, author: str):
        self.title = title
        self.author = author
        self.is_available = True

    def __str__(self):
        return f"Title: {self.title}, Author: {self.author}, Available: {self.is_available}"

# Etape 2 : ajouter la classe Bibliotheque et ses méthode ajouter livre, qui permettra de stoquer les
# futurs objets livres, probablement a l'aide d'une autre méthode, ainsi que la création de la méthode liste des livres,
# qui retournera les différents objets livres contenus dans la bibliothèque

class Library:
    def __init__(self):
        self.books = []

    def add_book(self, title: str, author: str):
        try:
            new_book = Book(title, author)
            self.books.append(new_book)
            print(f"Le livre '{title}' a été ajouté.")
        except Exception as e:
            print(f"Erreur lors de l'ajout du livre : {e}")

    def list_books(self):
        try:
            if not self.books:
                print("Aucun livre disponible dans la bibliothèque.")
            else:
                book_list = [str(book) for book in self.books]
                return book_list
        except Exception as e:
            print(f"Erreur lors de la liste des livres : {e}")
            return []

# Etape 3 : ajout de d'une méthode pour gérer le chargement initial des données (livres) appelée charger livre

# Etape 8 : on reprends la méthode load_books et ajoute save_books pour les enrregistrer dans un fichier a part
# utilisation de la docs : https://stackoverflow.com/questions/5849654/python-openx-r-function-how-do-i-know-or-control-which-encoding-the-file

    def load_books(self, file_path: str):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                for line in file:
                    line = line.strip()
                    title, author, is_available = line.split(',')
                    book = Book(title.strip(), author.strip())
                    book.is_available = is_available.strip() == 'True'
                    self.books.append(book)
            print(f"Les livres ont été chargés depuis le fichier '{file_path}'.")
        except FileNotFoundError:
            print(f"Erreur : Le fichier '{file_path}' n'a pas été trouvé.")
        except Exception as e:
            print(f"Erreur lors de la lecture du fichier : {e}")

    def save_books(self, file_path: str):
        try:
            with open(file_path, 'w+', encoding='utf-8') as file:
                for book in self.books:
                    file.write(f"{book.title},{book.author},{book.is_available}\n")
            print(f"Les livres ont été sauvegardés dans '{file_path}'.")
        except Exception as e:
            print(f"Erreur lors de la sauvegarde du fichier : {e}")


# Etape 5 : ajouter deux méthode a la classe librairie : une pour prêter un livre a une entitée objet, et l'autre pour le récupérer

# Etape 6 : je modifie les méthode de librairie liées a l'emprun et au retour, pour vérifier les cas suivants : un étudiant ne peut
# emprunter un livre qu'il est déja en cours d'emprun, et un livre non disponible ne peut être emprunté

    def lend_book(self, book_title: str, student: 'Student') -> bool:
        try:
            for book in self.books:
                if book.title == book_title:
                    if book.is_available:
                        if book in student.borrowed_books:
                            print(f"{student.name} a déjà emprunté '{book_title}' auparavant.")
                            return False
                        else:
                            student.borrow_book(book_title, self)
                            book.is_available = False
                            return True
                    else:
                        print(f"Le livre '{book_title}' est actuellement indisponible.")
                        return False
            print(f"Le livre '{book_title}' n'existe pas dans la bibliothèque.")
            return False
        except Exception as e:
            print(f"Erreur lors de l'emprunt du livre : {e}")
            return False

    def accept_return(self, book_title: str, student: 'Student'):
        try:
            for book in self.books:
                if book.title == book_title:
                    if book in student.borrowed_books:
                        student.return_book(book_title, self)
                        book.is_available = True
                        print(f"Le livre '{book_title}' a été retourné et est maintenant disponible.")
                        return
                    else:
                        print(f"L'étudiant n'a pas emprunté le livre '{book_title}'.")
                        return
            print(f"Le livre '{book_title}' n'existe pas dans la bibliothèque.")
        except Exception as e:
            print(f"Erreur lors du retour du livre : {e}")

# Etape 7 : pour cette étape, j'ajoute une méthode de recherche dans la classe, pour permettre de chercher des livres, 
# et si ils existent, de les return

    def search_books(self, query: str) -> list:
        try:
            results = []
            query = query.lower()
            for book in self.books:
                if query in book.title.lower() or query in book.author.lower():
                    results.append(str(book))
            return results
        except Exception as e:
            print(f"Erreur lors de la recherche des livres : {e}")
            return []


# Etape 4 : création de la table Etudiant, avec les attributs de classe demandés : livres empruntés et 
# Nom (de l'étudiant), ainsi que ses méthodes, Emprunter, et rendre, qui serviront a ajouter ou retirer 
# un objet livre du tableau d'objets : livres empruntés

# Etape 10: limiter les emprunts de livres des étudiants

class Student:
    def __init__(self, name: str, max_borrow_limit: int = 4):
        self.name = name
        self.borrowed_books = []
        self.max_borrow_limit = max_borrow_limit
    
    def borrow_book(self, book_title: str, library: Library):
        try:
            if len(self.borrowed_books) >= self.max_borrow_limit:
                print(f"{self.name} a atteint sa limite d'emprunt de {self.max_borrow_limit} livres.")
                return False
            
            success = library.lend_book(book_title, self)
            if success:
                self.borrowed_books.append(book_title)
                print(f"{self.name} a emprunté le livre '{book_title}'.")
                return True
            else:
                print(f"Le livre '{book_title}' est indisponible ou déjà emprunté.")
                return False
        except Exception as e:
            print(f"Erreur lors de l'emprunt du livre : {e}")
            return False

    def return_book(self, book_title: str, library: Library):
        try:
            if book_title in self.borrowed_books:
                self.borrowed_books.remove(book_title)
                library.accept_return(book_title, self)
                print(f"{self.name} a retourné le livre '{book_title}'.")
            else:
                print(f"{self.name} n'a pas emprunté le livre '{book_title}'.")
        except Exception as e:
            print(f"Erreur lors du retour du livre : {e}")


# Etape 9 : Enfin du fun et de la manipulation d'interfaces, je supprimes les logs, j'utilise maintenant run_library_system
# pour créer une interface en ligne de comandes

def run_library_system():

    library = Library()
    student = Student("John Doe")

    while True:
        print("\n--- Menu ---")
        print("1. Voir tous les livres")
        print("2. Rechercher un livre")
        print("3. Ajouter un livre")
        print("4. Emprunter un livre")
        print("5. Retourner un livre")
        print("6. Quitter")
        
        choice = input("Choisissez une option (1-6): ")
        
        try:
            if choice == "1":
                books = library.list_books()
                if books:
                    for book in books:
                        print(book)
                else:
                    print("Aucun livre disponible dans la bibliothèque.")
            
            elif choice == "2":
                query = input("Entrez un titre ou un auteur pour rechercher: ")
                results = library.search_books(query)
                if results:
                    print("\nLivres trouvés:")
                    for book in results:
                        print(book)
                else:
                    print("Aucun livre trouvé pour votre recherche.")
            
            elif choice == "3":
                title = input("Entrez le titre du livre: ")
                author = input("Entrez l'auteur du livre: ")
                library.add_book(title, author)
            
            elif choice == "4":
                book_title = input("Entrez le titre du livre que vous souhaitez emprunter: ")
                library.lend_book(book_title, student)
            
            elif choice == "5":
                book_title = input("Entrez le titre du livre que vous souhaitez retourner: ")
                library.accept_return(book_title, student)
            
            elif choice == "6":
                print("Merci d'avoir utilisé le système de gestion de bibliothèque. À bientôt !")
                break
            
            else:
                print("Option invalide. Veuillez choisir une option entre 1 et 6.")
        
        except Exception as e:
            print(f"Erreur : {e}")

run_library_system()

# test push git