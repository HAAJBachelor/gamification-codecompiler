from django.http import HttpResponse
import os.path,subprocess,json
from subprocess import STDOUT,PIPE
from django.views.decorators.csrf import csrf_exempt

def compile_java(file):
    subprocess.check_call(['javac', file])

def compile_csharp(file):
    print(file)
    subprocess.check_call(['mcs' , '-out:solution.exe', file])

def execute_csharp(file, stdin):
    cmd = ['mono', file]
    proc = subprocess.Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
    stdout,stderr = proc.communicate(stdin.encode())
    return stdout.decode().strip()

def execute_java(java_file, stdin):
    java_class,ext = os.path.splitext(java_file)
    cmd = ['java', java_class]
    proc = subprocess.Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
    stdout,stderr = proc.communicate(stdin.encode())
    return stdout.decode().strip()

def write_file(filename, data):
    if (os.path.exists(filename) == False):
        f = open(filename, "x")
    else:
        f = open(filename, "w+")
    f.write(data)
    f.close()



@csrf_exempt
def index(request):
    data = json.loads(request.body)
    lang = data["Language"]
    if lang == "csharp":
        write_file("solution.cs",data["UserCode"])
        compile_csharp("solution.cs")
    if lang == "java":
        write_file("Solution.java",data["UserCode"])
        compile_java('Solution.java')
    testcases = data["TestCases"]
    results=[]
    for testcase in testcases:
        input = testcase["Input"]
        output = testcase["Output"]
        if lang == "java":
            res=execute_java("Solution", input)
        if lang == "csharp":
            res=execute_csharp("solution.exe",input)
        results.append(res)
    ret = json.dumps(results)
    print(ret)
    return HttpResponse(ret)
