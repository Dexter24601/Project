import os
import re  # regex

from django.contrib.auth.decorators import login_required
from django.core.files import File
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import RegisterForm
from django.shortcuts import render, redirect
from .models import Student, Class, Image, Attendance, Absence, Date, Traning

from datetime import date


import PIL.Image
from RecognitionSystem.FaceDetection import *
from RecognitionSystem.FaceRecognition import *

import sys
sys.setrecursionlimit(10000)  # to solve the setrecursionlimit error


def DeleteFolderIfExist(Path):
    for filename in os.listdir(Path):
        file_path = os.path.join(Path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


def temp(request):
    return redirect('/Hadir/')


def index(request):
    return render(request, 'HadirApp/index.html')


@login_required(login_url='./login')
def detail(request):
    users = User.objects.all()
    students = Student.objects.all()
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
        else:
            return render(request, './HadirApp/login.html')


@login_required(login_url='./login')
def LogoutUser(request):
    logout(request)
    return redirect('/Hadir/login')


@login_required(login_url='./login')
def mainPage(request):
    return render(request, 'HadirApp/MainPage.html')


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

                messages.success(
                    request, f'Student {st.name} has been added to {classes.class_name} class succesfuly')
                return render(request, 'HadirApp/student_enrollment.html', {'class_name': classes.class_name})

            elif not match:
                wrongID = 'Invalid Student ID!'
                print(wrongID)
                return render(request, 'HadirApp/student_enrollment.html', {'wrongID': wrongID})

            FolderToSave = resource_path('RecognitionSystem/Processing/')

            n = 0
            for image in images:
                X = PIL.Image.open(image)
                X.save(f'{FolderToSave}{n}({st}).jpg')
                n += 1

            # Detect Submitted Faces
            ImgsNames = DetectFaces(
                PostProccessing=True, ImagePath=FolderToSave)

            # If we didn't detect any face -> try with less confidence
            if len(ImgsNames) < 1:
                ImgsNames = DetectFaces(
                    PostProccessing=True, ImagePath=FolderToSave, ConfidenceThreshold=0.64)

            # if we got detection
            if len(ImgsNames) >= 1:
                student = Student.objects.create(
                    name=name, student_id=student_id, profilePic=images[0])
                student.classes.add(classes)

                student.save()
                print(f'student {student} is registered')

                # Import to Database
                for im in ImgsNames:
                    Image.objects.create(
                        student=student, images=(f'Students/{im}'))

                DeleteFolderIfExist(FolderToSave)  # why?
            else:
                print('Didnt detect any faces.')

        except Exception as e:
            print(e)
            return redirect('/Hadir/404')
    return render(request, 'HadirApp/student_enrollment.html', {'class_name': class_name})


# to show all images // (insignificant)
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
        numOfStudents = request.POST['numOfStudents']

        matchName = re.match(r'\D{3,50}', className)
        matchID = re.match(r'\d{3}', classID)

        if not matchName:
            nameErr = 'Invalid Class Name'
            return render(request, 'HadirApp/class_form.html', {'nameErr': nameErr})
        elif not matchID:
            IDErr = 'Invalid Class ID'
            return render(request, 'HadirApp/class_form.html', {'IDErr': IDErr})

        try:
            if Class.objects.filter(class_id=classID).exists():
                idErr = 'A Class with this ID already exsists'
                print(idErr)
                return render(request, 'HadirApp/class_form.html', {'idErr': idErr})

            newClass = Class.objects.create(
                class_id=classID, class_name=className, num_of_students=numOfStudents, instructor=request.user)
            newClass.save()
            succes = (f"Class {className}-{classID} Created Succesfuly")
            print(succes)
            return redirect(f'/Hadir/student_enrollment/{className}-{classID}')
        except:
            print('404 Not Found')
            return redirect('/Hadir/404')
    return render(request, 'HadirApp/class_form.html')


@login_required(login_url='./login')
def Classes(request):
    if Class.objects.filter(instructor=request.user).exists():
        theClasses = []
        try:
            for clas in Class.objects.filter(instructor=request.user):
                if clas.instructor == request.user:
                    theClasses.append(clas)
                    print(clas)
        except:
            if Class.objects.filter(instructor=request.user).instructor == request.user:
                theClasses.append(clas)
        return render(request, 'HadirApp/classes.html', {'theClasses': theClasses})

    else:
        err = "You dont Have Any Classes"
        return render(request, 'HadirApp/classes.html', {'err': err})


@login_required(login_url='/Hadir/login?next=/Hadir/Classes')
def delete(request, class_id, class_name):

    if Class.objects.filter(instructor=request.user).exists():

        try:
            clas = Class.objects.get(class_id=class_id).delete()
            return redirect('/Hadir/Classes')
        except Exception as e:
            print(e)
            return redirect('/Hadir/404')
    else:
        return redirect('/Hadir/404')


@login_required(login_url='/Hadir/login?next=/Hadir/Classes')
def clas(request, class_id, class_name):
    try:
        if Class.objects.filter(class_id=class_id).exists():
            currentClass = Class.objects.get(class_id=class_id)
            students = Student.objects.all()
            classStd = []
            for student in students:
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

    return render(request, 'HadirApp/class.html')


@login_required(login_url='/Hadir/login?next=/Hadir/Classes')
def dashboard(request, class_name, class_id):
    if Class.objects.filter(class_id=class_id, instructor=request.user).exists():
        clas = Class.objects.get(class_id=class_id, instructor=request.user)
        students = Student.objects.filter(classes=clas)
        i = 1
        for student in students:
            i += 1
            print(student)

        # for student in students:
        #     print(student)
        return render(request, 'HadirApp/dashboard.html', {'class_name': class_name, 'class_id': class_id, 'students': students, 'i': i})
    else:
        return redirect('/Hadir/404')


@login_required(login_url='/Hadir/login?next=/Hadir/Classes')
def attendance(request, class_name, class_id):

    if Class.objects.filter(class_id=class_id, instructor=request.user).exists():

        today = date.today()
        currentClass = Class.objects.get(class_id=class_id)
        students = Student.objects.filter(classes=currentClass)

        if request.method == "POST":

            FolderToSave = resource_path('RecognitionSystem/Processing/')
            TakenImages = request.FILES.getlist('Images')
            DeleteFolderIfExist(FolderToSave)

            prestudents = []

            if len(TakenImages) > 0:
                n = 0
                for image in TakenImages:
                    X = PIL.Image.open(image)
                    X.save(f'{FolderToSave}{n}.jpg')
                    n += 1
                DetectFaces(PostProccessing=False, ImagePath=FolderToSave,
                            ConfidenceThreshold=0.65)
                students_ids = Recognize(students)
                print(
                    f'Recognized students: {Student.objects.get(student_id=students_ids[0])}')

                for id in students_ids:
                    if Student.objects.filter(student_id=id, classes=currentClass).exists():
                        prestudents.append(Student.objects.get(student_id=id))

            else:
                studentsNames = request.POST.getlist('student')
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
                print(f'Attandance for: {day}')
                for st in prestudents:
                    day.student.add(st)
                    day.save()
                    print(f'{st} Marked As Present!')

                abcentStudents = [
                    student for student in students if student not in prestudents]

                print("------------------------------")
                for student in abcentStudents:

                    if Date.objects.filter(date=today).exists():
                        DATE = Date.objects.get(date=today)
                        pass
                    else:
                        DATE = Date.objects.create(date=today)

                    if Absence.objects.filter(student=student, clas=currentClass).exists():

                        if Absence.objects.filter(student=student, clas=currentClass, date=DATE).exists():

                            print(
                                f"student {student} is already marked absent")

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
                return redirect('./Results')

        context = {'students': students,
                   'class_name': class_name, 'class_id': class_id}
        return render(request, 'HadirApp/take_attendance.html', context)
    else:
        return redirect('/Hadir/404')


@login_required(login_url='/Hadir/login?next=/Hadir/Classes')
def attendanceResult(request, class_name, class_id):

    try:

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
    except Exception as e:
        print(e)
        return redirect('/Hadir/404')
    return render(request, 'HadirApp/results.html', {'prestudents': prestudents, 'abcentStudents': abcentStudents})


@login_required(login_url='./login')
def traning(request):
    if request.method == "POST":
        images = request.FILES.getlist('images')

        for img in images:
            image = Traning.objects.create(images=(f'Traning/{img}'))
            image.save()
        print('Traning set added succesfuly')
    return render(request, 'HadirApp/Traning.html')


def PageNotFound(request):
    return render(request, 'HadirApp/404.html')
