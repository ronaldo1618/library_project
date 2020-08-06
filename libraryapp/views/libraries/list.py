import sqlite3
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import reverse
from libraryapp.models import model_factory
from libraryapp.models import Library
from libraryapp.models import Book
from ..connection import Connection

# @login_required
# def list_libraries(request):
#     if request.method == 'GET':
#       with sqlite3.connect(Connection.db_path) as conn:
#           conn.row_factory = sqlite3.Row
#           db_cursor = conn.cursor()

#           db_cursor.execute('''
#           SELECT
#             l.id,
#             l.title,
#             l.address
#           FROM libraryapp_library l
#           ''')

#           all_libraries = []
#           dataset = db_cursor.fetchall()

#           for row in dataset:
#               library = Library()
#               library.id = row['id']
#               library.title = row['title']
#               library.address = row['address']

#               all_libraries.append(library)

#           template = 'libraries/list.html'
#           context = {
#             'all_libraries': all_libraries
#           }

#           return render(request, template, context)

    # elif request.method == 'POST':
    #   form_data = request.POST

    #   with sqlite3.connect(Connection.db_path) as conn:
    #       db_cursor = conn.cursor()

    #       db_cursor.execute("""
    #       INSERT INTO libraryapp_library
    #       (
    #           title, address
    #       )
    #       VALUES (?, ?)
    #       """,
    #       (form_data['title'], form_data['address']))

    #   return redirect(reverse('libraryapp:libraries'))


@login_required
def list_libraries(request):
    if request.method == 'GET':
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = create_library
            db_cursor = conn.cursor()

            db_cursor.execute("""
                SELECT
                    li.id,
                    li.title,
                    li.address,
                    b.id book_id,
                    b.title book_title,
                    b.author,
                    b.year_published,
                    b.isbn
                FROM libraryapp_library li
                JOIN libraryapp_book b ON li.id = b.location_id
            """)

            libraries = db_cursor.fetchall()

            # Start with an empty dictionary
            library_groups = {}

            # Iterate the list of tuples
            for (library, book) in libraries:

                # If the dictionary does have a key of the current
                # library's `id` value, add the key and set the value
                # to the current library
                if library.id not in library_groups:
                    library_groups[library.id] = library
                    library_groups[library.id].books.append(book)

                # If the key does exist, just append the current
                # book to the list of books for the current library
                else:
                    library_groups[library.id].books.append(book)

            template = 'libraries/list.html'
            context = {
                'all_libraries': library_groups
            }

            return render(request, template, context)
            
    elif request.method == 'POST':
      form_data = request.POST

      with sqlite3.connect(Connection.db_path) as conn:
          db_cursor = conn.cursor()

          db_cursor.execute("""
          INSERT INTO libraryapp_library
          (
              title, address
          )
          VALUES (?, ?)
          """, (form_data['title'], form_data['address']))

      return redirect(reverse('libraryapp:libraries'))

def create_library(cursor, row):
    _row = sqlite3.Row(cursor, row)

    library = Library()
    library.id = _row["id"]
    library.title = _row["title"]
    library.address = _row["address"]

    # Note: You are adding a blank books list to the library object
    # This list will be populated later (see below)
    library.books = []

    book = Book()
    book.id = _row["book_id"]
    book.title = _row["book_title"]
    book.author = _row["author"]
    book.isbn = _row["isbn"]
    book.year_published = _row["year_published"]

    # Return a tuple containing the library and the
    # book built from the data in the current row of
    # the data set
    return (library, book,)