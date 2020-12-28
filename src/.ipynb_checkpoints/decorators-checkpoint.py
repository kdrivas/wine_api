import subprocess as cmd

def commitme(func):
    def wrapper(*args, **kwargs):
        print('Commit experiment ...')
        
        cmd.run("git add .", check=True, shell=True)
        cmd.run("git commit -m 'auto commit - experiment'", check=True, shell=True)
        
        func(*args, **kwargs)
        
    wrapper.unwrapped = func
    return wrapper