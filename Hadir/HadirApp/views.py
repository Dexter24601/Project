import re  # regex
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import RegisterForm
from django.urls import reverse
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Student, Class, Image, Attendance, Absence, Date

from datetime import date

import sys
sys.setrecursionlimit(10000)


def temp(request):
    return redirect('/Hadir/')


def index(request):
    # username = User.username
    # template = loader.get_template('HadirApp/index.html')
    # context = RequestContext(request, {
    #     'username': username,
    # })
    # # Because Context() is deprecated in django 1.11  .
    # context_dict = context.flatten()
    # return HttpResponse(template.render(context_dict))
    # latest_users = User.objects.order_by('-reg_date')[:5]
    # output = ", ".join(q.username for q in latest_users)
    # return HttpResponse(output)
    return render(request, 'HadirApp/index.html')


@login_required(login_url='./login')
def detail(request):
    users = User.objects.all()
    students = Student.objects.all()
    # images = Image.objects.all()
    classes = Class.objects.all()
    context = {'users': users, 'students': students, 'classes': classes}
    return render(request, 'HadirApp/detail.html', context)


def registerPage(request):

    if request.user.is_authenticated:
        return redirect('/Hadir/main')
    else:
        if request.method == 'POST':
            form = RegisterForm(request.POST)
            if form.is_valid():
                if User.objects.filter(email=request.POST['email']).exists():

                    err = (f'A user with this Email already exist!')
                    # exist = authenticate(user)
                    return render(request, 'HadirApp/register.html', {'err': err, 'form': form})
                else:
                    form.save()
                    user = form.save()
                    login(request, user)

                    return redirect('/Hadir/main')
                    # return render(request, 'HadirApp/MainPage.html', {'user': user})

            elif request.POST['password1'] != request.POST['password2']:
                err = (f'Passwords Doesnt Match!')
                return render(request, 'HadirApp/register.html', {'err2': err, 'form': form})

        else:
            print(request.method)
            form = RegisterForm()
            user = None
        return render(request, 'HadirApp/register.html', {'form': form})

    '''
    if request.method == 'POST':
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']  # Regex later !!!!!!
        password2 = request.POST['password2']
        # user_id = request.POST['user_id']

        try:
            if User.objects.filter(email=email).exists():
                err = (f'A user with this Email already exist!')
                return render(request, 'HadirApp/register.html', {'err': err, })

            elif password != password2:
                err = (f'Passwords Doesnt Match!')
                return render(request, 'HadirApp/register.html', {'err2': err, })

            user = User.objects.create(
                email=email, username=username, password=password,)
            user.save()
            print(f' User "{user}" created')
            # return redirect(f'/{username}/welcomeBack')
            return redirect(f'/Hadir/main')
        except:
            print("ERROR")
            return redirect('/404')

    context = {
        'err':err,
    }
    return render(request, 'HadirApp/sign-up.html', {'form': form})
    '''


def loginPage(request):  # redirect to the page user was on

    if request.user.is_authenticated:
        return redirect('/Hadir/main')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            logPassword = request.POST.get('password')
            # rawPass = logPassword.clear

            user = authenticate(request, username=username,
                                password=logPassword)
            if user is not None:
                login(request, user)
                print(f'User {user} has logged in succesfuly')
                # return render(request, 'HadirApp/MainPage.html', {'user': user})
                return redirect('/Hadir/main')
            else:
                Err = ('Email/Password is Invalid')
                return render(request, './HadirApp/login.html', {'Err': Err})

            # old way
            '''
        if User.objects.filter(password=logPassword, email=logEmail).exists():
            user = User.objects.get(password=logPassword, email=logEmail)
            user.save()
            print(f'welcome back {user}')
            if user is not None:
                login(request, user)
            # login(request, user)
            # return redirect(f'/{user.username}/welcomeBack')
            return render(request, 'HadirApp/MainPage.html', {'user': user})
        elif User.objects.filter(email=logEmail).exists():
            passErr = ('Password is Invalid')
            return render(request, 'HadirApp/login.html', {'passErr': passErr, })

        else:
            emailErr = ('Email is Invalid')
            return render(request, 'HadirApp/login.html', {'emailErr': emailErr, })
        '''
            '''
            if Instructor.objects.get(email=logEmail):
                if Instructor.objects.get(password=logPassword):

                    print(f'welcome back {user}')
                    redirect(f'/{user.username}/welcomeBack')
                else:
                    redirect('/404')
                    print('Wrong Password')
            else:
                redirect('/404')
                print("Email Doesnt Exsist")
            except:
            '''
        else:
            return render(request, './HadirApp/login.html',)


@login_required(login_url='./login')
def LogoutUser(request):
    logout(request)
    # return render(request, 'HadirApp/login.html')
    return redirect('/Hadir/login')


@login_required(login_url='./login')
def mainPage(request):

    # if request.method == "POST":
    # if user is not None:
    #     currentUser = user
    # {'currentUser': currentUser}
    return render(request, 'HadirApp/MainPage.html')
    # else:
    #     print(request.method)
    #     return redirect('/Hadir/login')


@login_required(login_url='/Hadir/Classes/login')
def student_enrollment(request, class_name, class_id):

    if request.method == 'POST':
        name = request.POST['name']
        student_id = request.POST['student_id']
        images = request.FILES.getlist('images')
        if Class.objects.filter(class_id=class_id).exists:
            classes = Class.objects.get(class_id=class_id)
            print(classes)
        else:
            print('404 Class Not Found')
            return redirect('/Hadir/404')

        match = re.match(r'^(4)(\d{2}0\d{4})$', student_id)

        try:
            if Student.objects.filter(student_id=student_id).exists():
                st = Student.objects.get(student_id=student_id)
                print(st.classes.all())

                for clas in st.classes.all():
                    if clas == classes:
                        idErr = 'A Student with this ID already exsist in this class'
                        print(idErr)
                        return render(request, 'HadirApp/student_enrollment.html', {'idErr': idErr})

                st.classes.add(classes)
                st.save()

                # succMsg = (f'Student {st.name} has been added to {classes.class_name} class succesfuly')
                # print(succMsg)

                messages.success(
                    request, f'Student {st.name} has been added to {classes.class_name} class succesfuly')
                # 'succMsg':succMsg
                return render(request, 'HadirApp/student_enrollment.html', {'class_name': classes.class_name})

            elif not match:
                wrongID = 'Invalid Student ID!'
                print(wrongID)
                return render(request, 'HadirApp/student_enrollment.html', {'wrongID': wrongID})
                # see the vid https://www.youtube.com/watch?v=f3iytAmzuNQ&t=298s

            student = Student.objects.create(
                name=name, student_id=student_id)  # classes=classes

            print('alive!')
            student.classes.add(classes)  # solution for many to many
            student.save()
            print(f'student {student} is registered')

            for image in images:
                # print(image)
                # print(student.student_id)
                Image.objects.create(images=image, student=student)
            images = Image.objects.all()
        except:
            print('404 Not Found')
            return redirect('/Hadir/404')

    return render(request, 'HadirApp/student_enrollment.html', {'class_name': class_name})


def upload(request):
    if request.method == "POST":
        images = request.FILES.getlist('images')
        for image in images:
            User.objects.create(images=image)
    images = User.objects.all()
    return render(request, 'index.html', {'images': images})


@login_required(login_url='./login')
def images(request):
    image = Image.objects.all()
    for img in image:
        print(img)
    return render(request, 'HadirApp/images.html', {'image': image})


@login_required(login_url='./login')
def create_class(request):

    if request.method == 'POST':
        classID = request.POST['classID']
        className = request.POST['className']
        # numOfStudents = request.POST['numOfStudents']

        matchName = re.match(r'\D{3,50}', className)
        matchID = re.match(r'\d{3}', classID)

        if not matchName:
            nameErr = 'Invalid Class Name'
            return render(request, 'HadirApp/class_form.html', {'nameErr': nameErr})
        elif not matchID:
            IDErr = 'Invalid Class ID'
            return render(request, 'HadirApp/class_form.html', {'IDErr': IDErr})

        try:
            # num_of_students=numOfStudents
            if Class.objects.filter(class_id=classID).exists():
                idErr = 'A Class with this ID already exsists'
                print(idErr)
                return render(request, 'HadirApp/class_form.html', {'idErr': idErr})

            newClass = Class.objects.create(
                class_id=classID, class_name=className, instructor=request.user)
            newClass.save()
            succes = (f"Class {className}-{classID} Created Succesfuly")
            print(succes)
            return redirect(f'/Hadir/student_enrollment/{className}-{classID}')
        except:
            print('404 Not Found')
            return redirect('/Hadir/404')
    # qrimg = qrcode.make('secID')
    return render(request, 'HadirApp/class_form.html')


@login_required(login_url='./login')
def Classes(request):
    # print(request.user)
    if Class.objects.filter(instructor=request.user).exists():
        theClasses = []
        try:
            for clas in Class.objects.filter(instructor=request.user):
                # print(clas)
                if clas.instructor == request.user:
                    theClasses.append(clas)
                    print('class found')
        except:
            if Class.objects.filter(instructor=request.user).instructor == request.user:
                theClasses.append(clas)

        return render(request, 'HadirApp/classes.html', {'theClasses': theClasses})

    else:
        err = "You dont Have Any Classes"
        return render(request, 'HadirApp/classes.html', {'err': err})


@login_required(login_url='/Hadir/login?next=/Hadir/Classes')
def dashboard(request, class_name, class_id):
    students = []
    # for student in Student.objects.all():
    #     st
    return render(request, 'HadirApp/dashboard.html', {'class_name': class_name})


@login_required(login_url='/Hadir/login?next=/Hadir/Classes')
def clas(request, class_id, class_name):

    try:
        if Class.objects.filter(class_id=class_id).exists():
            currentClass = Class.objects.get(class_id=class_id)
            students = Student.objects.all()
            classStd = []
            for student in students:
                # print(
                #     f'student === {student},,,, classes === {student.classes.all()}')
                for clas in student.classes.all():
                    if clas == currentClass:
                        classStd.append(student)
                        # classStd.save()

            if not classStd:
                print('no student in this class')

            print(classStd)

            return render(request, 'HadirApp/class.html', {'classStd': classStd, 'currentClass': currentClass})
        else:
            print('class 404 Not Found')
            return redirect('/Hadir/404')
            # here
    except:
        print('404 Not Found')
        return redirect('/Hadir/404')

    return render(request, 'HadirApp/class.html')  # , {'classStd': classStd}


@login_required(login_url='/Hadir/login?next=/Hadir/Classes')
def attendance(request, class_name, class_id):

    today = date.today()
    currentClass = Class.objects.get(class_id=class_id)

    students = Student.objects.filter(
        classes=currentClass)  # all student in the class

    # print(request.method)
    # print(Attendance.objects.all())
    if request.method == "POST":
        studentsNames = request.POST.getlist('student')
        #  Student.objects.filter(id=)
        prestudents = []    # present student in the class
        for name in studentsNames:
            prestudents.append(Student.objects.get(name=name))
        print('')
        print(f'Date: {today}')
        print("------------------------------")
        print(f'class: {currentClass} ')
        print("------------------------------")

        if Attendance.objects.filter(presence_date=today, clas=currentClass).exists():
            print("Exist (Attendance is Already took)")
            day = Attendance.objects.get(
                presence_date=today, clas=currentClass)

            # Absence.objects.filter(info=day, student=name)

            print(f'Attandance for: {day}')
            for st in prestudents:

                # st.student_absence.add(1)
                day.student.add(st)
                day.save()
                print(f'{st} Marked As Present!')

            abcentStudents = [
                student for student in students if student not in prestudents]

            """for student in abcentStudents:


                # student = Student.objects.get(name=student)
                if Absence.objects.filter(info=day, student=student).exists():

                    print(f"student {student} is already marked absent")
                    pass

                    # name.add(student)
                    # name.save()
                elif Absence.objects.filter(info=day).exists():
                    absence = Absence.objects.get(info=day)
                    absence.student.add(student)
                    print(f" Student {student} is Absent")
                else:
                    absence = Absence.objects.create(
                        info=day)
                    absence.student.add(student)
                    absence.save()
                    print(f"created: {absence}")
                    print(f" Student {student} is Absent")
                    # student.student_absence += 1
                    # student.save()

                absenceCounter = Student.objects.get(name=student)
                absenceCounter.student_absence = +1
                print(absenceCounter.student_absence) """
            print("------------------------------")
            for student in abcentStudents:

                if Date.objects.filter(date=today).exists():
                    DATE = Date.objects.get(date=today)
                    pass
                else:
                    DATE = Date.objects.create(date=today)

                if Absence.objects.filter(student=student, clas=currentClass).exists():

                    if Absence.objects.filter(student=student, clas=currentClass, date=DATE).exists():

                        print(f"student {student} is already marked absent")

                    else:
                        absent = Absence.objects.get(
                            student=student, clas=currentClass)
                        absent.save()
                        absent.counter += 1
                        absent.date.add(DATE)
                        absent.save()
                        print(f" Student {student} is Abcent")
                else:
                    absent = Absence.objects.create(
                        student=student, clas=currentClass)
                    absent.counter += 1
                    absent.date.add(DATE)
                    absent.save()
                    print(f" Student {student} is Abcent")
            return redirect('./Results')

        else:
            day = Attendance.objects.create(
                presence_date=today, clas=currentClass)
            day.save()
            print(f'{day} CREATED!')

            for st in prestudents:

                day.student.add(st)
                day.save()
                print(f'{st} Marked As Present!')

            abcentStudents = [
                student for student in students if student not in prestudents]

            for student in abcentStudents:
                print(f" Student {student} is Abcent")
                if Absence.objects.filter(student=student, clas=currentClass).exists():
                    absent = Absence.objects.get(
                        student=student, clas=currentClass)
                    absent.counter = + 1
                    absent.save()
                else:
                    absent = Absence.objects.create(
                        student=student, clas=currentClass)
                    absent.counter = + 1
                    absent.save()
                # student.student_absence += 1
                # student.save()

            return redirect('./Results')

    context = {'students': students,
               'class_name': class_name, 'class_id': class_id}
    return render(request, 'HadirApp/take_attendance.html', context)


@login_required(login_url='/Hadir/login?next=/Hadir/Classes')
def attendanceResult(request, class_name, class_id):

    today = date.today()
    # to get all present students today
    day = Attendance.objects.filter(presence_date=today)
    for st in day:
        prestudents = st.student.all()
    # print(f' students: {prestudents}')

    currentClass = Class.objects.get(class_id=class_id)
    students = Student.objects.filter(
        classes=currentClass)
    abcentStudents = [
        student for student in students if student not in prestudents]

    return render(request, 'HadirApp/results.html', {'prestudents': prestudents, 'abcentStudents': abcentStudents})
    # old way

    # template = loader.get_template('HadirApp/welcome.html')
    # context = RequestContext(request, {

    #     'latest_users': latest_users,
    # })
    # context_dict = context.flatten()
    # return HttpResponse(template.render(context_dict))

    # def absent(request, student_id):
    #     student = get_object_or_404(Student, pk=student_id)


def PageNotFound(request):
    return render(request, 'HadirApp/404.html')
