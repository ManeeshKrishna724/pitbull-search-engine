from django.shortcuts import render,redirect
from .models import Search,FreezeHistory
from .scrape import Scrape
from django.core.paginator import Paginator
from .forms import CreateUserForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib.auth.forms import PasswordResetForm
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes

# Create your views here.

def mail(message,recipient_list):
    email = EmailMessage(
    'From PITBULL',
    message,
    settings.EMAIL_HOST_USER,
    recipient_list
    )
    email.fail_silently=False
    email.send()
    """send_mail(
        subject='From PITBULL',
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=recipient_list,
    )"""
    return



def save_search(text,user):
    fh = FreezeHistory.objects.get(user_id=user.id)
    if not fh.freeze_history:
        Search.objects.create(user=user,search=text)
        return


@login_required(login_url='login-page')
def home(response):
    page_home = False
    
    if response.path == '/' or 'search/' in response.path:
        page_home = True

    if response.method == 'POST':
        if 'logout' in response.POST:
            logout(response)
        else:
            searched_text = response.POST.get('search')
            save_search(searched_text,response.user)
            return redirect('search-result',q=searched_text)

    news = Scrape('Trending').news(10)

    return render(response,'google/home.html',{
    'page_home':page_home,
    'news':news,
    })

@login_required(redirect_field_name='login-page')
def search_result(response,q):

    results = Scrape(q).normal_search()
    pg_number = response.GET.get('page')
    pag = Paginator(results,20)
    items = pag.get_page(pg_number)
    as_letter = 'p'*items.paginator.num_pages

    if 'search' in response.POST:
        text = response.POST.get('search')
        save_search(text,response.user)
        return redirect('search-result',text)
        
    
    contexts = {
        'value':q,
        'items':items,
        'letter':as_letter,
    }
    return render(response,'google/search-result.html',contexts)

@login_required(login_url='login-page')
def search_result_image(response,q,page):

    if 'search' in response.POST:
        text = response.POST.get('search')
        save_search(text,response.user)
        return redirect('search-result-img',q=text,page=0)

    items = Scrape(q).img(page)

    if len(str(page)) >= 1 and page !=0:
        page = str(page)+'00'

    
    as_letter = [0,100,200,300,400,500,600,700,800,900,1000]
    



    contexts = {
        'value':q,
        'objects':items,
        'letter':as_letter,
    }
    return render(response,'google/result-image.html',contexts)

@login_required(login_url='login-page')
def view_image(response,q):

    items = response.GET.items()
    jpg = response.GET.get('q')

    if len(response.GET) > 1:
        for k,y in items:
            if k != 'q':
                jpg = jpg+f'&{k}={y}'

    return render(response,'google/view-image.html',{'jpg':jpg})


@login_required(login_url='login-page')
def search_result_news(response,q):

    if 'search' in response.POST:
        text = response.POST.get('search')
        save_search(text,response.user)
        return redirect('search-result-news',text)


    news = Scrape(q).news(100)
    pg_number = response.GET.get('page')
    pag = Paginator(news,10)
    items = pag.get_page(pg_number)
    as_letter = 'p'*items.paginator.num_pages
    contexts = {
        'items':items,
        'value':q,
        'letter':as_letter,
    }


    return render(response,'google/result-news.html',contexts)

@login_required(login_url='login-page')
def search_result_videos(response,q,page):

    if 'search' in response.POST:
        text = response.POST.get('search')
        save_search(text,response.user)
        return redirect('search-result-videos',text,1)

    else:
        videos = Scrape(q).videos(page)
        page_num = response.GET.get('page')
        pag = Paginator(videos,35)
        pag_items = pag.get_page(page_num)
        page_letter = 'p'*10
        page_links = [1,36,71,106,141,176,211,246]

        contexts = {
            'value':q,
            'videos':pag_items,
            'letter':zip(page_letter,page_links)
        }
        return render(response,'google/result-videos.html',contexts)


def register_page(response):
    form = CreateUserForm()
    email_exists_in_db = True
    email_exists = True


    if response.method == 'POST':
        first_name = response.POST.get('username')
        user_email = response.POST.get('email')
        form = CreateUserForm(response.POST)
        password_1 = response.POST.get('password1')
        password_2 = response.POST.get('password2')

        #Checking if the email is already in use.
        if User.objects.filter(email=user_email).exists():
            messages.error(response,'The email you entered is already in use')
            email_exists_in_db = False

               


        if form.is_valid() and email_exists_in_db: 
            try:
                mail(f"Hey {first_name} just wanna say thank you for registering to pitbull.\n\n      -From Owner.",[user_email])
            except:
                email_exists=False
                messages.error(response,"The email you entered is invalid or does'nt exists")
            
            if email_exists:
                user = form.save()
                login(response,user)
                user_ins = User.objects.get(id=user.id)
                FreezeHistory.objects.create(user=user_ins,freeze_history=False)
                messages.success(response,f'Hey {first_name} welcome to PITBULL')
                return redirect('home')

        else:
            try:
                int(password_1)
                messages.error(response,'Password cannot contain only numbers')
            except:
                pass
            #Checking if the password and conformation password matches.

            """The reason why I put this here instead of putiing this with other error checker is because django will 
            automatically look for password mismatch errors so if the form is not valid then this might 
            be the reason so you don't have to put this statement at the top.It will also increase the speed.
            It is the same for whitespace in username error so we will put that here too. Thats why we put the other 
            error checkers above form.is_valid() statement django will not be looking for email already exists or password
            length is less than 8 errors."""

            
            if password_1 != password_2:
                messages.error(response,"The password does'nt match. Make sure you enter the same password on both fields")
            
            elif ' ' in response.POST.get('username'):
                messages.error(response,"You can't have whitespaces in user name replace it with a symbol.")

            elif len(password_1) < 8:
                messages.error(response,'Password should atleast contain 8 characters')
            
            else:
                messages.error(response,"Password can't be similar to username or other personal information")



    contexts = {
        'form':form,
    }
    
    return render(response,'google/register.html',contexts)


def login_page(response):
    if response.method == 'POST':
        username = response.POST.get('username')
        password = response.POST.get('password')

        user = authenticate(response,username=username,password=password)
        if user is not None:
            login(response,user)
            messages.success(response,f"Hey {username} Welcome to PITBULL")
            return redirect('home')
        else:
            messages.error(response,"The username or password you entered is incorrect or does'nt exists try again.")
        
    return render(response,'google/login.html')


@login_required(login_url='login-page')
def settings_page(response):
    return render(response,'google/settings.html')


@login_required(login_url='login-page')
def conformation_page(response,obj):
    

    if response.method == 'POST':
        if 'logout' in response.POST:
            logout(response)
            return redirect('login-page')
        
        elif 'user_password' in response.POST:
            user_id = response.user.id
            user = User.objects.get(id=user_id)
            if user.check_password(response.POST.get('user_password')):
                user.delete()
                return redirect('login-page')


        elif 'conform-clear' in response.POST:
            user_id = response.user.id
            searchs = Search.objects.filter(user_id=user_id)
            if len(searchs) > 0:
                for search in searchs:
                    search.delete()
                messages.success(response,'Succesfully cleared history')
            else:
                messages.error(response,"It seem like you don't have any recent activities ")
            return redirect('search-history')

        elif 'conform-freeze' in response.POST:
            user_id = response.user.id
            fh = FreezeHistory.objects.get(user_id=user_id)
            fh.freeze_history = True
            fh.save()
            messages.success(response,'Successfully freezed history.')
            return redirect('search-history')
        
        elif 'conform-unfreeze' in response.POST:
            user_id = response.user.id
            fh = FreezeHistory.objects.get(user_id=user_id)
            fh.freeze_history = False
            fh.save()
            messages.success(response,'Successfully unfreezed history.')
            return redirect('search-history')


    contexts = {
        'c_mode':obj,
    }
        
    return render(response,'google/conform-page.html',contexts)

def search_history(response):
    
    history_status = FreezeHistory.objects.get(user_id = response.user.id).freeze_history
    if response.method == 'POST':
        search_id = response.POST.items()
        for key,value in search_id:
            if key != 'csrfmiddlewaretoken':
                search_id = key.replace('.x','')
                break
            
        try:
            search = Search.objects.get(id=search_id)
            search.delete()
            return redirect('search-history')
        except:
            pass

    searchs = Search.objects.filter(user_id=response.user.id)
    contexts = {
        'searchs':searchs,
        'history_status':history_status,
    }
    return render(response,'google/search-history.html',contexts)



def password_reset(response):
    
    if response.method == 'POST':
        password_reset_form = PasswordResetForm(response.POST)
        if password_reset_form.is_valid():
            entered_email = response.POST.get('email')
            associated_users = User.objects.filter(email=entered_email)
            if associated_users.exists():

                for user in associated_users:
                    contexts = {
                        "email":user.email,
                        'domain':response.META['HTTP_HOST'],
                        'site_name': 'PITBULL',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    content = render_to_string('change-password/mail-content.txt',contexts)
                    mail(content,[user.email])
                    return redirect('password_reset_done')
            else:
                messages.error(response,"The email you entered does'nt exists")
    password_reset_form = PasswordResetForm()
    return render(response,'change-password/change-password.html',{"form":password_reset_form})                


