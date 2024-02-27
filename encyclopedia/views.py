from django.shortcuts import render
from django import forms
from . import util
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
import markdown2
import random

class Content(forms.Form):
    title = forms.CharField(label="Title:")
    content = forms.CharField(widget=forms.Textarea,label="Content:")
class Edit(forms.Form):
    content = forms.CharField(widget=forms.Textarea(), label='Content:')

def edit_page(request, title):
    if request.method=="GET":
        page = util.get_entry(title)
        return render(request, "encyclopedia/edit.html",{
            "form": Content(),
            "edit": Edit(initial={"content": page}),
            "title": title
        })
    else:
        form=Edit(request.POST) 
        if form.is_valid():
            content = form.cleaned_data["content"]
            util.save_entry(title,content)
            to_convert_to_html = util.get_entry(title)
            html_converted = markdown2.markdown(to_convert_to_html)
            return render(request, "encyclopedia/wiki.html",{
                "form": Content(),
                "html_content": html_converted,
                "title": title
            })
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
def compare(title):
    for page in util.list_entries():
        if title.lower()==page.lower():
            return False
    return True

def create_page(request):
    if request.method=="POST":
        form=Content(request.POST)
        if form.is_valid():
            content=form.cleaned_data["content"]
            title=form.cleaned_data["title"]
            if compare(title):
                page_created=util.save_entry(title,content)
                return HttpResponseRedirect(f"wiki/{title}")
            else:
                return render(request,"encyclopedia/new_page.html",{
                    "content_data":form,
                    "error":"This file name "+f"'{title}'"+" already exists!"
            })
        else:
            return render(request,"encyclopedia/new_page.html",{
                "content_data":form
            })
    return render(request,"encyclopedia/new_page.html",{
        "content_data":Content()
    })
def page(request,title):
    content=util.get_entry(title)
    if content is None:
        return render(request,"encyclopedia/page_non_existing.html",{
            "title":title,
        })
    else:
        return render(request,"encyclopedia/wiki.html",{
            "title":title,
            "html_content":markdown2.markdown(content)
        })
def random_page(request):
    random_page=random.choice(util.list_entries())
    return render(request,"encyclopedia/random.html",{
        "title":random_page,
        "random_page_html_content":markdown2.markdown(util.get_entry(random_page))
    })

def search(request):
    search_entry = request.GET.get('q','')
    if util.get_entry(search_entry) is None:
        related_pages=list()
        for page in util.list_entries():
            if search_entry.lower() in page.lower():
                related_pages.append(page)
        return render(request,"encyclopedia/search.html",{
            "related_pages":related_pages,
            "search_entry":search_entry,
            "empty_list": len(related_pages)==0
        })
    else:
        return HttpResponseRedirect(f"wiki/{search_entry}")
