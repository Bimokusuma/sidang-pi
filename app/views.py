from datetime import datetime, date
from django.utils.timezone import now, localtime
from calendar import month_abbr, monthrange
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, JsonResponse
from .forms import SignUpForm
from django.contrib.auth import login,logout, authenticate, update_session_auth_hash
from .models import Record, DailyQuest, Profile, Feedback
from .forms import RecordForm
import random

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }
    )

def feedback(request):
    if request.method == "POST":
        feed_value = [request.POST.get('q{}'.format(x)) for x in range(1,10)]
        value = ''.join(feed_value)
        print(type(value))
        name = request.POST.get('name')
        email = request.POST.get('email')
        f = Feedback(name=name, email=email, feed_value=value)
        f.save()
        return render(
            request,
            'profile/feedback-thanks.html',
            {
                'title': "Feedback",
                'year':datetime.now().year,
            }
        )
    questions = [
        'Website dapat dikenal fungsinya dari tampilan awal',
        'Kemudahan menemukan navigasi yang akan dituju',
        'Kenyamanan disain ( susunan tampilan, warna, jenis font, dll ) dari aplikasi',
        'Fasilitas yang tersedia, seperti kuis dan profile',
        'Kemudahan untuk mengerti bahasa yang ditampilkan ditiap halaman',
        'Kemudahan mengingat kembali menu-menu dan tampilan yang ada pada website',
        'Kemudahan membaca huruf-huruf',
        'Kemudahan memahami icon',
        'Keharusan melakukan pengembangan website'
    ]
    return render(
        request,
        'profile/feedback.html',
        {
            'title':'Feedback',
            'questions': questions,
            'year':datetime.now().year,
        }
    )
@login_required(login_url='/login/')
def get_feedback(request):
    feed_name = {
        '1': 'Ya',
        '2': 'Tidak',
        '3': 'Tidak tahu',
    }
    feeds = Feedback.objects.all()
    for feed in feeds:
        feed.feed_value = [feed_name[x] for x in list(feed.feed_value)]
    questions = [
        'Website dapat dikenal fungsinya dari tampilan awal',
        'Kemudahan menemukan navigasi yang akan dituju',
        'Kenyamanan disain ( susunan tampilan, warna, jenis font, dll ) dari aplikasi',
        'Fasilitas yang tersedia, seperti kuis dan profile',
        'Kemudahan untuk mengerti bahasa yang ditampilkan ditiap halaman',
        'Kemudahan mengingat kembali menu-menu dan tampilan yang ada pada website',
        'Kemudahan membaca huruf-huruf',
        'Kemudahan memahami icon',
        'Keharusan melakukan pengembangan website'
    ]
    return render(
        request,
        'profile/feedback-list.html',
        {
            'title': 'Feedback',
            'questions': questions,
            'year':datetime.now().year,
            'feeds': feeds,
        }
    )
@login_required(login_url='/login/')
def kuis(request):
    if request.user.is_authenticated:
        quests = DailyQuest.objects.all().filter(user=request.user, complete=False)
    else:
        quests = []
    records = Record.objects.all().filter(date__gte=localtime(now()).date()).order_by('-score')
    if request.method == "POST" and request.is_ajax():
        score = {
            'S':request.POST.get('score'),
            '+': request.POST.get('score_addition'),
            '-': request.POST.get('score_substraction'),
            '*': request.POST.get('score_multiplication'),
            '/': request.POST.get('score_division')
        }
        if request.user.is_authenticated:
            user = request.user
            r = Record(user=user, score=score['S'], score_addition=score['+'],score_substraction=score['-'],score_multiplication=score['*'],score_division=score['/'])
            r.save()

            quests = DailyQuest.objects.all().filter(user=user,complete=False)
            for q in quests:
                if q.quest_type =="A":
                    q.current_progress += int(score[q.quest_target_type])
                else:
                    q.current_progress = int(score[q.quest_target_type])
                q.save()
            return JsonResponse({'name':user.username}, status=200)
        else:
            r = Record(user=None, score=score['S'], score_addition=score['+'],score_substraction=score['-'],score_multiplication=score['*'],score_division=score['/'])
            r.save()
            return JsonResponse({'name':'Anonymous'}, status=200)

    return render(
        request,
        'app/kuis.html',
        {
            'title':"Kuis",
            'quests': quests,
            'records':records,
            'year':datetime.now().year
        }
    )

@login_required(login_url='/login/')
def profile(request):
    if request.method == "POST" and request.is_ajax():
        quest_id = request.POST.get('quest_id')
        quest = DailyQuest.objects.get(pk=quest_id)

        #Give user reward here
        user = request.user
        exp_reward = quest.reward
        user.profile.exp += exp_reward
        user.profile.calculate_level()
        user.profile.save()

        quest.complete = True
        quest.save()

        response = {
            'exp': exp_reward,
            'level': user.profile.level,
            'exp_needed': user.profile.exp_to_next_level(),
            'exp_progress': user.profile.get_exp_percentage()
        }
        return JsonResponse(response, status=200)

    profile = Profile.objects.get(user=request.user)
    daily_quests = DailyQuest.objects.all().filter(user=request.user, date__gte=datetime.now())
    #active quests
    quests = daily_quests.filter(complete=False)
    records = Record.objects.all().filter(user=request.user).order_by('-date')

    #check if daily quest is given or not
    if len(daily_quests) == 0:
        quest1 = DailyQuest(user=request.user, quest_name="Selesaikan 100 soal", quest_target=100, quest_target_type="S", quest_type="A", reward=50)
        q_target = random.randint(2,3) * 5
        q_target_type = random.choice(("+","-","*","/"))
        reward = q_target * 3
        q_name="Kerjakan {} soal ({}) dalam sekali kuis".format(q_target, q_target_type)
        quest2 = DailyQuest(user=request.user, quest_name=q_name, quest_target=q_target, quest_target_type=q_target_type, quest_type="B",reward=reward)
        quest1.save()
        quest2.save()

    #init date
    c_year = datetime.now().year #current year
    c_month = int(datetime.now().strftime('%m')) #current Month

    m_range = monthrange(c_year, c_month)

    months = [month_abbr[i] for i in range(1,13)]
    n_years = [int(r.date.strftime("%Y")) for r in records]
    years = list(set(n_years))
    obj = {
        'title':"Profile",
        'months':months,
        'hiscore':'N/A',
        'loscore':'N/A',
        'avgscore':'N/A',
        'years': years,
        'c_year':c_year,
        'c_month':c_month,
        'quests': [],
    }

    if len(records) > 0:
        scores = [x.score for x in records]
        data_stat = [
            sum([x.score_addition for x in records]),
            sum([x.score_substraction for x in records]),
            sum([x.score_multiplication for x in records]),
            sum([x.score_division for x in records])
        ]

        data_records = {}
        for i in range(m_range[1]):
            data_records[i+1] = []
        data_records_label = []
        data_records_data = []

        for r in records.filter(date__gte='{}-{}-1'.format(c_year, c_month), date__lt='{}-{}-1'.format(c_year,c_month+1)):
            r_day = int(r.date.strftime("%d"))
            data_records[r_day].append(r.score)

        for i,v in data_records.items():
            data_records_label.append(int(i))
            if len(v) > 0:
                data_records_data.append(round(sum(v)/len(v), 2))
            else:
                data_records_data.append(0);

        obj['records'] = records[:5]
        obj['hiscore'] = max(scores)
        obj['loscore'] = min(scores)
        obj['avgscore'] = round(sum(scores)/len(scores),2)
        obj['data_stat'] = data_stat
        obj['data_records_label'] = data_records_label
        obj['data_records_data'] = data_records_data

    if len(quests) > 0:
        obj['quests'] = quests
    return render(
        request,
        'profile/index.html',
        obj
    )

def get_data(request):
    if request.method == "GET" and request.is_ajax():
        c_year = int(request.GET.get('year'))
        c_month = int(request.GET.get('month'))
        m_range = monthrange(c_year, c_month)

        data_records_label = []
        data_records_data = []
        data_records = {}
        for i in range(m_range[1]):
            data_records[i+1] = []

        records = Record.objects.all().filter(user=request.user).order_by('date')

        for r in records.filter(date__gte='{}-{}-1'.format(c_year, c_month), date__lt='{}-{}-1'.format(c_year,c_month+1)):
            r_day = int(r.date.strftime("%d"))
            data_records[r_day].append(r.score)

        for i,v in data_records.items():
            data_records_label.append(int(i))
            if len(v) > 0:
                data_records_data.append(round(sum(v)/len(v), 2))
            else:
                data_records_data.append(0);

        response = {
            'data': data_records_data,
            'label': data_records_label
        }

    return JsonResponse(response)

def logout_view(request):
    logout(request)
    return redirect('home')

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            # load the profile instance created by the signal
            user.save()
            raw_password = form.cleaned_data.get('password1')

            # login user after signing up
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)

            # redirect user to home page
            return redirect('profile')
    else:
        form = SignUpForm()
    return render(request, 'auth/signup.html', {'form': form})
