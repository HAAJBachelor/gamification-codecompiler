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
    write_file(data["value"])
    compile_java('Solution.java')
    tasks = data["task"]["tasks"]
    results=[]
    for task in tasks:
        input = task["input"]
        output = task["output"]
        res=execute_java("Solution", input)
        if(res == output):
            results.append("Correct")
        else:
            results.append("Wrong, got {}, expected {}.".format(res, output))
    ret = json.dumps(results)
    return HttpResponse(ret)
