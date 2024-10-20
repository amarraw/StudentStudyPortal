from django.shortcuts import render , redirect
from .models import Notes , Homework , Todo 
from .forms import NoteForm , HomeworkForm , DashboardForm , TodoForm  , ConversionForm 
from django.contrib import messages
from django.views.generic import DetailView
from youtubesearchpython import VideosSearch
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .unitConversion import convert_units
import requests
import wikipedia
# Create your views here.


@login_required(login_url='login')
def home(request):
    return render(request, "dashboard/home.html")

@login_required(login_url='login')
def notes(request):
    if request.method == "POST":
        form = NoteForm(request.POST)
        if form.is_valid():
            notes = Notes(user=request.user, title=request.POST['title'], descriptions=request.POST['descriptions'])
            notes.save()
            messages.success(request, f"Note added {request.user.username} successfully")
    form = NoteForm()
    
    notes = Notes.objects.filter(user=request.user)
    context = {
        "notes":notes,
        "form":form ,
    }
    return render(request, "dashboard/notes.html", context)

@login_required(login_url='login')
def deletenote(request, pk):
    note = Notes.objects.get(id=pk)
    note.delete()
    return redirect("notes")


class NotesDetailsView(LoginRequiredMixin,DetailView):
    model = Notes
    template_name = "dashboard/notes_detail.html"


@login_required(login_url='login')
def homework(request):
    if request.method == "POST":
        form = HomeworkForm(request.POST)
        if form.is_valid():
            try:
                finished = request.POST['is_finished']
                if finished == "on":
                    finished = True
                else:
                    finished = False
            except:
                finished = False
            homeworks = Homework(
                user = request.user,
                subject = request.POST['subject'],
                title = request.POST['title'],
                description = request.POST['description'],  
                due = request.POST['due'],
                is_finished = finished,
            )
            homeworks.save()
            messages.success(request, f"homework added {request.user.username} successfully")
            form = HomeworkForm()
    else:
        form = HomeworkForm()

    homeworks = Homework.objects.filter(user=request.user)
    context = {
        "homeworks":homeworks,
        "form":form,
    }
    return render(request, "dashboard/homework.html", context)

@login_required(login_url='login')
def update_homework(request, pk=None):
    homework = Homework.objects.get(id=pk)
    if homework.is_finished == True:
        homework.is_finished = False
    else:
        homework.is_finished = True
    homework.save() 
    messages.success(request, f"homework updated  {homework.subject} successfully")
    return redirect("homework")

@login_required(login_url='login')
def delete_homework(request, pk=None):
    homework = Homework.objects.get(id=pk)
    homework.delete()
    return redirect("homework")

@login_required(login_url='login')
def youtube(request):
    if request.method == "POST":
        form = DashboardForm(request.POST)
        text = request.POST['text']
        video = VideosSearch(text, limit = 10)
        result_list = []
        for i in video.result()['result']:
            result_dict = {
                'input':text,
                'title':i['title'],
                'duration':i['duration'],
                'thumbnail':i['thumbnails'][0]['url'],
                'channel':i['channel']['name'],
                'link':i['link'],
                'views': i['viewCount']['short'], 
                'published':i['publishedTime'],
            
            }
            desc = ''
            
            if i.get('descriptionSnippet'):
                for j in i['descriptionSnippet']:
                    desc += j['text']
            result_dict['description'] = desc

            result_list.append(result_dict)
            context = {
                'form':form,   
                'results':result_list
            }
        return render(request, "dashboard/youtube.html", context )
    else:
        form = DashboardForm()
    context = {
        "form":form,
    }
    return render(request, "dashboard/youtube.html" , context)


@login_required(login_url='login')
def todo(request):
    if request.method == "POST":
        form = TodoForm(request.POST)
        if form.is_valid():
            try:
                finished = request.POST['is_finished']
                if finished == "on":
                    finished = True
                else:
                    finished = False
            except:
                finished = False
            todos = Todo(
                user = request.user,
                title = request.POST['title'],
                is_finished = finished
            )
            todos.save()
            messages.success(request, f"todo added {request.user.username} successfully")
            form = TodoForm()
    else:   
        form = TodoForm()

    todo = Todo.objects.filter(user=request.user)
    context = {
        "todos":todo,
        "form":form
    }
    return render(request, "dashboard/todo.html", context)

@login_required(login_url='login')
def update_todo(request, pk):
    todo = Todo.objects.get(id=pk)
    if todo.is_finished == True:
        todo.is_finished = False
    else:
        todo.is_finished = True
    todo.save()
    messages.success(request, f"todo updated  {todo.title} successfully")
    return redirect("todo")

@login_required(login_url='login')
def delete_todo(request, pk=None):
    todo = Todo.objects.get(id=pk)
    todo.delete()
    return redirect("todo")

@login_required(login_url='login')
def books(request):
    if request.method == "POST":
        form = DashboardForm(request.POST)
        text = request.POST['text']
        url = "https://www.googleapis.com/books/v1/volumes?q="+text
        r = requests.get(url)
        answer = r.json()
        result_list = []
        for i in range(10):
            result_dict = {
                'title':answer['items'][i]['volumeInfo']['title'],
                'subtitle':answer['items'][i]['volumeInfo'].get('subtitle'),
                'descrpitions':answer['items'][i]['volumeInfo'].get('description'),       
                'count':answer['items'][i]['volumeInfo'].get('pageCount'),
                'categories':answer['items'][i]['volumeInfo'].get('categories'),
                'rating':answer['items'][i]['volumeInfo'].get('pageRating'),
                'thumbnail':answer['items'][i]['volumeInfo'].get('imageLinks').get('thumbnail'),
                'preview':answer['items'][i]['volumeInfo'].get('previewLink')
            }
            result_list.append(result_dict)
            context = {
                "form":form , 
                "results":result_list
            }
        return render(request, "dashboard/books.html", context )
    else:
        form = DashboardForm()
    context = {
        "form":form
    }
    return render(request, "dashboard/books.html" , context)

@login_required(login_url='login')
def dictinory(request):
    form = DashboardForm()
    if request.method == "POST":
        form = DashboardForm(request.POST)
        text = request.POST['text']
        url = 'https://api.dictionaryapi.dev/api/v2/entries/en_US/' + text
        r = requests.get(url)
        answer = r.json()
        try:
            phonetics = answer[0]['phonetics'][0]['text']
            audio = answer[0]['phonetics'][0]['audio']
            definition = answer[0]['meanings'][0]['definitions'][0]['definition']
            example = answer[0]['meanings'][0]['definitions'][0].get('example', 'No example available')
            synonyms = answer[0]['meanings'][0]['definitions'][0].get('synonyms', [])
            context = {
                'form': form,
                'input': text,
                'phonetics': phonetics,
                'definition': definition,
                "example": example,
                "synonyms": synonyms,
                "audio": audio
            }
        except:
            context = {
                'form': form,
                'input': '',
            }
        return render(request, "dashboard/dictionary.html", context)
    else:
        form = DashboardForm()
    context = {
        "form": form
    }
    return render(request, "dashboard/dictionary.html", context)

@login_required(login_url='login')
def wiki(request):
    if request.method == "POST":
        form = DashboardForm(request.POST)
        text = request.POST['text']
        try:
            search = wikipedia.page(text)
            context = {
                "form": form,
                "title": search.title,
                "link": search.url,
                "details": search.summary
            }
        except Exception as e:
            context = {
                "form": form,
                "error": f"An error occurred: {str(e)}"
            }
        return render(request, "dashboard/wiki.html", context)
            
    else:
        form = DashboardForm()
    context = {
        "form": form
    }
    return render(request, "dashboard/wiki.html", context)


@login_required(login_url='login')
def unit_conversion_view(request):
    result = None  
    form = ConversionForm()  

    if request.method == 'POST': 
        form = ConversionForm(request.POST)  
        if form.is_valid():
            input_value = form.cleaned_data['input_value']
            from_unit = form.cleaned_data['from_unit']
            to_unit = form.cleaned_data['to_unit']
            result = convert_units(input_value, from_unit, to_unit)
          
    return render(request, 'dashboard/conversion.html', {'form': form, 'result': result})



@login_required(login_url='login')
def user_profile(request):
    homewroks = Homework.objects.filter(is_finished=False,user=request.user)    

    todos = Todo.objects.filter(is_finished=False,user=request.user)
    if len(homewroks) == 0:
        homeworks_done = True
    else:
        homeworks_done = False

    if len(todos) == 0:
        todo_done = True
    else:
        todo_done = False

    context = {
        'homeworks':homewroks,
        'todos':todos,
        'homeworks_done':homeworks_done,
        'todo_done':todo_done
    }
    return render(request, 'dashboard/profile.html', context)




