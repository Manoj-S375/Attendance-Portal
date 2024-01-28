from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Login, Detail,Attend
from django.db import IntegrityError, OperationalError, connection 
from datetime import datetime

uid = 0
cnt = 0
def login(request):
    logins = Login.objects.using('default').all()
    ids =[]
    pasw = []
    for i in logins:
        ids.append(i.uid)
        pasw.append(i.password)
    
    if request.method == 'POST':
        userid = request.POST['name']
        global uid
        global cnt
        cnt += 1
        if(cnt > 1):
            uid = 0
        uid += int(userid)
        pard = request.POST['pass']
        if(uid in ids):
            inx = ids.index(uid)
            if(pard == pasw[inx]):
                if(uid != 501):
                    return(redirect(details))
                else:
                    return(redirect(attend))
            else:
                msg = "Invalid username/password"
                uid = 0
                mess = {
                    'messages' : msg
                }
                return render(request, 'login.html', mess)
        else:
            msg = "Invalid username/password"
            uid = 0
            mess = {
                    'messages' : msg
            }
            return render(request, 'login.html', mess)
                
    return render(request, 'login.html',)

def details(request):
    details = Detail.objects.using('default').all()
    parm = {
        'check' : uid,
        'ptr' : details,
    }
    return render(request, 'details.html',parm)

def attend(request):
    mes = ""
    ch = 0
    if request.method == "POST":
        try:
            roll = request.POST['rno']
            subject = request.POST['sub'] 
            atdate = request.POST['dt']
            attends = Attend()

            attends.regno = roll
            attends.subj = subject
            attends.adate = atdate

            attends.save()

        except IntegrityError:
            mes +=  "You have already marked attendance for this subject on this day"
            ch += 1
    
        except OperationalError:
            mes +=  "The specified date is invalid"
            ch += 1
    
        if(ch == 0):
            mes += "Attendance marked successfully"

    mess = {
        'messages' : mes,
    }

    return render(request, 'attend.html',mess)

def seeatt(request):
    with connection.cursor() as cursor:
        cursor.execute("select count(regno) from attend where subj = 'DS' and regno = %s;", [str(uid)])
        a = cursor.fetchone()

    with connection.cursor() as cursor1:
        cursor1.execute("select count(regno) from attend where subj = 'DB' and regno = %s;", [str(uid)])
        a1 = cursor1.fetchone()

    with connection.cursor() as cursor2:
        cursor2.execute("select count(regno) from attend where subj = 'OS' and regno = %s;", [str(uid)])
        a2 = cursor2.fetchone()

    with connection.cursor() as cursor3:
        cursor3.execute("select count(regno) from attend where subj = 'CA' and regno = %s;", [str(uid)])
        a3 = cursor3.fetchone()

    with connection.cursor() as cursor4:
        cursor4.execute("select count(regno) from attend where subj = 'SE' and regno = %s;", [str(uid)])
        a4 = cursor4.fetchone()

    with connection.cursor() as cursor5:
        cursor5.execute("select count(regno) from attend where subj = 'FL' and regno = %s;", [str(uid)])
        a5 = cursor5.fetchone()
    pdate = []
    if request.method == 'POST':
        csub = request.POST['sub']
        with connection.cursor() as cursor6:
            cursor6.execute("select adate from attend where subj = %s and regno = %s;", [csub,str(uid)])
            a6 = cursor6.fetchall()
            for i in a6:
                for j in i:
                    pdate.append(j)
    
    num = {
        'reg' : uid,
        'dsa' : a[0],
        'dbms' : a1[0],
        'os' : a2[0],
        'ca' : a3[0],
        'se' : a4[0],
        'fl' : a5[0],
        'dt' : pdate,
    }
    return(render(request, 'attendance.html', num))

def sumy(request):
    if request.method == 'POST':
        std = request.POST['reg']
        with connection.cursor() as cursor:
            cursor.execute("select count(regno) from attend where subj = 'DS' and regno = %s;", [str(std)])
            a = cursor.fetchone()

        with connection.cursor() as cursor1:
            cursor1.execute("select count(regno) from attend where subj = 'DB' and regno = %s;", [str(std)])
            a1 = cursor1.fetchone()

        with connection.cursor() as cursor2:
            cursor2.execute("select count(regno) from attend where subj = 'OS' and regno = %s;", [str(std)])
            a2 = cursor2.fetchone()

        with connection.cursor() as cursor3:
            cursor3.execute("select count(regno) from attend where subj = 'CA' and regno = %s;", [str(std)])
            a3 = cursor3.fetchone()

        with connection.cursor() as cursor4:
            cursor4.execute("select count(regno) from attend where subj = 'SE' and regno = %s;", [str(std)])
            a4 = cursor4.fetchone()

        with connection.cursor() as cursor5:
            cursor5.execute("select count(regno) from attend where subj = 'FL' and regno = %s;", [str(std)])
            a5 = cursor5.fetchone()
        num = {
            'signal': 'True',
            'dsa' : a[0],
            'dbms' : a1[0],
            'os' : a2[0],
            'ca' : a3[0],
            'se' : a4[0],
            'fl' : a5[0],
        }
        return(render(request,'summary.html',num))
    return(render(request,'summary.html'))