import subprocess
bash = "git fsck --full"
process = subprocess.Popen(bash.split(), stdout=subprocess.PIPE)
output, error = process.communicate()
output = output.decode("utf8")
output = output.split("dangling blob")

for line in output[1:]:
    hash = line[0:7]
    print("Hash", hash)
    bashCommand = "git cat-file -p "+ hash  
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    code_put, error = process.communicate()

    # text = code_put.decode(errors="ignore")
    with open(f"recovery/{hash}.txt", "wb") as file:
        file.write(code_put)
   

