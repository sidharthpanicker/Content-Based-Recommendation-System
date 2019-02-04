# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment, MouseClicks, userLoginInfo
from .forms import PostForm, CommentForm
from django.utils import timezone
import json
import os.path
from django.http import JsonResponse
from datetime import datetime
from datetime import timedelta
from django.core import serializers
from django.db.models import Count
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
import csv
from subprocess import Popen, PIPE, STDOUT
import nltk
from nltk import word_tokenize, pos_tag
from nltk.collocations import *
from itertools import *
from nltk.util import ngrams
from nltk.corpus import stopwords

import sys

reload(sys)
sys.setdefaultencoding('utf8')


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return viewUserProfile(request)
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


def viewPosts(request):
    posts = Post.objects.all()
    comments = Comment.objects.all()
    return render(request, 'viewPosts.html', {'posts': posts, 'comments': comments})


def getQueryRecommendation(request):
    print("In getQueryRecommendation")
    dictionar = {
        '1': """"One way to implement deep copy is to add copy constructors to each associated class. A copy constructor takes an instance of 'this' as its single argument and copies all the values from it. Quite some work, but pretty straightforward and safe. EDIT: note that you don't need to use accessor methods to read fields. You can access all fields directly because the source instance is always of the same type as the instance with the copy constructor. Obvious but might be overlooked. Example: Edit: Note that when using copy constructors you need to know the runtime type of the object you are copying. With the above approach you cannot easily copy a mixed list (you might be able to do it with some reflection code).public class Order {private long number;public Order() {}/** * Copy constructor */public Order(Order source) {number = source.number;}}public class Customer {private String name;private List< Order > orders = new ArrayList< Order >();public Customer() {}/** * Copy constructor */public Customer(Customer source) {name = source.name;for (Order sourceOrder : source.orders) {orders.add(new Order(sourceOrder));}}public String getName() {return name;}public void setName(String name) {this.name = name;}}""",
        '2': """I was presented with this question in an end of module open book exam today and found myself lost. i was reading Head first Javaand both definitions seemed to be exactly the same. i was just wondering what the MAIN difference was for my own piece of mind. i know there are a number of similar questions to this but, none i have seen which provide a definitive answer.Thanks, Darren""",
        '3': """Inheritance is when a 'class' derives from an existing 'class'.So if you have a Person class, then you have a Student class that extends Person, Student inherits all the things that Person has.There are some details around the access modifiers you put on the fields/methods in Person, but that's the basic idea.For example, if you have a private field on Person, Student won't see it because its private, and private fields are not visible to subclasses.Polymorphism deals with how the program decides which methods it should use, depending on what type of thing it has.If you have a Person, which has a read method, and you have a Student which extends Person, which has its own implementation of read, which method gets called is determined for you by the runtime, depending if you have a Person or a Student.It gets a bit tricky, but if you do something likePerson p = new Student();p.read();the read method on Student gets called.Thats the polymorphism in action.You can do that assignment because a Student is a Person, but the runtime is smart enough to know that the actual type of p is Student.Note that details differ among languages.You can do inheritance in javascript for example, but its completely different than the way it works in Java.""",
        '4': """Polymorphism: The ability to treat objects of different types in a similar manner.Example: Giraffe and Crocodile are both Animals, and animals can Move.If you have an instance of an Animal then you can call Move without knowing or caring what type of animal it is.Inheritance: This is one way of achieving both Polymorphism and code reuse at the same time.Other forms of polymorphism:There are other way of achieving polymorphism, such as interfaces, which provide only polymorphism but no code reuse (sometimes the code is quite different, such as Move for a Snake would be quite different from Move for a Dog, in which case an Interface would be the better polymorphic choice in this case.In other dynamic languages polymorphism can be achieved with Duck Typing, which is the classes don't even need to share the same base class or interface, they just need a method with the same name.Or even more dynamic like Javascript, you don't even need classes at all, just an object with the same method name can be used polymorphically.""",
        '5': """I found out that the above piece of code is perfectly legal in Java. I have the following questions. ThanksAdded one more question regarding Abstract method classes.public class TestClass{public static void main(String[] args) {TestClass t = new TestClass();}private static void testMethod(){abstract class TestMethod{int a;int b;int c;abstract void implementMe();}class DummyClass extends TestMethod{void implementMe(){}}DummyClass dummy = new DummyClass();}}""",
        '6': """n java it's a bit difficult to implement a deep object copy function. What steps you take to ensure the original object and the cloned one share no reference? public class TestClass{public static void main(String[] args) {TestClass t = new TestClass();}private static void testMethod(){abstract class TestMethod{int a;int b;int c;abstract void implementMe();}class DummyClass extends TestMethod{void implementMe(){}}DummyClass dummy = new DummyClass();}}""",
        '7': """You can make a deep copy serialization without creating some files. Copy: Restore: ByteArrayOutputStream bos = new ByteArrayOutputStream();ObjectOutputStream oos = new ObjectOutputStream(bos);oos.writeObject(object);oos.flush();oos.close();bos.close();byte[] byteData = bos.toByteArray();; ByteArrayInputStream bais = new ByteArrayInputStream(byteData);(Object) object = (Object) new ObjectInputStream(bais).readObject();""",
        '8': """Java has the ability to create classes at runtime. These classes are known as Synthetic Classes or Dynamic Proxies. See for more information. Other open-source libraries, such as and also allow you to generate synthetic classes, and are more powerful than the libraries provided with the JRE. Synthetic classes are used by AOP (Aspect Oriented Programming) libraries such as Spring AOP and AspectJ, as well as ORM libraries such as Hibernate.""",
        '9': """In short: the web server issues a unique identifier to on his visit. The visitor must bring back that ID for him to be recognised next time around. This identifier also allows the server to properly segregate objects owned by one session against that of another. If is: If is: Once he's on the service mode and on the groove, the servlet will work on the requests from all other clients.Why isn't it a good idea to have one instance per client? Think about this: Will you hire one pizza guy for every order that came? Do that and you'd be out of business in no time. It comes with a small risk though. Remember: this single guy holds all the order information in his pocket: so if you're not cautious about, he may end up giving the wrong order to a certain client.""",
        '10': """A safe way is to serialize the object, then deserialize.This ensures everything is a brand new reference.about how to do this efficiently. Caveats: It's possible for classes to override serialization such that new instances are created, e.g. for singletons.Also this of course doesn't work if your classes aren't Serializable."""
    }
    outputDict = {}
    if request.method == "POST":
        data = request.POST[u'query']
        if data in dictionar:
            m = dictionar[data]
        else:
            m = str(data)
        s_corpus = m.lower()
        stop_words = set(stopwords.words('english'))
        tokens = nltk.word_tokenize(s_corpus)
        tokens = [word for word in tokens if word not in stop_words]
        c_tokens = [''.join(e for e in string if e.isalnum())
                    for string in tokens]
        c_tokens = [x for x in c_tokens if x]
        query = ' '.join(c_tokens)
        p = Popen(['java', '-jar', 'lu1.jar', query],
                  stdout=PIPE, stderr=STDOUT)
        flag = False
        fileArray = []
        for line in p.stdout:
            if "Found 10 hits" in str(line):
                flag = True
                # print(line)
            elif flag == True:
                tmp = line.split('.')[1].strip()
                # print(len(tmp))
                fileArray.append(tmp)
            else:
                print(line)
                continue
        print fileArray
        counter = 0
        for i in fileArray:
            filepath = "Website/" + i + ".txt"
            with open(filepath) as f:
                content = f.readlines()
                outputDict[counter] = {"topic": i, "content": content}
                counter += 1
        # print outputDict
    return HttpResponse(json.dumps(outputDict))
