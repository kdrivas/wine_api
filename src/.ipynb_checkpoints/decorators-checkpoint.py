import subprocess as cmd

def commitme(func):
    def wrapper(*args, **kwargs):
        print('Commit experiment ...')
        try:
            cmd.run("git add .", check=True)
            cmd.run("git commit -m 'auto commit - experiment'", check=True)
        except:
            print('Everything update')
            
        func(*args, **kwargs)
        
    wrapper.unwrapped = func
    return wrapper