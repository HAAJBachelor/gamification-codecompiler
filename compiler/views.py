from django.http import HttpResponse
import os.path,subprocess,json
from subprocess import STDOUT,PIPE
from django.views.decorators.csrf import csrf_exempt

def compile_java(java_file):
    subprocess.check_call(['javac', java_file])

def execute_java(java_file, stdin):
    java_class,ext = os.path.splitext(java_file)
    cmd = ['java', java_class]
    proc = subprocess.Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
    stdout,stderr = proc.communicate(stdin.encode())
    return stdout.decode().strip()

def write_file(data):
    if (os.path.exists("Solution.java") == False):
        f = open("Solution.java", "x")
    else:
        f = open("Solution.java", "w+")
    f.write(data)
    f.close()

@csrf_exempt
def index(request):
    data = json.loads(request.body)
    print(data)
    write_file(data["UserCode"])
    compile_java('Solution.java')
    testcases = data["TestCases"]
    results=[]
    for testcase in testcases:
        input = testcase["Input"]
        output = testcase["Output"]
        res=execute_java("Solution", input)
        results.append(res)
    ret = json.dumps(results)
    print(ret)
    return HttpResponse(ret)
