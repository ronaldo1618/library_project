import sqlite3
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import reverse
from libraryapp.models import Library
from ..connection import Connection

@login_required
def list_libraries(request):
    if request.method == 'GET':
      with sqlite3.connect(Connection.db_path) as conn:
          conn.row_factory = sqlite3.Row
          db_cursor = conn.cursor()

          db_cursor.execute('''
          SELECT
            l.id,
            l.title,
            l.address
          FROM libraryapp_library l
          ''')

          all_libraries = []
          dataset = db_cursor.fetchall()

          for row in dataset:
              library = Library()
              library.id = row['id']
              library.title = row['title']
              library.address = row['address']

              all_libraries.append(library)

          template = 'libraries/list.html'
          context = {
            'all_libraries': all_libraries
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
          """,
          (form_data['title'], form_data['address']))

      return redirect(reverse('libraryapp:libraries'))