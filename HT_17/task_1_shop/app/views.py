from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return HttpResponse('''
    <html lang="en">
        <head>
          <title>Main page</title>
        </head>
        <body>
            <ul class="sidebar-nav">
                <li><a href="/"}">Home</a></li>
                <li><a href="/admin/">admin</a></li>
                <li><a href="/product/">products (json)</a></li>
                <li><a href="/order/">order</a></li>
            </ul>
        </body>
    </html>
    ''')
