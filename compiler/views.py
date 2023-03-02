from django.http import HttpResponse
import os.path,subprocess,json
from subprocess import STDOUT,PIPE
from django.views.decorators.csrf import csrf_exempt


def compile_java(file, foldername):
    path = foldername + "/" + file
    cmd = ['javac', path]
    proc = subprocess.Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
    stdout,stderr = proc.communicate()
    global out
    if proc.returncode != 0:
        print("adding error")        
        out = stdout.decode().strip()
    return proc.returncode

def compile_csharp(file, foldername):
    path = foldername + "/" + file
    cmd = ['mcs' , '-out:' + foldername + '/Solution.exe', path]
    proc = subprocess.Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
    stdout,stderr = proc.communicate()
    global out
    if proc.returncode != 0:
        out = stdout.decode().strip()
    return proc.returncode

def execute_csharp(file, stdin, foldername):
    path = foldername + "/" + file
    cmd = ['runuser', '-l', 'coder', '-c', 'timelimit -t3 -T1 mono ' + path]
    proc = subprocess.Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
    stdout,stderr = proc.communicate(stdin.encode())
    global out
    out = stdout.decode().strip()
    return proc.returncode

def execute_java(java_file, stdin, foldername):
    java_class,ext = os.path.splitext(java_file)
    cmd = ['runuser', '-l', 'coder', '-c', 'timelimit -t3 -T1 java -classpath ' + foldername + '/ Solution']
    proc = subprocess.Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
    stdout,stderr = proc.communicate(stdin.encode())
    global out
    out = stdout.decode().strip()
    return proc.returncode

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
    try:
        subprocess.check_call(['rm', '-r', folder])
    except:
        print("folder doesn't exist")

def generate_compiler_error():
    response = {
       'Error' : True,
       'Error_message' : out
    }
    return HttpResponse(json.dumps(response))

def generate_runtime_error():
    return {
            'Error' : True,
            'Description' : out
            }
def generate_test_result():
    return {
            'Error' : False,
            'Description' : out
            }
    

@csrf_exempt
def index(request):
    data = json.loads(request.body)
    foldername = "/tmp/Solutions/Solution" + str(data["SessionId"])
    lang = data["Language"]
    if lang == "csharp":
        write_file("Solution.cs", data["UserCode"], foldername)
        rc = compile_csharp("Solution.cs", foldername)
        if rc != 0:
            delete_folder(foldername)
            return generate_compiler_error()
    if lang == "java":
        write_file("Solution.java", data["UserCode"], foldername)
        rc = compile_java('Solution.java', foldername)
        if rc != 0:
            delete_folder(foldername)
            return generate_compiler_error()
    testcases = data["TestCases"]
    results=[]
    for testcase in testcases:
        input = testcase["Input"]
        output = testcase["Output"]
        res={}
        if lang == "java":
            rc = execute_java("Solution.java", input, foldername)
            if rc != 0:
                res = generate_runtime_error()
            else:
                res = generate_test_result()
        if lang == "csharp":
            rc = execute_csharp("Solution.exe",input, foldername)
            if rc != 0:
                res = generate_runtime_error()
            else:
                res = generate_test_result()
        results.append(res)
    ret = {
        'Error' : False,
        'Results' : results
        }
    delete_folder(foldername)
    return HttpResponse(json.dumps(ret))
