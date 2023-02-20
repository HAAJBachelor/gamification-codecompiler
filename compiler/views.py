from django.http import HttpResponse
import os.path,subprocess,json
from subprocess import STDOUT,PIPE
from django.views.decorators.csrf import csrf_exempt

def compile_java(file, foldername):
    path = foldername + "/" + file
    subprocess.check_call(['javac', path])

def compile_csharp(file, foldername):
    path = foldername + "/" + file
    subprocess.check_call(['mcs' , '-out:' + foldername + '/Solution.exe', path])

def execute_csharp(file, stdin, foldername):
    path = foldername + "/" + file
    cmd = ['mono', path]
    proc = subprocess.Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
    stdout,stderr = proc.communicate(stdin.encode())
    return stdout.decode().strip()

def execute_java(java_file, stdin, foldername):
    java_class,ext = os.path.splitext(java_file)
    cmd = ['java', '-classpath', foldername, java_class]
    proc = subprocess.Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
    stdout,stderr = proc.communicate(stdin.encode())
    return stdout.decode().strip()

def write_file(filename, data, foldername):
    path = foldername + "/" + filename
    if (os.path.exists(foldername) == False):
        subprocess.check_call(['mkdir', foldername])
    if (os.path.exists(path) == False):
        f = open(path, "x")
    else:
        f = open(path, "w+")
    f.write(data)
    f.close()

def delete_folder(folder):
    subprocess.check_call(['rm', '-r', folder])
    

@csrf_exempt
def index(request):
    data = json.loads(request.body)
    foldername = "Solution" + str(data["SessionId"])
    lang = data["Language"]
    if lang == "csharp":
        write_file("Solution.cs", data["UserCode"], foldername)
        compile_csharp("Solution.cs", foldername)
    if lang == "java":
        write_file("Solution.java", data["UserCode"], foldername)
        compile_java('Solution.java', foldername)
    testcases = data["TestCases"]
    results=[]
    for testcase in testcases:
        input = testcase["Input"]
        output = testcase["Output"]
        if lang == "java":
            res=execute_java("Solution.java", input, foldername)
        if lang == "csharp":
            res=execute_csharp("Solution.exe",input, foldername)
        results.append(res)
    ret = json.dumps(results)
    print(ret)
    delete_folder(foldername)
    return HttpResponse(ret)
