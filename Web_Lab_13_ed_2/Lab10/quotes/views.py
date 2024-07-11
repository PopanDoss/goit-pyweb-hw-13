from bson import ObjectId

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect 
from django.core.paginator import Paginator

from quotes.models import Tag, Author

from quotes.forms import AuthorForm, QuoteForm


# Create your views here.
from .utils import get_mongodb

def main(request, page=1):
    db = get_mongodb()
    quotes = db.quotes.find()
    per_page = 10 
    paginator = Paginator(list(quotes), per_page)
    quotes_on_page = paginator.page(page)
    return render(request, 'quotes/index.html', context={'quotes':  quotes_on_page })

@login_required
def author(request):
    db = get_mongodb()

    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            new_author = form.save()
            

            # Тут ще додати збереження у монго
            db.authors.insert_one({
                "fullname": new_author.fullname,
                "born_date": new_author.born_date,
                "born_location": new_author.born_location,
                "description": new_author.description,
                
            })

            return redirect(to='quotes:main')
        else:
            return render(request, 'quotes/author.html', {'form': form})

    return render(request, 'quotes/author.html', {'form': AuthorForm()})

@login_required
def quote(request):
    db = get_mongodb()
    tags = Tag.objects.all()

    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            new_quote = form.save()
        
            choice_tags = Tag.objects.filter(name__in=request.POST.getlist('tags'))
            tag_names = [tag.name for tag in choice_tags]
            for tag in choice_tags.iterator():
                new_quote.tags.add(tag)

            author_in_db = db.authors.find_one({"fullname": new_quote.author.fullname})
            author_id = author_in_db["_id"]
           
            db.quotes.insert_one({
                "quote": new_quote.quote,
                "tags": tag_names,
                "author": author_id
            })

            return redirect(to='quotes:main')
        else:
            return render(request, 'quotes/quote.html', {"tags": tags, 'form': form})

    return render(request, 'quotes/quote.html', {"tags": tags, 'form': QuoteForm()})

def author_info(request, author_id ):
    
    db = get_mongodb()
    id = ObjectId(author_id)
    author = db.authors.find_one({'_id': id})
    print(author)

    return render (request,  'quotes/author_info.html', {"author": author } )
